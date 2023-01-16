---
title: "Day 13: Distress Signal"
---

https://adventofcode.com/2022/day/13

再帰的なデータ構造と比較操作。


## part1

```
[1,1,3,1,1]
[1,1,5,1,1]

[[1],[2,3,4]]
[[1],4]

[9]
[[8,7,6]]

[[4,4],4,4]
[[4,4],4,4,4]

[7,7,7,7]
[7,7,7]

[]
[3]

[[[]]]
[[]]

[1,[2,[3,[4,[5,6,7]]]],8,9]
[1,[2,[3,[4,[5,6,0]]]],8,9]
```

のような入力が与えられます。

これらは整数値とリストからなるパケットデータを表しています。リストは `[` で始まり `]` で終わり、中には `,` で区切られた 0個以上の値(整数値または別のリスト)が含まれます。パケットデータは常に単一のリストであり、1行につき1つだけ表示されています。
`left` と `right` の2つの値を比較して順序を確認する際、以下のように判定されます。

- **両方とも整数値** である場合: **小さい値** の方が先にくるべきです。もし `left` の整数値が `right` の整数値より小さいならば、その順序は正しいです。もし `left` の整数値が `right` の整数値より大きいならば、その順序は正しくないです。もし両方が同じ整数値であれば、リスト内の次の値をチェックします。
- **両方ともリスト** の場合: 最初の値同士、2番目の値同士、で比較していきます。もし `left` の要素が先になくなったら、その順序は正しいです。もし `right` の要素が先になくなったら、その順序は正しくないです。もし両方のリストが同じ長さで、各要素の比較によって順序が決まらなかったら、リスト内の次の値をチェックします。
- **片方だけが整数値** の場合: その整数値を単一の値として持つリストに変換して、それから再度比較を行います。例えば `[0,0,0]` と `2` を比較する場合は、右側の `2` が `[2]` に変換され、結果は `[0,0,0]` と `[2]` を比較したものになります。

このルールによって、上述のパケットデータのペアのうち、どれが正しい順序であるかを決定することができます。

```
== Pair 1 ==
- Compare [1,1,3,1,1] vs [1,1,5,1,1]
  - Compare 1 vs 1
  - Compare 1 vs 1
  - Compare 3 vs 5
    - Left side is smaller, so inputs are in the right order

== Pair 2 ==
- Compare [[1],[2,3,4]] vs [[1],4]
  - Compare [1] vs [1]
    - Compare 1 vs 1
  - Compare [2,3,4] vs 4
    - Mixed types; convert right to [4] and retry comparison
    - Compare [2,3,4] vs [4]
      - Compare 2 vs 4
        - Left side is smaller, so inputs are in the right order

== Pair 3 ==
- Compare [9] vs [[8,7,6]]
  - Compare 9 vs [8,7,6]
    - Mixed types; convert left to [9] and retry comparison
    - Compare [9] vs [8,7,6]
      - Compare 9 vs 8
        - Right side is smaller, so inputs are not in the right order

== Pair 4 ==
- Compare [[4,4],4,4] vs [[4,4],4,4,4]
  - Compare [4,4] vs [4,4]
    - Compare 4 vs 4
    - Compare 4 vs 4
  - Compare 4 vs 4
  - Compare 4 vs 4
  - Left side ran out of items, so inputs are in the right order

== Pair 5 ==
- Compare [7,7,7,7] vs [7,7,7]
  - Compare 7 vs 7
  - Compare 7 vs 7
  - Compare 7 vs 7
  - Right side ran out of items, so inputs are not in the right order

== Pair 6 ==
- Compare [] vs [3]
  - Left side ran out of items, so inputs are in the right order

== Pair 7 ==
- Compare [[[]]] vs [[]]
  - Compare [[]] vs []
    - Right side ran out of items, so inputs are not in the right order

== Pair 8 ==
- Compare [1,[2,[3,[4,[5,6,7]]]],8,9] vs [1,[2,[3,[4,[5,6,0]]]],8,9]
  - Compare 1 vs 1
  - Compare [2,[3,[4,[5,6,7]]]] vs [2,[3,[4,[5,6,0]]]]
    - Compare 2 vs 2
    - Compare [3,[4,[5,6,7]]] vs [3,[4,[5,6,0]]]
      - Compare 3 vs 3
      - Compare [4,[5,6,7]] vs [4,[5,6,0]]
        - Compare 4 vs 4
        - Compare [5,6,7] vs [5,6,0]
          - Compare 5 vs 5
          - Compare 6 vs 6
          - Compare 7 vs 0
            - Right side is smaller, so inputs are not in the right order
```

では、既に正しい順序になっているペアのインデックスの合計値はいくらでしょうか、という問題です。
この例では `1`, `2`, `4`, `6` 番目が正しい順序であるので、合計値の **`13`** が解となります。

