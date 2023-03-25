---
title: "Day 17: Pyroclastic Flow"
---

https://adventofcode.com/2022/day/17

無限テトリス？


## part1

```
>>><<><>><<<>><>>><<<>>><<<><<<>><>><<>>
```

のような入力が与えられます。

落下してくる岩を押して動かそうとする気流の方向のパターンを、 `<` は左方向、 `>` は右方向で表していています。上の例では、岩は最初は右方向に押され、その後は右、右、左、左、右、の順で押されていきます。
リストの最後まで到達すると、リストの先頭に戻ってまた同じパターンを繰り返します。

岩は、以下の `#` で表されるような `-` や `+` などの形をした5種類のものが、気流パターン同様に順番に繰り返し出現します。

```
####

.#.
###
.#.

..#
..#
###

#
#
#
#

##
##
```

**幅が7単位** である縦長の部屋で、それぞれの岩は、左端が左の壁から2単位離れた、底辺が部屋で最も高い岩(岩が無い場合は床)から3単位上に現れます。

岩は出現した後、 **気流によって押される** 1単位の横方向移動 と **1単位の落下** が交互に繰り返されます。もし岩の一部分でも移動先に壁や床、または止まった岩が存在している場合、移動は起きません。落下の動きが床や止まった岩にぶつかる場合、岩はその場に静止し、次の岩がすぐに出現します。

落下する岩を `@` で、静止した岩を `#` で表すと、上述の例では以下のような動きをします。

```
The first rock begins falling:
|..@@@@.|
|.......|
|.......|
|.......|
+-------+

Jet of gas pushes rock right:
|...@@@@|
|.......|
|.......|
|.......|
+-------+

Rock falls 1 unit:
|...@@@@|
|.......|
|.......|
+-------+

Jet of gas pushes rock right, but nothing happens:
|...@@@@|
|.......|
|.......|
+-------+

Rock falls 1 unit:
|...@@@@|
|.......|
+-------+

Jet of gas pushes rock right, but nothing happens:
|...@@@@|
|.......|
+-------+

Rock falls 1 unit:
|...@@@@|
+-------+

Jet of gas pushes rock left:
|..@@@@.|
+-------+

Rock falls 1 unit, causing it to come to rest:
|..####.|
+-------+

A new rock begins falling:
|...@...|
|..@@@..|
|...@...|
|.......|
|.......|
|.......|
|..####.|
+-------+

Jet of gas pushes rock left:
|..@....|
|.@@@...|
|..@....|
|.......|
|.......|
|.......|
|..####.|
+-------+

Rock falls 1 unit:
|..@....|
|.@@@...|
|..@....|
|.......|
|.......|
|..####.|
+-------+

Jet of gas pushes rock right:
|...@...|
|..@@@..|
|...@...|
|.......|
|.......|
|..####.|
+-------+

Rock falls 1 unit:
|...@...|
|..@@@..|
|...@...|
|.......|
|..####.|
+-------+

Jet of gas pushes rock left:
|..@....|
|.@@@...|
|..@....|
|.......|
|..####.|
+-------+

Rock falls 1 unit:
|..@....|
|.@@@...|
|..@....|
|..####.|
+-------+

Jet of gas pushes rock right:
|...@...|
|..@@@..|
|...@...|
|..####.|
+-------+

Rock falls 1 unit, causing it to come to rest:
|...#...|
|..###..|
|...#...|
|..####.|
+-------+

A new rock begins falling:
|....@..|
|....@..|
|..@@@..|
|.......|
|.......|
|.......|
|...#...|
|..###..|
|...#...|
|..####.|
+-------+
```

そこからさらに幾つかの岩が落下すると、以下のような形に積み上がります。

```
|..@@@@.|
|.......|
|.......|
|.......|
|....#..|
|....#..|
|....##.|
|##..##.|
|######.|
|.###...|
|..#....|
|.####..|
|....##.|
|....##.|
|....#..|
|..#.#..|
|..#.#..|
|#####..|
|..###..|
|...#...|
|..####.|
+-------+
```

