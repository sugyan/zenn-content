---
title: "Day 1: Calorie Counting"
---

https://adventofcode.com/2022/day/1

まずは小手調べ。


## part1

```
1000
2000
3000

4000

5000
6000

7000
8000
9000

10000
```

のような入力が与えられます。

各行はエルフが持っているアイテムのカロリー値を表し、空行によって別のエルフのものと区別されます。
1人目のエルフは `1000`, `2000`, `3000` のアイテムを持っているので合計で `6000` カロリー、2人目のエルフは `4000` カロリー、3人目は合計で `11000` カロリー、ということになります。

さて、各エルフの合計カロリーの最大値はいくらでしょうか、という問題です。
上述の例では 4人目の合計値 **`24000`** が解となります。

### 考え方

単純に最大値だけを求めるのであれば、順番に空行で区切られるまでの合計を計算しつつそれまでの最大値を更新しているかどうかの判定をしていけば良いでしょう。


## part2

最も合計値の多いものだけでなく、合計値 **上位3名** の総計はいくらでしょうか、という問題です。
前述の例では `24000 + 11000 + 10000` で **`45000`** が解となります。

### 考え方

上位3名を保持しながらpart1と同様にやっても良いですが、1回すべて集めてしまってから `sort` する方法を取ってしまっても良いと思います。計算量は $O(N)$ から $O(N\log{N})$ にはなってしまいますが、この問題くらいのデータ量であれば問題ありません。

そうすると part1 も part2 も「上位 $n$ 名の合計値を計算する」という共通の処理に帰着することができます。


## 実装例

### Python

```python
import sys
from typing import TextIO


class Solution:
    def __init__(self, io: TextIO) -> None:
        """ソート済みの合計値配列を事前に計算して保持"""
        self.sorted_calories = sorted(
            [sum(map(int, lines.splitlines())) for lines in io.read().split("\n\n")]
        )

    def part1(self) -> int:
        return self.sum_top_n(1)

    def part2(self) -> int:
        return self.sum_top_n(3)

    def sum_top_n(self, n: int) -> int:
        return sum(self.sorted_calories[-n:])


if __name__ == "__main__":
    solution = Solution(sys.stdin)
    print(f"Part 1: {solution.part1()}")
    print(f"Part 2: {solution.part2()}")
```

`"\n\n"` で区切って、あとは予め合計したもののリストとしてソートして保持します。末尾から `n` 要素の合計を返せるようにすればpart1もpart2も同様に解けます。

### Rust

```rust
use itertools::Itertools;
use std::io::{BufRead, BufReader, Read};

struct Solution {
    sorted_calories: Vec<u32>,
}

impl Solution {
    fn new(r: impl Read) -> Self {
        // ソート済みの合計値配列を事前に計算して保持
        Self {
            sorted_calories: BufReader::new(r)
                .lines()
                .filter_map(Result::ok)
                .collect_vec()
                .split(String::is_empty)
                .map(|lines| {
                    lines
                        .iter()
                        .filter_map(|line| line.parse::<u32>().ok())
                        .sum()
                })
                .sorted()
                .collect(),
        }
    }
    fn part1(&self) -> u32 {
        self.sum_top_n(1)
    }
    fn part2(&self) -> u32 {
        self.sum_top_n(3)
    }
    fn sum_top_n(&self, n: usize) -> u32 {
        self.sorted_calories.iter().rev().take(n).sum()
    }
}

fn main() {
    let solution = Solution::new(std::io::stdin().lock());
    println!("Part 1: {}", solution.part1());
    println!("Part 2: {}", solution.part2());
}
```

こちらもPythonと同様の実装です。入力のparseが若干面倒ですがこれくらいならメソッドチェーンで繋げて処理できます。
