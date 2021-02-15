---
title: "Day 7: Handy Haversacks"
---

https://adventofcode.com/2020/day/7

そろそろデータ構造の考慮が必要になってくる。


## part1

```
light red bags contain 1 bright white bag, 2 muted yellow bags.
dark orange bags contain 3 bright white bags, 4 muted yellow bags.
bright white bags contain 1 shiny gold bag.
muted yellow bags contain 2 shiny gold bags, 9 faded blue bags.
shiny gold bags contain 1 dark olive bag, 2 vibrant plum bags.
dark olive bags contain 3 faded blue bags, 4 dotted black bags.
vibrant plum bags contain 5 faded blue bags, 6 dotted black bags.
faded blue bags contain no other bags.
dotted black bags contain no other bags.
```

のような入力が与えられる。自然言語……。

part1は、`shiny gold bag`があったときに それを入れるbagとして有り得るのは何種類か、というもの。
この例だと `bright white` と `muted yellow` に入るのと、それらがそれぞれ `dark orange` と `light red` に入り得るので合計の `4` が解となる。


### 考え方

正規表現を使う、もしくは `" bags contain "` で `split` などして、bagとcontentsの関係は取得できる。
`shiny gold`を入れ得るものを探すので、contentsから逆に「自分を含み得る親のbag」を辿っていくための `dict` を構築していく。contentsが`"no other bags."`のときは無視して良い。

それが構築できれば、目的の`shiny gold`をrootとし 親として有り得るbagたちをどんどん辿っていけば良い。例のように`bright white`や`muted yellow`は`light red`と`dark orange`の双方が含み得る といったことがあるので、重複は避けるため親のbagは `set` に入れながらカウントすると良い。


## part2

part1では入力に含まれる数値は完全に無視していたが、今度は使われる。書かれている数の通りにbagを詰めていくとすると、1つの`shiny gold bag`の中には幾つのbagが含まれることになるか、という問題。
前述の例だと `1 + 1*7 + 2 + 2*11` で `32` が解となる。


### 考え方

今度はbagが持つべきcontentsの `(個数, 色)`、のリストを保持する `dict` を用意。`"no other bags."`のときは空のcontentsを持つ、とする。
あとは `(1, "shiny gold")` をrootとして、個数を掛けながら子を辿っていって全部足し合わせていけば良い。


## 解答例

```python
import re
from collections import defaultdict, deque
from typing import List


class Solution:
    def __init__(self, inputs: List[str]) -> None:
        # ruleを抽出し、各colorに含まれるべきもののlistを格納しておく
        re_contain = re.compile(r"(.*?) bags contain (.*?).")
        self.rules = {}
        for line in inputs:
            match = re_contain.fullmatch(line)
            if not match:
                continue
            self.rules[match.group(1)] = match.group(2).split(", ")

    def part_1(self) -> int:
        # 「そのcolorのbagを入れ得る親のbag」のlistを引くためのdictを構築
        dd = defaultdict(list)
        for bag, contents in self.rules.items():
            if contents == ["no other bags"]:
                continue
            for content in contents:
                color = content[content.find(" ") + 1 : content.rfind(" ")]
                dd[color].append(bag)
        s = set()
        # 幅優先探索で可能性のあるcolorを列挙していく
        dq = deque(["shiny gold"])
        while dq:
            color = dq.popleft()
            if color not in s:
                s.add(color)
                dq.extend(dd[color])
        return len(s) - 1

    def part_2(self) -> int:
        re_numcolor = re.compile(r"(\d+) (.*?) bags?")
        # 「そのbagには"幾つ、どのcolorが"入るか」のlistを引くためのdictを構築
        dd = defaultdict(list)
        for bag, contents in self.rules.items():
            for content in contents:
                match = re_numcolor.fullmatch(content)
                if match:
                    dd[bag].append((int(match.group(1)), match.group(2)))
        ret = 0
        # 深くなるごとに個数を掛け合わせながら探索していく
        dq = deque([(1, "shiny gold")])
        while dq:
            num, color = dq.popleft()
            ret += num
            dq.extend([(num * e[0], e[1]) for e in dd[color]])
        return ret - 1
```