このようにして `2022`個の岩が落下して静止した後、岩は何単位の高さになっているでしょうか、という問題です。
上述の例のパターンの場合、解は **`3068`** となります。

### 考え方

ひたすら忠実にシミュレーションする実装をしていきます。
止まった岩や壁を表現するために、2次元の配列をStackとして使っても良いですし、岩の各座標を `HashSet` に入れて管理しても良いでしょう。
岩が存在する場所を `boolean` で表現して移動の可否を計算しても良いですし、1段ごとに 7bit の整数で表現しておいてビット演算で判定することもできます。


## part2

では今度は `1000000000000`個の岩が落下して静止した後、岩は何単位の高さになっているでしょうか、という問題です。
前述の例のパターンの場合、解は **`1514285714288`** となります。

### 考え方

part1 の続きとして忠実にシミュレーションしていくと、計算が終わりません。
ここで、岩も気流も数個〜数十個程度(実際のデータは1万程度ありますが)のパターンを延々と繰り返しているだけなので、岩の積み上がり方も周期的に同じパターンを繰り返すはず、と考えることができます。その周期を見つけて周期間での高さ差分を得ることができれば、掛け算を使って一気に計算することができます。

ではどうやってその周期を見つけるか、が問題です。まず明らかに必要なのが、ある岩が落下しはじめる時点での「次の岩は何か」「次の気流は何か」の情報です。岩については5種類のうち何番目か、気流についてはパターンのうち何番目か、を記録しておけば良いでしょう。
ではこの2つの値が一致するものが出現すれば周期が回ってきたと言えるでしょうか？ それだけでは足りません。床(と既に静止している岩)の状態によってその先の状態も変化し得るからです。ですので、正しく周期を検出するためには、「岩の番号」「気流の番号」そして「床・岩の状態」の3つをキーとして記録して確認する必要があります。

この「床・岩の状態」をどう表すかも難しいところです。7単位の幅それぞれで最も高い位置との差分を取る、などが簡単ですが、下図のように「気流によって横穴に入りこむ」といったことも起こり得るので、横方向も考慮しておく必要があります。

```
|.......|
|..#..@.|
|.###.@.|
|..#@@@.|
|.####..|
|  ...  |
```

ですので、正確に「床・岩の状態」を表現するならば、「最も高い岩の高さより1段上から見たときに下・左右方向で届く全範囲」をBFSなどで求めるのが確実です。例えば以下の `!` で表される場所が該当します。

```
|!!!!!!!|
|!!#!!!!|
|!!#!!!!|
|####!!!|
|..###!!|
|...#!!!|
|..####!|
+-------+
```

毎回これらの領域を求めるのは大変ですが、これならば床・岩の状態も一致した上で周期が回っているというのを検出することができます。
ただし、入力の気流パターンが すべて `<` であったりして常に片側の壁に隙間が空き続けるようなときには、この方法では周期を検出できませんので注意してください(通常は有り得ないので考慮する必要は無いと思います)。

ここまで書いておいてなんですが、実際にはこの「床・岩の状態」を考慮しなくても答えを求めることはできるようです。
「岩の番号」「気流の番号」の2つだけをキーとして検出しようとする場合、床・岩の状態が異なるために周期を誤検出してしまう可能性がありますが、それはごく序盤のときだけで、何周かした後であればパターンが安定してきます。

- 最初の数百〜数千回は無視してから記録を開始し検出を試みる
- 2周ほど同じ周期で同じ差分で高さが増加しているのを確認できたら周期検出とみなす

などの方法で誤検出は回避することができそうです。具体的な値は入力によっても異なってくるので調整が必要になりますが、一つのアイデアとして参考にしてみてください。

