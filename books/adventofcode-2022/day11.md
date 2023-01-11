---
title: "Day 11: Monkey in the Middle"
---

https://adventofcode.com/2022/day/11

荷物で遊ぶ猿たち。


## part1

```
Monkey 0:
  Starting items: 79, 98
  Operation: new = old * 19
  Test: divisible by 23
    If true: throw to monkey 2
    If false: throw to monkey 3

Monkey 1:
  Starting items: 54, 65, 75, 74
  Operation: new = old + 6
  Test: divisible by 19
    If true: throw to monkey 2
    If false: throw to monkey 0

Monkey 2:
  Starting items: 79, 60, 97
  Operation: new = old * old
  Test: divisible by 13
    If true: throw to monkey 1
    If false: throw to monkey 3

Monkey 3:
  Starting items: 74
  Operation: new = old + 3
  Test: divisible by 17
    If true: throw to monkey 0
    If false: throw to monkey 1
```

のような入力が与えられます。

それぞれの猿がアイテムの **心配度** に応じて処理を行います。

- `Starting items` は、最初にその猿が持っていてこれから調べるアイテムそれぞれの **心配度** を表します。
- `Operation` は、その猿がアイテムを調べることで心配度がどう変化するかを表します。(`new = old * 5` は、猿が調べることでアイテムの心配度が調べる前の5倍の値にります)。
- `Test` は、心配度をもとにそのアイテムを投げる先の猿をどう決定するかを表します。
  - `If true` は、 `Test` の結果が真のときにどうするかを表します。
  - `If false` は、 `Test` の結果が偽のときにどうするかを表します。

ここで、心配度の値は猿がアイテムを調べた後に `Test` をする前に **3で割って** 最も近い整数に丸めます。

猿は持っているアイテムを調べて投げる、を順番に繰り返します。各猿は1回の順番の中で、持っているアイテムを1つずつ順番に調べて投げます。
`0` 番目、 `1` 番目、と各猿に1回ずつ順番が回るまでを 1 **ラウンド** と呼びます。

猿が他の猿にアイテムを投げると、そのアイテムは受け取った猿のアイテムリストの末尾に追加されます。ラウンド開始時にアイテムを1つも持っていなかった猿も、順番が回ってくるまでにアイテムを受け取っていてそれらを調べて投げることになるかもしれません。順番が回ってきた時点で何もアイテムを持っていなかった猿は何もせずに次の猿に順番が回ります。

上述の例では、最初のラウンドで以下のように動きます。

