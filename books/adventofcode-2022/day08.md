---
title: "Day 8: Treetop Tree House"
---

https://adventofcode.com/2022/day/8

2次元配列を、色々な方向から。


## part1

```
30373
25512
65332
33549
35390
```

のような入力が与えられます。

それぞれの数値はグリッド上にある木の高さを示しています。
各木は、その木とグリッドの端との間にあるすべての木が **その木より低い** 場合に、外側から **見える** とします。

では外側から見える木は全部で何本あるでしょうか、という問題です。
上述の例では、グリッドの端にある木はすべて **見える** ということになります。内側にある9本について考えると、

- 左上の `5` は、右や下からは見えないが左と上からは **見える**
- 上段中央の `5` は、右と上から **見える**
- 右上の `1` は、端との間がすべて `0` でないといけないが、そうではないので見えない
- 中段左の `5` は、右からだけ **見える**
- 中央の `3` は、どこからも見えない
- 中段右の `3` は、右から **見える**
- 下段は、中央の `5` は **見える** が、 `3` と `4` は見えない

となるため、全部で **`21`** が解となります。

### 考え方

最初にグリッドと同じサイズの2次元bool配列を用意してから、上下左右の4方向から木の高さを確認しながら奥まで進んでいくことで、見えるか否かを確認します。それまでに見えた木の高さの最大値より高ければその木は **見える** と判定できます。最後に `true` になっている数をカウントすれば良いでしょう。


## part2

今度は各木からの **景色のスコア** を考えます。
視距離というものを「ある方向を見たときにグリッドの端まで行くか、もしくは同じ高さ以上の木で止まるまでの距離」と定義し、それぞれの木から各4方向の視距離を **掛け合わせて** 計算されます。

最も高い **景色のスコア** はいくらになるでしょうか、という問題です。
前述の例では、グリッドの端にある木はすべて端方向が視距離 `0` のため、やはり内側にある9本について考えます。
例えば上段中央の `5` は、

- 上方向: 端まで見通すことができ、視距離は **`1`**
- 左方向: すぐ隣で止まり、視距離は **`1`**
- 右方向: 端まで見通すことができ、視距離は **`2`**
- 下方向: 2つ下の `5` で止まり、視距離は **`2`**

なのでスコアは `1 * 1 * 2 * 2` で **`4`** になります。
が、下段中央の `5` について見ると

- 上方向: 2つ上の `5` で止まり、視距離は **`2`**
- 左方向: 端まで見通すことができ、視距離は **`2`**
- 下方向: 端まで見通すことができ、視距離は **`1`**
- 右方向: 2つ右の `9` で止まり、視距離は **`2`**

なのでスコアは `2 * 2 * 1 * 2` で **`8`** になり、これが最も高い数値として解になります。

### 考え方

「その木と同じ高さ以上の木が最後に出現した場所」は Monotonic Stack などを使用して効率的に求めることができるかもしれませんが、そこまで大きなグリッドでもないので単純に「すべての木を順番に見ていってそれぞれ4方向についての視距離を計算していく」という手法でも問題ありません。
ただ実装は面倒になりがちで、簡潔に書くためのテクニックが使えると良いと思います。


## 実装例

### Python

```python
import sys
from itertools import chain
from typing import TextIO


class Solution:
    def __init__(self, io: TextIO) -> None:
        def rotate90(grid: list[list[int]]) -> list[list[int]]:
            """`grid`の要素を90度回転させる"""
            return list(map(list, zip(*grid[::-1])))

        grid = [list(map(int, s.strip())) for s in io]
        self.v = [[0 for _ in row] for row in grid]
        self.s = [[1 for _ in row] for row in grid]
        for _ in range(4):
            for i, row in enumerate(grid):
                for j, col in enumerate(row):
                    lower = [h < col for h in row[j + 1 :]]
                    self.v[i][j] |= all(lower)
                    self.s[i][j] *= len(lower) if all(lower) else lower.index(False) + 1
            grid, self.v, self.s = map(rotate90, [grid, self.v, self.s])

    def part1(self) -> int:
        return sum(chain(*self.v))

    def part2(self) -> int:
        return max(chain(*self.s))


if __name__ == "__main__":
    solution = Solution(sys.stdin)
    print(f"Part 1: {solution.part1()}")
    print(f"Part 2: {solution.part2()}")
```

各方向についての計算を実装するかわりに、グリッド全体を回転させながら1方向だけの計算を4回繰り返すことで「外側から見えるか否か」と「視距離」をそれぞれ計算しています。

```python
list(map(list, zip(*grid[::-1])))
```

というのは魔法のようなコードですが、これは各行を逆順で末尾要素から取り出し新しいリストを作ることによって元のグリッドを90度回転させた新しいグリッドを作るものです。

あとはその4回の回転の中で各要素 `grid[i][j]` について、 `grid[i][j+1:]` のスライスだけを見れば、4方向について計算するのと同じことが実現できます。
切り出したスライスの各要素について「該当の木より低いか否か」を判定しておけば、 `all()` で「端まで見通せる」すなわち「外側から見えるか否か」を判定できます。視距離についても、 `all()` が真であれば `len()` がそのまま視距離になり、偽の場合は最初に `False` が現れた位置を `index()` で取得して `+1` することで求められます。

あとはそれぞれ論理和や積を取っていくだけです。

### Rust

```rust
use itertools::Itertools;
use std::io::{BufRead, BufReader, Read};

struct Solution {
    trees: Vec<(bool, usize)>,
}

impl Solution {
    fn new(r: impl Read) -> Self {
        let grid = BufReader::new(r)
            .lines()
            .filter_map(Result::ok)
            .map(|line| line.bytes().map(|b| b - b'0').collect::<Vec<_>>())
            .collect::<Vec<_>>();
        let (rows, cols) = (grid.len(), grid[0].len());
        Self {
            trees: (0..rows)
                .cartesian_product(0..cols)
                .map(|(i, j)| {
                    let h = grid[i][j];
                    [
                        (0..i).rev().map(|ii| grid[ii][j]).collect::<Vec<_>>(),
                        (0..j).rev().map(|jj| grid[i][jj]).collect::<Vec<_>>(),
                        (i + 1..rows).map(|ii| grid[ii][j]).collect::<Vec<_>>(),
                        (j + 1..cols).map(|jj| grid[i][jj]).collect::<Vec<_>>(),
                    ]
                    .iter()
                    .fold((false, 1), |acc, x| {
                        (
                            acc.0 | x.iter().all(|&e| e < h),
                            acc.1 * x.iter().position(|&e| e >= h).map_or(x.len(), |p| p + 1),
                        )
                    })
                })
                .collect(),
        }
    }
    fn part1(&self) -> usize {
        self.trees.iter().filter(|(visible, _)| *visible).count()
    }
    fn part2(&self) -> usize {
        self.trees.iter().map(|(_, score)| *score).max().unwrap()
    }
}

fn main() {
    let solution = Solution::new(std::io::stdin().lock());
    println!("Part 1: {}", solution.part1());
    println!("Part 2: {}", solution.part2());
}
```

こちらは、グリッドの回転はしない代わりに `grid[i][j]` について各4方向に見ていったときの要素を集めた `Vec` を最初に4つ用意して、それぞれに対し共通の処理をすることで似たようなことを実現しています。
求めたいのはカウントか最大値なので計算結果はグリッドで保持する必要もなく、1次元の `Vec` にまとめてしまっています。
