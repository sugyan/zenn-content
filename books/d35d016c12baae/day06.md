---
title: "Day 6: Custom Customs"
---

https://adventofcode.com/2020/day/6

集合の扱い方が問われる。


## part1

```
abc

a
b
c

ab
ac

a
a
a
a

b
```

のように、[day04](https://zenn.dev/sugyan/books/d35d016c12baae/viewer/day04)と同様な空行で区切られたgroupがあり、各行がその同一group内で各人が`"yes"`と回答した質問を表している。

part1は、各groupにおいて誰か1人でも`"yes"`と回答した質問の数をかぞえ、合計を求めよ、という問題。
この例だと `3 + 3 + 3 + 1 + 1` で `11` が解となる。


### 考え方

単純に各group内で出現するuniqueな文字数をカウントして合計すれば良いだけ。
`a`から`z`までというのは分かっているので辞書には `dict` などを使う必要もなく、`26` 個の`bool`配列だけ用意すれば良い。単一の32bit整数の下位26bitにそれぞれ割り当ててしまっても良い。


## part2

実は数えるべきは「groupの**誰かが**`"yes"`と回答した」ではなく「groupの**全員が**`"yes"`と回答した」質問の数だった、という変更があった場合に合計数はどうなるか。


### 考え方

`bool`演算でいうと `OR` で見ていたのが実は `AND` で見る必要があった、ということになる。
group内で各人の回答に対し、part1は `|` で、part2は `&` で全員の値を `reduce` していけば、あとは最終的な値のbit countを調べるだけで良くなる。


## 解答例

```python
from functools import reduce
from typing import Iterable, List


class Solution:
    def __init__(self, inputs: List[str]) -> None:
        # 空行で区切る
        def split_at_empty() -> Iterable[List[str]]:
            indices = [idx for idx, x in enumerate(inputs) if not x]
            for start, end in zip([-1, *indices], [*indices, len(inputs)]):
                yield inputs[start + 1 : end]

        # 各文字を 'a'..'z' で下位から 0..26 bit目として`1`にした値に変換する
        def convert(answers: str) -> int:
            return sum(map(lambda c: 1 << (ord(c) - ord("a")), answers))

        # 各group毎に上記で変換した値を保持
        self.groups = []
        for lines in split_at_empty():
            self.groups.append([convert(line) for line in lines])

    def part_1(self) -> int:
        # group内で `|` で集合和を取った値のbit countを求める
        def count(answers: List[int]) -> int:
            return bin(reduce(lambda x, y: x | y, answers)).count("1")

        return sum(map(count, self.groups))

    def part_2(self) -> int:
        # group内で `&` で集合積を取った値のbit countを求める
        def count(answers: List[int]) -> int:
            return bin(reduce(lambda x, y: x & y, answers)).count("1")

        return sum(map(count, self.groups))
```
