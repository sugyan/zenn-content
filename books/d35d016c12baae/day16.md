---
title: "Day 16: Ticket Translation"
---

https://adventofcode.com/2020/day/16

論理パズル的なもの。


## part1

```
class: 1-3 or 5-7
row: 6-11 or 33-44
seat: 13-40 or 45-50

your ticket:
7,1,14

nearby tickets:
7,3,47
40,4,50
55,2,20
38,6,12
```

のような入力が与えられる。
最初に各fieldの範囲の条件が `1-3 or 5-7` のような形で与えられる。境界を含む「1以上3以下 または 5以上7以下」というのを表現している。
次に *your ticket* の数値列が与えられ、その次からは *naerby tickets* の数値列。

part1はまず、完全にinvalidなticketを探す、という問題。どのfieldの条件にも当てはまらない数値が含まれているので、それを見つける。
上の例では `4`, `55`, `12` という数値が 最初の3つのfieldで示される範囲どれにも該当しない。のでそれらを足し合わせた `71` が解となる。


### 考え方

すべてのticketsのすべての数値についてそれぞれすべてのfieldの範囲内かチェックしていっても可能だが、値の範囲がせいぜい`1,000`程度のようなので、可能な範囲内か否かを示す `list` を作ってしまっても良さそう。
最初にすべてのfieldの範囲の数値に関して取り得るかどうかをセットしてしまえば、後ですべての*nearby tickets*の値を調べるときにはvalidかどうかのチェックが $O(1)$ でできる。


## part2

ではいよいよ、自分のticketの数値がそれぞれどのfieldに該当するものなのかを特定したい。自分のもの含めすべてのticketsは固定順のfieldになっている。part1で求めた完全にinvalidな値を持つnearby ticketsはすべて無視する、とのこと。

例として

```
class: 0-1 or 4-19
row: 0-5 or 8-19
seat: 0-13 or 16-19

your ticket:
11,12,13

nearby tickets:
3,9,18
15,1,5
5,14,9
```

のような入力があるとすると、`0`番目のcolumnが `3`, `15`, `5` の値を取り得るが それを許容できるのは `row` だけ（`class`は`3`が入らないし `seat`は`15`が入らない）なので `0`番目は`row`と確定できる。そうすると`1`番目は`class`か`seat`のどちらかだが、`seat`に`14`が入らないので`class`に確定する。すると残りの`2`番目は`seat`に確定、という感じになる。

すべてのfieldが何番目のcolumnかを確定し、`departure`で始まるfieldの*your ticket*のvalueをすべて掛け合わせた値を求めよ、という問題。


### 考え方

問題自体は順番に潰していけば解けるように出来ているようで（「どれも確定できないがこれをこのfieldと仮定すると矛盾が生じるのでこれは有り得ない」のような試行は必要なさそう）、ならば20個のfieldと各columnのvalueで有り得る組み合わせのmatrixを作っていけば良い。

上の例でいうと各fieldの取り得る範囲に入っているかどうかをすべてチェックすることで以下のような組み合わせが得られる。

```
           0      1     2
class  False   True  True
row     True   True  True
seat   False  False  True
```

この中で `True`が1つだけしか無いcolumnを探せばそれが何のfieldに該当するかが確定でき、そのcolumnとfieldはmatrixから削除して（無視して）良くなる。残ったものからまた確定できるものを探す、という操作を繰り返していけば良い。


## 解答例

```python
from collections import defaultdict
from functools import reduce
from typing import Iterable, List


class Solution:
    def __init__(self, inputs: List[str]) -> None:
        # 空行で区切る
        def split_at_empty() -> Iterable[List[str]]:
            indices = [idx for idx, x in enumerate(inputs) if not x]
            for start, end in zip([-1, *indices], [*indices, len(inputs)]):
                yield inputs[start + 1 : end]

        def parse_ticket(line: str) -> List[int]:
            return [int(x) for x in line.split(",")]

        for i, lines in enumerate(split_at_empty()):
            if i == 0:
                # 各fieldについて取り得る値の範囲を格納
                self.rules = []
                for line in lines:
                    k, v = line.split(": ")
                    ranges = []
                    for minmax in v.split(" or "):
                        ranges.append([int(m) for m in minmax.split("-")])
                    self.rules.append((k, ranges))
            if i == 1:
                self.ticket = parse_ticket(lines[1])
            if i == 2:
                self.nearby = [parse_ticket(line) for line in lines[1:]]

    def part_1(self) -> int:
        valid = set()  # なんらかのfieldに入り得る値をすべて保存する
        for _, ranges in self.rules:
            # 各rangeについて、その区間をすべて埋める
            for rmin, rmax in ranges:
                for i in range(rmin, rmax + 1):
                    valid.add(i)
        # `valid`に含まれていない値はすべてinvalidとなる
        invalid = []
        for ticket in self.nearby:
            invalid.extend([val for val in ticket if val not in valid])
        return sum(invalid)

    def part_2(self) -> int:
        fields = self.identify()
        return reduce(
            lambda x, y: x * y,
            [v for v, f in zip(self.ticket, fields) if f.startswith("departure")],
        )

    # 各columnがどのfieldに該当するかを特定する
    def identify(self) -> List[str]:
        # 取り得る値の範囲をpart1同様に各fieldごとに管理
        availables = defaultdict(set)
        for field, ranges in self.rules:
            for rmin, rmax in ranges:
                for i in range(rmin, rmax + 1):
                    availables[i].add(field)

        # すべてのcolumnに対してすべてのfieldが入り得る状態から開始
        fields = [field for field, _ in self.rules]
        candidates = [set(fields) for _ in range(len(self.ticket))]
        for ticket in self.nearby:
            # invalidな値が含まれている場合は無視
            if any([not availables[val] for val in ticket]):
                continue
            # `availables`を参照し、入り得るfieldだけに絞っていく
            for i, val in enumerate(ticket):
                candidates[i] &= availables[val]

        while any([len(c) > 1 for c in candidates]):
            # 候補となるfieldが1つだけになっているcolumnを確定させていく
            for i, c1 in enumerate(candidates):
                if len(c1) == 1:
                    field = next(iter(c1))
                    # 確定済みのものは他のcolumnの候補から除外していく
                    for j, c2 in enumerate(candidates):
                        if j != i:
                            c2 -= set([field])
        return [next(iter(c)) for c in candidates]
```