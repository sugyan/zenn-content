---
title: "Day 19: Monster Messages"
---

https://adventofcode.com/2020/day/19

再帰的パターンマッチング。


## part1

```
0: 4 1 5
1: 2 3 | 3 2
2: 4 4 | 5 5
3: 4 5 | 5 4
4: "a"
5: "b"

ababbb
bababa
abbbab
aaabbb
aaaabbb
```

のような入力が与えられる。
前半はメッセージが従うべきルール、後半は1行ごと送られてくるメッセージを表している。
rule `0` に完全にmatchするメッセージは幾つあるか？という問題。
上の例だと、 `ababbb` と `abbbab` の`2`件だけがrule `0` に完全にmatchする。


### 考え方

正規表現を組み立てるという方法もありそうだが、言語によって差異もありそうなので ここでは正規表現を一切使わない解答を考える。

part1は、完全にmatchする入力をすべて展開する力技でも一応解ける。
文字の組み合わせで解釈できるものを `Dict[int, Set[str]]` に入れていって、各ruleがすべて展開できるものから次々に候補を展開して格納していく。
最終的にすべてのruleが展開できたら`0`に該当する `Set[str]` が得られるので、各メッセージはそこに含まれるか否かだけで判定できる。
（候補のメッセージ数は百万以上になったりするのでかなり厳しいが…）とりあえず答えは出せる。


## part2

入力のruleに変更が生じ、再帰的なruleが登場。

```
8: 42 | 42 8
11: 42 31 | 42 11 31
```


### 考え方

再帰があるので全展開の力技は無限に候補が生成されてしまい通用しない。

まずはruleをちゃんと定義し、

- 文字を表すもの
- 連続したruleの組み合わせを表すもの
- 複数（この問題では高々2個）のruleのどちらか（`OR`）、を表すもの

の3種に分類する。
入力のparse時にはこの分類ごとに型を分けて格納していく。

そして、文字列にruleをmatchさせる関数を用意する。
ここで、この関数が返すのは「文字列`s`に対してこの`rule`を適用させて、読み込み残った文字列として有り得るもの」のリスト、とする。
例えば `"a"` に該当するruleに `"ab"` というメッセージをmatchさせると `["b"]` が返る。`"bb"` のようにmatchしないメッセージだと `[]` と空の列を返す。
連続ruleの場合は、順番にmatchさせた結果を繰り返し適用していく。
複数どちらかの場合は両方の場合が有り得るのでそれぞれの結果を合わせたものになる。

こうしてこの関数を使ってメッセージ文字列に対し rule `0`を再帰的にmatchさせていくと、完全にmatchする場合は `""`を含むものが返ってくる。
まったくmatchしない場合は空の`list`になり、前方はmatchするが後方に余計なものが含まれている場合は残った部分文字列が含まれることになる。

part2の場合は再帰のmatchのさせ方によって `["", "aaababaa", "aaaaaabaaaababaa"]` のように複数の結果を得ることがある。
なんにせよ `""` が含まれるのであれば完全にmatchさせるパターンが存在しているということなので、これはvalidとみなせる。


## 解答例

```python
from copy import deepcopy
from typing import Any, Dict, Iterable, List


class Solution:
    def __init__(self, inputs: List[str]) -> None:
        # 空行で区切る
        def split_at_empty() -> Iterable[List[str]]:
            indices = [idx for idx, x in enumerate(inputs) if not x]
            for start, end in zip([-1, *indices], [*indices, len(inputs)]):
                yield inputs[start + 1 : end]

        self.rules: Dict[int, Any] = {}
        rule_lines, self.messages = split_at_empty()
        # ruleの展開
        for line in rule_lines:
            k, v = line.split(": ")
            # `"` が含まれているなら文字を表すもの -> `str`
            if '"' in v:
                self.rules[int(k)] = v[1]
            # `|` が含まれているなら`OR`条件のもの -> `tuple`
            elif "|" in v:
                self.rules[int(k)] = tuple(
                    [list(map(int, r.split(" "))) for r in v.split(" | ")]
                )
            # それ以外なら連続ruleの組み合わせのもの -> `list`
            else:
                self.rules[int(k)] = list(map(int, v.split(" ")))

    def part_1(self) -> int:
        return self.__validate(deepcopy(self.rules))

    def part_2(self) -> int:
        # `8` と `11` だけ、再帰を含むruleに書き換える
        rules = deepcopy(self.rules)
        rules[8] = ([42], [42, 8])
        rules[11] = ([42, 31], [42, 11, 31])
        return self.__validate(rules)

    def __validate(self, rules: Dict[int, Any]) -> int:
        # 文字列に対してruleをmatchさせ、読み込み残った文字列として有り得るものを返す関数
        def match(s: str, rule: Any) -> List[str]:
            ret = []
            # 文字に先頭matchしていれば2文字目以降のものを返す
            if type(rule) == str:
                if s.startswith(rule):
                    ret.append(s[1:])
            # 複数の組み合わせは`[s]`から始めて順番に適用させた結果を返す
            if type(rule) == list:
                ret.append(s)
                for r in rule:
                    messages = []
                    for m in ret:
                        messages += match(m, rules[r])
                    ret = messages
            # ORの場合は双方の結果を結合したものを返す
            if type(rule) == tuple:
                for r in rule:
                    ret += match(s, r)
            return ret

        # `0`にmatchさせて 空文字を含むlistが返ってきていれば完全にmatchしたと判定
        def validate(message: str) -> bool:
            return "" in match(message, rules[0])

        return len(list(filter(validate, self.messages)))
```