```
Monkey 0:
  Monkey inspects an item with a worry level of 79.
    Worry level is multiplied by 19 to 1501.
    Monkey gets bored with item. Worry level is divided by 3 to 500.
    Current worry level is not divisible by 23.
    Item with worry level 500 is thrown to monkey 3.
  Monkey inspects an item with a worry level of 98.
    Worry level is multiplied by 19 to 1862.
    Monkey gets bored with item. Worry level is divided by 3 to 620.
    Current worry level is not divisible by 23.
    Item with worry level 620 is thrown to monkey 3.
Monkey 1:
  Monkey inspects an item with a worry level of 54.
    Worry level increases by 6 to 60.
    Monkey gets bored with item. Worry level is divided by 3 to 20.
    Current worry level is not divisible by 19.
    Item with worry level 20 is thrown to monkey 0.
  Monkey inspects an item with a worry level of 65.
    Worry level increases by 6 to 71.
    Monkey gets bored with item. Worry level is divided by 3 to 23.
    Current worry level is not divisible by 19.
    Item with worry level 23 is thrown to monkey 0.
  Monkey inspects an item with a worry level of 75.
    Worry level increases by 6 to 81.
    Monkey gets bored with item. Worry level is divided by 3 to 27.
    Current worry level is not divisible by 19.
    Item with worry level 27 is thrown to monkey 0.
  Monkey inspects an item with a worry level of 74.
    Worry level increases by 6 to 80.
    Monkey gets bored with item. Worry level is divided by 3 to 26.
    Current worry level is not divisible by 19.
    Item with worry level 26 is thrown to monkey 0.
Monkey 2:
  Monkey inspects an item with a worry level of 79.
    Worry level is multiplied by itself to 6241.
    Monkey gets bored with item. Worry level is divided by 3 to 2080.
    Current worry level is divisible by 13.
    Item with worry level 2080 is thrown to monkey 1.
  Monkey inspects an item with a worry level of 60.
    Worry level is multiplied by itself to 3600.
    Monkey gets bored with item. Worry level is divided by 3 to 1200.
    Current worry level is not divisible by 13.
    Item with worry level 1200 is thrown to monkey 3.
  Monkey inspects an item with a worry level of 97.
    Worry level is multiplied by itself to 9409.
    Monkey gets bored with item. Worry level is divided by 3 to 3136.
    Current worry level is not divisible by 13.
    Item with worry level 3136 is thrown to monkey 3.
Monkey 3:
  Monkey inspects an item with a worry level of 74.
    Worry level increases by 3 to 77.
    Monkey gets bored with item. Worry level is divided by 3 to 25.
    Current worry level is not divisible by 17.
    Item with worry level 25 is thrown to monkey 1.
  Monkey inspects an item with a worry level of 500.
    Worry level increases by 3 to 503.
    Monkey gets bored with item. Worry level is divided by 3 to 167.
    Current worry level is not divisible by 17.
    Item with worry level 167 is thrown to monkey 1.
  Monkey inspects an item with a worry level of 620.
    Worry level increases by 3 to 623.
    Monkey gets bored with item. Worry level is divided by 3 to 207.
    Current worry level is not divisible by 17.
    Item with worry level 207 is thrown to monkey 1.
  Monkey inspects an item with a worry level of 1200.
    Worry level increases by 3 to 1203.
    Monkey gets bored with item. Worry level is divided by 3 to 401.
    Current worry level is not divisible by 17.
    Item with worry level 401 is thrown to monkey 1.
  Monkey inspects an item with a worry level of 3136.
    Worry level increases by 3 to 3139.
    Monkey gets bored with item. Worry level is divided by 3 to 1046.
    Current worry level is not divisible by 17.
    Item with worry level 1046 is thrown to monkey 1.
```

ラウンド終了後、各猿は以下のような心配度のアイテムたちを持っていることになります。

```
Monkey 0: 20, 23, 27, 26
Monkey 1: 2080, 25, 167, 207, 401, 1046
Monkey 2: 
Monkey 3: 
```

このプロセスがもう数ラウンド続きます。

```
After round 2, the monkeys are holding items with these worry levels:
Monkey 0: 695, 10, 71, 135, 350
Monkey 1: 43, 49, 58, 55, 362
Monkey 2: 
Monkey 3: 

After round 3, the monkeys are holding items with these worry levels:
Monkey 0: 16, 18, 21, 20, 122
Monkey 1: 1468, 22, 150, 286, 739
Monkey 2: 
Monkey 3: 

After round 4, the monkeys are holding items with these worry levels:
Monkey 0: 491, 9, 52, 97, 248, 34
Monkey 1: 39, 45, 43, 258
Monkey 2: 
Monkey 3: 

After round 5, the monkeys are holding items with these worry levels:
Monkey 0: 15, 17, 16, 88, 1037
Monkey 1: 20, 110, 205, 524, 72
Monkey 2: 
Monkey 3: 

After round 6, the monkeys are holding items with these worry levels:
Monkey 0: 8, 70, 176, 26, 34
Monkey 1: 481, 32, 36, 186, 2190
Monkey 2: 
Monkey 3: 

After round 7, the monkeys are holding items with these worry levels:
Monkey 0: 162, 12, 14, 64, 732, 17
Monkey 1: 148, 372, 55, 72
Monkey 2: 
Monkey 3: 

After round 8, the monkeys are holding items with these worry levels:
Monkey 0: 51, 126, 20, 26, 136
Monkey 1: 343, 26, 30, 1546, 36
Monkey 2: 
Monkey 3: 

After round 9, the monkeys are holding items with these worry levels:
Monkey 0: 116, 10, 12, 517, 14
Monkey 1: 108, 267, 43, 55, 288
Monkey 2: 
Monkey 3: 

After round 10, the monkeys are holding items with these worry levels:
Monkey 0: 91, 16, 20, 98
Monkey 1: 481, 245, 22, 26, 1092, 30
Monkey 2: 
Monkey 3: 

...

After round 15, the monkeys are holding items with these worry levels:
Monkey 0: 83, 44, 8, 184, 9, 20, 26, 102
Monkey 1: 110, 36
Monkey 2: 
Monkey 3: 

...

After round 20, the monkeys are holding items with these worry levels:
Monkey 0: 10, 12, 14, 26, 34
Monkey 1: 245, 93, 53, 199, 115
Monkey 2: 
Monkey 3: 
```

