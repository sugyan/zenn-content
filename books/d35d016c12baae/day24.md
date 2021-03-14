---
title: "Day 24: Lobby Layout"
---

https://adventofcode.com/2020/day/24

またもや登場、変則ライフゲーム。


## part1

```
sesenwnenenewseeswwswswwnenewsewsw
neeenesenwnwwswnenewnwwsewnenwseswesw
seswneswswsenwwnwse
nwnwneseeswswnenewneswwnewseswneseene
swweswneswnenwsewnwneneseenw
eesenwseswswnenwswnwnwsewwnwsene
sewnenenenesenwsewnenwwwse
wenwwweseeeweswwwnwwe
wsweesenenewnwwnwsenewsenwwsesesenwne
neeswseenwwswnwswswnw
nenwswwsewswnenenewsenwsenwnesesenew
enewnwewneswsewnwswenweswnenwsenwsw
sweneswneswneneenwnewenewwneswswnese
swwesenesewenwneswnwwneseswwne
enesenwswwswneneswsenwnewswseenwsese
wnwnesenesenenwwnenwsewesewsesesew
nenewswnwewswnenesenwnesewesw
eneswnwswnwsenenwnwnwwseeswneewsenese
neswnwewnwnwseenwseesewsenwsweewe
wseweeenwnesenwwwswnew
```

のような入力が与えられる。
六角形を敷き詰めたタイル上で、各行は起点となる中心から白黒反転すべきタイルの位置を示していて、`e`, `se`, `sw`, `w`, `nw`, `ne`の6方向への移動を区切りなく繋げたもの。
初期状態はすべて白になっていて、一度反転すると黒になるがもう一度反転すると白に戻る。

各行すべて順番に反転作業を行った後、黒になっているタイルは何枚か、という問題。
上の例だと、20行あるが実際には10枚が黒になり5枚が2回反転されて白に戻るため、最終的な黒の枚数は `10` となる。


### 考え方

結局各行がどの位置に行き着くか、を求めたい。
単純なXY軸方向ではなく斜めのものがあるので難しい…と思ってしまうかもしれないが、XY座標に投影してしまえば簡単で、`se`, `sw`, `nw`, `ne`がそれぞれ`(+1, -1)`, `(-1, -1)`, `(-1, +1)`, `(+1, +1)`への斜め移動と考えて`e`, `w`をそれぞれ`(+2, 0)`, `(-2, 0)`の2マス移動と考えてしまえば良い。
文字の区切りが無いので例えば`e`が`se`のものか`e`のものか区別しづらいが、それも`s`か`n`の直後かどうかだけ見れば問題なく判別できる。

あとは求めた座標を `set` にでも入れておいて、既に反転済みだったら削除する、といった操作をしてやれば良い。


## part2

part1で反転したものから、ライフゲームが始まる。
次の日のタイルは隣接する6つのタイルによって状態が決まる。

- 黒のタイルは、`0`個もしくは`2`個より多くの黒タイルが隣接していた場合に白になる
- 白のタイルは、ちょうど`2`個の黒タイルが隣接していた場合に黒になる

というルールで毎日同時に状態が遷移する。
では100日後には何枚が黒になっているか？という問題。
前述の例だと、 `10` 枚からスタートして最終的に `2208` 枚が黒になるのでそれが解となる。


### 考え方

今までの [day11](https://adventofcode.com/2020/day/11) や [day17](https://adventofcode.com/2020/day/17) のときと同様に、見るべき隣接タイルの位置は分かっているのだから、各黒タイルとそれに隣接するタイルすべてにおいて、次の日が黒になるべきか否かを判定していけば良い。


## 解答例

```python
from copy import deepcopy
from operator import add
from typing import List, Set, Tuple


class Solution:
    def __init__(self, inputs: List[str]) -> None:
        # 与えられた行の文字列から座標に変換する
        def position(s: str) -> Tuple[int, int]:
            p = [0, 0]
            # `n`か`s`に続いているものは斜め移動なので横には1つだけ移動
            # そうでなければ真横に2つ移動することになる
            ns = False
            for c in s:
                if c == "e":
                    p[0] += 1 if ns else 2
                    ns = False
                if c == "s":
                    p[1] -= 1
                    ns = True
                if c == "w":
                    p[0] -= 1 if ns else 2
                    ns = False
                if c == "n":
                    p[1] += 1
                    ns = True
            return p[0], p[1]

        # 黒タイルになっているべきものの座標を格納していく
        self.flipped: Set[Tuple[int, int]] = set()
        for line in inputs:
            pos = position(line)
            # 既に反転されていて白タイルに戻るのならsetから削除する
            if pos in self.flipped:
                self.flipped.remove(pos)
            else:
                self.flipped.add(pos)

    def part_1(self) -> int:
        return len(self.flipped)

    def part_2(self) -> int:
        # 見るべき隣接タイル6枚の相対位置
        neighbors = ((2, 0), (1, -1), (-1, -1), (-2, 0), (-1, 1), (1, 1))
        flipped = deepcopy(self.flipped)

        # 与えられた座標のタイルが次の日に黒タイルになっているべきか否か
        def flip(p: Tuple[int, int]) -> bool:
            count = sum([tuple(map(add, p, d)) in flipped for d in neighbors])
            return count == 2 or (count == 1 and p in flipped)

        for _ in range(100):
            candidates = set(flipped)
            for p in flipped:
                for d in neighbors:
                    candidates.add((p[0] + d[0], p[1] + d[1]))
            flipped = set(filter(flip, candidates))
        return len(flipped)
```
