---
title: "Day 7: No Space Left On Device"
---

https://adventofcode.com/2022/day/7

ファイルシステム、のようですが。


## part1

```
$ cd /
$ ls
dir a
14848514 b.txt
8504156 c.dat
dir d
$ cd a
$ ls
dir e
29116 f
2557 g
62596 h.lst
$ cd e
$ ls
584 i
$ cd ..
$ cd ..
$ cd d
$ ls
4060174 j
8033020 d.log
5626152 d.ext
7214296 k
```

のような入力が与えられます。

ファイルとディレクトリからなる木構造のファイルシステムでの、ターミナル入出力を表しています。
`$` で始まる行は実行したコマンドで、

- `cd` はディレクトリの移動
  - `cd x` は今いるディレクトリ上にあるディレクトリ `x` への移動
  - `cd ..` は1つ上の階層への移動
  - `cd /` は最も上の階層への移動
- `ls` は今いるディレクトリ内の、ファイルまたはディレクトリのリストを表示
  - `123 abc` はサイズ `123` のファイルであることを示す
  - `dir xyz` は `xyz` という名前のディレクトリであることを示す

馴染みのある形式のコマンドと出力です。
上述の例で得られた出力からは、以下のようなツリー構造を得ることができます。

```
- / (dir)
  - a (dir)
    - e (dir)
      - i (file, size=584)
    - f (file, size=29116)
    - g (file, size=2557)
    - h.lst (file, size=62596)
  - b.txt (file, size=14848514)
  - c.dat (file, size=8504156)
  - d (dir)
    - j (file, size=4060174)
    - d.log (file, size=8033020)
    - d.ext (file, size=5626152)
    - k (file, size=7214296)
```

各ディレクトリの持つ **合計サイズ** を求めようとしています。これは、そのディレクトリが直接または間接的に持つファイルのサイズの合計値です。

- ディレクトリ `e` は、サイズ `584` のファイル `i` だけを持つので合計サイズは **`584`**
- ディレクトリ `a` は、ファイル `f` (サイズ `29116`), `g` (サイズ `2557`), `h.lst` (サイズ `62596`) を持ち、また間接的に `i` を持つので合計サイズは **`94853`**
- ディレクトリ `d` は、4つのファイルを持つので合計サイズは **`24933642`**
- 最上ディレクトリ `/` は、すべてのファイルを持つことになるので合計サイズは **`48381165`**

となります。

まずは、この合計サイズが `100000` 以下のものを列挙しようとしています。該当するディレクトリの合計サイズをすべて足し合わせるといくらになるでしょうか、という問題です。
上述の例では、`a` と `e` が条件に合致するので、`94853 + 584` で **`95437`** が解となります(ここではファイルを重複カウントしていても許されます)。

### 考え方

全ディレクトリに対して、それぞれ合計サイズを求める必要があります。
まずは各コマンドに対する出力からこのファイルシステムを表す木構造を構築し、最上ディレクトリから再帰的に探索することで求めることはできます。
が、実際にはそこまでしなくても合計サイズを求める方法もあります。

少なくともこの問題の入力ではディレクトリ移動とリスト表示は順序よく行われており、同じディレクトリを何度も訪れたり同じディレクトリでのリスト表示を何度も繰り返したりしていません。
すべてのファイルは正しく1回ずつ表示されるので、それが存在するディレクトリ **と、その上位のディレクトリたちに** ファイルのサイズを加算していくことで各ディレクトリの合計サイズが求まります。

前述の例を、今いるディレクトリだけを管理しながら順番に見ていくと、

- `$ cd /` => **`/` に移動**
- `$ ls`
  - `14848514`, `8504156` の2つを `/` に加算
- `$ cd a` => **`/a` に移動**
- `$ ls`
  - `29116`, `2557`, `62596` の3つを `/a` **と上位の `/` にそれぞれ** 加算
- `$ cd e` => **`/a/e` に移動**
- `$ ls`
  - `584` を `/a/e/` **と上位の `/a` と `/` にそれぞれ** 加算
- `$ cd ..` => **`/a` に移動**
- `$ cd ..` => **`/` に移動**
- `$ cd d` => **`/d` に移動**
- `$ ls`
  - `4060174`, `8033020`, `5626152`, `7214296` を `/d` **と上位の `/` にそれぞれ** 加算

という操作をしていけば良いです。
これで全ディレクトリの合計サイズを求めることができるので、その中から `100000` 以下のものを抽出して足し合わせることで解が求められます。


## part2

このファイルシステムの全容量は **`70000000`** で、今 **`30000000`** 以上の空き容量が必要です。
あるディレクトリを丸ごと削除することで必要な空き容量を確保しようとしています。それを実現できる最小のディレクトリの合計サイズはいくらになるでしょうか、という問題です。
前述の例では、現在使用している合計の容量(すなわち最上ディレクトリの合計サイズ)が `48381165` なので、空き容量は `21618835` です。`30000000` 以上の空き容量を確保するためには少なくとも `8381165` 以上の合計サイズを持つディレクトリを削除する必要があります。

