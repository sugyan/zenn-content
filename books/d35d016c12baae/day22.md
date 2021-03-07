---
title: "Day 22: Crab Combat"
---

https://adventofcode.com/2020/day/22

カードゲームのシミュレーション。


## part1

```
Player 1:
9
2
6
3
1

Player 2:
5
8
4
7
10
```

のような入力が与えられる。
2人のplayerのカードデッキの初期状態を表している。

各playerは一番上のカードを出し合い、数字の大きい方が勝ちとしてデッキ末尾に取り込む。
というのを繰り返してどちらかがデッキが空になったら勝負が決する、というもの。
そのときの勝者のscore（最終デッキの下から順に`i`番目のカードの数値に`i`を掛けたものの合計）を求めよ、という問題。

上の例だと、最終的に Player 2 が `3, 2, 10, 6, 8, 5, 9, 4, 7, 1` の順でカードを持った状態で終了し、score `306` が解となる。


### 考え方

そのままルール通りに実装してシミュレーションしてやれば良いだけ。
`deque` を使うのが良さそう。


## part2

player1が勝つための特殊なルールが追加された。

- 無限ループを防ぐため、同一game内で両者で同一のデッキ状態が出現した場合、即座に**player 1の勝ちとする** （ひどい）
- 各roundで双方のカードの数字が自分のデッキの残り枚数より少ない場合、先頭からその枚数ずつcopyしたデッキで構成した新しいデッキを使ってsubgameに入る。このsubgameの勝者が、元のgameにおいて出していたカードの数字の大小にかかわらず、そのroundの勝者になる

というrecursiveなルールに。
このルールで勝負した場合の最終scoreを求めよ、という問題。


### 考え方

やはりその通りに実装していけば良いだけ。
同一デッキの検出のために `set` に各playerのデッキをkeyにして保存していく。


## 解答例

```python
from collections import deque
from copy import deepcopy
from typing import Deque, Iterable, List


class Solution:
    def __init__(self, inputs: List[str]) -> None:
        # 空行で区切る
        def split_at_empty() -> Iterable[List[str]]:
            indices = [idx for idx, x in enumerate(inputs) if not x]
            for start, end in zip([-1, *indices], [*indices, len(inputs)]):
                yield inputs[start + 1 : end]

        self.decks = []
        for lines in split_at_empty():
            self.decks.append(deque(map(int, lines[1:])))

    def part_1(self) -> int:
        return sum(map(self.__score, self.__combat(deepcopy(self.decks), False)))

    def part_2(self) -> int:
        return sum(map(self.__score, self.__combat(deepcopy(self.decks), True)))

    # combatのシミュレーションを行い、最終的な結果を返す関数
    def __combat(self, decks: List[Deque[int]], recursive: bool) -> List[Deque[int]]:
        # ループ検出のためのmemory
        memo = set()
        # どちらかのデッキが空になるまで続ける
        while all(decks):
            # recursiveの場合はループをチェックし、検出されたらplayer 1が勝つようにする
            if recursive:
                key = tuple([tuple(deck) for deck in decks])
                if key in memo:
                    decks[1].clear()
                    return decks
                memo.add(key)
            # 各playerの一番上のカードを使って勝負するが `recursive` か否かで判定が変わる
            cards = [deck.popleft() for deck in decks]
            if recursive and cards[0] <= len(decks[0]) and cards[1] <= len(decks[1]):
                # 先頭から番号枚数ずつコピーした新たなデッキで勝負した結果を使う
                results = self.__combat(
                    [
                        deque(list(decks[0])[: cards[0]]),
                        deque(list(decks[1])[: cards[1]]),
                    ],
                    True,
                )
                if results[0]:
                    decks[0].extend([cards[0], cards[1]])
                else:
                    decks[1].extend([cards[1], cards[0]])
            else:
                # `recursive` でなければ 単にカードの数値の大小だけで判定
                if cards[0] > cards[1]:
                    decks[0].extend([cards[0], cards[1]])
                else:
                    decks[1].extend([cards[1], cards[0]])
        return decks

    # デッキからscoreを計算する関数
    @staticmethod
    def __score(deck: Deque[int]) -> int:
        return sum([card * (len(deck) - i) for i, card in enumerate(deck)])
```
