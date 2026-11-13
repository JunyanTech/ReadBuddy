# ReadBuddy

A single-file, offline-first web app that helps primary-school children (around grade 3) practise reading aloud. The child reads a short original story page by page; what was read correctly turns blue, what was misread or skipped turns red, and the app reports time spent and reading accuracy the moment the story is finished.

The project ships **two independent editions** behind one language chooser:

| Page | Edition | Judged per | Theme |
| --- | --- | --- | --- |
| `index.html` | language chooser (start here) | — | warm paper |
| `ReadBuddy_cn.html` | Chinese («中文版») | character, wrong characters show pinyin | warm paper / orange accent |
| `ReadBuddy_de.html` | German («Deutsch») | word, no pinyin | light green / green accent |

Both editions are self-contained: no server, no account, no database, and no build step for the end user. Each page works on its own once opened; the chooser simply links the two.

---

## Features

- **Read-aloud tracking** — while the child reads, the microphone transcript is aligned against the text of the current page. Correct units turn blue immediately; misread or skipped units turn red (Chinese also shows pinyin above the character).
- **Tap mode** — a complete, equivalent alternative when no microphone is available: tap a character/word to mark it correct, press and hold (~0.56 s) to mark it wrong.
- **Live metrics** — a timer that keeps running while reading and a running accuracy figure.
- **Story library** — 80 original short stories in 4 categories (Minecraft / Technology / Everyday Life / Nature), 20 each, 4 pages per story, grade-3 difficulty. The German edition carries the same 80 stories, translated and localised (`Milo`, `Lina`, `Jonas`, `Mia`).
- **Shelf pagination** — 10 stories per page with previous/next buttons and a page indicator.
- **Progress cards** — *First-Reading Accuracy* (mean of each story's first attempt) and *Review-Reading Accuracy* (mean of each story's second attempt onwards), per story, not a rolling time window.
- **Badges** — 12 achievements (first story, no mistakes, 95 %, 90 %, 3-day streak, 7-day streak, 5 good scores in a row, 10 stories, 30 stories, 10 Minecraft stories, 5 tech stories, whole shelf).
- **Sound effects** — short synthesised tones (Web Audio) for correct/incorrect marking, page turn, finishing, badge unlocked. Can be muted from the header.
- **CSV export** — one row per reading session, UTF-8 with BOM, opens cleanly in Excel.
- **Reset scores** — clears every reading, badge and unfinished progress entry behind a confirmation sheet; sound and mode settings are kept.
- **Resume** — an unfinished story can be continued from the page where the child stopped.
- **Local-only storage** — all data stays in the browser's `localStorage` on the device. No upload, no tracking.

## Supported devices

| Device | How to open |
| --- | --- |
| iPad / iPhone (Safari) | Open the hosted page (see below), then *Share → Add to Home Screen* for a full-screen, app-like launch |
| Android phone (Chrome or system browser) | Open the hosted page or the file, then add to home screen |
| Windows PC (Chrome / Edge) | Double-click `index.html` and pick an edition |

The layout is responsive down to 360 px wide screens and up to wide desktop viewports.

## Quick start

1. Open `index.html` (hosted URL or local file).
2. Pick «中文版» or «Deutsch».
3. Allow microphone access if you want read-aloud tracking, then tap **Start reading** / **Vorlesen starten**.
4. If the browser has no speech recognition, or the room is too noisy, switch to tap mode.

Each edition has a small switch in the top-right corner of its home screen (`DE` ↔ `CN`) that jumps to the other edition. The two editions keep **separate scores**.

## Hosting it for yourself (GitHub Pages)

iOS will not run speech recognition from a local `file://` page, and a raw GitHub link opens as plain text. For iPad/iPhone use, serve the pages over HTTPS:

1. Repository **Settings → Pages**: source *Deploy from a branch*, branch `main`, folder `/ (root)`; save.
2. Open `https://<user>.github.io/<repo>/index.html` in Safari and choose an edition.
3. *Share → Add to Home Screen* — the saved icon is labelled `ReadBuddy` on all three pages (same icon, title, theme colour).

