---
title: "Day 20: Jurassic Jigsaw"
---

https://adventofcode.com/2020/day/20

おそらく最も実装が大変な問題。


## part1

```
Tile 2311:
..##.#..#.
##..#.....
#...##..#.
####.#...#
##.##.###.
##...#.###
.#.#.#..##
..#....#..
###...#.#.
..###..###

Tile 1951:
#.##...##.
#.####...#
.....#..##
#...######
.##.#....#
.###.#####
###.##.##.
.###....#.
..#.#..#.#
#...##.#..

...
```

といった入力が与えられる。
TileのID、続いてモノクロ画像を表すその内容。
各Tileの画像はそれぞれバラバラに**回転**や**反転**されていたりする。が、隣り合うTile同士は同じ境界を持っている、とのこと。
すべてを正しく組み合わせることで元の全体画像を復元できる、らしい。

part1はまず、正しく組み合わせたときに四隅の角の位置に来るTileのIDを掛け合わせた値を求めよ、という問題。


### 考え方

この時点ではまだ完全に回転や反転まで求める必要は無い。

幸い（？）、複数の接続箇所で同一の境界パターンが出現することは無いようなので、すべてのTileの各辺のパターンを列挙して出現頻度を数えてみれば四隅に来るべきTileを特定することが出来る。

とりあえず回転や反転に関する値を定義

```python
from enum import Enum


class Orientation(Enum):
    ROTATE000 = (0, False)
    ROTATE090 = (1, False)
    ROTATE180 = (2, False)
    ROTATE270 = (3, False)
    ROTATE000_FLIPPED = (0, True)
    ROTATE090_FLIPPED = (1, True)
    ROTATE180_FLIPPED = (2, True)
    ROTATE270_FLIPPED = (3, True)
```

90°ずつ回転したもの、それらをそれぞれをx軸で（べつにy軸でも良い）反転したもの、で8種類のパターンが存在することになる。

Tileに関して `top`, `left`, `bottom`, `right` それぞれの辺の表現を各`Orientation`で求めるメソッドを用意しておくとやりやすい。


ここまで準備できれば、あとは入力をparseして各Tileの各辺のパターン出現頻度を数え上げていく。
反転したものも有り得るので、各Tileにつき2パターンでの境界辺を算出する。

Tileを正しく並べたときには隣り合うTile同士は辺を共有するのでその辺の出現数は`2`、隣が存在しない端の位置のTileの端の辺は出現数が`1`になる。
各Tileにおいて4辺それぞれの出現数を見たとき、四隅のTileだけは出現数`1`の辺が2つ存在する、ということになるので それだけを抽出すれば良い。


## part2

実際にすべてのTileを正しく並べ、境界を取り除いて元の全体画像を復元して、それを正しく回転・反転した場合に

```
                  # 
#    ##    ##    ###
 #  #  #  #  #  #   
```

で表されるsea monsterのパターンが検出される。
その際にsea monsterではない`#`の数を求めよ、という問題。


### 考え方

ここでは完全に正しい並べ方を求める必要がある。
とはいえ四隅がどのTileになるかは求めることが出来ているし、各辺を共有する隣り合うTile同士のIDは求められるので、ただ順番に並べて行けば良いだけではある。

まずは四隅に該当するものを1つだけ抽出。これが一番左上に来るとすると`top`と`left`が出現数`1`、`bottom`と`right`が出現数`2`になるはずなので、そうなる向きを求める。

そうして左上隅とその向きが確定したら、あとはその`right`と境界を共有するTileのIDは分かるし、そのTileの`left`がそれと同じものになる向きを求めれば右隣のIDと`Orientation`が確定する。それを繰り返して最上段が確定できる。

そこから同様にして今度は最下段Tileの`bottom`と境界を共有するTileの`top`を同じパターンになるよう`Orientation`を探し、順番に下に繋げていけば、全体が完成する。

そうしたら境界を取り除いた全体画像を生成し、やはり8パターンの回転・反転を試しながらsea monsterのパターンに一致する数を求めていく。


## 解答例

