---
title: "Day 3: Toboggan Trajectory"
---

https://adventofcode.com/2020/day/3

たびたび登場する、`.`と`#`などによる2次元の入力。


## part1

```
..##.......
#...#...#..
.#....#..#.
..#.#...#.#
.#...##..#.
..#.##.....
.#.#.#....#
.#........#
#.##...#...
#...##....#
.#..#...#.#
```

のように`.`と`#`で表される地図（ただし横方向に無限に同じパターンが続いている）で、左上を起点に一定方向に降りていくと何回`#`にぶつかるか、を数える。

part1は「右に`3`、下に`1`」で進むと何回ぶつかるか。
上の例だと`7`回ぶつかることになるので、それが解となる。


### 考え方

入力をparseして2次元配列に入れ、単純にfor loopで見ていく。横方向には同じパターンが続いているということで、横方向indexは常にwidthでの剰余を使うようにすれば、はみ出た場合を考慮できる。


## part2

part1では「右に`3`、下に`1`」の場合だけを考えれば良かったが、他の進み方をしたときも計算する必要がある。

- 右に`1`、下に`1`
- 右に`3`、下に`1` (part1のもの)
- 右に`5`、下に`1`
- 右に`7`、下に`1`
- 右に`1`、下に`2`

それぞれのパターンでのぶつかる回数をすべて掛け合わせた数を求める。前述の例だと `2, 7, 3, 4, 2` をすべて掛け合わせた `336` が解となる。


### 考え方

各方向の場合で数えるメソッドを用意する。縦方向のstep移動もできるよう対応する必要がある。


## 解答例

```python
from functools import reduce
from typing import List


class Solution:
    def __init__(self, inputs: List[str]) -> None:
        self.grid = inputs

    def part_1(self) -> int:
        return self.__count(3, 1)

    def part_2(self) -> int:
        return reduce(
            lambda x, y: x * y,
            [
                self.__count(1, 1),
                self.__count(3, 1),
                self.__count(5, 1),
                self.__count(7, 1),
                self.__count(1, 2),
            ],
        )

    # right, down に対してgrid移動したときのぶつかる回数を求めるメソッド
    def __count(self, right: int, down: int) -> int:
        ret = 0
        for j, i in enumerate(range(0, len(self.grid), down)):
            row = self.grid[i]
            # 横方向で無限に続くので `% len(row)` で見るだけで良い
            if row[(j * right) % len(row)] == "#":
                ret += 1
        return ret
```
