---
title: "Day 5: Binary Boarding"
---

https://adventofcode.com/2020/day/5

簡単に解ける方法を思い付けるかどうか。


## part1

```
FBFBBFFRLR
```

のように `F` or `B` からなる7文字に続いて `L` or `R` からなる3文字が続く文字列が与えられる。
前半7文字で`128`rowsのうちどれか、後半3文字で`8`columnsのうちどれか、をそれぞれ二分探索のような操作で表そうとしている。
この例だと `FBFBBF` が row `44` を、 `RLR` が column `5` を表す。seat ID はrowを8倍してcolumnを足したもの、になるので `44 * 8 + 5 = 357` となる。

part1は入力すべての中で最も大きな値になる seat ID は何か、という問題。


### 考え方

これは問題をよく読んでちょっと考えると単純に2進数に変換できることに気付く。

`F` と `L` を `0`、 `B` と `R` を `1` としてそれぞれ扱う。`FBFBBFF` は `0b0101100` なので `44` に、 `RLR` は `0b101` なので `5` になる。
そして求めるべき seat ID は `(row << 3) + column` なのでこれはそのまま繋げて2進数として扱うだけで良い。 `FBFBBFFRLR` がそのまま `0b0101100101` で `357` になる。

この方法で単純に全入力を変換した上で `max` を求めれば良いだけ。


## part2

入力列の中に唯一存在していない seat ID を求める。ただし実際に有り得る `0` から `1023` までのうち小さい方や大きい方のIDはそもそも存在していない、とのこと。


### 考え方

一度すべて `set` に入れておいて、それらの最小値から最大値までの範囲で順番に存在確認をするだけで良い。


## 解答例

```python
from typing import List


class Solution:
    def __init__(self, inputs: List[str]) -> None:
        # BとRは`1`に FとLは`0`に変換し、2進数として解釈する
        def convert(seat: str) -> int:
            return int(seat.translate(str.maketrans("BRFL", "1100")), 2)

        self.seats = list(map(convert, inputs))

    def part_1(self) -> int:
        return max(self.seats)

    def part_2(self) -> int:
        s = set(self.seats)
        for seat in range(min(s), max(s) + 1):
            if seat not in s:
                return seat
        raise ValueError
```