```python
from collections import defaultdict
from copy import deepcopy
from dataclasses import astuple, dataclass
from enum import Enum
from functools import reduce
from typing import Iterable, List, Optional, Tuple


# 元の状態から90°ずつ回転したもの、それぞれをX軸で反転したもの、で8パターンを考慮する
class Orientation(Enum):
    ROTATE000 = (0, False)
    ROTATE090 = (1, False)
    ROTATE180 = (2, False)
    ROTATE270 = (3, False)
    ROTATE000_FLIPPED = (0, True)
    ROTATE090_FLIPPED = (1, True)
    ROTATE180_FLIPPED = (2, True)
    ROTATE270_FLIPPED = (3, True)


# 各辺のパターンを表す
@dataclass
class Borders:
    top: str
    left: str
    bottom: str
    right: str


# IDとTileの初期状態を保持するClass
class Tile:
    def __init__(self, tile_id: int, lines: List[str]) -> None:
        self.id = tile_id
        self.data = [list(s) for s in lines]

    # 指定した`orientation`で回転・反転させたときの各辺パターンを計算する
    def borders(self, orientation: Orientation) -> Borders:
        data = self.translated(orientation)
        return Borders(
            *[
                "".join(x)
                for x in [
                    data[0],
                    [data[i][0] for i in range(len(data))],
                    data[-1],
                    [data[i][-1] for i in range(len(data))],
                ]
            ]
        )

    # 指定した`orientation`で回転・反転させたときの画像内容を計算する
    def translated(self, orientation: Orientation) -> List[List[str]]:
        rotate, flip = orientation.value
        data = deepcopy(self.data)
        for _ in range(rotate):
            next_data = deepcopy(data)
            for i, row in enumerate(data):
                for j, col in enumerate(row):
                    next_data[j][len(row) - 1 - i] = data[i][j]
            data = next_data
        if flip:
            for row in data:
                row.reverse()
        return data


# 正しく並べるときの`Tile`と`Orientation`の組み合わせを保持するClass
@dataclass
class Arrangement:
    tile: Tile
    orientation: Orientation

    def borders(self) -> Borders:
        return self.tile.borders(self.orientation)

    # borderの部分を除去した完成画像データを返す
    def data_without_border(self) -> List[List[str]]:
        data = self.tile.translated(self.orientation)
        return [row[1:-1] for row in data[1:-1]]


class Solution:
    def __init__(self, inputs: List[str]) -> None:
        # 空行で区切る
        def split_at_empty() -> Iterable[List[str]]:
            indices = [idx for idx, x in enumerate(inputs) if not x]
            for start, end in zip([-1, *indices], [*indices, len(inputs)]):
                yield inputs[start + 1 : end]

        tiles = []
        for lines in split_at_empty():
            if not lines:
                continue
            tile_id = int(lines[0].split(" ")[1].rstrip(":"))
            tiles.append(Tile(tile_id, lines[1:]))

        # 最初にすべて組み立てた結果を求めてしまう
        self.reassembled = self.__reassemble(tiles)

    def part_1(self) -> int:
        # 四隅に来るTileのIDだけを使う
        return reduce(
            lambda x, y: x * y,
            [
                self.reassembled[0][0].tile.id,
                self.reassembled[0][-1].tile.id,
                self.reassembled[-1][0].tile.id,
                self.reassembled[-1][-1].tile.id,
            ],
        )

    def part_2(self) -> int:
        # すべて組み合わせてborder除去し完成した画像データを一つのTileとして格納する
        image_data = []
        for row in self.reassembled:
            data_row = [col.data_without_border() for col in row]
            for i in range(len(data_row[0])):
                image_data.append(
                    "".join(["".join(data_col[i]) for data_col in data_row])
                )
        image = Tile(0, image_data)

        # sea monsterがmatchすべき相対座標の`list`を用意
        sea_monster = [
            "                  # ",
            "#    ##    ##    ###",
            " #  #  #  #  #  #   ",
        ]
        monster_height = len(sea_monster)
        monster_width = len(sea_monster[0])
        monster_positions = []
        for i in range(len(sea_monster)):
            for j in range(len(sea_monster[i])):
                if sea_monster[i][j] == "#":
                    monster_positions.append((i, j))

        # 画像中に居るsea monsterの数を求める関数
        def search_monsters(image: List[List[str]]) -> int:
            # (i, j)からみてすべての相対座標が`#`であれば発見されたとみなす
            def found(i: int, j: int) -> bool:
                def match_monster(d: Tuple[int, int]) -> bool:
                    return image[i + d[0]][j + d[1]] == "#"

                return all(map(match_monster, monster_positions))

            count = 0
            for i in range(len(image) - monster_height):
                for j in range(len(image[i]) - monster_width):
                    if found(i, j):
                        count += 1
            return count

        # 全`Orientation`パターンでsea monsterを数える
        for o in Orientation:
            translated = image.translated(o)
            num_monsters = search_monsters(translated)
            # 1匹以上発見できたら全体の`#`の数から sea monsterのぶんだけ引いた数を返す
            if num_monsters > 0:
                return len(
                    list(filter(lambda x: x == "#", sum(image.data, [])))
                ) - num_monsters * len(monster_positions)
        return 0

    def __reassemble(self, tiles: List[Tile]) -> List[List[Arrangement]]:
        # 各辺パターンを持つIDのlistを保持する
        border_ids = defaultdict(list)
        for t in tiles:
            # 逆向きの辺も考慮する必要があるので2つの`Orientation`で全辺パターンを算出
            for o in [Orientation.ROTATE000, Orientation.ROTATE180]:
                for border in astuple(t.borders(o)):
                    border_ids[border].append(t.id)

        def first_row() -> List[Arrangement]:
            def first_col() -> Arrangement:
                # 他のTileと共有している辺が2個だけなら四隅に来るべきもの
                def is_corner(tile: Tile) -> bool:
                    def has_adjacent(border: str) -> bool:
                        return len(border_ids[border]) > 1

                    borders = astuple(tile.borders(Orientation.ROTATE000))
                    return len(list(filter(has_adjacent, borders))) < 3

                # 四隅のものを1つだけ抽出
                corner = next(filter(is_corner, tiles))

                # 指定した`orientation`にすると`top`と`left`が共有されない辺になるか否か
                def is_top_left(orientation: Orientation) -> bool:
                    borders = corner.borders(orientation)
                    return (
                        len(border_ids[borders.top]) == 1
                        and len(border_ids[borders.left]) == 1
                    )

                return Arrangement(corner, next(filter(is_top_left, Orientation)))

            # 左上のIDとOrientationが確定するので格納し、ここを起点として右に伸ばしていく
            row = [first_col()]

            # 右に繋がるTileとOrientationを求めていく
            def find_right(curr: Arrangement) -> Optional[Arrangement]:
                right = curr.borders().right
                ids = border_ids[right]
                if len(ids) != 2:
                    return None
                right_id = ids[0] if ids[1] == curr.tile.id else ids[1]
                t = next(filter(lambda t: t.id == right_id, tiles))
                for o in Orientation:
                    if t.borders(o).left == right:
                        return Arrangement(t, o)
                return None

            while True:
                right = find_right(row[-1])
                if right:
                    row.append(right)
                else:
                    break
            return row

        # 最上段のIDとOrientationが確定するので格納し、ここを起点として下に伸ばしていく
        rows = [first_row()]

        # 下に繋がるTileとOrientationを求めていく
        def find_bottom(curr: Arrangement) -> Optional[Arrangement]:
            bottom = curr.borders().bottom
            ids = border_ids[bottom]
            if len(ids) != 2:
                return None
            bottom_id = ids[0] if ids[1] == curr.tile.id else ids[1]
            t = next(filter(lambda t: t.id == bottom_id, tiles))
            for o in Orientation:
                if t.borders(o).top == bottom:
                    return Arrangement(t, o)
            return None

        while True:
            row = []
            for col in rows[-1]:
                bottom = find_bottom(col)
                if bottom:
                    row.append(bottom)
            if row:
                rows.append(row)
            else:
                break

        return rows
```
