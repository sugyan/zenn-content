---
title: "Day 23: Crab Cups"
---

https://adventofcode.com/2020/day/23

前日に続いて、蟹との対決。


## part1

```
389125467
```

のような入力が与えられる。
`1`から`9`までのカップをこの順番に時計回りに並べ、次の規則で動かしていく。

- 入力の最初のカップを *current cup* とする
- *current cup* から時計回りに見て3つを取り出す
- *current cup* の数値から`1`だけ引いた数値のcupを *destination cup* とする
  - `1`引いた数値のものが取り出されている3つに含まれていたら さらに`1`引いていく
  - `1`を引き続けて最低値に到達したら次は最大値に折り返される
- 取り出した3つのcupを *destination cup* から時計回りにそのままの順番で移動する
- *current cup* から時計回りで隣のものを次の *current cup* とする

これを`100`回繰り返したとき、`1`のカップから時計回りに見ていくとどういう順番でカップが並ぶか？という問題。
上の例だと、 `67384529` が解になる。


### 考え方

`9`個のカップを`100`回動かす程度なら、`list` に入れて順番に`remove`と`insert`を繰り返していっても問題なくsimulateできる。


## part2

なんと、カップは9個だけではなく**100万個**だった…！ 最初の幾つか（入力の9個）はその順番で並べられ、それ以降の数が続いて順番に並べられる、とのこと。
そして動かす回数も100回ではなく**1000万回**！

で動かした後に、`1`のcupから時計回りに続く2つのcupの値を掛け合わせたものを求めよ、という問題。
前述の例だと、 `1` から `934001`, `159792` が続くので `149245887792` が解となる。


### 考え方

さすがにこれは`list`の`remove`や`insert`ではまったく計算が終わらない。
Linked List を繋ぎ直していく、というのが分かりやすいアプローチになりそう。

実際の操作をよく考えてみると、

```
current cup -> [picked up 3 cups] -> next1 -> ... -> destination cup -> next2 -> 
```

という順番で繋がっているものを

```
current cup -> next1 -> ... -> destination cup -> [picked up 3 cups] -> next2 -> 
```

と繋ぎ直せば良いだけなので、この操作をする際には「あるカップのすぐ時計回り方向の隣にあるカップの番号」だけ分かっていれば良い。

*current cup* から取り上げる3つは *current cup* を起点に順番に3つ辿れば良いだけ。
そのさらに次のcupが、繋ぎ直した後に *current cup* の隣（次）に来るべきものになる。
*destination cup* の次のcupが、繋ぎ直した後に取り上げた3つの隣（次）に来るべきもの、になる。

ということで、 `dict` などで「指定した番号のcupから、次に並ぶcupの番号」を引けるようにすれば、それを書き換えていくだけで操作が可能になる。
`dict` ではなく `list` でも実装できるので、その方が計算も早いと思われる。


## 解答例

```python
from functools import reduce
from typing import List, Tuple


class Solution:
    def __init__(self, inputs: List[str]) -> None:
        self.cups = list(map(int, inputs[0]))

    def part_1(self) -> int:
        # 動かした後の「時計回り隣にあるcupの数字」を表すmapを得る
        next_map = self.__simulate(len(self.cups), 100)

        # 順番に辿っていって回答の数値を生成していく
        def labels(curr: Tuple[int, int], _: int) -> Tuple[int, int]:
            cup = next_map[curr[1]]
            return (curr[0] * 10 + cup, cup)

        return reduce(labels, range(8), (0, 1))[0]

    def part_2(self) -> int:
        # 動かした後の「時計回り隣にあるcupの数字」を表すmapを得る
        next_map = self.__simulate(1_000_000, 10_000_000)

        # 順番に辿って掛け合わせていく
        def labels_product(curr: Tuple[int, int], _: int) -> Tuple[int, int]:
            cup = next_map[curr[1]]
            return (curr[0] * cup, cup)

        return reduce(labels_product, range(2), (1, 1))[0]

    # 実際に与えられた`cups`から`moves`回動かした後の「時計回り隣の数字」を表すmapを計算する
    def __simulate(self, cups: int, moves: int) -> List[int]:
        # `cups`個の情報を格納できる配列を用意。`0`番目は無視して使う
        ret = [0] * (cups + 1)
        # 与えられた`self.cups`で、それぞれ次に続くcupsの値を格納していく
        for i, cup in enumerate(self.cups):
            if i > 0:
                ret[self.cups[i - 1]] = cup
            last = cup
        # `cups`の数がそれより大きい場合は続きから順番に埋めていく
        for i in range(len(self.cups), cups):
            ret[last] = last = i + 1
        ret[last] = self.cups[0]

        # current cup を設定してsimulation開始
        curr = self.cups[0]
        for _ in range(moves):
            # currentから続く3つを抽出
            p = curr
            pickups = []
            for _ in range(3):
                p = ret[p]
                pickups.append(p)
            # destination cup を計算
            dest = (curr - 2) % cups + 1
            while dest in pickups:
                dest = (dest - 2) % cups + 1
            # それぞれ継ぎ換える
            ret[curr], ret[p], ret[dest] = ret[p], ret[dest], ret[curr]
            # current cup を時計回り隣のものに更新
            curr = ret[curr]
        return ret
```
