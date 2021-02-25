---
title: "Day 15: Rambunctious Recitation"
---

https://adventofcode.com/2020/day/15

計算量が多いので効率的な実装が求められる。


## part1

```
0,3,6
```

のような入力が与えられる。
ここから続きの数を繋げていくが、次の数字は最後の数字に着目し、

- その数字が初めて現れた場合は `0`
- そうでない場合は、幾つ前に現れたか、の値

になる、というルール。
上の例だと、`6`は初めてなので次は`0`、`0`は3つ前に出ているので次は`3`、`3`はやはり3つ前に出ているので次はまた`3`、といった具合に
`0, 3, 6, 0, 3, 3, 1, 0, 4, 0, ...`
と続いていく。

*Van Eck's sequence* と呼ばれるものらしい（特に`0`から始まって`0, 0, 1, 0, 2, 0, ...`と続くものをそう呼ぶ？）。

こうやって続けていったとき、`2020`番目の数字は何になるか、という問題。


### 考え方

`2020`程度の数なら、愚直にすべて記録していって毎回遡りながら見ていっても求められる。


## part2

では、`30,000,000`番目（！）は何になるかという問題。


### 考え方

流石にこれは毎回遡っていては終わらない。

実際すべての数を記録しておく必要はなく、「各数字が最後に現れた位置」だけが分かれば次の数を求められる。
単純に考えると`dict`でそれを記録できそうだが、それでも3000万回操作を繰り返す中で存在checkしたりinsertしたりの操作だと結構重くなる。

どうせkeyは整数値になると分かっているのだから、`list`で記録してしまう方がindexアクセスできて早い。最初にドカンと`30_000_000`サイズの`list`を確保してしまって、そこに記録していく。


## 解答例

```python
from typing import List


class Solution:
    def __init__(self, inputs: List[str]) -> None:
        self.numbers = [int(x) for x in inputs[0].split(",")]

    def part_1(self) -> int:
        return self.__play(2020)

    def part_2(self) -> int:
        return self.__play(30_000_000)

    def __play(self, turns: int) -> int:
        # 過去にその数字が現れた位置、を記録するための領域
        memory = [0] * turns
        for i, number in enumerate(self.numbers):
            memory[number] = i + 1
        prev = self.numbers[-1]
        # 次の数を決定しつつ、その数が出た位置として記録していく
        for i in range(len(self.numbers), turns):
            last = memory[prev]
            memory[prev] = i
            prev = 0 if last == 0 else i - last
        return prev
```
