import json, re, math, numpy as np
from scipy.io import wavfile
clips = json.load(open("clips.json"))
SECS = {}
for c in clips: SECS.setdefault(c["id"][0], []).append(c)
FR = 0.02
def syl(t): return max(1, len(re.findall(r"[aeiou]+", t.lower())))
def analyse(sec):
    sr, x = wavfile.read(f"rec/{sec}.wav"); x = x.astype(np.float32)/32768
    n = int(sr*FR); fr = len(x)//n
    db = 20*np.log10(np.sqrt((x[:fr*n].reshape(fr, n)**2).mean(1)) + 1e-9)
    floor = np.percentile(db, 10); peak = np.percentile(db, 98)
    voiced = db > floor + 0.30*(peak-floor)
    # drop isolated blips shorter than 80 ms (clicks, breaths)
    idx = np.where(voiced)[0]
    runs = []; s = idx[0]; p = idx[0]
    for i in idx[1:]:
        if i != p+1: runs.append((s, p)); s = i
        p = i
    runs.append((s, p))
    runs = [r for r in runs if (r[1]-r[0]+1)*FR >= 0.08]
    # drop isolated clicks (very short bursts with long silence on both sides), e.g. the stop button
    keep = []
    for i, r in enumerate(runs):
        L = (r[1]-r[0]+1)*FR
        gb = (r[0]-runs[i-1][1]-1)*FR if i > 0 else 9
        ga = (runs[i+1][0]-r[1]-1)*FR if i+1 < len(runs) else 9
        if L < 0.2 and gb > 0.3 and ga > 0.3: continue
        keep.append(r)
    return sr, x, keep
def align(sec):
    items = SECS[sec]; N = len(items)
    sr, x, runs = analyse(sec)
    start = runs[0][0]*FR; end = (runs[-1][1]+1)*FR
    cands = [((a[1]+1)*FR, b[0]*FR) for a, b in zip(runs[:-1], runs[1:]) if (b[0]-a[1]-1)*FR >= 0.22]
    M = len(cands)
    S = [syl(c["ms"]) for c in items]
    # voiced speech rate estimate
    r = (end-start - 0.25*(N-1)*1.2) / sum(S)
    def segcost(i, t0, t1):
        d = t1 - t0
        e = r*S[i]
        return (math.log((d+0.3)/(e+0.3)))**2
    def gapcost(k):
        g = cands[k][1]-cands[k][0]
        return -0.6*math.log(g/1.0)
    INF = 1e18
    # dp[i][k]: boundary i (after clip i) at cand k
    dp = [[INF]*M for _ in range(N-1)]; bk = [[-1]*M for _ in range(N-1)]
    for k in range(M): dp[0][k] = segcost(0, start, cands[k][0]) + gapcost(k)
    for i in range(1, N-1):
        for k in range(i, M):
            best = INF; arg = -1
            for j in range(i-1, k):
                if dp[i-1][j] >= INF: continue
                v = dp[i-1][j] + segcost(i, cands[j][1], cands[k][0])
                if v < best: best, arg = v, j
            if arg >= 0: dp[i][k] = best + gapcost(k); bk[i][k] = arg
    best = INF; kk = -1
    for k in range(M):
        v = dp[N-2][k] + segcost(N-1, cands[k][1], end)
        if v < best: best, kk = v, k
    bounds = [kk]
    for i in range(N-2, 0, -1): bounds.append(bk[i][bounds[-1]])
    bounds = bounds[::-1]
    segs = []; t0 = start
    for k in bounds: segs.append((t0, cands[k][0], cands[k][1]-cands[k][0])); t0 = cands[k][1]
    segs.append((end if False else t0, end, None))
    out = []
    for c, sgm, s_ in zip(items, segs, S):
        out.append({"id": c["id"], "t0": sgm[0], "t1": sgm[1], "gap_after": sgm[2], "dur": sgm[1]-sgm[0], "exp": r*s_, "text": c["ms"]})
    # weakest chosen gap vs strongest unchosen gap
    chosen = set(bounds)
    unchosen = sorted([cands[k][1]-cands[k][0] for k in range(M) if k not in chosen], reverse=True)[:2]
    weakest = min(cands[k][1]-cands[k][0] for k in chosen)
    return out, r, weakest, unchosen
if __name__ == "__main__":
    res = {}
    for sec in SECS:
        out, r, weak, unch = align(sec)
        res[sec] = out
        print(f"\n{sec}: rate {r:.3f}s/syl  weakest chosen gap {weak:.2f}  biggest skipped gaps {[round(u,2) for u in unch]}")
        for o in out:
            flag = "  <-- check" if not (0.6 < (o['dur']+.3)/(o['exp']+.3) < 1.6) else ""
            print(f"  {o['id']} {o['t0']:6.2f}-{o['t1']:6.2f}  {o['dur']:4.2f}s (exp {o['exp']:4.2f})  {o['text'][:48]}{flag}")
    json.dump(res, open("align.json","w"), ensure_ascii=False, indent=0)
