---
title: "Day 4: Camp Cleanup"
---

https://adventofcode.com/2022/day/4

お掃除の範囲。


## part1

```
2-4,6-8
2-3,4-5
5-7,7-9
2-8,3-7
6-6,4-6
2-6,4-8
```

のような入力が与えられます。

各行はペアになったエルフがそれぞれ割り当てられた範囲を表しています。

- 1組目: 片方は `2` から `4` まで (すなわち `2`, `3`, `4`)、もう片方は `6`, `7`, `8`
- 2組目: 片方は `2`, `3`、もう片方は `4`, `5`
- 3組目: 片方は `5`, `6`, `7`、もう片方は `7`, `8`, `9`
- ...

のような意味であり、より視覚的に表現すると以下のようになります。

```
.234.....  2-4
.....678.  6-8

.23......  2-3
...45....  4-5

....567..  5-7
......789  7-9

.2345678.  2-8
..34567..  3-7

.....6...  6-6
...456...  4-6

.23456...  2-6
...45678.  4-8
```

これらのペアに、どちらか一方の範囲がもう片方の範囲を **完全に含んでいる** ものがあります。そういったペアはいくつあるでしょうか、という問題です。
上述の例では、`2-8` が `3-7` を完全に含んでおり、また `6-6` が `4-6` を完全に含んでいるので、 **`2`** が解となります。

### 考え方

例では1桁だけの数字で範囲が表されていましたが、実際の入力は`100`程度までの2桁の数字で表されるため、少し範囲のサイズが大きくなります。
とはいえそこまで大きな数でもないので、各範囲に含まれる数値を1つ1つ拾って集合を作って計算しても十分な速度で求めることができるでしょう。


## part2

今度は **まったく重複の無い** ペアを探すことにしました。
前述の例では、最初の2組のペア(`2-4,6-8` と `2-3,4-5`)がそれに該当し、残りの4組は重複している範囲が存在しています。

- `5-7,7-9` は `7` が重複しています。
- `2-8,3-7` は `3` から `7` すべてが `2-8` に含まれていて重複しています。
- `6-6,4-6` は `6` が重複していることになります。
- `2-6,4-8` は `4` から `6` の範囲が重複しています。

では重複があるペアはいくつあるでしょうか、という問題です。
前述の例ではこの **`4`** が解となります。

### 考え方

part1 と同様で、集合で計算しても十分な速度で求められます。
始点と終点のインデックスだけ見て、境界で判定する方法でも良いでしょう。


## 実装例

### Python

```python
import sys
from typing import TextIO


class Solution:
    def __init__(self, io: TextIO) -> None:
        def parse(line: str) -> tuple[set[int], set[int]]:
            """`,`で区切って、`-`の両側を数値に変換して`range`から`set`を生成"""
            a0, a1 = map(lambda x: list(map(int, x.split("-"))), line.split(","))
            return (
                set(range(a0[0], a0[1] + 1)),
                set(range(a1[0], a1[1] + 1)),
            )

        self.pairs = list(map(parse, io.readlines()))

    def part1(self) -> int:
        return len(list(filter(lambda a: a[0] <= a[1] or a[1] <= a[0], self.pairs)))

    def part2(self) -> int:
        return len(list(filter(lambda a: any(a[0] & a[1]), self.pairs)))


if __name__ == "__main__":
    solution = Solution(sys.stdin)
    print(f"Part 1: {solution.part1()}")
    print(f"Part 2: {solution.part2()}")
```

`set(range())` を使って該当範囲の整数値をすべて含む集合を作ってしまいます。完全に含んでいるか否かを `<=` 演算子で判定できます。

### Rust

```rust
use itertools::Itertools;
use std::io::{BufRead, BufReader, Read};

struct Solution {
    pairs: Vec<((u32, u32), (u32, u32))>,
}

impl Solution {
    fn new(r: impl Read) -> Self {
        Self {
            pairs: BufReader::new(r)
                .lines()
                .filter_map(Result::ok)
                .filter_map(|s| {
                    s.split(',')
                        .filter_map(|s| s.split('-').filter_map(|s| s.parse().ok()).collect_tuple())
                        .collect_tuple()
                })
                .collect(),
        }
    }
    fn part1(&self) -> usize {
        self.pairs
            .iter()
            .filter(|(a0, a1)| (a0.0 <= a1.0 && a1.1 <= a0.1) || (a1.0 <= a0.0 && a0.1 <= a1.1))
            .count()
    }
    fn part2(&self) -> usize {
        self.pairs
            .iter()
            .filter(|(a0, a1)| a0.0.max(a1.0) <= a0.1.min(a1.1))
            .count()
    }
}

fn main() {
    let solution = Solution::new(std::io::stdin().lock());
    println!("Part 1: {}", solution.part1());
    println!("Part 2: {}", solution.part2());
}
```

こちらは始点と終点のインデックスだけを保持して、その大小比較で判定する実装にしました。
