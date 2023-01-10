---
title: "Day 10: Cathode-Ray Tube"
---

https://adventofcode.com/2022/day/10

機械語でブラウン管モニタの制御。


## part1

```
noop
addx 3
addx -5
```

のような入力が与えられます。

`X` という、初期値が `1` である単一のレジスタがあり、CPUが2つの命令をサポートしています。

- `addx V` 命令は完了まで **2 サイクル** かかります。2サイクルが終わった後、 `X` レジスタは `V` の値だけ(負の場合もある)増加します。
- `noop` は完了に **1サイクル** かかります。あとは何も起きません。

上述のプログラムを実行すると、

- 1サイクル目: 開始時に `noop` 命令が実行されます。このサイクルの間の `X` は `1` です。このサイクル終了時は `noop` が何もせずに終了します。
- 2サイクル目: 開始時に `addx 3` 命令が実行されます。このサイクルの間の `X` はまだ `1` のままです。
- 3サイクル目: このサイクルの間の `X` はまだ `1` です。このサイクルの終了時に `addx 3` 命令が完了し、 `X` が `4` にセットされます。
- 4サイクル目: 開始時に `addx -5` 命令が実行されます。このサイクルの間の `X` はまだあ `4` です。
- 5サイクル目: このサイクルの間の `X` はまだ `4` です。このサイクルの終了時に `addx -5` 命令が完了し、 `X` が `-1` にセットされます。

のようにレジスタの値が変化していきます。
もう少し長いプログラムの例を示します。

```
addx 15
addx -11
addx 6
addx -3
addx 5
addx -1
addx -8
addx 13
addx 4
noop
addx -1
addx 5
addx -1
addx 5
addx -1
addx 5
addx -1
addx 5
addx -1
addx -35
addx 1
addx 24
addx -19
addx 1
addx 16
addx -11
noop
noop
addx 21
addx -15
noop
noop
addx -3
addx 9
addx 1
addx -3
addx 8
addx 1
addx 5
noop
noop
noop
noop
noop
addx -36
noop
addx 1
addx 7
noop
noop
noop
addx 2
addx 6
noop
noop
noop
noop
noop
addx 1
noop
noop
addx 7
addx 1
noop
addx -13
addx 13
addx 7
noop
addx 1
addx -33
noop
noop
noop
addx 2
noop
noop
noop
addx 8
noop
addx -1
addx 2
addx 1
noop
addx 17
addx -9
addx 1
addx 1
addx -3
addx 11
noop
noop
addx 1
noop
addx 1
noop
noop
addx -13
addx -19
addx 1
addx 3
addx 26
addx -30
addx 12
addx -1
addx 3
addx 1
noop
noop
noop
addx -9
addx 18
addx 1
addx 2
noop
noop
addx 9
noop
noop
noop
addx -1
addx 2
addx -37
addx 1
addx 3
noop
addx 15
addx -21
addx 22
addx -6
addx 1
noop
addx 2
addx 1
noop
addx -10
noop
noop
addx 20
addx 1
addx 2
addx 2
addx -6
addx -11
noop
noop
noop
```

ここで「サイクル番号と `X` レジスタの値の積」で定義される **信号強度** というものを考えます。
このプログラムを実行すると、信号強度は次のようになります。

- 20サイクル目: このサイクルの間の `X` は `21` です。したがって信号強度は `20 * 21` で **`420`** になります。
- 60サイクル目: このサイクルの間の `X` は `19` です。したがって信号強度は `60 * 19` で **`1140`** になります。
- 100サイクル目: このサイクルの間の `X` は `18` です。したがって信号強度は `100 * 18` で **`1800`** になります。
- 140サイクル目: このサイクルの間の `X` は `21` です。したがって信号強度は `140 * 21` で **`2940`** になります。
- 180サイクル目: このサイクルの間の `X` は `16` です。したがって信号強度は `180 * 16` で **`2880`** になります。
- 220サイクル目: このサイクルの間の `X` は `18` です。したがって信号強度は `220 * 18` で **`3960`** になります。

以上のように 20サイクル目、 60サイクル目、100サイクル目、140サイクル目、180サイクル目、220サイクル目、について考えたとき、その **6つの信号強度の和** はいくらになるでしょうか、という問題です。
この例では **`13140`** が解となります。

