---
title: "Day 21: Allergen Assessment"
---

https://adventofcode.com/2020/day/21

論理パズル的なもの、再び。


## part1

```
mxmxvkd kfcds sqjhc nhms (contains dairy, fish)
trh fvjkl sbzzf mxmxvkd (contains dairy)
sqjhc fvjkl (contains soy)
sqjhc mxmxvkd sbzzf (contains fish)
```

のような入力が与えられる。
どれかのアレルゲンがどれか1つの材料に入っているが、左側のリストにある材料に含まれてるアレルゲンがすべて右側の括弧で表示されているとは限らない、とのこと。

part1はまず、アレルゲンの入っている可能性の無いものが出現する回数を数えよ、という問題。
上の例だと `kfcds`, `nhms`, `sbzzf`, `trh` が可能性の無いものであり、合計出現回数は `5` となる。


### 考え方

例の場合について考えると、1行目と2行目で双方に `dairy` が含まれるので、共通して含まれているものが候補になる。
この場合だと `mxmxvkd` がそれに該当する（ここでは1つだけなので確定してしまうが、実際には複数あるかもしれない）。
同様に1行目と4行目に `fish` が含まれるので、共通する `mxmxvkd` と `sqjhc` が候補になる。
`soy` については3行目だけしか無いので `sqjhc` と `fvjkl` の2つが候補になる。

こうして挙げられた、各アレルゲンが含まれるリストに共通して含まれている材料がすべて「該当するかもしない候補」になるので、**それ以外すべて**が、求めるべき「可能性の無いもの」になる。
つまり、各アレルゲンについて「含まれているリストすべてに共通して出現している材料」を抽出し、それらの候補に含まれないものだけを数え上げてやれば良い。


## part2

では実際にどのアレルゲンがどの材料に含まれているかを特定し、アレルゲンの名前順に該当する材料を列挙して返せ、という問題。
前述の例だと `dairy`, `fish`, `soy` の順に繋げて `mxmxvkd,sqjhc,fvjkl` が解となる。


### 考え方

前述の例で考えると、part1で述べたように `dairy` は `mxmxvkd` と特定できる。
そうすると `fish` は `mxmxvkd` と `sqjhc` が候補だったが `mxmxvkd` が `dairy` と分かっているなら残る `sqjhc` の方が含むことになる。
同様に考えて `soy` は残っている `fvjkl` になる。

このように、候補が複数あっても他が確定することによって候補が絞られていって確定していけるようになっている。
このあたりは [day16](https://zenn.dev/sugyan/books/d35d016c12baae/viewer/day16) と同様に考えて解ける。


## 解答例

```python
import re
from collections import defaultdict
from typing import Dict, List


class Solution:
    def __init__(self, inputs: List[str]) -> None:
        # 材料リストと含まれるアレルゲンを抽出する正規表現
        re_contains = re.compile(r"^(.*?) \(contains (.*?)\)$")
        self.list = []
        # それぞれ抽出して`Tuple[List, List]`として一旦全部格納
        for line in inputs:
            match = re_contains.fullmatch(line)
            if match:
                self.list.append(
                    (match.group(1).split(" "), match.group(2).split(", "))
                )

    def part_1(self) -> int:
        # 含まれる候補に無い材料だけをすべて数えていけば良い
        candidates = set(list(sum(self.__candidates().values(), [])))
        ret = 0
        for ingredients, _ in self.list:
            ret += len(list([x for x in ingredients if x not in candidates]))
        return ret

    def part_2(self) -> str:
        candidates = self.__candidates()
        dangerous_ingredients = {}
        while len(candidates):
            # 候補となる材料が1種類しかないものを確定させる
            figure_outs = [
                (allergen, ingredients[0])
                for allergen, ingredients in candidates.items()
                if len(ingredients) == 1
            ]
            for figure_out in figure_outs:
                dangerous_ingredients[figure_out[0]] = figure_out[1]
                # 確定した材料を他のアレルゲンに関する候補から削除していく
                ingredient = candidates.pop(figure_out[0])[0]
                for ingredients in candidates.values():
                    if ingredient in ingredients:
                        ingredients.remove(ingredient)
        return ",".join(
            [dangerous_ingredients[key] for key in sorted(dangerous_ingredients.keys())]
        )

    # 各アレルゲンに関して、含んでいる可能性のある材料の候補をすべて列挙する
    def __candidates(self) -> Dict[str, List[str]]:
        # まず各アレルゲンごとに材料の出現回数を調べる
        counts_dict: Dict[str, Dict[str, int]] = defaultdict(lambda: defaultdict(int))
        for ingredients, allergens in self.list:
            for allergen in allergens:
                for ingredient in ingredients:
                    counts_dict[allergen][ingredient] += 1
        candidates = defaultdict(list)
        for allergen, counts in counts_dict.items():
            # すべてのリストに含まれている(== 最大出現回数である)材料を抽出する
            max_count = max(counts.values())
            for ingredient, count in counts.items():
                if count == max_count:
                    candidates[allergen].append(ingredient)
        return candidates
```