ここで、 **最もアクティヴな2匹の猿** を考えます。20ラウンドの中で **各猿が調べたアイテムの総数** を数えます。

```
Monkey 0 inspected items 101 times.
Monkey 1 inspected items 95 times.
Monkey 2 inspected items 7 times.
Monkey 3 inspected items 105 times.
```

**猿の忙しさ** を2匹の最もアクティヴな猿がそれぞれ調べたアイテム総数の積で表します。
20ラウンドが終了した時点での **猿の忙しさ** はいくらになるでしょうか、という問題です。
この例では `101 * 105` で **`10605`** が解となります。

### 考え方

まず入力のparseが少し面倒そうですが、 [day05](./day05) と同様で取得したい数値が出現する箇所はだいたい決まっているので、数値部分だけピンポイントで切り出すことができます。
`Test` はすべて `divisible by` で割り算しかしないので、数値だけ取り出せば良いです。問題は `Operation` ですが、これも実際には `old` に対して「 $n$ を足す」「 $n$ を掛ける」「2乗する」の3種類しかないので、それだけ対応すれば良さそうです。

あとは実際に20ラウンドぶんシミュレーションをしてみるだけです。
アイテムはリストの順番に調べて、投げられて受け取ったものは末尾に追加する、という仕様なので両端キューで持つようにした方が良さそうではありますが、実際には1回の順番の中でアイテムはすべて処理される上に 求めたいのは調べた回数だけなので、stackなどで扱ってリストの順番を無視しても問題ありません。


## part2

part1 では荷物を調べられるごとに **心配度が3で割られていましたが、もはやそれがなくなりました** 。そして猿たちはもっと長く、 **10000ラウンド** 続けそうです。
そうなると10000ラウンドが終了した時点での **猿の忙しさ** はいくらになるでしょうか、という問題です。

前述の例で考えると、以下のようになります。

```
== After round 1 ==
Monkey 0 inspected items 2 times.
Monkey 1 inspected items 4 times.
Monkey 2 inspected items 3 times.
Monkey 3 inspected items 6 times.

== After round 20 ==
Monkey 0 inspected items 99 times.
Monkey 1 inspected items 97 times.
Monkey 2 inspected items 8 times.
Monkey 3 inspected items 103 times.

== After round 1000 ==
Monkey 0 inspected items 5204 times.
Monkey 1 inspected items 4792 times.
Monkey 2 inspected items 199 times.
Monkey 3 inspected items 5192 times.

== After round 2000 ==
Monkey 0 inspected items 10419 times.
Monkey 1 inspected items 9577 times.
Monkey 2 inspected items 392 times.
Monkey 3 inspected items 10391 times.

== After round 3000 ==
Monkey 0 inspected items 15638 times.
Monkey 1 inspected items 14358 times.
Monkey 2 inspected items 587 times.
Monkey 3 inspected items 15593 times.

== After round 4000 ==
Monkey 0 inspected items 20858 times.
Monkey 1 inspected items 19138 times.
Monkey 2 inspected items 780 times.
Monkey 3 inspected items 20797 times.

== After round 5000 ==
Monkey 0 inspected items 26075 times.
Monkey 1 inspected items 23921 times.
Monkey 2 inspected items 974 times.
Monkey 3 inspected items 26000 times.

== After round 6000 ==
Monkey 0 inspected items 31294 times.
Monkey 1 inspected items 28702 times.
Monkey 2 inspected items 1165 times.
Monkey 3 inspected items 31204 times.

== After round 7000 ==
Monkey 0 inspected items 36508 times.
Monkey 1 inspected items 33488 times.
Monkey 2 inspected items 1360 times.
Monkey 3 inspected items 36400 times.

== After round 8000 ==
Monkey 0 inspected items 41728 times.
Monkey 1 inspected items 38268 times.
Monkey 2 inspected items 1553 times.
Monkey 3 inspected items 41606 times.

== After round 9000 ==
Monkey 0 inspected items 46945 times.
Monkey 1 inspected items 43051 times.
Monkey 2 inspected items 1746 times.
Monkey 3 inspected items 46807 times.

== After round 10000 ==
Monkey 0 inspected items 52166 times.
Monkey 1 inspected items 47830 times.
Monkey 2 inspected items 1938 times.
Monkey 3 inspected items 52013 times.
```

