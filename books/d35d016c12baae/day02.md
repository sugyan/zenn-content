---
title: "Day 2: Password Philosophy"
---

https://adventofcode.com/2020/day/2

入力のparseが必要になる。


### part1

```
1-3 a: abcde
1-3 b: cdefg
2-9 c: ccccccccc
```

のような入力が与えられる。

与えられた条件を満たしている行の数を返す。
part1では `1-3 a` は「`a` が `1`回以上 `3`回以下出現する」という意味になる。

:::details 考え方

そのまま実装するだけ。

:::


### part2

解釈が変わって、 `1-3 a` は「`1`文字目か `3`文字目 どちらかだけが `a`である」という意味になる。 indexは 0-origin ではないことに注意。

:::details 考え方

そのまま実装するだけ。

:::


### 解答例

:::details Python実装

```python
import re


class Solution:
    def __init__(self, inputs: List[str]) -> None:
        self.lines = inputs
        # 正規表現でcaptureして処理する
        self.re = re.compile(r"(\d+)\-(\d+) (.): (.+)")

    def part_1(self) -> int:
        def validate(line: str) -> bool:
            match = self.re.match(line)
            if match:
                lo = int(match.group(1))
                hi = int(match.group(2))
                c = match.group(3)
                password = match.group(4)
                return lo <= password.count(c) <= hi
            else:
                return False

        return len(list(filter(validate, self.lines)))

    def part_2(self) -> int:
        def validate(line: str) -> bool:
            match = self.re.match(line)
            if match:
                p1 = int(match.group(1)) - 1
                p2 = int(match.group(2)) - 1
                c = match.group(3)
                password = match.group(4)
                return (password[p1] == c) ^ (password[p2] == c)
            else:
                return False

        return len(list(filter(validate, self.lines)))
```
