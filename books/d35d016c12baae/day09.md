---
title: "Day 9: Encoding Error"
---

https://adventofcode.com/2020/day/9

ひたすら配列を走査。


## part1

```
35
20
15
25
47
40
62
55
65
95
102
117
150
182
127
219
299
277
309
576
```

のような数値列の入力が与えられる。
最初の幾つかの数値は *preamble* と呼ばれ（上の例では`5`個、問題では`25`個がpreambleになる）、以降の数値はすべてその数値より前の`(preambleの長さ)`個の中の異なる2つの数値の和でなければならない。

part1は、そのルールに従っていない数値があるので最初に現れるその数値を探せ、という問題。
上の例だと `127`が、その前にある `95`, `102`, `117`, `150`, `182` の5個のうち どの2つの和でも表せないので解となる。


### 考え方

*preamble* の長さだけ直前の数値列を保持しておき、そこから総当たりで組み合わせを試して次の数値になるものがあるかどうかを試すのが良さそう。
毎回 `25 * (25 - 1)` 回の試行になってしまうが大した計算量ではない。
`deque` を使って順番で出し入れしていく。
数値は32bitにはおさまらないものも入ってくるので 言語によっては注意が必要。


## part2

part1で求めたinvalid numberの値に対し、総和がその値になる入力の連続部分列を探し、その部分列の最小値と最大値を足したものを求めよ、という問題。

前述の例だと `127` を `15+25+47+40` で表せるので、その4つの数値の最小値`15`と最大値`47`の和である`62`が解となる。


### 考え方

invalid numberの検出はpart1のものをそのまま使う。
連続部分列はいわゆる尺取り法で、左端と右端を和が目的の値になるまで動かしていくことで求められる。
あとはその部分列をもう一度舐めていって最小値と最大値を求めてやれば良い。これも計算量はそれほど気にしなくて良さそうだ。


## 解答例

```python
from collections import deque
from itertools import combinations
from typing import Iterable, List


class Solution:
    def __init__(self, inputs: List[str], preamble: int = 25) -> None:
        self.numbers = [int(x) for x in inputs]
        self.preamble = preamble

    def part_1(self) -> int:
        # 和が`target`と一致する2つの組み合わせを探す
        def has_pair(numbers: Iterable[int], target: int) -> bool:
            for c in combinations(dq, 2):
                if sum(c) == target:
                    return True
            return False

        # preambleサイズだけの値を保持するqueueを用意
        dq = deque(self.numbers[: self.preamble])
        for number in self.numbers[self.preamble :]:
            if not has_pair(dq, number):
                return number
            dq.popleft()
            dq.append(number)
        raise ValueError

    def part_2(self) -> int:
        # 目的の値は`part_1`で求めたもの
        target = self.part_1()
        # 総和を保持しながら、`target`より小さければ右に伸ばし 大きければ左を縮めていく
        lo, hi = (0, 0)
        total = self.numbers[0]
        while total != target:
            if total < target:
                hi += 1
                total += self.numbers[hi]
            else:
                total -= self.numbers[lo]
                lo += 1
        # あとはその部分列の最小値と最大値を求めて足すだけ
        contiguous = self.numbers[lo : hi + 1]
        return min(contiguous) + max(contiguous)
```