### 考え方

命令が実行されてすぐにはレジスタの値が変化しない、というのが厄介に感じられますが、そこまで難しく考える必要はなく、時系列の `X` の値を表す配列を次のように作ることができます。

- `noop` の場合は次のサイクルもそのままなので、末尾要素 `last` の値を `.push(last)`
- `addx V` の場合は次のサイクルはそのままで、その次のサイクルで変化した値になるので 末尾要素 `last` を使って `.push(last)` してさらに `.push(last + V)`

このように、 `addx` の場合は変更前と変更後の2つの値を追加することで2サイクルかかる動作を表現できます。
配列を作ってしまえば、あとは `20` 番目、`40` 番目、… と値を取得していけば良いだけです。


## part2

このレジスタ `X` は、横40 縦6 のサイズのCRT(ブラウン管)モニタの水平方向のスプライト位置を制御するものだったようです。
下記のように1サイクルごとに1ピクセルの要素を一番上の行の左から右へ、次の行の左から右へと描画していきます。

```
Cycle   1 -> ######################################## <- Cycle  40
Cycle  41 -> ######################################## <- Cycle  80
Cycle  81 -> ######################################## <- Cycle 120
Cycle 121 -> ######################################## <- Cycle 160
Cycle 161 -> ######################################## <- Cycle 200
Cycle 201 -> ######################################## <- Cycle 240
```

スプライトの幅が3ピクセルあり、各ピクセルを描画するタイミングでその位置にスプライトがあるかどうかでそのピクセルを点灯させるか否かを判定します。

```
Sprite position: ###.....................................

Start cycle   1: begin executing addx 15
During cycle  1: CRT draws pixel in position 0
Current CRT row: #

During cycle  2: CRT draws pixel in position 1
Current CRT row: ##
End of cycle  2: finish executing addx 15 (Register X is now 16)
Sprite position: ...............###......................

Start cycle   3: begin executing addx -11
During cycle  3: CRT draws pixel in position 2
Current CRT row: ##.

During cycle  4: CRT draws pixel in position 3
Current CRT row: ##..
End of cycle  4: finish executing addx -11 (Register X is now 5)
Sprite position: ....###.................................

Start cycle   5: begin executing addx 6
During cycle  5: CRT draws pixel in position 4
Current CRT row: ##..#

During cycle  6: CRT draws pixel in position 5
Current CRT row: ##..##
End of cycle  6: finish executing addx 6 (Register X is now 11)
Sprite position: ..........###...........................

Start cycle   7: begin executing addx -3
During cycle  7: CRT draws pixel in position 6
Current CRT row: ##..##.

During cycle  8: CRT draws pixel in position 7
Current CRT row: ##..##..
End of cycle  8: finish executing addx -3 (Register X is now 8)
Sprite position: .......###..............................

Start cycle   9: begin executing addx 5
During cycle  9: CRT draws pixel in position 8
Current CRT row: ##..##..#

During cycle 10: CRT draws pixel in position 9
Current CRT row: ##..##..##
End of cycle 10: finish executing addx 5 (Register X is now 13)
Sprite position: ............###.........................

Start cycle  11: begin executing addx -1
During cycle 11: CRT draws pixel in position 10
Current CRT row: ##..##..##.

During cycle 12: CRT draws pixel in position 11
Current CRT row: ##..##..##..
End of cycle 12: finish executing addx -1 (Register X is now 12)
Sprite position: ...........###..........................

Start cycle  13: begin executing addx -8
During cycle 13: CRT draws pixel in position 12
Current CRT row: ##..##..##..#

During cycle 14: CRT draws pixel in position 13
Current CRT row: ##..##..##..##
End of cycle 14: finish executing addx -8 (Register X is now 4)
Sprite position: ...###..................................

Start cycle  15: begin executing addx 13
During cycle 15: CRT draws pixel in position 14
Current CRT row: ##..##..##..##.

During cycle 16: CRT draws pixel in position 15
Current CRT row: ##..##..##..##..
End of cycle 16: finish executing addx 13 (Register X is now 17)
Sprite position: ................###.....................

Start cycle  17: begin executing addx 4
During cycle 17: CRT draws pixel in position 16
Current CRT row: ##..##..##..##..#

During cycle 18: CRT draws pixel in position 17
Current CRT row: ##..##..##..##..##
End of cycle 18: finish executing addx 4 (Register X is now 21)
Sprite position: ....................###.................

Start cycle  19: begin executing noop
During cycle 19: CRT draws pixel in position 18
Current CRT row: ##..##..##..##..##.
End of cycle 19: finish executing noop

Start cycle  20: begin executing addx -1
During cycle 20: CRT draws pixel in position 19
Current CRT row: ##..##..##..##..##..

During cycle 21: CRT draws pixel in position 20
Current CRT row: ##..##..##..##..##..#
End of cycle 21: finish executing addx -1 (Register X is now 20)
Sprite position: ...................###..................
```

