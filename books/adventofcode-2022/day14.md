---
title: "Day 14: Regolith Reservoir"
---

https://adventofcode.com/2022/day/14

これも物理シミュレーション…？


## part1

```
498,4 -> 498,6 -> 496,6
503,4 -> 502,4 -> 502,9 -> 494,9
```

のような入力が与えられます。

各行はXY座標上で岩がある位置を直線経路で表現しています。最初の座標以降に続く各座標は前の座標から引くべき垂直または水平の直線の終点を表しています。
この例では2本の直線からなる岩の壁と、3本の直線からなる岩の壁があることを意味しています。

そしてこの座標系において、 `500, 0` の位置から砂が流れ込んできます。
上述の例を、岩を `#` で、空間を `.` で、砂の流入源を `+` で表現すると、以下のようになります。

```

  4     5  5
  9     0  0
  4     0  3
0 ......+...
1 ..........
2 ..........
3 ..........
4 ....#...##
5 ....#...#.
6 ..###...#.
7 ........#.
8 ........#.
9 #########.
```

砂は **1単位ずつ** 流入し、それが静止するまで次の砂は現れません。

1単位の砂は可能な限り **1段ずつ落下** します。すぐ下の段が岩または砂で塞がっている場合は、代わりに **1つ左下** の斜め方向に移動を試みます。その方向も岩または砂で塞がっている場合は、今度は **1つ右下** への移動を試みます。砂は各ステップごとに下、左下、右下、の順に移動を試み、可能な限り移動を続けます。3つの移動先候補がすべて岩または砂で塞がっていたときに、砂はその場所に **静止** します。そして次の1単位の砂がまた流入源に現れます。

静止した砂を `o` で表現すると、上述の例で 最初の1単位の砂は真っ直ぐに落下して静止します。

```
......+...
..........
..........
..........
....#...##
....#...#.
..###...#.
........#.
......o.#.
#########.
```

次の1単位の砂は同様に落下して最初の砂の上に着地し、その左隣で静止します。

```
......+...
..........
..........
..........
....#...##
....#...#.
..###...#.
........#.
.....oo.#.
#########.
```

このようにして合計5単位の砂が静止した後、以下のようなパターンになります。

```
......+...
..........
..........
..........
....#...##
....#...#.
..###...#.
......o.#.
....oooo#.
#########.
```

22単位までが静止すると、以下のようなパターンになります。

```
......+...
..........
......o...
.....ooo..
....#ooo##
....#ooo#.
..###ooo#.
....oooo#.
...ooooo#.
#########.
```

そして、ここからあと2単位だけが静止することができます。

```
......+...
..........
......o...
.....ooo..
....#ooo##
...o#ooo#.
..###ooo#.
....oooo#.
.o.ooooo#.
#########.
```

これ以降の砂は以下の `~` の経路を通って無限の底に落ちていきます。

```
.......+...
.......~...
......~o...
.....~ooo..
....~#ooo##
...~o#ooo#.
..~###ooo#.
..~..oooo#.
.~o.ooooo#.
~#########.
~..........
~..........
~..........
```

このように砂が無限の底に流れていくようになるまでに、静止した砂は何単位になるでしょうか、という問題です。
この例では、上述の通り **`24`** が解となります。

### 考え方

XY座標で表される2次元の空間を用意して定義通りにシミュレーションを行うことで求めることができます。
空間は2次元の `boolean` 配列でも良いですし、`Set` などで座標の集合を管理しても良いでしょう。配列の場合はサイズが気になりますが、 `500, 0` から正の値の領域で斜めもしくは下にしか動かないことを考えると `1000, 500` が最大の値になりそうです。
あとは入力で与えられる岩の壁の直線を1マスずつ最初に埋めておき、砂が流入源から移動して静止するたびにその位置を埋めていくという操作をすることでシミュレーションを行うことができるでしょう。

