---
title: "Day 4: Passport Processing"
---

https://adventofcode.com/2020/day/4

ひたすらparseと判定が面倒なだけの問題…。


## part1

```
ecl:gry pid:860033327 eyr:2020 hcl:#fffffd
byr:1937 iyr:2017 cid:147 hgt:183cm

iyr:2013 ecl:amb cid:350 eyr:2023 pid:028048884
hcl:#cfa07d byr:1929

hcl:#ae17e1 iyr:2013
eyr:2024
ecl:brn pid:760753108 byr:1931
hgt:179cm

hcl:#cfa07d eyr:2025 pid:166559648
iyr:2011 ecl:brn hgt:59in
```

のような入力が与えられる。空行区切りでひとまとめのdataで、各dataはspaceまたは改行で区切られたfieldを持ち、各fieldは `:` で区切られたkey-valueとなる。

part1は「`cid` だけがoptionalなので欠損していてもよく、それ以外はrequired」としたときにvalidな件数は幾つか、という問題。この例だと1つ目と3つ目のものがvalidなので `2` が解となる。


### 考え方

ただその条件の通りにparseしてcountするだけ。
keyの存在だけ確認すれば良いので `set` なり `dict` なりに入れて「8つ揃っている」もしくは「7つだけ揃っていて `cid`が含まれていない」で判定すれば良い。


## part2

今度はkeyの存在確認だけではなく、valueも正しい値であることを確認する必要がある。ひたすらその条件の通りに実装していくだけ。


### 考え方

今度はvalueも見る必要があるので `dict` にデータを格納。
判定する場合はすべてのfieldについてそれぞれ条件に当てはまっているかを確認。1つでも不正な値が検出されたら `False` を返してやる。


## 解答例

```python
import re
from typing import Dict, Iterable, List


class Solution:
    def __init__(self, inputs: List[str]) -> None:
        # 空行で区切る
        def split_at_empty() -> Iterable[List[str]]:
            indices = [idx for idx, x in enumerate(inputs) if not x]
            for start, end in zip([-1, *indices], [*indices, len(inputs)]):
                yield inputs[start + 1 : end]

        self.passports = []
        for lines in split_at_empty():
            # 各fieldのkey-valueを保存
            fields = {}
            for line in lines:
                for field in line.split(" "):
                    k, v = field.split(":")
                    fields[k] = v
            self.passports.append(fields)

    def part_1(self) -> int:
        # keyの数を確認、7つだけのときは`cid`が含まれていないか否かで判定
        def validate(passport: Dict[str, str]) -> bool:
            return len(passport) == 8 or (len(passport) == 7 and "cid" not in passport)

        return len(list(filter(validate, self.passports)))

    def part_2(self) -> int:
        re_hgt = re.compile(r"(\d+)(cm|in)")
        re_hcl = re.compile(r"#[0-9a-f]{6}")
        re_ecl = re.compile(r"(?:amb|blu|brn|gry|grn|hzl|oth)")
        re_pid = re.compile(r"[0-9]{9}")

        # keyの数をpart1同様に確認しつつ、valueの中身も確認していく
        def validate(passport: Dict[str, str]) -> bool:
            def validate_values() -> bool:
                for k, v in passport.items():
                    if k == "byr" and not 1920 <= int(v) <= 2002:
                        return False
                    if k == "iyr" and not 2010 <= int(v) <= 2020:
                        return False
                    if k == "eyr" and not 2020 <= int(v) <= 2030:
                        return False
                    if k == "hgt":
                        match = re_hgt.fullmatch(v)
                        if match:
                            unit = match.group(2)
                            if unit == "cm" and 150 <= int(match.group(1)) <= 193:
                                pass
                            elif unit == "in" and 59 <= int(match.group(1)) <= 76:
                                pass
                            else:
                                return False
                        else:
                            return False
                    if k == "hcl" and not re_hcl.fullmatch(v):
                        return False
                    if k == "ecl" and not re_ecl.fullmatch(v):
                        return False
                    if k == "pid" and not re_pid.fullmatch(v):
                        return False
                    if k == "cid":
                        pass
                return True

            return (
                len(passport) == 8 or (len(passport) == 7 and "cid" not in passport)
            ) and validate_values()

        return len(list(filter(validate, self.passports)))
```