`sw.js` caches the chooser, both editions and the icon (`readbuddy-v3`) so the app still opens offline. Bump `CACHE` in `sw.js` whenever you publish a new build, and close/reopen the home-screen app once so the new version takes effect. On `file://` (or any non-HTTP protocol) the registration is skipped, so the single-file download behaves exactly as before.

Note that the two launch paths keep separate storage: the Safari tab and the home-screen app each have their own `localStorage`. Pick one and stay with it.

## Privacy and data

- Chinese edition: `rb.readings.v1`, `rb.badges.v1`, `rb.settings.v1`, `rb.progress.v1`.
- German edition: `rb_de.readings.v1`, `rb_de.badges.v1`, `rb_de.settings.v1`, `rb_de.progress.v1`.
- The prefixes are different on purpose, so the two editions never touch each other's scores.
- Nothing is sent anywhere. The only network use is the browser's built-in speech-recognition service, which the Web Speech API requires.
- Clearing browser data or using private/incognito mode will erase history. Export the CSV if you want a backup.

## Repository layout

```
index.html                    language chooser (entry point, links both editions)
ReadBuddy_cn.html             built Chinese edition (do not edit by hand)
ReadBuddy_de.html             built German edition (do not edit by hand)
icon-180.png                  iOS home-screen icon (180 x 180)
sw.js                         optional offline cache for the hosted build
README.md                     this file
requirements.txt              Python dependency for the Chinese build (pypinyin)
build/
  app_template.html           Chinese source template (HTML + CSS + JS)
  app_template_de.html        German source template (HTML + CSS + JS)
  build.py                    builds ReadBuddy_cn.html: stories + per-character pinyin
  build_de.py                 builds ReadBuddy_de.html: stories only, no pinyin
  stories_mc.py               Minecraft stories, mc01-mc20
  stories_tech.py             technology stories, tech01-tech10
  stories_life_nature.py      everyday-life stories life01-life10, nature stories nat01-nat10
  stories_extra.py            tech11-20, life11-20, nat11-20
  stories_page4.py            fourth page for the original 50 stories
  stories_de_mc.py            Minecraft stories (German), mc01-mc20
  stories_de_tech.py          technology stories (German), tech01-tech20
  stories_de_alltag.py        everyday-life stories (German), life01-life20
  stories_de_natur.py         nature stories (German), nat01-nat20
  make_align_test.py          regression page for the read-aloud alignment logic
  make_resp_test.py           narrow/wide viewport check page
```

The product requirements document (`PRD.md`) is kept locally and is intentionally not part of this repository.

## Rebuilding from source

Both builds replace a `/*__STORIES__*/` placeholder in their template and write the single-file app one level up. The Chinese build additionally injects per-character pinyin; the German build does not, because German is judged word by word.

```bash
pip install -r requirements.txt
cd build
python build.py       # -> ../ReadBuddy_cn.html
python build_de.py    # -> ../ReadBuddy_de.html
```

Expected output: `80 stories, 320 pages` — 19164 characters for the Chinese build, 10204 words for the German one — and files of roughly 250 KB and 130 KB.

Each build script asserts, and fails the build if any of these break:

- exactly 80 stories;
- 4–5 pages per story;
- exactly 20 stories per category;
- unique story ids and titles;
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

- **Single reading (Chinese)**: `correct characters / (correct + wrong characters)`. Skipped characters (1–2 in a row) count as wrong; characters the child never reached are not counted at all.
- **Single reading (German)**: `correct words / (correct + wrong words)`, same skipping rule applied per word.
- **First-Reading Accuracy** (home card 1): for each story, take the first attempt by timestamp; average those values across all stories read at least once.
- **Review-Reading Accuracy** (home card 2): for each story read two or more times, average the attempts from the second one onwards; then average those per-story values. Stories read only once do not enter this denominator.

## Known limitations

- Speech recognition depends on the browser's Web Speech API and needs a network connection; support varies, especially on some Android browsers. Tap mode is always available as a fallback.
- Recognition is not verified end-to-end on real hardware in CI — the alignment logic is covered by automated checks, but a microphone test on iPad, Android and desktop is still recommended before a release.
- No cloud sync across devices; the CSV export is the only backup path.
- The old single edition URL (`ReadBuddy.html`) no longer exists; home-screen icons added before the split have to be removed and re-added from `index.html`.