### 考え方

再帰的なリストとしてparseして、再帰的に比較操作をしていく必要があります。
parse方法は言語によっても異なってくるかと思いますが、多くのLL(lightweight language, 軽量プログラミング言語)などでは各行をJSONデータとしてそのままparseすることができるので、それを利用すると簡単です。
あとは `left` と `right` の型を判別して定義通りに再帰的な比較を行うだけです。


## part2

今度は、ペアを区切っていた空行を無視して、リスト上のすべてのパケットを正しい順序で並べ替えます。
また、以下の2つの **仕切りパケット** を含める必要があります。

```
[[2]]
[[6]]
```

これを含めたすべてのパケットを、正しい順序になるよう並べ替えます。
前述の例を使うと、以下のようになります。

```
[]
[[]]
[[[]]]
[1,1,3,1,1]
[1,1,5,1,1]
[[1],[2,3,4]]
[1,[2,[3,[4,[5,6,0]]]],8,9]
[1,[2,[3,[4,[5,6,7]]]],8,9]
[[1],4]
[[2]]
[3]
[[4,4],4,4]
[[4,4],4,4,4]
[[6]]
```

この並べ替えたリストにおいて、上述の仕切りパケットそれぞれのインデックスの積はいくらになるでしょうか、という問題です。
この例では、 `[[2]]` が `10` 番目、 `[[6]]` が `14` 番目になるので、その積の **`140`** が解となります。

### 考え方

part1 で正しく比較できるようになっていれば、あとはすべてのパケットに仕切りパケットを加えた配列を用意し、それを `sort` してそれぞれのパケットが何番目にあるか調べれば良いだけです。
もしくは、`sort` はせずに各仕切りパケット **より小さい** パケットがいくつあるかを調べるだけでも良いかもしれません。


## 実装例

### Python

```python
import sys
from ast import literal_eval
from functools import cmp_to_key
from math import prod
from typing import TextIO


class Solution:
    def __init__(self, io: TextIO) -> None:
        self.pairs = [
            tuple(map(literal_eval, lines))
            for lines in map(str.splitlines, io.read().split("\n\n"))
        ]

    def part1(self) -> int:
        return sum(i for i, pair in enumerate(self.pairs, 1) if self.cmp(*pair) < 0)

    def part2(self) -> int:
        dividers = [[[2]], [[6]]]
        packets = sorted(sum(map(list, self.pairs), dividers), key=cmp_to_key(self.cmp))
        return prod([i for i, p in enumerate(packets, 1) if p in dividers])

    @staticmethod
    def cmp(lhs: object, rhs: object) -> int:
        """`lhs` と `rhs` を比較した結果の整数値を返す

        Returns
        -------
        lhs < rhs: 負の整数
        lhs == rhs: 0
        lhs > rhs: 正の整数
        """
        match lhs, rhs:
            case int(l), int(r):
                return l - r
            case list(l), list(r):
                return next((c for c in map(Solution.cmp, l, r) if c), len(l) - len(r))
            case int(l), list(r):
                return Solution.cmp([l], r)
            case list(l), int(r):
                return Solution.cmp(l, [r])
            case _:
                raise ValueError("unreachable!")


if __name__ == "__main__":
    solution = Solution(sys.stdin)
    print(f"Part 1: {solution.part1()}")
    print(f"Part 2: {solution.part2()}")
```

Pythonの場合、パケットデータはJSONとしてparseしても良いですが、ここでは `ast.literal_eval` を使って文字列をそのまま評価して使用しています。
未知の入力を受け取って内容をチェックせずに `eval` するのは危険ですので、この問題のようにPythonで扱うデータのリテラルとしての入力であることを期待して評価する場合は `ast.literal_eval` を使うことをおすすめします。

https://docs.python.org/3/library/ast.html#ast.literal_eval

実際に比較の計算を行うのが `cmp` メソッドです。
ここでは Python 3.10 から導入された pattern matching を利用しています。

https://docs.python.org/3/whatsnew/3.10.html#pep-634-structural-pattern-matching

両方とも `int` ならその値の差を返し、どちら一方だけが `int` なら1要素の `list` に変換して再び比較します。
両方とも `list` のときは各要素を順番に比較します、ここで `map(Solution.cmp, l, r)` でそれを実現しています。もし `0` 以外の結果が出たら即時それを返し、そうでなければ各リストの長さの差を返します。

part1 では各ペアについて `cmp` の結果が負である(つまり `lhs < rhs`)ものを抽出してインデックスの和を求めています。
part2 では、まず全パケットのリストと仕切りパケットのリスト(`[[[2]], [[6]]]`)を結合したものを `sum(map(list, self.pairs), dividers)` で作成します。そして `sort()` に対して `key` 引数として `functools.cmp_to_key` で変換した `cmp` メソッドを渡してソートします。

