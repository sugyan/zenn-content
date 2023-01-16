---
title: "Day 5: Supply Stacks"
---

https://adventofcode.com/2022/day/5

Stackに積んだり動かしたり。


## part1

```
    [D]    
[N] [C]    
[Z] [M] [P]
 1   2   3 

move 1 from 2 to 1
move 3 from 1 to 3
move 2 from 2 to 1
move 1 from 1 to 2
```

のような入力が与えられます。

前半はStackの初期状態を表しています。1番目のStackは `Z` を底に `N` を上に積んであります。2番目のStackは `M` を底に `C`, `D` の順で積まれています。3番目のStackは `P` だけが積まれています。
後半は並べ替えの手順が示されています。各ステップで指定された個数の荷物を指定番号のStack間で移動します。

上述の例の1つ目のステップではStack `2` から `1` へ 1つだけ移動し、以下のようになります。

```
[D]        
[N] [C]    
[Z] [M] [P]
 1   2   3 
```

2つ目のステップでは Stack `1` から `3` へ3つ移動しますが、 **1つずつ** 処理されるため、 `D`, `N`, `Z` の順で移動することにより、以下のようになります。

```
        [Z]
        [N]
    [C] [D]
    [M] [P]
 1   2   3 
``` 

その後、Stack `2` から `1` へ2つ移動し、

```
        [Z]
        [N]
[M]     [D]
[C]     [P]
 1   2   3 
```

最後に Stack `1` から `2` へ1つ移動し、

```
        [Z]
        [N]
        [D]
[C] [M] [P]
 1   2   3 
```

の状態になります。

与えられた初期状態からすべての手順を処理した後、各Stackの一番上に配置される荷物(の名前)を繋げると何になるでしょうか、という問題です。
この例では最終的な図が上記のようになり、 **`CMZ`** が解となります。

### 考え方

入力のparseが多少面倒ではありますが、実際にStackを作って `pop` と `push` を繰り返すシミュレーションを実装すれば良いだけです。


## part2

荷物を移動させるクレーンの機能が想定と違っていました。複数の荷物を **一気に移動させる** ことができるものでした。

前述の例で再度考えると、1つ目のステップは1つだけの移動なので同じ結果ですが、

```
[D]        
[N] [C]    
[Z] [M] [P]
 1   2   3 
```

2つ目のステップでの3つの移動は **順序が保持されたまま** Stack `1` から `3` へ動くため、以下のようになります。

```
        [D]
        [N]
    [C] [Z]
    [M] [P]
 1   2   3 
```

3つ目のステップでのStack `2` から `1` への2つの移動もそのままで動かされ、

```
        [D]
        [N]
[C]     [Z]
[M]     [P]
 1   2   3 
```

最後は以下のような状態になります。

```
        [D]
        [N]
        [Z]
[M] [C] [P]
 1   2   3 
```

このクレーンによってすべての手順が処理された後、各Stackの一番上に配置される荷物(の名前)を繋げると何になるでしょうか、という問題です。
前述の例では上記のように、 **`MCD`** が解となります。

### 考え方

基本的には part1 と同様で、移動処理の動作だけを変えることになります。
動かすものを部分配列として切り取って、移動先へ連結する際に順序を反転するか否かだけ切り替える、などの方法が考えられます。
または動かす個数だけ両端キュー(double-ended queue)に詰め替えて、「どちらの端から取り出すか」だけを切り替えるといった方法もあります。


## 実装例

### Python