また、周期が残りの岩の数の約数になるまで待ってから計算する、というだけでも効果があるようです。 $n_i$ 個目の岩の開始時が高さ $h_i$ で、 $n_j$ 個目の開始時が高さ $h_j$ で同一の状態(と思われるもの)が検出されたとすると、 $n_j - n_i$ が周期となり、高さの差分が $h_j - h_i$ になります。「求める最終的な岩の数」を $n$ とすると、 $(n - n_j) \equiv 0 \mod (n_j - n_i)$ と、残りの数を周期で割り切ることができれば $h_j + ((n - n_j) \div (n_j - n_i) ) \times (h_j - h_i)$ で解が求まります。
このように求めるために、同一の状態を検出しても周期の倍数が残りの岩の数に一致するまでは無視する、というだけです。確実ではなさそうですが、実際この問題においては多くの入力に対してこの方法だけで正しい解が求まっているようです。


## 実装例

### Python

```python
import sys
from collections import deque
from itertools import cycle
from typing import TextIO


ROCKS = [
    (0j, 1j, 2j, 3j),
    (1j, 1 + 0j, 1 + 1j, 1 + 2j, 2 + 1j),
    (0j, 1j, 2j, 1 + 2j, 2 + 2j),
    (0, 1, 2, 3),
    (0j, 1j, 1 + 0j, 1 + 1j),
]


class Solution:
    def __init__(self, io: TextIO) -> None:
        self.jets = [{">": 1j, "<": -1j}[c] for c in io.read().strip()]

    def part1(self) -> int:
        return self.tower_height(2022)

    def part2(self) -> int:
        return self.tower_height(1_000_000_000_000)

    def tower_height(self, num_rocks: int) -> int:
        def empty(c: complex) -> bool:
            return c.real > 0 and 0 <= c.imag < 7 and c not in tower

        def check(pos: complex, d: complex, rock: tuple[complex, ...]) -> bool:
            return all(empty(pos + d + r) for r in rock)

        tower: set[complex] = set()
        cache: dict[tuple[int, int, frozenset[complex]], tuple[int, int]] = dict()
        rocks = cycle(enumerate(ROCKS))
        jets = cycle(enumerate(self.jets))
        top, i, j = 0, 0, 0
        for n in range(num_rocks):
            key = self.key(tower, top)
            if prev := cache.get((i, j, key)):
                d, m = divmod(num_rocks - n, n - prev[0])
                if m == 0:
                    return top + d * (top - prev[1])
            else:
                cache[(i, j, key)] = n, top

            pos = complex(top + 4, 2)
            i, rock = next(rocks)
            while True:
                j, jet = next(jets)
                if check(pos, jet, rock):
                    pos += jet
                if check(pos, -1, rock):
                    pos += -1
                else:
                    break
            tower |= {pos + r for r in rock}
            top = max(top, int(pos.real) + max(int(c.real) for c in rock))

        return top

    @staticmethod
    def key(tower: set[complex], top: int) -> frozenset[complex]:
        ret = set()
        q = deque([0 + 0j])
        while q:
            c = q.popleft()
            for d in [d for d in [(c - 1), (c - 1j), (c + 1j)] if d not in ret]:
                if d.imag in range(7) and -d.real <= top and top + 1 + d not in tower:
                    ret.add(d)
                    q.append(d)
        return frozenset(ret)


if __name__ == "__main__":
    solution = Solution(sys.stdin)
    print(f"Part 1: {solution.part1()}")
    print(f"Part 2: {solution.part2()}")
```

2次元の座標を [day09](./day09) と同様に `complex` で表現し、静止した岩の座標をすべて `set[complex]` で管理するようにしています。
移動のシミュレーションは、岩を形成する全座標について移動先の座標が壁や床でなく、かつ静止している岩に重ならないか、をチェックしています。
岩や気流は `enumerate` と `itertools.cycle` を使って番号を取りながら繰り返し取り出すことができるようにしています。

周期のチェックには BFS で下、左、右の方向に探索して岩の頂上の形状を `fronzenset[complex]` で表現しています。
少なくとも私の入力では `key` 関数はここまでせず定数値を返すだけでも正解は得られましたが、正しく実装するならこのようにする必要がありそうです。