- ディレクトリ `e` を削除すると空き容量は `584` 増える
- ディレクトリ `a` を削除すると空き容量は `94853` 増える
- ディレクトリ `d` を削除すると空き容量は `24933642` 増える
- 最上ディレクトリ `/` を削除すると空き容量は `48381165` 増える

ことになりますが、 `e` と `a` は小さすぎて条件を満たしません。従って、次に小さい値である `d` を削除したときの **`24933642`** が解となります。

### 考え方

part1 で全ディレクトリの合計サイズが算出できていれば、`最上ディレクトリの合計サイズ - ディレクトリの合計サイズ < 40000000` を満たすものを抽出できるので、その中から最小値を選べば良いだけです。


## 実装例

### Python

```python
import sys
from collections import defaultdict
from typing import TextIO


class Solution:
    def __init__(self, io: TextIO) -> None:
        self.total_sizes: dict[tuple[str, ...], int] = defaultdict(int)
        curr: list[str] = []
        for line in io:
            parts = line.strip().split()
            if parts[:2] == ["$", "cd"]:
                if parts[2] == "..":
                    curr.pop()
                else:
                    curr.append(parts[2])
            if parts[0].isnumeric():
                for i in range(len(curr)):
                    self.total_sizes[tuple(curr[: i + 1])] += int(parts[0])

    def part1(self) -> int:
        return sum(filter(lambda x: x <= 100_000, self.total_sizes.values()))

    def part2(self) -> int:
        total = self.total_sizes[tuple(["/"])]
        return min(filter(lambda x: total - x < 40_000_000, self.total_sizes.values()))


if __name__ == "__main__":
    solution = Solution(sys.stdin)
    print(f"Part 1: {solution.part1()}")
    print(f"Part 2: {solution.part2()}")
```

今いるディレクトリを `list[str]` で管理し、移動とともに `.pop()` と `.append(...)` で更新していきます。それ(を `tuple` にしたもの)を key とした `defaultdict` で合計サイズを管理します。
ファイルが見つかった場合、そのディレクトリと上位のディレクトリすべてに足し合わせていきます。毎回階層深さ分のループをすることにはなりますが、異常に深いディレクトリに大量のファイルが出てこない限りは計算量的には問題ないと思います。

あとは条件に合うものを `filter` で見つけ出せば良いだけです。

### Rust

```rust
use std::io::{BufRead, BufReader, Read};

struct Solution {
    total_sizes: Vec<u32>,
}

impl Solution {
    fn new(r: impl Read) -> Self {
        let mut stack = Vec::new();
        let mut total_sizes = Vec::new();
        for line in BufReader::new(r).lines().filter_map(Result::ok) {
            match line.rsplit_once(char::is_whitespace) {
                Some(("$ cd", d)) => {
                    if d == ".." {
                        if let Some(total) = stack.pop() {
                            total_sizes.push(total);
                            if let Some(last) = stack.last_mut() {
                                *last += total;
                            }
                        }
                    } else {
                        stack.push(0);
                    }
                }
                Some((s, _)) => {
                    if let Ok(size) = s.parse::<u32>() {
                        if let Some(last) = stack.last_mut() {
                            *last += size;
                        }
                    }
                }
                _ => unreachable!(),
            }
        }
        while let Some(total) = stack.pop() {
            total_sizes.push(total);
            if let Some(last) = stack.last_mut() {
                *last += total;
            }
        }
        Self { total_sizes }
    }
    fn part1(&self) -> u32 {
        self.total_sizes.iter().filter(|&x| *x <= 100_000).sum()
    }
    fn part2(&self) -> u32 {
        *self
            .total_sizes
            .iter()
            .filter(|&x| self.total_sizes[self.total_sizes.len() - 1] - x < 40_000_000)
            .min()
            .unwrap()
    }
}

fn main() {
    let solution = Solution::new(std::io::stdin().lock());
    println!("Part 1: {}", solution.part1());
    println!("Part 2: {}", solution.part2());
}
```

こちらは stack だけを使って全ディレクトリの合計サイズを求めるように実装してみました。

ディレクトリ移動は順序よく実行されているので、 `$ cd ..` された時点で **そのディレクトリ以下のファイルはすべてチェックし終わっている** と考えることができます。 なので、stack を1つ用意して「今いるディレクトリのファイルサイズ合計」を末尾要素に足し合わせていき、 `pop()` した際にその合計をまた新しい末尾要素に足し合わせる、という操作をしていくことでディレクトリの合計サイズを計算していくことができます。もやはディレクトリの名前も必要ありません。

あとはこの stack から `.pop()` するごとにその値を `Vec` で保持しておけば良いだけです。すべて実行し終わった後に stack が空になるまで `pop()` する操作が必要になるので注意します。一番最後に `.pop()` されて得た合計サイズが最上ディレクトリの合計サイズ(すなわち全ファイルのサイズ総計)になります。
