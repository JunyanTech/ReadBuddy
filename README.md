# ReadBuddy (For practising reading Chinese)

A single-file, offline-first web app that helps primary-school children (around grade 3) practise reading aloud. The child reads a short original story page by page; characters read correctly turn blue, misread or skipped characters turn red with their pinyin shown above, and the app reports time spent and reading accuracy the moment the story is finished.

Everything lives in one HTML file: no server, no account, no database, no build step for the end user. Open it and it works.

---

## Features

- **Read-aloud tracking** — while the child reads, the microphone transcript is aligned against the text of the current page. Correct characters turn blue immediately; misread or skipped characters turn red with pinyin.
- **Tap mode** — a complete, equivalent alternative when no microphone is available: tap a character to mark it correct, press and hold (~0.56 s) to mark it wrong.
- **Live metrics** — a timer that keeps running while reading and a running accuracy figure (`correct / (correct + wrong)`).
- **Story library** — 80 original short stories in 4 categories (Minecraft / Technology / Everyday Life / Nature), 20 each, 4 pages per story, grade-3 difficulty.
- **Progress cards** — *First-Reading Accuracy* (mean of each story's first attempt) and *Review-Reading Accuracy* (mean of each story's second attempt onwards), per story, not a rolling time window.
- **Badges** — 12 achievements (first story, no mistakes, 95 %, 90 %, 3-day streak, 7-day streak, 5 good scores in a row, 10 stories, 30 stories, 10 Minecraft stories, 5 tech stories, whole shelf).
- **Sound effects** — short synthesised tones (Web Audio) for correct/incorrect marking, page turn, finishing, badge unlocked. Can be muted.
- **CSV export** — one row per reading session, UTF-8 with BOM, opens cleanly in Excel.
- **Resume** — an unfinished story can be continued from the page where the child stopped.
- **Local-only storage** — all data stays in the browser's `localStorage` on the device. No upload, no tracking.

## Supported devices

| Device | How to open |
| --- | --- |
| iPad / iPhone (Safari) | Open the file from the Files app, or use *Share → Add to Home Screen* for a full-screen, app-like launch |
| Android phone (Chrome or system browser) | Open the file from a file manager, or add to home screen |
| Windows PC (Chrome / Edge) | Double-click the HTML file |

The layout is responsive down to 360 px wide screens and up to wide desktop viewports.

## Quick start

1. Download `ReadBuddy.html`.
2. Open it in a browser (see the table above).
3. Allow microphone access if you want read-aloud tracking, then tap **Start reading**.
4. If the browser has no speech recognition, or the room is too noisy, switch to tap mode.

## Privacy and data

- Data is written to `localStorage` under four keys: `rb.readings.v1`, `rb.badges.v1`, `rb.settings.v1`, `rb.progress.v1`.
- Nothing is sent anywhere. The only network use is the browser's built-in speech-recognition service, which the Web Speech API requires.
- Clearing browser data or using private/incognito mode will erase history. Export the CSV if you want a backup.

## Repository layout

```
ReadBuddy.html                built, ready-to-open single-file app (do not edit by hand)
README.md                     this file
requirements.txt              Python dependency for the build
build/
  app_template.html           source template (HTML + CSS + JS)
  build.py                    generates the app: injects stories + per-character pinyin
  stories_mc.py               Minecraft stories, mc01-mc20
  stories_tech.py             technology stories, tech01-tech10
  stories_life_nature.py      everyday-life stories life01-life10, nature stories nat01-nat10
  stories_extra.py            tech11-20, life11-20, nat11-20
  stories_page4.py            fourth page for the original 50 stories
  make_align_test.py          regression page for the read-aloud alignment logic
  make_resp_test.py           narrow/wide viewport check page
```

The product requirements document (`PRD.md`) is kept locally and is intentionally not part of this repository.

## Rebuilding from source

The build replaces the `/*__STORIES__*/` placeholder in `build/app_template.html` with the full story data and per-character pinyin, then writes the single-file app one level up.

```bash
pip install -r requirements.txt
cd build
python build.py
```

Expected output: `Stories 80，Pages 320，Total Words 19164` and a file of roughly 249 KB.

`build.py` asserts, and fails the build if any of these break:

- exactly 80 stories;
- 4–5 pages per story;
- exactly 20 stories per category;
- unique story ids;
- no ASCII double quotes in story text (they would break the inline JSON);
- no `</script>` or U+2028/U+2029 in story text.

To add or edit a story, change one of the `stories_*.py` files and rebuild. Never edit the generated HTML directly.

## Development helpers (optional)

Two scripts generate throw-away pages used for manual regression checks; their output is git-ignored:

```bash
cd build
python make_align_test.py    # self-check page for the read-aloud alignment logic
python make_resp_test.py     # copy that auto-opens one story, for narrow/wide viewport checks
```

Ad-hoc scripts named `build/_*.py` and generated pages named `build/_*.html` are development scratch and are not part of the repository.

## How accuracy is calculated

- **Single reading**: `correct characters / (correct + wrong characters)`. Skipped characters (1–2 in a row) count as wrong; characters the child never reached are not counted at all.
- **First-Reading Accuracy** (home card 1): for each story, take the first attempt by timestamp; average those values across all stories read at least once.
- **Review-Reading Accuracy** (home card 2): for each story read two or more times, average the attempts from the second one onwards; then average those per-story values. Stories read only once do not enter this denominator.

## Known limitations

- Speech recognition depends on the browser's Web Speech API and needs a network connection; support varies, especially on some Android browsers. Tap mode is always available as a fallback.
- Recognition is not verified end-to-end on real hardware in CI — the alignment logic is covered by a self-check, but a microphone test on iPad, Android and desktop is still recommended before a release.
- No cloud sync across devices; the CSV export is the only backup path.