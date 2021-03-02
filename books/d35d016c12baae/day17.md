---
title: "Day 17: Conway Cubes"
---

https://adventofcode.com/2020/day/17

またもや変則ライフゲーム。


## part1

```
.#.
..#
###
```

のような入力が与えられる。
`#`が *active* 、`.`が *inactive* を示していて、無限に広がる**3次元空間**内の ある平面の位置だけこの入力の状態で、あとはすべて *inactive* で初期化されているとする。
各座標のcubeは、3次元での各軸で±1以内の距離にある`26`個のneighborsの状態によって次の状態が決まる。

- 既に *active* なcubeは、neighborsが**2個または3個だけ**が *active* な場合だけ *active* のまま、そうでない場合は *inactive* になる
- *inactive* なcubeは、neighborsが**ちょうど3個だけ** *activate* な場合だけ *active* になり、そうでない場合は *inactive* のまま

というルールで状態が同時に更新される、とのこと。
初期状態から6サイクル遷移した後、 *active* なcubeは幾つあるか？という問題。

上の例だと、3次元空間に拡がりながら形を変えて、最終的に `362` 個のcubeが *active* になる。


### 考え方

考えるべき空間の範囲が定まっておらず、 `list` をnestさせていって状態を保持する座標空間を用意していくようなものは実装しづらい。
最終的に求めるべきは *active* になっているcubeの数だけだし、 *active* な座標だけを `set` で保持して、その座標とそのneighborsにあたる座標だけ次の状態を計算していけば良い。

初期状態は、例えば左上を `(0, 0, 0)` として Z軸の値は `0` のまま `(0, 1, 0)` や `(1, 2, 0)` などを `active` として扱う。


## part2

なんと、無限に広がる空間は3次元ではなく**4次元**だった（！）。
part1同様のルールで状態遷移していくが、各次元軸で±1以内の距離にあるneighborsが今度は`26`ではなく`80`個になる。


### 考え方

part1 では左上を `(0, 0, 0)` としていたのを `(0, 0, 0, 0)` に増やしてやるだけで良い。
part1も座標空間としては最初から4次元で用意し、W軸を考慮するかどうかだけ切り替えれば同じ考え方で解ける。


## 解答例

```python
from copy import deepcopy
from itertools import product, repeat
from operator import add
from typing import List, Set, Tuple


class Solution:
    # part2のことも考慮し、4次元の中のXY座標、と考えて保持する
    def __init__(self, inputs: List[str]) -> None:
        self.active: Set[Tuple[int, ...]] = set()
        for i, row in enumerate(inputs):
            for j, c in enumerate(row):
                if c == "#":
                    self.active.add((i, j, 0, 0))

    def part_1(self) -> int:
        # neighborsは3次元で±1の範囲の26(= 3**3 - 1)個
        return self.__simulate(list(filter(any, product(*repeat([-1, 0, 1], 3), [0]))))

    def part_2(self) -> int:
        # neighborsは4次元で±1の範囲の80(= 3**4 - 1)個
        return self.__simulate(list(filter(any, product(*repeat([-1, 0, 1], 4)))))

    def __simulate(self, neighbors: List[Tuple[int, ...]]) -> int:
        # 次の状態が`active`になるか否か
        def activate(p: Tuple[int, ...]) -> bool:
            count = sum([tuple(map(add, p, d)) in active for d in neighbors])
            return count == 3 or (count == 2 and p in active)

        active = deepcopy(self.active)
        for _ in range(6):
            # 次に`active`になる得る候補は、現時点で`active`なものと そのneighborたち
            candidates = set(active)
            for p in active:
                candidates.update([(tuple(map(add, p, d))) for d in neighbors])
            # 次に`active`になる座標だけの`set`に更新
            active = set(filter(activate, candidates))
        return len(active)
```