あとは無限の底に落ちていくか否かの判定ですが、最初に岩の壁のY座標の最大値を求めておくと良いでしょう。砂の移動においてY座標は常に増加するので、この値がどの岩の壁よりも大きな値になったらその先は決して静止することはありません。


## part2

無限の底は存在しておらず、 **岩の壁の最も高いY座標 `+2`** の高さに床がありました。この床は水平方向に無限に続いているとします。

前述の例では、岩の壁のY座標の最大値が `9` だったので、以下のように `y=11` の直線の(`-infinity,11 -> infinity,11` のような)岩の壁が追加される形になります。

```
        ...........+........
        ....................
        ....................
        ....................
        .........#...##.....
        .........#...#......
        .......###...#......
        .............#......
        .............#......
        .....#########......
        ....................
<-- etc #################### etc -->
```

今度は砂が `500, 0` で静止し流入源が塞がれるまでシミュレートします。
この例では、以下のような状態になったところで砂の流入源が塞がれます。

```
............o............
...........ooo...........
..........ooooo..........
.........ooooooo.........
........oo#ooo##o........
.......ooo#ooo#ooo.......
......oo###ooo#oooo......
.....oooo.oooo#ooooo.....
....oooooooooo#oooooo....
...ooo#########ooooooo...
..ooooo.......ooooooooo..
#########################
```

このように流入源が塞がれるまでに、静止した砂は何単位になるでしょうか、という問題です。
この例では、上図になるまでの **`93`** が解となります。

### 考え方

基本的には part1 と同じシミュレーションを行うことで求められます。
「岩の壁のY座標の最大値より大きな値になったら終了」としていたところを、代わりに `Y座標最大値+2` に壁があると仮定して静止させて また次の砂の計算を続け、 `500, 0` で停止するようになったら終了するようにすれば良いでしょう。

しかし実際にやってみると、計算が終わらないというほどではないですが多少時間がかかってしまうと思います。
もう少し計算量を減らす方法を考えてみます。

1単位ずつ落ちてくる砂は、必ず同じ場所から出発して、途中までは直前の砂と同じ経路を辿っている、ということに気付くでしょうか。1番目の砂が落下して静止した後、2番目の砂は静止した1番目の砂にぶつかるまではまったく同じ経路を辿って落下しますね。3番目もやはり同じ経路を辿って落下します。ぶつかって左右に滑り落ちるところは処理が変わりますが、そこまでの落下は何度も同じ計算をするのが無駄に思えます。

砂の移動を「進む方向を3方向のうちどれかから選択する」過程の繰り返し、と考えるとどうでしょうか。行き止まりになって静止すると、一つ前の状態から別の選択肢を選んでまた進む、ということを繰り返します。これはDFS(depth-first search, 深さ優先探索)とまったく同じ動きです。
ですので、stackや再帰などを用いてDFSを実装すれば、静止したあとは直前の位置に戻ってまた別の方向への移動を試みる、だけなのでそこまでの途中経過を再計算する必要がなくなり、計算量を大幅に削減することができます。


## 実装例

### Python

```python
import sys
from ast import literal_eval
from itertools import pairwise, product
from typing import TextIO


class Solution:
    def __init__(self, io: TextIO) -> None:
        self.cave = set()
        self.ymax = 0
        for line in map(str.strip, io):
            for (x0, y0), (x1, y1) in pairwise(map(literal_eval, line.split(" -> "))):
                xs = range(min(x0, x1), max(x0, x1) + 1)
                ys = range(min(y0, y1), max(y0, y1) + 1)
                self.cave |= set(product(xs, ys))
                self.ymax = max(self.ymax, y0, y1)

    def part1(self) -> int:
        return self.count_units(False)

    def part2(self) -> int:
        return self.count_units(True)

    def count_units(self, floor: bool) -> int:
        """終了条件を満たすまでシミュレーションを繰り返し、静止した砂の数を返す"""
        block = set(self.cave)
        stack = [(500, 0)]
        while stack:
            x, y = stack[-1]
            candidates = [(x, y + 1), (x - 1, y + 1), (x + 1, y + 1)]
            if n := next((p for p in candidates if p not in block), None):
                if y < self.ymax + 1:
                    stack.append(n)
                    continue
                elif not floor:
                    break
            block.add(stack.pop())
        return len(block) - len(self.cave)


if __name__ == "__main__":
    solution = Solution(sys.stdin)
    print(f"Part 1: {solution.part1()}")
    print(f"Part 2: {solution.part2()}")
```

