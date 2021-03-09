---
title: "Day 12: Rain Risk"
---

https://adventofcode.com/2020/day/12

座標を動かす系の問題。


## part1

```
F10
N3
F7
R90
F11
```

のような入力が与えられる。
各行は`action`を表す先頭文字、続いて`value`を示す整数値が入る。
船は東向きの状態から開始し、各`action`に対応して

- `N` は 北方向に、`value`だけ動く
- `S` は 南方向に、`value`だけ動く
- `E` は 東方向に、`value`だけ動く
- `W` は 西方向に、`value`だけ動く
- `L` は 左方向に、`value`度だけ回転する
- `R` は 右方向に、`value`度だけ回転する
- `F` は 現在向いている方向に、`value`だけ前進する

という命令だと解釈したとき、開始位置からどれだけ離れた位置に到達するか、そのマンハッタン距離を求めよ、という問題。
上の例だと、 `(0, 0)` から開始したとすると `(10, 0) -> (10, 3) -> (17, 3) -> (17, -8)` に到達するので `25` が解となる。


### 考え方

そのまま順番に実行してやれば良いだけ。
現時点の座標を表す`p = (0, 0)`と、現時点の方向を表す`d = (1, 0)`を用意しておいて、 `'N' | 'S' | 'E' | 'W'` のときは座標`p`を動かし、 `'L' | 'R'` のときは方向`d`を更新してやれば良い。 `F` が来たら方向`d`に座標`p`を動かせば良い。


## part2

なんと、各命令の解釈は間違っていた（！）。
船から東に`10`、北に`1`の位置に `waypoint`が存在しており、

- `N` は **waypointが**北方向に、`value`だけ動く
- `S` は **waypointが**南方向に、`value`だけ動く
- `E` は **waypointが**東方向に、`value`だけ動く
- `W` は **waypointが**西方向に、`value`だけ動く
- `L` は **waypointが船から見て左方向に**、`value`度だけ回転する
- `R` は **waypointが船から見て右方向に**、`value`度だけ回転する
- `F` は **waypointが示す方向に**、`value`だけ前進する

というのが正しかったようだ。
前述の例だと、 `(0, 0) [(10, 1)] -> (100, 10) [(10, 1)] -> (100, 10) [(10, 4)] -> (170, 38) [(10, 4)] -> (170, 38) [(4, -10)] -> (214, -72) [(4, -10)]` といった形で 船の位置もしくはwaypointが動き、最終的な到達位置と開始位置のマンハッタン距離 `286` が解となる。


### 考え方

part1を「東に`1`の位置にwaypointがある」状態とみなすことができ、 `N`, `S`, `E`, `W` で動かすのが船そのものかwaypointか、が変わるだけで あとは共通の処理で書けそうだ。

共通のメソッドに「waypointの初期値」と「waypointを動かすか否か」の引数だけ与えて処理するようにしてやれば良い。


## 解答例

```python
from enum import Enum
from typing import List, Tuple


class Action(Enum):
    N = "N"
    S = "S"
    E = "E"
    W = "W"
    L = "L"
    R = "R"
    F = "F"


class Solution:
    def __init__(self, inputs: List[str]) -> None:
        # `action`と`value`に分けてparse
        def parse(line: str) -> Tuple[Action, int]:
            action, value = line[0], line[1:]
            return Action(action), int(value)

        self.insructions = list(map(parse, inputs))

    def part_1(self) -> int:
        return sum([abs(v) for v in self.__navigate((1, 0), False)])

    def part_2(self) -> int:
        return sum([abs(v) for v in self.__navigate((10, 1), True)])

    def __navigate(self, d: Tuple[int, int], waypoint: bool) -> Tuple[int, int]:
        # 初期位置、初期waypoint位置
        p = [0, 0]
        w = list(d)
        for action, value in self.insructions:
            # N, S, E, W のときは `waypoint`が`True`の場合は`w`を、`False`の場合は`p`を動かす
            if action == Action.N:
                if waypoint:
                    w[1] += value
                else:
                    p[1] += value
            if action == Action.S:
                if waypoint:
                    w[1] -= value
                else:
                    p[1] -= value
            if action == Action.E:
                if waypoint:
                    w[0] += value
                else:
                    p[0] += value
            if action == Action.W:
                if waypoint:
                    w[0] -= value
                else:
                    p[0] -= value
            # L, R のときは 90度の回転を繰り返す
            if action == Action.L:
                for _ in range(value // 90):
                    w = [-w[1], w[0]]
            if action == Action.R:
                for _ in range(value // 90):
                    w = [w[1], -w[0]]
            # F のときは `w`の量だけ`p`を動かす
            if action == Action.F:
                p[0] += w[0] * value
                p[1] += w[1] * value
        return (p[0], p[1])
```