```python
import sys
from typing import TextIO


class Solution:
    def __init__(self, io: TextIO) -> None:
        """入力をparseし、`stacks` と `procedure` でそれぞれ保持"""
        parts = list(map(str.splitlines, io.read().split("\n\n")))
        self.stacks: list[list[str]] = [[] for _ in range((len(parts[0][0]) + 1) // 4)]
        for line in parts[0][-2::-1]:
            for i, c in enumerate(line[1::4]):
                if c.isalpha():
                    self.stacks[i].append(c)
        self.procedure = []
        for line in parts[1]:
            self.procedure.append(tuple(map(int, line.split()[1::2])))

    def part1(self) -> str:
        return self.top_crates(True)

    def part2(self) -> str:
        return self.top_crates(False)

    def top_crates(self, reverse: bool) -> str:
        """`stacks`の移動をシミュレートし、最終状態の末尾要素を連結して返す"""
        stacks = [s[:] for s in self.stacks]
        for m, f, t in self.procedure:
            # 移動元から切り出し、同順または逆順で移動先に追加
            stacks[t - 1] += stacks[f - 1][-m:][:: -1 if reverse else 1]
            del stacks[f - 1][-m:]
        return "".join([s[-1] for s in stacks])


if __name__ == "__main__":
    solution = Solution(sys.stdin)
    print(f"Part 1: {solution.part1()}")
    print(f"Part 2: {solution.part2()}")
```

まずは入力のparseですが、空行で分割した後、前半部分を逆順で1行ずつ見ていくことで各Stackに積むべき要素を見つけていくことができます。文字が出現する場所は $4n+1$ 番目の文字で固定されているので、その位置のものが空白でなければ `.append()` していく、という操作で初期状態を作ることができました。
移動手順の部分は正規表現などを使っても良いですが、単語と数値が交互に出てくるので `.split()` して偶数番目の要素だけ `int` としてparseして取得すれば必要な情報は得られます。

あとは実際にシミュレーションしていくだけです。part1 と part2 を両方解くためにはparseして得た初期状態をコピーして使う必要があります。
長さ `m` のsliceで取得したものを移動先のStackに追加した後で、移動元から`del`で削除することによって移動処理をしています。

### Rust

```rust
use itertools::Itertools;
use std::collections::VecDeque;
use std::io::{BufRead, BufReader, Read};

struct Solution {
    stacks: Vec<Vec<char>>,
    procedure: Vec<(usize, usize, usize)>,
}

impl Solution {
    fn new(r: impl Read) -> Self {
        let lines = BufReader::new(r)
            .lines()
            .filter_map(Result::ok)
            .collect_vec();
        let parts = lines.split(String::is_empty).collect_vec();
        let mut stacks = vec![Vec::new(); (parts[0][0].len() + 1) / 4];
        for line in parts[0].iter().rev().skip(1) {
            for (i, c) in line.chars().skip(1).step_by(4).enumerate() {
                if c.is_ascii_uppercase() {
                    stacks[i].push(c);
                }
            }
        }
        Self {
            stacks,
            procedure: parts[1]
                .iter()
                .filter_map(|s| {
                    s.split_ascii_whitespace()
                        .skip(1)
                        .step_by(2)
                        .filter_map(|s| s.parse().ok())
                        .collect_tuple()
                })
                .collect(),
        }
    }
    fn part1(&self) -> String {
        self.top_crates(VecDeque::pop_front)
    }
    fn part2(&self) -> String {
        self.top_crates(VecDeque::pop_back)
    }
    fn top_crates(&self, f: impl Fn(&mut VecDeque<char>) -> Option<char>) -> String {
        // `stacks`の移動をシミュレートし、最終状態の末尾要素を連結して返す
        let mut stacks = self.stacks.clone();
        for &(count, from, to) in &self.procedure {
            let mut vd = (0..count).filter_map(|_| stacks[from - 1].pop()).collect();
            while let Some(c) = f(&mut vd) {
                stacks[to - 1].push(c);
            }
        }
        stacks.iter().filter_map(|s| s.last()).collect()
    }
}

fn main() {
    let solution = Solution::new(std::io::stdin().lock());
    println!("Part 1: {}", solution.part1());
    println!("Part 2: {}", solution.part2());
}
```

入力のparseに関してはPythonと同様の実装です。
荷物の移動は、一度 `count` 回数分だけ移動元から `.pop()` して `VecDeque` に詰め、移動先に `.push()` していくものを `pop_front()` で取り出すか `pop_back()` で取り出すかによって処理を切り替えるようにしました。
