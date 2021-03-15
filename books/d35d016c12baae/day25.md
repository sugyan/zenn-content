---
title: "Day 25: Combo Breaker"
---

https://adventofcode.com/2020/day/25

RSA暗号のようなもの。


## part1

```
5764801
17807724
```

のような入力が与えられる。
カードの公開鍵とドアの公開鍵をそれぞれ表している。
カードとドアの間でそれぞれ秘密の *loop size* を使ってhandshakeが行われる。

まず *subject number* をtransformするという手続きがあり、これは値を`1`から始めて「*subject number* を掛けた値を `20201227` で割ったもの」に変換する。
これを *loop size* 回繰り返す。

- カードは *subject number* `7`でカードの *loop size* 回のtransformを行う。これがカードの公開鍵の値となる。
- ドアも同様に *subject number* `7`でドアの *loop size* 回のtransformを行う。これがドアの公開鍵の値となる。
- カードはドアの公開鍵を *subject number* としてカードの *loop size* 回のtransformを行う。これが求める暗号キーになる。
- ドアも同様にカードの公開鍵を *subject number* としてドアの *loop size* 回のtransformを行う。これがカードで計算した暗号キーと同じ値になる。

上の例でいうと、最初の *subject number* `7`を`8`回transformすることで `5764801`が求められる、のでカードの *loop size* は`8`、同様に考えてドアの *loop size* は`11`ということが分かる。

```python
>>> (7 ** 8) % 20201227
5764801
>>> (7 ** 11) % 20201227
17807724
```

なので ドアの公開鍵 `17807724` をカードの *loop size* `8`でtransformしていくことで 暗号キー `14897079` が求められる。
同様にしてカードの公開鍵 `5764801` をドアの *loop size* `11`でtransformしても同じ値が求められる。

```python
>>> (17807724 ** 8) % 20201227
14897079
>>> (5764801 ** 11) % 20201227
14897079
```

そういうものらしい…。
ともかく、このようにして求められる暗号キーを算出せよ、という問題。


### 考え方

brute forceで最初の *subject number* `7`を繰り返しtransformしていくことで両公開鍵になるための *loop size* を求められるので、それを求めたらあとはどちらかの公開鍵を使ってもう片方の *loop size* 回だけtransformしてやれば良い。


## part2

`49`個（ここまでの24日 × 2つずつ + この日のpart1）の星を集めていれば、自動的にpart2もcomplete、となる。

`50`個の星がすべて集まった！やったー！！


## 解答例

```python
from functools import reduce
from typing import List

DIV = 20_201_227


class Solution:
    def __init__(self, inputs: List[str]) -> None:
        self.card_key = int(inputs[0])
        self.door_key = int(inputs[1])

    def part_1(self) -> int:
        # 目的の`key`の価になるまでtransformを繰り返し、その回数を求める
        def loop_size(key: int) -> int:
            loop, value = 0, 1
            while value != key:
                value = (value * 7) % DIV
                loop += 1
            return loop

        card_loop = loop_size(self.card_key)
        door_loop = loop_size(self.door_key)
        assert card_loop != door_loop
        # 各`loop_size`が求められれば あとはそれを使ってtransformしていくだけ
        return reduce(lambda x, _: (x * self.door_key) % DIV, range(card_loop), 1)
```