10000ラウンド終了後、最もアクティヴな2匹の猿が調べたアイテムの数は `52166` と `52013` なので、その積の **`2713310158`** が解となります。

### 考え方

今度は3で割られない上にラウンド数が多いため、そのまま正直に計算していくと、あっという間にとてつもない数字になってしまいます。

ここで注目すべきは、 `Test` で調べるのは「心配度がある数値で割り切れるか否か」だけであることです。また、最終的に求めるべきは調べた回数だけなので、 `Test` の結果としてどの猿にアイテムが投げられるかさえ計算できれば心配度の数値を正確に知る必要はありません。
そして、心配度の数値は加算か乗算でしか変化しないことも考えると、適切な値での剰余を取ることで `Test` 結果に影響を与えることなく大きすぎない値で心配度を管理できることに気付きます。

ではどんな値で剰余を取れば良いのでしょうか。数学的な説明は省きますが、「各猿が `Test` で割ろうと試みる数の **最小公倍数**」がそれを満たします。前述の例でも おそらく実際の入力例でも、この問題ではそれらの数値は素数になっていますので、単純にすべての値を掛け合わせるだけでそれを求めることができます。

あとは part1 と同様のシミュレーションで、「3で割る」かわりに「最小公倍数で剰余を取る」という操作をすれば64bit程度の整数値だけで10000ラウンドの計算を十分な速度で行うことができます。


## 実装例

### Python

```python
import sys
from dataclasses import dataclass
from math import prod
from typing import Callable, TextIO


@dataclass
class Test:
    divisible: int
    throw_to: tuple[int, int]


@dataclass
class Monkey:
    starting_items: list[int]
    operation: Callable[[int], int]
    test: Test


class Solution:
    def __init__(self, io: TextIO) -> None:
        def parse(lines: list[str]) -> Monkey:
            return Monkey(
                starting_items=list(map(int, lines[1][18:].split(", "))),
                operation=eval(f"lambda old: {lines[2][19:]}"),
                test=Test(
                    divisible=int(lines[3][21:]),
                    throw_to=(int(lines[5][30:]), int(lines[4][29:])),
                ),
            )

        self.monkeys = list(map(parse, map(str.splitlines, io.read().split("\n\n"))))

    def part1(self) -> int:
        return self.monkey_business(20, 3)

    def part2(self) -> int:
        return self.monkey_business(10000, 1)

    def monkey_business(self, round: int, divide: int) -> int:
        """`round`回数実行し、最もアクティヴな2匹の猿が調べたアイテムの数の積を返す"""
        items = list(map(lambda m: m.starting_items[:], self.monkeys))
        lcm = prod(m.test.divisible for m in self.monkeys)
        inspected = [0] * len(self.monkeys)
        for _ in range(round):
            for i, monkey in enumerate(self.monkeys):
                while items[i]:
                    level = monkey.operation(items[i].pop()) // divide
                    to = monkey.test.throw_to[level % monkey.test.divisible == 0]
                    items[to].append(level % lcm)
                    inspected[i] += 1
        return prod(sorted(inspected)[-2:])


if __name__ == "__main__":
    solution = Solution(sys.stdin)
    print(f"Part 1: {solution.part1()}")
    print(f"Part 2: {solution.part2()}")
```

