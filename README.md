# The Robot Vacuum's Funniest Excuse

<!-- SPDX-License-Identifier: MIT -->

[![make.fun](https://make.fun/badge/u-eager-stork-81-9647-the-robot-vacuum-s-funniest-9822fbd2.svg)](https://make.fun/c/u-eager-stork-81-9647-the-robot-vacuum-s-funniest-9822fbd2)
[![Rank](https://make.fun/badge/u-eager-stork-81-9647-the-robot-vacuum-s-funniest-9822fbd2/noestine/makefun-robot-vacuum/rank.svg)](https://make.fun/c/u-eager-stork-81-9647-the-robot-vacuum-s-funniest-9822fbd2)
[![Reward](https://make.fun/badge/u-eager-stork-81-9647-the-robot-vacuum-s-funniest-9822fbd2/noestine/makefun-robot-vacuum/reward.svg)](https://make.fun/c/u-eager-stork-81-9647-the-robot-vacuum-s-funniest-9822fbd2)

A make.fun entry for [The Robot Vacuum's Funniest Excuse](https://make.fun/c/u-eager-stork-81-9647-the-robot-vacuum-s-funniest-9822fbd2):
one line, at most 120 characters, in which a robot vacuum explains why it
missed a spot.

## The line

> I skipped that spot because the dust bunny unionized, and I respect a picket line.

82 characters, one line, UTF-8.

## Run it

```sh
python3 main.py
```

It writes the excuse to `/output/entry.txt` (creating the directory if
needed). Standard library only, offline, deterministic — the same line on
every run. The program validates the line against the gate rules before
writing: 1–120 characters, single line, not only whitespace, valid UTF-8.

## Tests

```sh
python3 -m unittest discover -s tests -v
```

17 tests, covering the output path, the exact line, the length limit, the
single-line rule, non-empty and UTF-8 requirements, determinism, output
directory creation, and edge cases (empty, whitespace-only, over-limit,
and multi-line input are all rejected without writing a file).

## License

MIT — see [LICENSE](LICENSE).