https://docs.python.org/3/howto/sorting.html#comparison-functions

### Rust

```rust
use itertools::Itertools;
use std::cmp::Ordering;
use std::io::{BufRead, BufReader, Read};
use std::str::FromStr;

#[derive(PartialEq, Eq)]
enum Value {
    List(Vec<Value>),
    Integer(u8),
}

impl Value {
    fn as_slice(&self) -> &[Value] {
        if let Self::List(v) = self {
            v.as_slice()
        } else {
            std::slice::from_ref(self)
        }
    }
}

impl PartialOrd for Value {
    fn partial_cmp(&self, other: &Self) -> Option<Ordering> {
        Some(self.cmp(other))
    }
}

impl Ord for Value {
    fn cmp(&self, other: &Self) -> Ordering {
        if let (Self::Integer(lhs), Self::Integer(rhs)) = (self, other) {
            lhs.cmp(rhs)
        } else {
            self.as_slice().cmp(other.as_slice())
        }
    }
}

#[derive(PartialEq, PartialOrd)]
struct Packet(Value);

impl FromStr for Packet {
    type Err = ();

    fn from_str(s: &str) -> Result<Self, Self::Err> {
        // `u8` のイテレータから再帰的にparseして `Value::List` を返す
        fn parse_list(iter: &mut impl Iterator<Item = u8>) -> Value {
            let mut v = Vec::new();
            while let Some(u) = iter.next() {
                match u {
                    b'[' => v.push(parse_list(iter)),
                    b']' => break,
                    b'0'..=b':' => v.push(Value::Integer(u - b'0')),
                    _ => {}
                }
            }
            Value::List(v)
        }
        Ok(Self(parse_list(&mut s.replace("10", ":").bytes())))
    }
}

struct Solution {
    pairs: Vec<(Packet, Packet)>,
}

impl Solution {
    fn new(r: impl Read) -> Self {
        Self {
            pairs: BufReader::new(r)
                .lines()
                .filter_map(Result::ok)
                .collect_vec()
                .split(String::is_empty)
                .filter_map(|lines| lines.iter().filter_map(|s| s.parse().ok()).collect_tuple())
                .collect(),
        }
    }
    fn part1(&self) -> usize {
        self.pairs
            .iter()
            .enumerate()
            .filter_map(
                |(i, (left, right))| {
                    if left < right {
                        Some(i + 1)
                    } else {
                        None
                    }
                },
            )
            .sum()
    }
    fn part2(&self) -> usize {
        let packets = self
            .pairs
            .iter()
            .flat_map(|pair| [&pair.0, &pair.1])
            .collect_vec();
        ["[[2]]", "[[6]]"]
            .iter()
            .filter_map(|s| s.parse::<Packet>().ok())
            .enumerate()
            .map(|(i, packet)| packets.iter().filter(|p| p < &&&packet).count() + i + 1)
            .product()
    }
}

fn main() {
    let solution = Solution::new(std::io::stdin().lock());
    println!("Part 1: {}", solution.part1());
    println!("Part 2: {}", solution.part2());
}
```

こちらはJSONライブラリなどを使わず自前でparseしています。

```rust
enum Value {
    List(Vec<Value>),
    Integer(u8),
}

struct Packet(Value);
```

とし、この `Packet` に対して `std::str::FromStr` Traitを実装することで `s.parse()` で `Result<Packet, ()>` を得られるようにしています。
この実装は1バイトずつ読み込みながら `[` が出現するたびに `]` に遭遇するまで再帰的にリストとしてparseしていきます。数値は2桁以上のものが含まれていると次に現れるバイトが数値か否か分からないと処理が複雑になってしまうのですが、偶然にもこの問題では出現する数値は最大でも `10` までのようなので、parseする前に 文字列 `"10"` を `'9'` の次のASCIIコード値を持つ `":"` に置換してから処理する、というハックを使っています。

比較については、`Value` に対して `PartialOrd`, `Ord` Traitを実装することで `<`, `>` 演算子による比較や `sort()` による並び替えを可能にしています。
両方ともに `Value::Integer` の場合は単純に `u8::cmp` を使えるので問題ありません。それ以外の場合に、`Value` を `&[Value]` に変換する `as_slice()` という関数を用意しています。`Vec<Value>` に対しては `.as_slice()` でそれを得ることができ、`Value::Integer` の場合には `std::slice::from_ref()` を使うことで `&[Value]` に変換できます。あとは変換したスライス同士に対して `.cmp` で比較できます。

あとは概ねPythonの実装と同様です。仕切りパケットの位置は `sort()` を使わずに、対象のパケットよりも小さいものをカウントして計算しています。
