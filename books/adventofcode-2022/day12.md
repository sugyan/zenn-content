---
title: "Day 12: Hill Climbing Algorithm"
---

https://adventofcode.com/2022/day/12

最短経路、下から見るか？上から見るか？


## part1

```
Sabqponm
abcryxxl
accszExk
acctuvwj
abdefghi
```

のような入力が与えられます。

グリッド状の標高地図で、各マス目の文字はその位置の高さを表しています。 `a` が最も低く `b` が次に低く、という具合に最も高い標高 `z` まで高くなっていきます。
また、高さが `a` である「現在地」が `S` 、高さが `z` である「目的地」が `E` で表されています。

ここで、 **できるだけ少ない** ステップで `S` から `E` へ到達したいと考えています。
各ステップでは、上下左右に1マスだけ移動しますが、移動先は現在の高さよりも **最大1段階だけ高い** ところまでに限られます。つまり、もし今いる高さが `m` の場合、 `n` へは移動できますが `o` には移動できません(ずっと低いところに移動することは可能です)。

`S` から `E` へ到達する最短ステップ数はいくつでしょうか、という問題です。
上述の例では、左上からスタートして 最初は下にも右にも移動できます。どちらの場合でも結局は最下段の `e` に向かう必要があり、そこから渦を巻くようにして `E` に到達します。

以下は、ある経路を通るときの移動方向を 上(`^`)、下(`v`)、左(`<`)、右(`>`) で示したものです。 `.` は訪問しなかったマス目になります。

```
v..v<<<<
>v.vv<<^
.>vv>E^^
..v>>>^^
..>>>>>^
```

この経路は **31** ステップで到達し、最短である解となります。

### 考え方

最短経路問題ということになりますが、これはBFS(Breadth-first search, 幅優先探索)で各マスへの最短ステップ数を求めていくのが簡単です。
既に最短ステップ数が分かっているか否かを管理しながら、移動できる方向を判定して両端キューに追加していく、といった実装で最終的に `E` に到達したときの最短ステップ数を求めることができます。


## part2

今度はスタート地点が `S` の位置に限定されなくなります。
依然として目的地は `E` ですが、標高が `a` であるマス目からスタートして目的地に到達する最短ステップ数はいくつでしょうか、という問題です。
前述の例では、スタート地点の選択肢が 6個あります(`a` のマスが5個、`S` のマスも高さ `a` として扱われます)。左下のマスから開始すると、最も早く目的地に到達できます。

```
...v<<<<
...vv<<^
...v>E^^
.>v>>>^^
>^>>>>>^
```

この経路は **29** ステップで到達し、最短である解となります。

### 考え方

開始地点を変えながら part1 と同様に `E` までの最短ステップ数を求めていってそれらの最小値を求めても良いですが、与えられる入力は `a` のマスが数多くあり、すべてを試して計算しようとすると何百〜何千倍もの時間がかかってしまいます。

ここで逆転の発想です。隣接するマス間の移動の可否は固定されているので、じつは逆向きに考えても同様に最短ステップ数を求めていくことができます。
part1 と同様のBFSで、 `E` をスタート地点として逆方向に各マスへの最短ステップ数を求めていきます。すると、part1 は `S` までの最短ステップ数、part2 は `S` または `a` のいずれかのマスまでの最短ステップ数を求めれば良い、ということになります。


## 実装例

### Python

```python
import sys
from collections import defaultdict, deque
from typing import TextIO


class Solution(Solve):
    def __init__(self, io: TextIO) -> None:
        grid = [list(line.strip()) for line in io]
        d: deque[tuple[tuple[int, int], int]] = deque()
        heightmap = {}
        min_steps = {}
        for i, row in enumerate(grid):
            for j, c in enumerate(row):
                heightmap[i, j] = ord({"S": "a", "E": "z"}.get(c, c))
                if c == "E":
                    d.append(((i, j), 0))
        while d:
            (i, j), steps = d.popleft()
            if (i, j) in min_steps:
                continue
            min_steps[i, j] = steps
            for p in [(i - 1, j), (i + 1, j), (i, j - 1), (i, j + 1)]:
                if heightmap.get(p, 0) >= heightmap[i, j] - 1:
                    d.append((p, steps + 1))
        dd = defaultdict(list)
        for (i, j), steps in min_steps.items():
            dd[grid[i][j]].append(steps)
        self.min_steps = {k: min(v) for k, v in dd.items()}

    def part1(self) -> int:
        return self.min_steps["S"]

    def part2(self) -> int:
        return min(self.min_steps[c] for c in ["S", "a"])


if __name__ == "__main__":
    solution = Solution(sys.stdin)
    print(f"Part 1: {solution.part1()}")
    print(f"Part 2: {solution.part2()}")
```

