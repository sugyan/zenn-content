---
title: "Day 14: Docking Data"
---

https://adventofcode.com/2020/day/14

ちょっと特殊なビット演算。


## part1

```
mask = XXXXXXXXXXXXXXXXXXXXXXXXXXXXX1XXXX0X
mem[8] = 11
mem[7] = 101
mem[8] = 0
```

のような入力が与えられる。
memory address, value ともに 36-bit unsigned integer として動作している。
36-bit それぞれに適用される mask が指定され、（part1では）それ以降の操作でmemoryへ**書き込まれる値**がそれぞれmaskによって以下のルールで書き換えられる。

- `0` はその位置のbitを常に`0`に上書きする
- `1` はその位置のbitを常に`1`に上書きする
- `X` は何も変更しない

memoryはすべて`0`で初期化されている状態から開始し、一連の操作を行った後に最終的に書き込まれている値の合計は幾つになるか、という問題。
上の例だと、maskされた結果 `mem[7]`には`101` が、`mem[8]`には`64`が書き込まれることになり、合計値 `165` が解となる。


### 考え方

書かれている通りに値を書き換えていくだけだが、毎回36bitすべて見ながら書き換えるのも面倒なので、1回の操作で書き換えられるよう 「`0`で上書きするためのmask」と「`1`で上書きするためのmask」を別々に用意する。前者は`0b111....111`、後者は`0b000...000`で初期値を用意し、maskを指定された際に ある位置の値が`0`なら前者を、`1`なら後者を変更してやる。`X`は無視。
実際に書き込む値に適用する際には `value & masks[0] | masks[1]` を計算することで仕様通りの書き換えが出来る。

memoryはaddressが大きな値になる可能性もあるので`dict`で持っておく。keyもvalueも36-bit unsigned integerがおさまるように言語によっては気をつける必要がある。


## part2

別versionのprogramとして動かす必要があったらしい。今度は**valueではなくaddressの方を書き換える**動作をするようだ。maskの動作も以下のように変わる。

- `0` は何も変更しない
- `1` はその位置のbitを常に`1`に上書きする
- `X` はその位置のbitをfloating bitとして扱う

floating bitは有り得るすべての値の組み合わせを生じ、それらのaddressすべてに値を書き込むことになる。

```
mask = 000000000000000000000000000000X1001X
mem[42] = 100
mask = 00000000000000000000000000000000X0XX
mem[26] = 1
```

という例では、`mem[42]`の`42`がmaskによって`26`, `27`, `58`, `59`になり、その4つの addressすべてに`100`が書き込まれる。
`mem[26]`は`26`がmaskによって `16`, `17`, `18`, `19`, `24`, `25`, `26`, `27`になり、その8つのaddressすべてに`1`が書き込まれる。
結果として最終的に書き込まれた値の合計は`208`となる。


### 考え方

今度はmaskの`0`を無視して、`1`のときはpart1と同様の操作に。問題は`X`のときだが、後で展開するためにとりあえず出現する位置だけを記録しておく。
そして、`1`のmaskで上書きした値から開始し、`X`が出現する位置が「`0`の場合の値」と「`1`の場合の値」をそれぞれ計算し追加していくことで、すべての組み合わせを生成していく。

あとはこうして生成されたすべてのaddressに対してvalueを入れていって合計値を計算するだけ。


## 解答例

```python
import re
from abc import ABC, abstractmethod
from collections import defaultdict
from typing import Dict, List


# part1, part2 共通のdecoder interfaceを用意
class Decoder(ABC):
    def __init__(self) -> None:
        self.mem: Dict[int, int] = defaultdict(int)

    @abstractmethod
    def set_mask(self, mask: str) -> None:
        pass

    @abstractmethod
    def write(self, address: int, value: int) -> None:
        pass


class Solution:
    def __init__(self, inputs: List[str]) -> None:
        self.inputs = inputs

    def part_1(self) -> int:
        class V1Decoder(Decoder):
            # `0`の場合のmaskと`1`の場合のmaskをそれぞれ計算
            def set_mask(self, mask: str) -> None:
                self.masks = [(1 << 36) - 1, 0]
                for i, c in enumerate(reversed(mask)):
                    if c == "0":
                        self.masks[0] &= ~(1 << i)
                    if c == "1":
                        self.masks[1] |= 1 << i

            # `value`に対して2つのmaskを適用させて書き込む
            def write(self, address: int, value: int) -> None:
                self.mem[address] = value & self.masks[0] | self.masks[1]

        return sum(self.__run(V1Decoder()).values())

    def part_2(self) -> int:
        class V2Decoder(Decoder):
            # `X`の場合は出現したindexだけを格納しておく
            def set_mask(self, mask: str) -> None:
                self.floating: List[int] = []
                self.mask = 0
                for i, c in enumerate(reversed(mask)):
                    if c == "1":
                        self.mask |= 1 << i
                    if c == "X":
                        self.floating.append(i)

            # `addresses`のlistを、`i`番目のbitが`0`のものと`1`のものに分けて更新していく
            def write(self, address: int, value: int) -> None:
                addresses = [address | self.mask]
                for i in self.floating:
                    addresses = sum(
                        [[a | 1 << i, a & ~(1 << i)] for a in addresses], []
                    )
                for address in addresses:
                    self.mem[address] = value

        return sum(self.__run(V2Decoder()).values())

    # mask更新の行とwriteの行を、それぞれ順番にdecoderに実行させる共通処理
    def __run(self, decoder: Decoder) -> Dict[int, int]:
        re_program = re.compile(r"mem\[(\d+)\] = (\d+)")
        for line in self.inputs:
            match = re_program.fullmatch(line)
            if match:
                decoder.write(int(match.group(1)), int(match.group(2)))
            elif line.startswith("mask = "):
                decoder.set_mask(line[7:])
        return decoder.mem
```