### Rust

```rust
use itertools::Itertools;
use std::collections::HashMap;
use std::io::Read;

const ROCKS: [[u8; 4]; 5] = [
    [0b0001_1110, 0b0000_0000, 0b0000_0000, 0b0000_0000],
    [0b0000_1000, 0b0001_1100, 0b0000_1000, 0b0000_0000],
    [0b0001_1100, 0b0000_0100, 0b0000_0100, 0b0000_0000],
    [0b0001_0000, 0b0001_0000, 0b0001_0000, 0b0001_0000],
    [0b0001_1000, 0b0001_1000, 0b0000_0000, 0b0000_0000],
];

enum Direction {
    Left,
    Right,
}

struct Solution {
    jet_patterns: Vec<Direction>,
}

impl Solution {
    fn new(mut r: impl Read) -> Self {
        let mut buf = String::new();
        r.read_to_string(&mut buf).ok();
        Self {
            jet_patterns: buf
                .trim()
                .chars()
                .map(|c| match c {
                    '<' => Direction::Left,
                    '>' => Direction::Right,
                    _ => unreachable!(),
                })
                .collect(),
        }
    }
    fn part1(&self) -> u64 {
        self.tower_height(2022)
    }
    fn part2(&self) -> u64 {
        self.tower_height(1_000_000_000_000)
    }
    fn tower_height(&self, num_rocks: usize) -> u64 {
        let mut tower = vec![0; 0];
        let mut hm = HashMap::new();
        let mut ij = 0;
        for i in 0..num_rocks {
            let ir = i % ROCKS.len();
            let key = (ir, ij, tower.iter().rev().take(4).cloned().collect_vec());
            if let Some((pi, plen)) = hm.get(&key) {
                if (num_rocks - i) % (i - pi) == 0 {
                    return ((num_rocks - i) / (i - pi) * (tower.len() - plen) + tower.len())
                        as u64;
                }
            } else {
                hm.insert(key, (i, tower.len()));
            }
            let mut rock = ROCKS[ir];
            let mut j = tower.len() + 3;
            tower.extend(vec![0; 7]);
            loop {
                let jet = &self.jet_patterns[ij];
                ij = (ij + 1) % self.jet_patterns.len();
                match jet {
                    Direction::Left => {
                        if rock
                            .iter()
                            .enumerate()
                            .all(|(k, u)| u & 0x40 == 0 && tower[j + k] & (u << 1) == 0)
                        {
                            rock.iter_mut().for_each(|u| *u <<= 1);
                        }
                    }
                    Direction::Right => {
                        if rock
                            .iter()
                            .enumerate()
                            .all(|(k, u)| u & 0x01 == 0 && tower[j + k] & (u >> 1) == 0)
                        {
                            rock.iter_mut().for_each(|u| *u >>= 1);
                        }
                    }
                }
                if j == 0
                    || rock
                        .iter()
                        .enumerate()
                        .any(|(k, u)| u & tower[j + k - 1] != 0)
                {
                    break;
                }
                j -= 1;
            }
            rock.iter().enumerate().for_each(|(k, u)| tower[j + k] |= u);
            while let Some(&last) = tower.last() {
                if last == 0 {
                    tower.pop();
                } else {
                    break;
                }
            }
        }
        tower.len() as u64
    }
}

fn main() {
    let solution = Solution::new(std::io::stdin().lock());
    println!("Part 1: {}", solution.part1());
    println!("Part 2: {}", solution.part2());
}
```

こちらは岩の座標を `Vec<u8>` のStackで管理しています。各段における幅7単位の状態をビット列で表現しています。
それぞれの岩も `[u8; 4]` で表現し、論理積を使って高速に重なりをチェックできます。

周期の検出用のキーとしてはこちらはStackの末尾4段を取得して使っていますが、Python同様、これは無くても正解は得られました。
