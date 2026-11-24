# THE WORLD TODAY — Monday 23 November 2026

[![make.fun · news-image-20261123](https://make.fun/badge/news-image-20261123.svg)](https://make.fun/bounty/news-image-20261123?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261123)
[![rank](https://make.fun/badge/news-image-20261123/akbare12/news-23-b116-front-page-dense/rank.svg)](https://make.fun/bounty/news-image-20261123/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261123)
[![reward](https://make.fun/badge/news-image-20261123/akbare12/news-23-b116-front-page-dense/reward.svg)](https://make.fun/bounty/news-image-20261123?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261123)

A one-image front page summing up 23 November 2026's world news: 31 stories across
6 regions — the AI rout that hit Asia (Kospi −3.3%), Guterres urging AI rules at the
Bridgetown summit, and the US lead over China at a record low in the Asia Power Index.

## How it is built

- `draw.py` renders `entry.png` (1024×1024) with PIL: masthead, number strip, region
  bar, three hero scenes, ten story cards, a world map with numbered pins, an ALSO
  list, and a DATE CHECK box that keeps 22/21/19 November stories out of the day.
- `main.py` is stdlib-only: it validates the PNG header by hand (signature, IHDR,
  CRCs, IDAT/IEND) and copies `entry.png` to `$MAKEFUN_OUTPUT_DIR/entry.png`.

## Run

```sh
python3 draw.py            # regenerates entry.png
MAKEFUN_OUTPUT_DIR=out python3 main.py   # validates + copies entry.png to out/
```
