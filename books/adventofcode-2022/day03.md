---
title: "Day 3: Rucksack Reorganization"
---

https://adventofcode.com/2022/day/3

集合を扱う問題。


## part1

```
vJrwpWtwJgWrhcsFMMfFFhFp
jqHRNqRjqzjGDLGLrsFMfFZSrLrFZsSL
PmmdzqPrVvPwwTWBwg
wMqvLMZHhHMvwLHjbvcjnnSBnvTQFn
ttgJtRGJQctTZtZT
CrZsJsPPZsGzwwsLwLmpwMDw
```

のような入力が与えられます。

各行はそれぞれリュックサックに入っているアイテムを各1文字で表しています。
リュックサックは仕切りによって2つに分かれており、常にそれぞれ同じ数のアイテムが入っています。従って、文字列の前半と後半でそれぞれの仕切りの中に含まれるものを示すことになります。

本来はすべてのアイテムは必ずそれらの仕切りのどちらか一方にしか入らないようにしないといけないところ、ある1種のアイテムだけ両方に含めてしまったそうです。
上述の例では

- 1行目: 前半は `vJrwpWtwJgWr`、後半は `hcsFMMfFFhFp` で **`p`** だけが両方に含まれている
- 2行目: 前半は `jqHRNqRjqzjGDLGL`、後半は `rsFMfFZSrLrFZsSL` で **`L`** だけが両方に含まれている
- 3行目: 前半は `PmmdzqPrV`、後半は `vPwwTWBwg` で **`P`** だけが両方に含まれている
- 4行目: 前半と後半の両方に **`v`** が含まれている
- 5行目: 前半と後半の両方に **`t`** が含まれている
- 6行目: 前半と後半の両方に **`s`** が含まれている

ということになります。
それぞれのアイテムの種類を priority の数値に変換します。

- 小文字は `a` から `z` で `1` から `26` に対応
- 大文字は `A` から `Z` で `27` から `52` に対応

では各リュックサックで仕切りの両方に入れてしまったアイテムの priority の総計はいくつでしょうか、という問題。

上述の例では、各行で前後半両方に含まれてしまっているアイテムの priority は `16` (`p`), `38` (`L`), `42` (`P`), `22` (`v`), `20` (`t`), `19` (`s`) で、合計 **`157`** が解となります。


### 考え方

各文字列を前半と後半に分割し、双方を1文字ずつ処理していきます。
前後半それぞれで文字の出現を管理する `Set` などを作って集合積をとれれば、両方に含まれる文字を見つけることができます。
あとは priority に変換して総和を計算するだけです。


## part2

これらのリュックサックを持つエルフたちは3人1組のグループで分かれていきます。各グループにおいて、3人に共通して同じアイテムが1つだけ含まれるようになっています。
前述の例では

```
vJrwpWtwJgWrhcsFMMfFFhFp
jqHRNqRjqzjGDLGLrsFMfFZSrLrFZsSL
PmmdzqPrVvPwwTWBwg
```

が1つ目のグループで、 `r` だけが3行すべてに含まれています。

```
wMqvLMZHhHMvwLHjbvcjnnSBnvTQFn
ttgJtRGJQctTZtZT
CrZsJsPPZsGzwwsLwLmpwMDw
```

が2つ目のグループで、 `Z` だけが3行すべてに含まれています。

では各グループでこのように共通で含まれているアイテムの priority の総和はいくつでしょうか、という問題。この例では `18` (`r`) と `52` (`Z`) で **`70`** が解となります。

### 考え方

今度は各行について前半・後半で分割する必要はありません。が、それぞれの集合をとっていればその集合和でその行の文字の出現に関する集合をとれます。
あとは入力を3行ずつに分割して、3つの集合の集合積をとれば part1 と同様に処理して共通の文字を見つけることができるので、part1 と同様に priority に変換して総和を計算するだけです。


## 実装例

### Python

```python
import sys
from typing import Iterator, TextIO


class Solution:
    def __init__(self, io: TextIO) -> None:
        self.items = list(map(str.strip, io.readlines()))

    def part1(self) -> int:
        def find_item(items: str) -> str:
            """前半と後半に分割して集合積をとり、その最初の要素を取得"""
            half = len(items) // 2
            return next(iter(set(items[:half]) & set(items[half:])))

        return sum(map(Solution.priority, map(find_item, self.items)))

    def part2(self) -> int:
        def groups() -> Iterator[list[str]]:
            """3行ずつに区切ったリストを生成"""
            for i in range(0, len(self.items), 3):
                yield self.items[i : i + 3]

        def find_item(group: list[str]) -> str:
            """各行の集合積をとり、その最初の要素を取得"""
            return next(iter(set(group[0]) & set(group[1]) & set(group[2])))

        return sum(map(Solution.priority, map(find_item, groups())))

    @staticmethod
    def priority(c: str) -> int:
        """アイテムの文字をpriorityの数値に変換"""
        if c.islower():
            return ord(c) - ord("a") + 1
        else:
            return ord(c) - ord("A") + 27


if __name__ == "__main__":
    solution = Solution(sys.stdin)
    print(f"Part 1: {solution.part1()}")
    print(f"Part 2: {solution.part2()}")
```

`set(<string>)` で文字列の各文字についての集合をとれるので、それを利用します。
集合積の結果は1要素だけになっているはずなので、 `next(iter(<set>))` でそれを取り出しています。

### Rust

```rust
use std::io::{BufRead, BufReader, Read};

struct Solution {
    items: Vec<(u64, u64)>,
}

impl Solution {
    fn new(r: impl Read) -> Self {
        // String::bytes() で得られる `u8` から priority に変換
        let b2i = |b| b - 38 - 58 * u8::from(b > 96);
        Self {
            items: BufReader::new(r)
                .lines()
                .filter_map(Result::ok)
                .map(|s| {
                    // 前半と後半に分けて集合を管理
                    let (s1, s2) = s.split_at(s.len() / 2);
                    (
                        s1.bytes().fold(0, |acc, x| acc | 1 << b2i(x)),
                        s2.bytes().fold(0, |acc, x| acc | 1 << b2i(x)),
                    )
                })
                .collect(),
        }
    }
    fn part1(&self) -> u32 {
        self.items
            .iter()
            .map(|(i1, i2)| (i1 & i2).trailing_zeros())
            .sum()
    }
    fn part2(&self) -> u32 {
        self.items
            .chunks(3)
            .map(|group| {
                group
                    .iter()
                    .fold(!0, |acc, x| acc & (x.0 | x.1))
                    .trailing_zeros()
            })
            .sum()
    }
}

fn main() {
    let solution = Solution::new(std::io::stdin().lock());
    println!("Part 1: {}", solution.part1());
    println!("Part 2: {}", solution.part2());
}
```

Pythonと同様に集合を扱うとなると `HashSet` などを使うことになると思いますが、`52`種類しか文字が出現しないことを考えると `u64` を使ってビット演算で代用することができます。

priority に対応する bit をセットする、という操作で集合を得られ、論理和・論理積で集合同様の計算ができます。集合積の結果は1要素だけになっているはずなので、 `.trailing_zero()` で priority の値を得ることができます。
`.iter().fold()` で集合積を取る場合は初期値として `!0` としていることに注意してください。