`@dataclass` で各猿の情報を保持するようにしました。
かなり強引な技ですが、 `Operation` の部分は `new = ` 以降を取り出して `lambda old: ` に繋げたものを `eval()` で得ることで、 `Callable[[int], int]` な関数として扱えるようにしています。
`Test.throw_to` は「割り切れるか否か」のbool値をそのままインデックスとして使えるよう、 `false` のときのものを `[0]` に、 `true` のときのものを `[1]` に入れています。

実際のシミュレーションは `self.monkey_business()` 関数で行います。part1 の場合も `lcm` で剰余を取るのは問題ないので共通処理で、「実行するラウンド数」と「3で割るか否か(もしくは3で割るか1で割るか)」だけを引数で渡して処理を分けます。
シミュレーションで使う `items` は `self.monkeys` の値を変更しないために `[:]` でコピーしていることに注意してください。

### Rust

```rust
use std::io::{BufRead, BufReader, Read};

enum Operation {
    Add(u64),
    Mul(u64),
    Square,
}

struct Monkey {
    starting_items: Vec<u64>,
    operation: Operation,
    test: (u64, [usize; 2]),
}

impl From<&[String]> for Monkey {
    fn from(lines: &[String]) -> Self {
        Self {
            starting_items: lines[1][18..]
                .split(", ")
                .filter_map(|s| s.parse().ok())
                .collect(),
            operation: match (&lines[2][23..24], &lines[2][25..]) {
                ("*", "old") => Operation::Square,
                ("*", s) => Operation::Mul(s.parse().unwrap()),
                ("+", s) => Operation::Add(s.parse().unwrap()),
                _ => unreachable!(),
            },
            test: (
                lines[3][21..].parse().unwrap(),
                [
                    lines[5][30..].parse().unwrap(),
                    lines[4][29..].parse().unwrap(),
                ],
            ),
        }
    }
}

struct Solution {
    monkeys: Vec<Monkey>,
}

impl Solution {
    fn new(r: impl Read) -> Self {
        Self {
            monkeys: BufReader::new(r)
                .lines()
                .filter_map(Result::ok)
                .collect::<Vec<_>>()
                .split(String::is_empty)
                .map(Monkey::from)
                .collect(),
        }
    }
    fn part1(&self) -> u64 {
        self.monkey_business(20, 3)
    }
    fn part2(&self) -> u64 {
        self.monkey_business(10000, 1)
    }
    fn monkey_business(&self, round: usize, divide: u64) -> u64 {
        let mut items = self
            .monkeys
            .iter()
            .map(|m| m.starting_items.clone())
            .collect::<Vec<_>>();
        let mut inspected = vec![0; self.monkeys.len()];
        let lcm = self.monkeys.iter().map(|m| m.test.0).product::<u64>();
        for _ in 0..round {
            for (i, monkey) in self.monkeys.iter().enumerate() {
                while let Some(item) = items[i].pop() {
                    let level = match monkey.operation {
                        Operation::Add(n) => item + n,
                        Operation::Mul(n) => item * n,
                        Operation::Square => item * item,
                    } / divide;
                    let to = monkey.test.1[usize::from(level % monkey.test.0 == 0)];
                    items[to].push(level % lcm);
                    inspected[i] += 1;
                }
            }
        }
        inspected.sort_unstable();
        inspected.iter().rev().take(2).product()
    }
}

fn main() {
    let solution = Solution::new(std::io::stdin().lock());
    println!("Part 1: {}", solution.part1());
    println!("Part 2: {}", solution.part2());
}
```

`Operation` は enum にしています。 `* old` であれば2乗、そうでなければ単純な加算か乗算、と判定できます。
あとはPythonと同様の実装です。 `u64` であればオーバーフローすることなく計算できるはずです。