最初の入力の処理は、各行を `.split(" -> ")` した後、座標を表す部分を再び `.split(".")` してそれぞれ `int()` する手間を省くため [day13](./day13) でも使用した `ast.literal_eval` でparseしています。
そして Python3.10 から使用できるようになった `itertools.pairwise` 関数で、隣り合う要素のペアを順番に取り出しています。X座標とY座標でそれぞれ `range` を作って、それらの積集合を `itertools.product` でとれば水平方向でも垂直方向でも関係なく壁の座標の集合が得られます。

あとは stack を利用してDFSを実装します。 `(500, 0)` から始めて `(x, y + 1)`, `(x - 1, y + 1)`, `(x + 1, y + 1)` のうち最初に進めるものを選択します。進めるものが見つかった場合はそれを stack に積み、また同じことを繰り返します。どこにも進めなくなったら、その時点での stack 末尾を `pop()` して `block` に追加し、次の末尾要素をもとにまた選択を繰り返していきます。
part1 は `floor` が無いので `self.ymax + 1` まで到達したらその時点で探索終了、 part2 は `floor` が有るためそこでは静止するだけで `stack` が空になるまで探索を続けます。 `len(block)` と `len(self.cave)` の差分が、静止した砂の単位数となります。

### Rust

```rust
use itertools::Itertools;
use std::io::{BufRead, BufReader};

struct Solution {
    cave: Vec<Vec<bool>>,
    ymax: usize,
}

impl Solution {
    fn new(r: impl std::io::Read) -> Self {
        let mut cave = vec![vec![false; 500]; 1001];
        let mut ymax = 0;
        for line in BufReader::new(r).lines().filter_map(Result::ok) {
            for (p0, p1) in line
                .split(" -> ")
                .filter_map(|xy| {
                    xy.split(',')
                        .filter_map(|s| s.parse().ok())
                        .collect_tuple::<(usize, usize)>()
                })
                .tuple_windows()
            {
                (p0.0.min(p1.0)..=p0.0.max(p1.0)).for_each(|x| cave[x][p0.1] = true);
                (p0.1.min(p1.1)..=p0.1.max(p1.1)).for_each(|y| cave[p0.0][y] = true);
                ymax = ymax.max(p0.1.max(p1.1));
            }
        }
        Self { cave, ymax }
    }
    fn part1(&self) -> u32 {
        self.count_units(false)
    }
    fn part2(&self) -> u32 {
        self.count_units(true)
    }
    fn count_units(&self, floor: bool) -> u32 {
        let mut block = self.cave.clone();
        let mut stack = vec![(500, 0)];
        let mut units = 0;
        while let Some(&(x, y)) = stack.last() {
            if let Some(&next) = [(x, y + 1), (x - 1, y + 1), (x + 1, y + 1)]
                .iter()
                .find(|p| !block[p.0][p.1])
            {
                if y < self.ymax + 1 {
                    stack.push(next);
                    continue;
                } else if !floor {
                    break;
                }
            }
            if let Some((x, y)) = stack.pop() {
                block[x][y] = true;
                units += 1;
            }
        }
        units
    }
}

fn main() {
    let solution = Solution::new(std::io::stdin().lock());
    println!("Part 1: {}", solution.part1());
    println!("Part 2: {}", solution.part2());
}
```

Pythonと同様の実装ですが、こちらは座標の集合を使わずに `Vec<Vec<bool>>` で `1001 x 500` の配列を最初に確保して使うようにしました。集合サイズは取れないので、DFSの中で明示的に砂の単位数をカウントしています。
