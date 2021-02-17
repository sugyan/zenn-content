---
title: "Day 11: Seating System"
---

https://adventofcode.com/2020/day/11

変則ライフゲーム、的なもの。


## part1

```
L.LL.LL.LL
LLLLLLL.LL
L.L.L..L..
LLLL.LL.LL
L.LL.LL.LL
L.LLLLL.LL
..L.L.....
LLLLLLLLLL
L.LLLLLL.L
L.LLLLL.LL
```

のように、`.`で床を `L`で座席の配置を表す入力が与えられる。

part1は、隣接する8つの位置を見て

- その座席が空席で(`L`)、隣接するすべての位置にも埋まっている座席(`#`)が1つも無ければ、埋まる(→`#`)
- その座席が埋まっていて(`#`)、隣接する座席のうち4つ以上が埋まっていたら(`#`)、空席になる(→`L`)

というルールに従って同時に更新される。床(`.`)はずっと床のまま変わらない。
この規則での更新が繰り返されるとやがて安定し、どの座席も状態が更新されなくなるという。
そのときの埋まっている席数を求めよ、という問題。


### 考え方

素朴に、安定するまでsimulationを続けていく、で良い。
各座標でそれぞれ隣接する8つの座席の状況を確認。ルールに従って次の状態を決定していく。
次の状態が現在の状態と差異が無かったらloopを停止し、改めて`#`の数をcountして返す。


## part2

実は考えなければならないのは「隣接している8つの位置の座席」ではなく「8方向それぞれで見える最初の座席」だった。
床(`.`)は無視してその方向で最も近い座席の空席状況を見ることになる。
ついでに、空席になる条件として「**4つ**以上が埋まっていたら」だったのが「**5つ**以上が埋まっていたら」と閾値が変わる。
このルールを適用した場合に、更新されなくなったときに埋まっている座席数を求めよ、という問題。


### 考え方

part1では無条件で隣接する座標の状況だけを確認していたが、今度は座標によって見るべき座席の座標が変わってくる。
毎回求めていては非効率なので 予め「この座席の位置からは、この座標の座席たちの状況を確認する」という `dict` を作っておくと良さそう。
それぞれの座席から、8方向それぞれに最初に見える座席を探していく。`adjacent`が`True`のときはその探索を距離`1`で打ち切ることで、part1の場合の条件になる。

これで、各座標から見るべき座席の座標が引けるようになるので、part1同様にsimulationしていく。
part1とpart2で空席になる閾値が変わるので引数`threshold`を受け取るようにする。

これで、part1, part2ともに共通の処理で引数を変えるだけで答えが求められるようになる。


## 解答例

```python
from collections import defaultdict
from copy import deepcopy
from typing import Dict, List, Optional, Tuple

Pos = Tuple[int, int]


class Solution:
    def __init__(self, inputs: List[str]) -> None:
        self.layout = [list(x) for x in inputs]

    def part_1(self) -> int:
        return sum([s.count("#") for s in self.__simulate(True, 4)])

    def part_2(self) -> int:
        return sum([s.count("#") for s in self.__simulate(False, 5)])

    def __simulate(self, adjacent: bool, threshold: int) -> List[List[str]]:
        # 各座標からチェックすべき座席の座標リストを先に求めて保持しておく
        positions = self.__target_positions(adjacent)
        # ただの代入では参照渡しになってしまうので注意
        curr_state = deepcopy(self.layout)
        while True:
            next_state = deepcopy(curr_state)
            for i, row in enumerate(curr_state):
                for j, ch in enumerate(row):
                    if ch == ".":
                        continue
                    # 各座標からチェックすべき座標の座席が埋まっている数を数える
                    occupied = len(
                        [True for i, j in positions[(i, j)] if curr_state[i][j] == "#"]
                    )
                    # 条件に合わせて次の状態を更新
                    if ch == "L" and occupied == 0:
                        next_state[i][j] = "#"
                    if ch == "#" and occupied >= threshold:
                        next_state[i][j] = "L"
            # 何も変化が起きなくなったら終了
            if next_state == curr_state:
                break
            else:
                curr_state = next_state
        return curr_state

    def __target_positions(self, adjacent: bool) -> Dict[Pos, List[Pos]]:
        # 各方向に移動していって最初に見つかる座席の座標を探す(見つからなければ`None`)
        def search_seat(i: int, j: int, di: int, dj: int) -> Optional[Pos]:
            while True:
                i += di
                j += dj
                if 0 <= i < len(self.layout) and 0 <= j < len(self.layout[i]):
                    if self.layout[i][j] != ".":
                        return (i, j)
                    # `adjacent`の場合は距離`1`までしか見ない
                    elif adjacent:
                        return None
                else:
                    return None

        d = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]
        target_positions = defaultdict(list)
        for i in range(len(self.layout)):
            for j in range(len(self.layout[i])):
                # 各方向に座席を探し、見つかったらその座標をリストに追加
                for di, dj in d:
                    pos = search_seat(i, j, di, dj)
                    if pos:
                        target_positions[(i, j)].append(pos)
        return target_positions
```
