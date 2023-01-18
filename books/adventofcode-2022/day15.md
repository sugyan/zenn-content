---
title: "Day 15: Beacon Exclusion Zone"
---

https://adventofcode.com/2022/day/15

またもや2次元座標、そしてビーコン…


## part1

```
Sensor at x=2, y=18: closest beacon is at x=-2, y=15
Sensor at x=9, y=16: closest beacon is at x=10, y=16
Sensor at x=13, y=2: closest beacon is at x=15, y=3
Sensor at x=12, y=14: closest beacon is at x=10, y=16
Sensor at x=10, y=20: closest beacon is at x=10, y=16
Sensor at x=14, y=17: closest beacon is at x=10, y=16
Sensor at x=8, y=7: closest beacon is at x=2, y=10
Sensor at x=2, y=0: closest beacon is at x=2, y=10
Sensor at x=0, y=11: closest beacon is at x=2, y=10
Sensor at x=20, y=14: closest beacon is at x=25, y=17
Sensor at x=17, y=20: closest beacon is at x=21, y=22
Sensor at x=16, y=7: closest beacon is at x=15, y=3
Sensor at x=14, y=3: closest beacon is at x=15, y=3
Sensor at x=20, y=1: closest beacon is at x=15, y=3
```

のような入力が与えられます。

