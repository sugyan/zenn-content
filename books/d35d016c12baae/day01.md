---
title: "Day 1: Report Repair"
---

https://adventofcode.com/2020/day/1

まずは小手調べ的な問題。


### part1

```
1721
979
366
299
675
1456
```

のような入力が与えられる。

足して `2020` になる2つの数の組み合わせを探し、その積を返す。
上の例だと `1721` と `299` がその組み合わせになるので、掛け合わせた `514579` が解となる。

:::details 考え方

全組み合わせを探索しても良いが、 `set` に入れて `2020 - n` が存在していたかどうか確認しながら見ていけば $O(N)$ で解ける。

:::


### part2

入力の中から、足して `2020` になる **3つ** の数の組み合わせを探す。
前述の例だと `979` と `366` と `675` なので、それらを掛け合わせた `241861950` が解となる。

:::details 考え方

part1 を上の方法でやっていれば `2020 - n - m` が存在していたかどうか確認しながら `n` と `m` の組み合わせを見ていけば $O(N^2)$ で解ける。

しかし実際には入力はせいぜい200件程度なので、力技で3重ループで回していくだけでも問題なく解けそうだ…。

:::


### 解答例

:::details Python実装

```python
from itertools import combinations
from typing import List


class Solution:
    def __init__(self, inputs: List[str]) -> None:
        # とりあえずすべての入力値をlistで持つ
        self.reports: List[int] = [int(i) for i in inputs]

    def part_1(self) -> int:
        # 最初にsetに入れてしまう
        s = set(self.reports)
        # あとは足して2020になるものが存在するか否か調べるだけ
        for report in self.reports:
            if 2020 - report in s:
                return report * (2020 - report)
        raise ValueError

    def part_2(self) -> int:
        # part1同様
        s = set(self.reports)
        # 2つ選ぶ組み合わせを列挙し、合計値を2020から引いたものがあるか否かを調べる
        for reports in combinations(self.reports, 2):
            if 2020 - sum(reports) in s:
                return (2020 - sum(reports)) * reports[0] * reports[1]
        raise ValueError
```

:::
