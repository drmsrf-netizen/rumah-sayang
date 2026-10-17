import json, subprocess, os, re, numpy as np
from scipy.io import wavfile
from align import align, analyse, FR
import sys
os.makedirs("voice/ms", exist_ok=True); os.makedirs("norm", exist_ok=True); os.makedirs("cut", exist_ok=True)
def loudnorm(sec):
    src, dst = f"rec/{sec}.wav", f"norm/{sec}.wav"
    p = subprocess.run(["ffmpeg","-hide_banner","-i",src,"-af","loudnorm=I=-16:TP=-1.5:LRA=11:print_format=json","-f","null","-"],capture_output=True,text=True)
    m = json.loads(re.findall(r"\{[^{}]*\"input_i\"[^{}]*\}", p.stderr)[-1])
    af = ("loudnorm=I=-16:TP=-1.5:LRA=11:linear=true:"
          f"measured_I={m['input_i']}:measured_TP={m['input_tp']}:measured_LRA={m['input_lra']}:measured_thresh={m['input_thresh']}:offset={m['target_offset']}")
    subprocess.run(["ffmpeg","-v","error","-y","-i",src,"-af",af,"-ar","44100","-ac","1",dst],check=True)
    return dst
summary = []
def trim(sec, out):
    _, _, runs = analyse(sec)
    spans = [(a*FR, (b+1)*FR) for a, b in runs]
    for oi, o in enumerate(out):
        lim = 0.45 if oi == len(out)-1 else 0.35  # end of a take often has the stop-button tap
        inside = [sp for sp in spans if sp[0] >= o["t0"]-1e-6 and sp[1] <= o["t1"]+1e-6]
        # drop short leading/trailing bursts (breaths, clicks) set apart from the spoken line
        # a tail/head cluster with under 0.35 s of sound, after a pause over 0.5 s, is not speech
        for k in range(1, len(inside)):
            if inside[k][0]-inside[k-1][1] > 0.5 and sum(b-a for a, b in inside[k:]) < lim:
                inside = inside[:k]; break
        for k in range(len(inside)-1, 0, -1):
            if inside[k][0]-inside[k-1][1] > 0.5 and sum(b-a for a, b in inside[:k]) < 0.35:
                inside = inside[k:]; break
        o["t0"], o["t1"] = inside[0][0], inside[-1][1]
    return out
for sec in (sys.argv[1] if len(sys.argv) > 1 else "ABCDEFG"):
    out, *_ = align(sec)
    out = trim(sec, out)
    path = loudnorm(sec)
    sr, x = wavfile.read(path); x = x.astype(np.float32)
    for i, o in enumerate(out):
        prev_end = out[i-1]["t1"] if i else 0.0
        next_start = out[i+1]["t0"] if i+1 < len(out) else len(x)/sr
        a = max(o["t0"] - 0.12, (prev_end + o["t0"])/2)
        b = min(o["t1"] + 0.22, (o["t1"] + next_start)/2)
        seg = x[int(a*sr):int(b*sr)].copy()
        fi, fo = int(0.015*sr), int(0.08*sr)
        seg[:fi] *= np.linspace(0,1,fi); seg[-fo:] *= np.linspace(1,0,fo)
        w = f"cut/{o['id']}.wav"
        wavfile.write(w, sr, np.clip(seg, -32768, 32767).astype(np.int16))
        subprocess.run(["ffmpeg","-v","error","-y","-i",w,"-codec:a","libmp3lame","-b:a","64k","-ac","1",f"voice/ms/{o['id']}.mp3"],check=True)
        summary.append((o["id"], round(b-a,2)))
print(len(summary), "clips exported")
print(sum(os.path.getsize(f"voice/ms/{f}") for f in os.listdir("voice/ms"))//1024, "KB total")
