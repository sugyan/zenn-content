---
title: "Day 18: Operation Order"
---

https://adventofcode.com/2020/day/18

数式の評価を実装する問題。


## part1

```
1 + 2 * 3 + 4 * 5 + 6
1 + (2 * 3) + (4 * (5 + 6))
```

のような入力が与えられる。
数値計算だが、普通の四則演算とは演算子の順序が異なる。
`*`が`+`より優先されるということがなく、左から右に順番に評価され、括弧だけがそれらより優先される。

上の例の1つ目だと、

```
  1 + 2 * 3 + 4 * 5 + 6
= 3 * 3 + 4 * 5 + 6
= 9 + 4 * 5 + 6
= 13 * 5 + 6
= 65 + 6
= 71
```

2つ目だと、

```
  1 + (2 * 3) + (4 * (5 + 6))
= 1 + (2 * 3) + (4 * 11)
= 1 + (2 * 3) + 44
= 1 + 6 + 44
= 7 + 44
= 51
```

という具合。
この法則に従ってすべての式の結果の和を求めよ。という問題。


### 考え方

最優先は括弧の中なので、括弧で囲まれた部分を抽出して再帰的に処理してその計算結果で置換していく。
あとは括弧の存在しない`*`と`+`だけの式を扱う前提で、出現する数値を演算子が出てくるたびに計算して結果を返してやれば良い。


## part2

今度は、`+`が`*`よりも優先される、という法則で計算する、とのこと。
この法則に従って同様にすべての式の結果の和を求めよ、という問題。


### 考え方

この場合は、都度処理していくわけにもいかないので、一旦 *operator* と *oprand* の組み合わせを `list` に格納するだけにしていって、最後に計算の処理をする。

part1の場合はこの `list`を先頭から見ていって順番に処理していくだけ。part2の場合はこれをstackとして処理していく。
最後の要素を取り出し、`+`ならその前のものと足し合わせ、`*`なら答えに掛け合わせていく。
これを繰り返すことで最終的な結果が得られる。


## 解答例

```python
import re
from typing import List


class Solution:
    def __init__(self, inputs: List[str]) -> None:
        self.expressions = inputs
        # 括弧で括られた部分を抽出するための正規表現
        self.re = re.compile(r"\(([^\(\)]*)\)")

    def part_1(self) -> int:
        return sum([self.evaluate(e, False) for e in self.expressions])

    def part_2(self) -> int:
        return sum([self.evaluate(e, True) for e in self.expressions])

    # 再帰的に処理して与えられた文字列の評価結果を返す関数
    def evaluate(self, exp: str, adv: bool) -> int:
        # まずは括弧内を先に評価していって置換していく
        while True:
            match = self.re.search(exp)
            if match:
                exp = self.re.sub(str(self.evaluate(match.group(1), adv)), exp, count=1)
            else:
                # 括弧のない文字列になったら次へ進む
                break
        # `+` か `*` で分割していって (operator, operand) の `list` として保持
        parsed = ["*", *(map(str.strip, re.split(r"([\+\*])", exp)))]
        terms = [
            (parsed[x * 2], int(parsed[x * 2 + 1])) for x in range(len(parsed) // 2)
        ]
        # 初期値は`1`として、advanceか否かで計算処理を分ける
        ret = 1
        if adv:
            # stackの末尾から見ていって更新していく
            while terms:
                ope, val = terms.pop()
                if ope == "+":
                    terms[-1] = (terms[-1][0], terms[-1][1] + val)
                if ope == "*":
                    ret *= val
        else:
            # 先頭から順番に処理していく
            for ope, val in terms:
                if ope == "+":
                    ret += val
                if ope == "*":
                    ret *= val
        return ret
```
