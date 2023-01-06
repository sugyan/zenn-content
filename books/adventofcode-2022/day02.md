---
title: "Day 2: Rock Paper Scissors"
---

https://adventofcode.com/2022/day/2

ジャンケン大会。


## part1

```
A Y
B X
C Z
```

のような入力が与えられます。

ジャンケンの攻略ガイドだそうで、各行の1列目は相手が出してくる手を表します。`A` はグー(Rock)、 `B` はパー(Paper)、 `C` はチョキ(Scissors)を表すことまでは分かっています。
各行2列目は自分が何を選択すべきかを表すものらしく、 `X`, `Y`, `Z` も同様にそれぞれ グー、パー、チョキを表していると考えました。
このジャンケン大会では各ラウンドで **自分の手の得点** として「グーは `1`、パーは `2`、チョキは `3`」が加算され、またそのラウンドでの **結果の得点** として「負けたら `0`、引き分けなら `3`、勝ったら `6`」が加算されます。

ではこの攻略ガイドに従うと全ラウンドの得点総計はいくつになるでしょうか、という問題。
上述の例では

- 1ラウンド目: 相手のグーに対しパーを選択し勝利、 `2` + `6` で **`8`** 得点
- 2ラウンド目: 相手のパーに対しグーを選択し敗北、 `1` + `0` で **`1`** 得点
- 3ラウンド目: 相手のチョキに対しチョキを選択し引き分け、 `3` + `3` で **`6`** 得点

で合計 **`15`** が解となります。


### 考え方

各ラウンドで相手も自分も選択する手が判明しているので、それぞれ結果を判定して得点を計算し、足し合わせていけば良いでしょう。


## part2

じつは `X`, `Y`, `Z` は自分が選択すべき手ではなく、「どの結果になるべきか」を表すものでした。「`X` の場合はそのラウンドは負ける、 `Y` の場合は引き分ける、 `Z` の場合は勝つ」という結果になるよう手を選択する必要がある、ということです。

ではこの通りにガイドに従っていくと得点総計はいくつになるでしょうか、という問題。
前述の例では

- 1ラウンド目: 相手のグーに対しグーを選択し引き分け、 `1` + `3` で **`4`** 得点
- 2ラウンド目: 相手のパーに対しグーを選択し敗北、 `1` + `0` で **`1`** 得点
- 3ラウンド目: 相手のチョキに対しグーを選択し勝利、 `1` + `6` で **`7`** 得点

で合計 **`12`** が解となります。


### 考え方

part1 と同じように考えると「自分が選択すべき手」を計算する手間が生じますが、それさえできれば同様に計算していくことができます。

別の考え方としては、「自分が選択する手」と「勝負の結果」はそれぞれ3通りずつしか有り得ないので、全組み合わせの9通りについてそれぞれ何得点できるかを事前に計算しておく方法があります。入力におけるそれぞれの出現回数だけ分かっていれば、 `得点 * 回数` の積の総和で解を求めることができます。
part1 と part2 では、入力行パターンと得点の間のマッピングが変わるだけで同様に計算できます。


## 実装例

### Python

```python
import sys
from collections import Counter
from typing import TextIO


class Solution:
    def __init__(self, io: TextIO) -> None:
        """それぞれの出現回数だけをカウントして保持"""
        self.counts = Counter(map(str.strip, io.readlines()))

    def part1(self) -> int:
        return self.total_score(
            {
                "A X": 4,  # 1 + 3
                "A Y": 8,  # 2 + 6
                "A Z": 3,  # 3 + 0
                "B X": 1,  # 1 + 0
                "B Y": 5,  # 2 + 3
                "B Z": 9,  # 3 + 6
                "C X": 7,  # 1 + 6
                "C Y": 2,  # 2 + 0
                "C Z": 6,  # 3 + 3
            }
        )

    def part2(self) -> int:
        return self.total_score(
            {
                "A X": 3,  # 3 + 0
                "A Y": 4,  # 1 + 3
                "A Z": 8,  # 2 + 6
                "B X": 1,  # 1 + 0
                "B Y": 5,  # 2 + 3
                "B Z": 9,  # 3 + 6
                "C X": 2,  # 2 + 0
                "C Y": 6,  # 3 + 3
                "C Z": 7,  # 1 + 6
            }
        )

    def total_score(self, scores: dict[str, int]) -> int:
        return sum([v * scores.get(k, 0) for k, v in self.counts.items()])


if __name__ == "__main__":
    solution = Solution(sys.stdin)
    print(f"Part 1: {solution.part1()}")
    print(f"Part 2: {solution.part2()}")
```

`collections.Counter` を使うことで簡単に出現回数を取得することができます。あとは得点のマッピングを渡して積の総和をとるだけです。

### Rust

```rust
use std::io::{BufRead, BufReader, Read};

struct Solution {
    counts: [u32; 9],
}

impl Solution {
    fn new(r: impl Read) -> Self {
        // それぞれの出現回数だけをカウントして保持
        let mut counts = [0; 9];
        BufReader::new(r)
            .lines()
            .filter_map(Result::ok)
            .for_each(|s| {
                let b = s.as_bytes();
                counts[((b[0] - b'A') * 3 + b[2] - b'X') as usize] += 1;
            });
        Self { counts }
    }
    fn part1(&self) -> u32 {
        // `A X`: 1 + 3 => 4, `A Y`: 2 + 6 => 8, `A Z`: 3 + 0 => 3,
        // `B X`: 1 + 0 => 1, `B Y`: 2 + 3 => 5, `B Z`: 3 + 6 => 9,
        // `C X`: 1 + 6 => 7, `C Y`: 2 + 0 => 2, `C Z`: 3 + 3 => 6,
        self.total_score([4, 8, 3, 1, 5, 9, 7, 2, 6])
    }
    fn part2(&self) -> u32 {
        // `A X`: 3 + 0 => 3, `A Y`: 1 + 3 => 4, `A Z`: 2 + 6 => 8,
        // `B X`: 1 + 0 => 1, `B Y`: 2 + 3 => 5, `B Z`: 3 + 6 => 9,
        // `C X`: 2 + 0 => 2, `C Y`: 3 + 3 => 6, `C Z`: 1 + 6 => 7,
        self.total_score([3, 4, 8, 1, 5, 9, 2, 6, 7])
    }
    fn total_score(&self, score_map: [u32; 9]) -> u32 {
        self.counts.iter().zip(&score_map).map(|(c, s)| c * s).sum()
    }
}

fn main() {
    let solution = Solution::new(std::io::stdin().lock());
    println!("Part 1: {}", solution.part1());
    println!("Part 2: {}", solution.part2());
}
```

Pythonと同様の実装ですが、カウンターとしてわざわざ `HashMap` などを使うほどでもないので 長さ `9` の配列を使用しています。
