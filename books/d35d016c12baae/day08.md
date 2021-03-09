---
title: "Day 8: Handheld Halting"
---

https://adventofcode.com/2020/day/8

少し機械語っぽい入力になって、パズル度が増してくる。


## part1

```
nop +0
acc +1
jmp +4
acc +3
jmp -3
acc -99
acc +1
jmp -4
acc +6
```

のような入力が与えられる。各行は *operation* と *argument* からなっていて、`nop` は何もせずに次の行へ、`acc` はaccumulatorに値を加算してから次の行へ。`jmp` は次の行ではなく 現在行から相対的な値の行へjumpする。

実際に0行目から順に実行してみると無限ループになるので、そのループにより2周目に入る直前時点でのaccumulatorの値を求めよ、という問題。
上の例だと、2行目を2回目に訪れる直前の値は `5` なのでそれが解となる。


### 考え方

愚直にsimulationして実行していく、で良い。実行済みの行を保存する `set` だけ用意しておき、そこに記録しながら1行ずつ実行していく。
実行済みの行に辿り着いたらそのときのaccumulatorの値を返せば良い。


## part2

実はどこか1箇所だけ `nop` と `jmp` が入れ替わってしまっていることが原因で無限ループになっており、そこを直せば正しく最終行に到達できるはず、とのこと。
前述の例だと、最後から2番目の `jmp -4` を `nop -4` に置き換えることで最終行に到達できるようになる。そのときのaccumulatorの値 `8` が解となる。


### 考え方

part1同様にsimulation実行する。ただし引数に `Optional` なindexを渡し、指定されていたらその行だけ `nop` と `jmp` を入れ替えて実行するようにする。
メソッドの返り値は `Tuple[int, bool]` にし、「accumulatorの値」と「正しく最終行まで実行されていたら `True`, ループに突入していたら `False` を示すbool値」のペアを返すようにする。

part1 はこれを使って `None` を指定しどこも変更せずに実行して得た値を使えばよい。
part2 は入れ替える行を総当たりで指定して試してみて、`True` が返ってきたらそれで終了、とする。

入力は600行程度なので一応こういったbrute force的な方法でもとりあえず解は得られる。
より効率的にやるなら、backtracking的に 途中まで実行した状態を保持しておいて、入れ替えてみて失敗した(無限ループに突入してしまった)場合は入れ替える直前状態まで戻るだけ、にすると良さそう。


## 解答例

```python
from enum import Enum
from typing import List, Optional, Tuple


class Operation(Enum):
    ACC = "acc"
    JMP = "jmp"
    NOP = "nop"


class Solution:
    def __init__(self, inputs: List[str]) -> None:
        # 入力各行を`operation`と`argument`に分割して保持
        def parse(line: str) -> Tuple[Operation, int]:
            ope, arg = line.split(" ")
            return Operation(ope), int(arg)

        self.instructions = list(map(parse, inputs))

    def part_1(self) -> int:
        # 何も指定せずに実行した結果 (返り値ペアのbool値は当然`False`になるがそれで問題ない)
        return self.__run()[0]

    def part_2(self) -> int:
        # 総当たりで変更する行を変えて実行してみる
        for i in range(len(self.instructions)):
            ret = self.__run(i)
            # 返り値ペアのbool値が`True`なら最終行まで到達できているので終了
            if ret[1]:
                return ret[0]
        raise ValueError

    def __run(self, change: Optional[int] = None) -> Tuple[int, bool]:
        # 既に実行済みの行を保存しておく
        visited = set()
        i, acc = 0, 0
        while i < len(self.instructions):
            # 実行済みの行だったらその時点でのaccumulatorの値を`False`とともに返す
            if i in visited:
                return acc, False
            visited.add(i)

            ope, arg = self.instructions[i]
            # 変更指定されている行だったら JMP ⇔ NOP を入れ替えて実行する
            if i == change:
                if ope == Operation.ACC:
                    pass
                elif ope == Operation.JMP:
                    ope = Operation.NOP
                elif ope == Operation.NOP:
                    ope = Operation.JMP
            # 各operationに対する処理
            if ope == Operation.ACC:
                acc += arg
                i += 1
            if ope == Operation.JMP:
                i += arg
            if ope == Operation.NOP:
                i += 1
        # 無事に最終行まで到達していたらaccumulatorの値を`True`とともに返す
        return acc, True
```