このような動作により、前述の例では以下のような画面が表示されることになります。

```
##..##..##..##..##..##..##..##..##..##..
###...###...###...###...###...###...###.
####....####....####....####....####....
#####.....#####.....#####.....#####.....
######......######......######......####
#######.......#######.......#######.....
```

パズル入力のプログラムを実行したときに表示される8文字は何になるでしょうか、という問題です。
例として私のパズル入力を実行した場合は以下のようになり、

```
###..####.####.#..#.####.####.#..#..##..
#..#....#.#....#.#..#....#....#..#.#..#.
#..#...#..###..##...###..###..####.#..#.
###...#...#....#.#..#....#....#..#.####.
#.#..#....#....#.#..#....#....#..#.#..#.
#..#.####.####.#..#.####.#....#..#.#..#.
```

**`RZEKEFHA`** が解となります。

### 考え方

part1 で各サイクルにおける `X` の値が得られていれば、あとは 40 ずつの長さに区切って、各行について `i` 番目の `X` の値と `i` との差分が `1` 以下になっているか否かで判定していけばそのピクセルの点灯を判定できます。


## 実装例

### Python

```python
import sys
from typing import TextIO


class Solution:
    def __init__(self, io: TextIO) -> None:
        self.values = [1]
        for line in map(str.strip, io):
            if line == "noop":
                self.values.append(self.values[-1])
            else:
                self.values.append(self.values[-1])
                self.values.append(self.values[-1] + int(line[5:]))

    def part1(self) -> int:
        return sum([self.values[i - 1] * i for i in [20, 60, 100, 140, 180, 220]])

    def part2(self) -> str:
        rows = []
        for values in [self.values[i * 40 : (i + 1) * 40] for i in range(6)]:
            rows.append("".join([".#"[abs(i - x) < 2] for i, x in enumerate(values)]))
        return "\n" + "\n".join(rows)


if __name__ == "__main__":
    solution = Solution(sys.stdin)
    print(f"Part 1: {solution.part1()}")
    print(f"Part 2: {solution.part2()}")
```

初期値として `1` を入れておき、あとは命令に応じて 1つまたは 2つの要素を追加していくことで時系列の `X` の値の配列を作成します。
part2は条件に合致するか否かに応じて `.` か `#` を出力するように各行を文字列で作成します。

### Rust

```rust
use itertools::Itertools;
use std::io::{BufRead, BufReader, Read};

struct Solution {
    values: Vec<i32>,
}

impl Solution {
    fn new(r: impl Read) -> Self {
        let mut values = vec![1];
        let mut x = 1;
        for line in BufReader::new(r).lines().filter_map(Result::ok) {
            if let Some(s) = line.strip_prefix("addx ") {
                values.push(x);
                if let Ok(n) = s.parse::<i32>() {
                    x += n;
                }
                values.push(x);
            } else {
                values.push(x);
            }
        }
        Self { values }
    }
    fn part1(&self) -> i32 {
        [20, 60, 100, 140, 180, 220]
            .iter()
            .map(|&i| i * self.values[i as usize - 1])
            .sum()
    }
    fn part2(&self) -> String {
        String::from("\n")
            + &self
                .values
                .chunks(40)
                .take(6)
                .map(|row| {
                    (0..)
                        .zip(row)
                        .map(|(i, &x)| if (i - x).abs() < 2 { '#' } else { '.' })
                        .collect::<String>()
                })
                .join("\n")
    }
}

fn main() {
    let solution = Solution::new(std::io::stdin().lock());
    println!("Part 1: {}", solution.part1());
    println!("Part 2: {}", solution.part2());
}
```

こちらもPythonと同様の実装です。
