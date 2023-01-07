---
title: "Day 6: Tuning Trouble"
---

https://adventofcode.com/2022/day/6

信号処理…？


## part1

```
mjqjpqmgbljsphdztnvjfqwrcgsmlb
```

のような入力が与えられます。

この連続する文字データから、 **すべてが異なる連続4文字** である「パケット開始マーカー」を見つける必要があります。

先頭から1文字ずつ読んでいって、その4文字のマーカーが最初に読み終わるまでの文字数はいくつになるでしょうか、という問題。
上述の例では、最初の 3文字 `mjq` まではまだ文字数が足りずマーカーは発見されません。4文字目まで読むと `mjqj` となりますが、これは `j` が重複しているためマーカーではありません。 **`7`** 文字目まで読むと `jpqm` がすべて異なる4文字になるので、これが解となります。

他の例では

- `bvwbjplbgvbhsrlpgdmjqwftvncz`: **`5`** 文字目まで
- `nppdvjthqldpwncqszvftbrmjlhg`: **`6`** 文字目まで
- `nznrnfrfntjfmvfwmzdfjlvtqnbhcprsg`: **`10`** 文字目まで
- `zcfzfwzzqfrljwzlrfnpqdbhtmscgvjw`: **`11`** 文字目まで

が解となります。


### 考え方

素直に1つずつインデックスを動かしながら、そこから始まる(またはそこで終わる)4文字が互いに異なるか否か、を判定していく実装をしていけば良いです。 [day03](./day03) のときのように集合として処理して要素数が `4` になるか、などで判定ができるでしょう。


## part2

今度は「メッセージ開始マーカー」を探します。このマーカーは4文字ではなく **すべてが異なる連続14文字** です。

同様にマーカーが最初に読み終わるまでの文字数はいくつになるでしょうか、という問題。
前述で例では

- `mjqjpqmgbljsphdztnvjfqwrcgsmlb`: **`19`** 文字目まで
- `bvwbjplbgvbhsrlpgdmjqwftvncz`: **`23`** 文字目まで
- `nppdvjthqldpwncqszvftbrmjlhg`: **`23`** 文字目まで
- `nznrnfrfntjfmvfwmzdfjlvtqnbhcprsg`: **`29`** 文字目まで
- `zcfzfwzzqfrljwzlrfnpqdbhtmscgvjw`: **`26`** 文字目まで

が解となります。

### 考え方

part1 と同様に処理して、毎度判定するべき長さ $k$ が `4` から `14` に増えるだけなので十分な速度で求めることができます。
これがどんどん長くなると $O(nk)$ と計算量も比例して増えてしまうので、それが気になる場合は「直前 $k$ 文字の中に出てくる出現カウント」をテーブルで管理しながらみていくことで $O(n)$ で実装することもできます。


## 実装例

### Python

```python
import sys
from typing import TextIO


class Solution:
    def __init__(self, io: TextIO) -> None:
        self.data = io.read().strip()

    def part1(self) -> int:
        return self.marker_detected_position(4)

    def part2(self) -> int:
        return self.marker_detected_position(14)

    def marker_detected_position(self, window_size: int) -> int:
        """マーカーが最初に読み終わるまでの文字数を返す"""
        for i in range(window_size, len(self.data) + 1):
            if len(set(self.data[i - window_size : i])) == window_size:
                return i
        raise ValueError("unreachable!")


if __name__ == "__main__":
    solution = Solution(sys.stdin)
    print(f"Part 1: {solution.part1()}")
    print(f"Part 2: {solution.part2()}")
```

速度や効率をそこまで厳しく考えなければ、このように簡単に記述できます。
`i` 文字目までの、長さ `window_size` の文字列を切り出し、 [day03](./day03) と同様に `set` に入れてサイズを確認すれば、すべてが異なる文字であるか否かを判定できます。

### Rust

```rust
use std::io::{BufRead, BufReader, Read};

struct Solution {
    data: Vec<usize>,
}

impl Solution {
    fn new(r: impl Read) -> Self {
        Self {
            data: BufReader::new(r)
                .lines()
                .find_map(Result::ok)
                .map(|s| s.trim().bytes().map(|u| (u - b'a') as usize).collect())
                .unwrap(),
        }
    }
    fn part1(&self) -> usize {
        self.marker_detected_position(4)
    }
    fn part2(&self) -> usize {
        self.marker_detected_position(14)
    }
    fn marker_detected_position(&self, window_size: usize) -> usize {
        let mut counts = [0; 26];
        let mut size = 0;
        for i in 0..self.data.len() {
            counts[self.data[i]] += 1;
            if counts[self.data[i]] == 1 {
                size += 1;
            }
            if i >= window_size {
                counts[self.data[i - window_size]] -= 1;
                if counts[self.data[i - window_size]] == 0 {
                    size -= 1;
                }
            }
            if size == window_size {
                return i + 1;
            }
        }
        unreachable!()
    }
}

fn main() {
    let solution = Solution::new(std::io::stdin().lock());
    println!("Part 1: {}", solution.part1());
    println!("Part 2: {}", solution.part2());
}
```

こちらは $O(n)$ の解法で実装してみました。 `counts` 配列で `window_size` の枠内に出現する文字の回数をそれぞれカウントし、種類の数の増減を別途 `size` で更新していきます。
