# Rumah Sayang

A bilingual (Bahasa Melayu / English) 3D pet-care game for children aged 3–7. Children look after Oyen the kitten, then Bobo the puppy, Gebu the rabbit and Kiki the bird. Along the way they practise:

- **Observing**: reading each pet's need bubble and body cues (muddy paws, droopy eyes, a raised sore paw)
- **Deciding**: choosing the right care, and spotting foods that are unsafe for animals
- **Prioritising**: deciding which friend to help first when two need help at once
- **Values**: saying Bismillah before food and drink, gentleness, responsibility and love

**Play it:** https://drmsrf-netizen.github.io/rumah-sayang/

## How the game works

- Each day has 5 tasks. When they're done, night falls and the pets go to sleep.
- Stars unlock new friends: Bobo at 5, Gebu at 12, Kiki at 20.
- The difficulty adjusts by itself across four levels (Benih, Tunas, Anak pokok, Pokok). Three correct first tries in a row move up a level; repeated mistakes move back down.
- Wrong choices are explained gently and the child tries again. Nothing is taken away.
- A parent panel (press and hold 👪 for one second) shows progress and lets you play every recorded voice line.
- Progress is saved in the browser on that device only.

## Voice

The Malay narration is a real recorded voice: 90 short lines in `voice/ms/`, numbered A01–H14. `script.html` is the recording script that lists every line. Any line without a recording falls back to the device's text-to-speech, and English mode currently uses text-to-speech. English recordings can be added in `voice/en/` with the same file names.

## Project layout

| Path | What it is |
| --- | --- |
| `index.html` | The game (built file — edit the source in `tools/` instead) |
| `script.html` | Recording script for the voice lines (built file) |
| `voice/ms/*.mp3` | Recorded Malay voice lines |
| `tools/game-src.html` | Game source |
| `tools/clips.py` | The 90 voice lines in BM and English; writes `clips.json` |
| `tools/build.py` | Builds `index.html` and `script.html` |
| `tools/align.py`, `tools/export.py` | Split section recordings into single lines and encode them (needs ffmpeg, numpy, scipy; raw recordings go in `tools/rec/`, which isn't committed) |

To rebuild after changing the game or the lines:

```
python3 tools/clips.py    # only if you changed the lines (run inside tools/)
python3 tools/build.py
```

The 3D scene uses [three.js](https://threejs.org) r128, loaded from cdnjs.