センサーとビーコンが整数値で表されるXY座標上に存在しています。
各センサーは **[マンハッタン距離](https://ja.wikipedia.org/wiki/%E3%83%9E%E3%83%B3%E3%83%8F%E3%83%83%E3%82%BF%E3%83%B3%E8%B7%9D%E9%9B%A2) で最も近い** 位置にあるビーコン1個だけの位置を示します。(2つ以上のビーコンが同じ距離で最も近い、というものは有り得ないとします)

つまり、 `2, 18` の位置のセンサーからは `-2, 15` のビーコンが最も近くにあり、 `9, 16` のセンサーからは `10, 16` のビーコンが最も近くにあります。

センサーを `S`、ビーコンを `B` としてそれぞれの配置を下図のように表せます。

```
               1    1    2    2
     0    5    0    5    0    5
 0 ....S.......................
 1 ......................S.....
 2 ...............S............
 3 ................SB..........
 4 ............................
 5 ............................
 6 ............................
 7 ..........S.......S.........
 8 ............................
 9 ............................
10 ....B.......................
11 ..S.........................
12 ............................
13 ............................
14 ..............S.......S.....
15 B...........................
16 ...........SB...............
17 ................S..........B
18 ....S.......................
19 ............................
20 ............S......S........
21 ............................
22 .......................B....
```

これは必ずしも、この図示範囲にあるビーコンを網羅しているわけではありません。しかし、各センサーは最も近い位置のビーコンは識別しているので、そのビーコンの他には近くにビーコンが存在しないことは分かります。
例えば `8, 7` にあるセンサーについて考えてみると、最も近い位置のビーコンは `2, 10` なので、それと同等もしくはそれよりも近い位置 (下図の `#` で示される領域) には他のビーコンは存在しない、ということになります。

```
               1    1    2    2
     0    5    0    5    0    5
-2 ..........#.................
-1 .........###................
 0 ....S...#####...............
 1 .......#######........S.....
 2 ......#########S............
 3 .....###########SB..........
 4 ....#############...........
 5 ...###############..........
 6 ..#################.........
 7 .#########S#######S#........
 8 ..#################.........
 9 ...###############..........
10 ....B############...........
11 ..S..###########............
12 ......#########.............
13 .......#######..............
14 ........#####.S.......S.....
15 B........###................
16 ..........#SB...............
17 ................S..........B
18 ....S.......................
19 ............................
20 ............S......S........
21 ............................
22 .......................B....
```

まずは、`y=2000000` である行においてビーコンが存在し得ない位置はいくつあるでしょうか、という問題です。
上述の例で `y=10` の行について考えると、各センサーがカバーしている範囲は以下のようになり、

```
                 1    1    2    2
       0    5    0    5    0    5
 9 ...#########################...
10 ..####B######################..
11 .###S#############.###########.
```

`y=10` で `#` で示されている位置は **`26`** 個ということになります。

### 考え方

各センサーの位置とそれに最も近いビーコンの位置は分かっているので、「そのセンサーがカバーしている距離」は予め計算しておくことができます。
ではそれら各センサーが「ある行に対してカバーし得る範囲」はどのようにして求められるでしょうか。上述の例で `8, 7` の位置のセンサーがカバーする領域をもう一度見てみます。

```
               1    1    2    2
     0    5    0    5    0    5

 6 ..#################.........
 7 .#########S#######S#........
 8 ..#################.........
 9 ...###############..........
10 ....B############...........
11 ..S..###########............
```

`2, 10` のビーコンを最も近い位置としているので、カバーする距離は $|8-2|+|7-10|=9$ です。センサーから真っ直ぐ `y=10` に移動すると `8, 10` の位置に距離 `3` で移動できるので、その位置からX軸の正負それぞれの方向に `6` だけ移動した位置 `2, 10` から `14, 10` までがカバーできる範囲、と計算できます。また、対象とする行までの距離がそのセンサーのカバー距離よりも大きい場合は、その行に対してカバーできる範囲は存在しません。

つまり、センサーの位置を $(x_s, y_s)$ 、対応する最近接ビーコンの位置を $(x_b, y_b)$ とすると、 $y$ におけるカバー範囲 $x_{min}, x_{max}$ は、

$$
\begin{aligned}
d &= |x_s - x_b| + |y_s - y_b| \\
r &= d - |y_s - y| \\
x_{min}, x_{max} &= \begin{cases}
                        x_s - r, x_s + r & (r \geq 0) \\
                        なし & (r \lt 0)
                    \end{cases}
\end{aligned}
$$

と計算できます。

このようにして各センサーからのカバー範囲を求めて、重複範囲があるものはマージするといった操作をすることで、ある行に対してカバーできる範囲をすべて求めることができます。
重複のマージについては、具体的には範囲の最小値でソートして順番に確認しつつ、重複があればマージしていくという操作を行うことで実現できるでしょう。

また、ここで求めるものは「ビーコンが存在し得ない位置」の数なので、カバーし得る範囲とは別にその行にビーコンが既に存在していることも考慮する必要があります。これは単純に現時点で分かっているビーコンの座標をすべて確認し、対象行に存在しているものをカウントするだけ求められます。
全カバー範囲の位置数からビーコン数を引いたものが、求める解になります。


## part2

X, Y座標それぞれ `0` から `4000000` の範囲で、どのセンサーからも検出されていない唯一の座標位置にビーコンがあるようです。
その位置のX座標の値に `4000000` を掛けて Y座標の値を足したものはいくらになるでしょうか、という問題です。
前述の例においては探索範囲はX, Yそれぞれ最大 `20` とします。その場合には `x=14, y=11` が唯一の座標になるので、 **`56000011`** が解となります。

### 考え方

探索範囲がかなり広いので、全座標について一つ一つ調べるというのは現実的ではありません。
part1 で汎用的に「ある行に対してカバーできる範囲」を求められるようにしておくと、それを利用して `4000000` 回の繰り返しで解を求めることができます。

具体的には、`0` から `4000000` までの `y` で各行に対してカバーできる範囲を求め、その範囲が2つに分断されている行を見つけられればその隙間の場所が求める位置となる、というものです。
前述の例では、 `y=11` において `-3` から `13` までの範囲と `15` から `25` までの2つに分かれているので、その隙間の `x=14` が求める位置となります。

```
                 1    1    2    2
       0    5    0    5    0    5
11 .###S#############.###########.
```

計算量を考えます。
探索範囲の広さ(座標最大値)を $N$ 、センサー・ビーコンの数(入力行数)を $k$ とすると、全座標でそれぞれすべてのセンサーのカバー領域にいるかどうか調べようとすると $O(N^2k)$ となります。part1 で求める「ある行に対してカバーできる範囲」は $O(k\log{k})$ で計算できるので、これを利用すると $O(Nk\log{k})$ で解を求めることができます。実際の入力でも $k$ は `24` 程度なので、これで大幅に計算量を削減できるということになります。

しかし、それでも `4000000` 回の繰り返し計算はそれなりに時間がかかります。さらに計算量を削減する方法を考えてみましょう。

「どのセンサーからも検出されない位置座標が範囲内に1つだけ存在している」という条件を使うと、その求めるべき座標は「あるセンサーのカバー範囲から1つだけ外側にある」ということになります。
例えば、`8, 7` のセンサーの場合はビーコンの位置が `2, 10` で距離が `9` なので、センサーからの距離がちょうど `10` の位置 (下図の `@` で示される領域) が候補となります。

```
             1    1    2
   0    5    0    5    0
 0 .....@#####@.........
 1 ....@#######@........
 2 ...@#########@.......
 3 ..@###########@......
 4 .@#############@.....
 5 @###############@....
 6 #################@...
 7 ########S#########@..
 8 #################@...
 9 @###############@....
10 .@B############@.....
11 ..@###########@......
12 ...@#########@.......
13 ....@#######@........
14 .....@#####@.........
15 ......@###@..........
16 .......@#@...........
17 ........@............
18 .....................
19 .....................
20 .....................
```

このようにして複数のセンサーからのカバー範囲を1つだけ超えた領域が重なりあって、探索範囲内に1つだけの隙間を作り出すことになります。
さらに突き詰めると、

```
...####S####........
....#######.........
.....#####@.........
......###@#.........
.......#@###........
.......@#####.......
.......###S###......
........#####.......
```

や

```
.......#####S#####..
.......@#########...
.......#@#######....
......#S#@#####.....
.......#...###......
............#.......
....................
....................
```

のように、2つの隣接するカバー範囲の隙間によって作られる直線が存在し、それらの交点によって1箇所だけの隙間が作られます。
このような直線領域が存在し得る範囲を細かく求めていけば解析的に解を求めることもできますが、条件分岐などが複雑になって実装も大変なので、ここではざっくりと「隙間が作られる候補の位置」の列挙を考えることにします。

求める隙間の座標は上図のような「範囲を1つだけ超えた領域を示す直線同士の交点のどれか」として、まずはそれらの直線を考えます。
センサー $(x_s, y_s)$ からビーコンまでの距離を $d$ とすると、 $(x_s - d - 1, y_s)$, $(x_s + d + 1, y_s)$, $(x_s, y_s - d - 1)$, $(x_s, y_s + d + 1)$ の4点を斜めに結ぶ直線が考えられます。それぞれ $y = ax + b$ の形で表すと

$$
\begin{align}
y &= x + (y_s - x_s + (d + 1)) \\
y &= x + (y_s - x_s - (d + 1)) \\
y &= -x + (y_s + x_s + (d + 1)) \\
y &= -x + (y_s + x_s - (d + 1)) \\
\end{align}
$$

となります。
つまり各センサーから傾き `1` の直線と 傾き `-1` の直線が2本ずつ作られ、それらの交点が隙間の候補となります。各直線について切片 $b$ だけ計算しておけば、 $y=x+b_0$ と $y=-x+b_1$ の交点のY座標は $(b_0 + b_1)/2$ と求められるので、簡単に候補を列挙することができます。

このようにすると、候補数はセンサー数の2乗となり、解を求めるための計算量は $O(k^2 \times k\log{k})$ となります。Y座標を `0` から `4000000` までしらみつぶしに試す必要はなく、高々 `2304` 回程度の試行で済むようになるので、大幅な計算量の削減ができます。

さらに候補を絞っておくこともできます。上述の通り直線領域は2つの隣接するカバー範囲の隙間によって作られるということなので、切片 $b$ は重複して現れることになるはずです。そういった条件で候補を抽出すると、計算量はさらに削減できます。

ただ、このような候補の求め方は「必ず探索領域の内部(四隅や端ではない)位置に隙間が存在している」という前提で考えています。おそらく実際の入力でも求める隙間が四隅や端に存在することはないと思いますが、その点には注意が必要です。


## 実装例

### Python

```python
import re
import sys
from collections import Counter
from dataclasses import dataclass
from itertools import product
from typing import TextIO


@dataclass
class Report:
    @dataclass
    class Coordinate:
        x: int
        y: int

    sensor: Coordinate
    beacon: Coordinate
    distance: int

    def __init__(self, sx: int, sy: int, bx: int, by: int) -> None:
        self.sensor = self.Coordinate(sx, sy)
        self.beacon = self.Coordinate(bx, by)
        self.distance = abs(sx - bx) + abs(sy - by)


class Solution:
    MAX = 4_000_000

    def __init__(self, io: TextIO) -> None:
        def parse(line: str) -> Report:
            return Report(*map(int, re.findall(r"[xy]=(-?\d+)", line)))

        self.reports = list(map(parse, io))

    def part1(self) -> int:
        xs = set([r.beacon.x for r in self.reports if r.beacon.y == self.MAX // 2])
        return sum(map(lambda r: r[1] - r[0] + 1, self.ranges(self.MAX // 2))) - len(xs)

    def part2(self) -> int:
        ps, ns = [], []
        for r in self.reports:
            ps.append(r.sensor.y - r.sensor.x + (r.distance + 1))
            ps.append(r.sensor.y - r.sensor.x - (r.distance + 1))
            ns.append(r.sensor.y + r.sensor.x + (r.distance + 1))
            ns.append(r.sensor.y + r.sensor.x - (r.distance + 1))
        for y in set(
            (b0 + b1) // 2
            for b0, b1 in product(
                (b for b, n in Counter(ps).items() if n > 1),
                (b for b, n in Counter(ns).items() if n > 1),
            )
        ):
            ranges = self.ranges(y)
            if len(ranges) > 1:
                return (ranges[0][1] + 1) * 4_000_000 + y
        raise ValueError("unreachable!")

    def ranges(self, y: int) -> list[tuple[int, int]]:
        """指定したY座標におけるカバー範囲のリストを返す"""
        def f(report: Report) -> tuple[int, int]:
            return report.sensor.x, report.distance - abs(report.sensor.y - y)

        ranges: list[tuple[int, int]] = []
        for (xmin, xmax) in sorted(
            (x - r, x + r) for x, r in map(f, self.reports) if r >= 0
        ):
            if not ranges or xmin > ranges[-1][1] + 1:
                ranges.append((xmin, xmax))
            ranges[-1] = (ranges[-1][0], max(ranges[-1][1], xmax))
        return ranges


if __name__ == "__main__":
    solution = Solution(sys.stdin)
    print(f"Part 1: {solution.part1()}")
    print(f"Part 2: {solution.part2()}")
```

座標や各センサー・ビーコンの位置などは `@dataclass` を使って保持しています。インスタンス作成時にカバー距離を計算してしまいます。
探索範囲は `Solution.MAX` と定義しています。入力例に対するテストのときはこれを `20` と上書きすることで条件を変えることができます。

`ranges` 関数が、両partで使う「指定したY座標におけるカバー範囲のリスト」を返す関数です。昇順にみていき、それまでの最大値よりも大きな値から始まる範囲があるかどうかでマージするか否かを判定します。

part2 では前述の「考え方」で述べたようなY座標候補の絞り込みを実装しています。傾き `1` (positive) の直線の切片を集める `ps` と、傾き `-1` (negative) の直線の切片を集める `ns` でまずすべて抽出し、 `collections.Counter` を使って2回以上出現しているものだけに絞っています。

### Rust

```rust
use itertools::Itertools;
use std::io::{BufRead, BufReader, Read};
use std::str::FromStr;

struct Coordinate {
    x: i64,
    y: i64,
}

struct Report {
    sensor: Coordinate,
    beacon: Coordinate,
    distance: i64,
}

impl FromStr for Report {
    type Err = ();

    fn from_str(s: &str) -> Result<Self, Self::Err> {
        s.split_once(": ")
            .and_then(|(s, b)| {
                [&s[10..], &b[21..]]
                    .iter()
                    .filter_map(|s| {
                        s.split_once(", ").and_then(|(x, y)| {
                            Some(Coordinate {
                                x: x[2..].parse().ok()?,
                                y: y[2..].parse().ok()?,
                            })
                        })
                    })
                    .collect_tuple()
                    .map(|(sensor, beacon)| {
                        let distance = (sensor.x - beacon.x).abs() + (sensor.y - beacon.y).abs();
                        Report {
                            sensor,
                            beacon,
                            distance,
                        }
                    })
            })
            .ok_or(())
    }
}

struct Solution {
    reports: Vec<Report>,
}

impl Solution {
    fn new(r: impl Read) -> Self {
        Self {
            reports: BufReader::new(r)
                .lines()
                .filter_map(Result::ok)
                .filter_map(|line| line.parse().ok())
                .collect(),
        }
    }
    fn part1(&self) -> i64 {
        let target_row = if cfg!(test) { 10 } else { 2_000_000 };
        let count = self
            .reports
            .iter()
            .filter_map(|report| {
                if report.beacon.y == target_row {
                    Some(report.beacon.x)
                } else {
                    None
                }
            })
            .unique()
            .count() as i64;
        self.ranges(target_row)
            .iter()
            .map(|r| r.1 - r.0 + 1)
            .sum::<i64>()
            - count
    }
    fn part2(&self) -> i64 {
        let max = if cfg!(test) { 20 } else { 4_000_000 };
        let mut ps = vec![0];
        let mut ns = vec![max];
        for report in &self.reports {
            ps.push(report.sensor.y - report.sensor.x + (report.distance + 1));
            ps.push(report.sensor.y - report.sensor.x - (report.distance + 1));
            ns.push(report.sensor.y + report.sensor.x + (report.distance + 1));
            ns.push(report.sensor.y + report.sensor.x - (report.distance + 1));
        }
        ps.iter()
            .cartesian_product(&ns)
            .filter_map(|b| Some((b.0 + b.1) / 2).filter(|y| (0..=max).contains(y)))
            .find_map(|y| {
                let v = self.ranges(y);
                let x = v[0].1 + 1;
                if v.len() == 2 && (0..=max).contains(&x) {
                    Some(x * 4_000_000 + y)
                } else {
                    None
                }
            })
            .unwrap()
    }
    fn ranges(&self, y: i64) -> Vec<(i64, i64)> {
        let mut ret: Vec<(i64, i64)> = Vec::new();
        for (min, max) in self
            .reports
            .iter()
            .filter_map(|report| {
                Some(report.distance - (y - report.sensor.y).abs()).and_then(|r| {
                    if r >= 0 {
                        Some((report.sensor.x - r, report.sensor.x + r))
                    } else {
                        None
                    }
                })
            })
            .sorted_unstable()
        {
            if let Some(last) = ret.last_mut() {
                if last.1 >= min - 1 {
                    last.1 = max.max(last.1);
                    continue;
                }
            }
            ret.push((min, max));
        }
        ret
    }
}

fn main() {
    let solution = Solution::new(std::io::stdin().lock());
    println!("Part 1: {}", solution.part1());
    println!("Part 2: {}", solution.part2());
}
```

Pythonとほぼ同様の実装です。入力のparseに正規表現を使わずに実装していて少し煩雑ですが、データ構造としては一緒です。

part2ではY座標候補を計算するのもやはり同様ですが、こちらは出現回数カウントによる絞り込みはせずにすべての候補に対して計算しています。切片 `0` と `max` のものも予め含めておくことで、たとえ求める隙間座標が四隅や端にあっても正しく見つけることができるようになります。
