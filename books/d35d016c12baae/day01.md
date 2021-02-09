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

この中から、足して `2020` になる2つの数の組み合わせを探す。


:::details 考え方

全組み合わせを探索しても良いけど、 `set` に入れて `2020 - n` が存在していたかどうか確認しながら見ていけば $O(N)$ で解ける。

:::


### part2

入力の中から、足して `2020` になる **3つ** の数の組み合わせを探す。

:::details 考え方

part1 を上の方法でやっていれば `2020 - n - m` が存在していたかどうか確認しながら `n` と `m` の組み合わせを見ていけば $O(N^2)$ で解ける。

しかし実際には入力はせいぜい200件程度なので、力技で3重ループで回していくだけでも簡単に解けそうだ…。

:::


### 解答例

:::details Python実装

```python
from itertools import combinations
from typing import List


class Solution:
    def __init__(self, inputs: List[str]) -> None:
        self.reports: List[int] = [int(i) for i in inputs]

    def part_1(self) -> int:
        s = set(self.reports)
        for report in self.reports:
            if 2020 - report in s:
                return report * (2020 - report)
        raise ValueError

    def part_2(self) -> int:
        s = set(self.reports)
        for reports in combinations(self.reports, 2):
            if 2020 - sum(reports) in s:
                return (2020 - sum(reports)) * reports[0] * reports[1]
        raise ValueError
```

:::