`__init__()` 内で各マスへの最短ステップ数を求めてしまっています。
`heightmap` には `(i, j)` をキーにして標高の数値を `ord()` の値で格納しています。 `E` を見つけたらその位置までのステップ数を `0` として `deque` に格納、あとは `popleft()` を繰り返しながら隣接マスが移動可能であれば `steps + 1` で末尾に追加する、という形でBFSを実装しています。
移動可能か否か、は下から登るときは「対象の標高が今の標高より`1`だけ高いか、それ以下である」ことが条件なので、逆から辿るときは「対象の標高が今の標高より`1`だけ低いか、それ以上である」とすることで判定できます。枠外の座標は十分に低い標高であるとみなすことで移動不可能であると判定できます。

移動可能な各マスへの最短ステップ数が求められたら、標高ごとにまとめて最小ステップ数まで算出してしまいます。あとは問題への解答は値を取り出すだけです。

### Rust

```rust
use std::collections::VecDeque;
use std::io::{BufRead, BufReader, Read};

struct Solution {
    min_steps: Vec<Vec<Option<(u32, char)>>>,
}

impl Solution {
    fn new(r: impl Read) -> Self {
        let heightmap = BufReader::new(r)
            .lines()
            .filter_map(Result::ok)
            .map(|s| s.bytes().collect::<Vec<_>>())
            .collect::<Vec<_>>();
        let (rows, cols) = (heightmap.len(), heightmap[0].len());
        let mut vd = VecDeque::new();
        for (i, row) in heightmap.iter().enumerate() {
            for (j, col) in row.iter().enumerate() {
                if *col == b'E' {
                    vd.push_back(((i, j), 0));
                }
            }
        }
        let mut min_steps = vec![vec![None; cols]; rows];
        while let Some(((i, j), steps)) = vd.pop_front() {
            if min_steps[i][j].is_some() {
                continue;
            }
            min_steps[i][j] = Some((steps, heightmap[i][j] as char));
            let height = match heightmap[i][j] {
                b'E' => b'z',
                h => h,
            };
            for d in [0, 1, 0, !0, 0].windows(2) {
                let ii = i.wrapping_add(d[0]);
                let jj = j.wrapping_add(d[1]);
                if (0..rows).contains(&ii)
                    && (0..cols).contains(&jj)
                    && (heightmap[ii][jj] >= height - 1
                        || (heightmap[ii][jj] == b'S' && height <= b'b'))
                {
                    vd.push_back(((ii, jj), steps + 1));
                }
            }
        }
        Self { min_steps }
    }
    fn part1(&self) -> u32 {
        self.min_steps
            .iter()
            .flatten()
            .find_map(|o| match o {
                Some((steps, 'S')) => Some(*steps),
                _ => None,
            })
            .unwrap()
    }
    fn part2(&self) -> u32 {
        self.min_steps
            .iter()
            .flatten()
            .filter_map(|o| match o {
                Some((steps, 'a' | 'S')) => Some(*steps),
                _ => None,
            })
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

処理の流れと目的としてはPython実装と同様です。
各マスへの最短ステップ数は `HashMap` などを使わずに、与えられたグリッドと同じサイズの `Option<u32>` を持つ2次元配列で管理しています。
上下左右それぞれ隣接したマスの座標は、 `usize` のまま計算するために `!0` を `-1` の代わりに使っています。これを `.wrapping_add()` した値が `0..rows` または `0..cols` に含まれるかどうかで、枠外か否かを判定しています。
