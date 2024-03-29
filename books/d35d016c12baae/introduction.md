---
title: "はじめに"
---


## Advent of Code とは

https://adventofcode.com/about

Advent of Code は、Eric Wastl氏によって作成されているプログラミングパズルです。
クリスマスの季節12月に、1日から25日までの期間で毎日問題が出題されます。
2015年から始まっているようで 2020年が6回目の開催となりました。

期間中に毎日出題される問題は「パズル入力」が与えられ、それに対する「解答」を提出する方式になっています。ログインしているユーザごとに異なる入力と正解が用意されているため、他の人の解答をコピーしても正解にはならないようになっているようです。

問題はpart1とpart2の2つに分かれていて、最初は比較的簡単な問題としてpart1が出題され、それに正解するとより難しいpart2の問題に進むことができます。
part1とpart2で問題の入力は共通のものが使われ、その入力への解釈が変わったり計算の条件が変わることにより各partの解答が異なるものになります。

各partを解くごとに「星」を得ることができ、25日間×2partで合計 `50` 個の星を集めることができれば、その年のAdvent of Codeは完走、ということになります。


いわゆる競技プログラミングやオンラインジャッジのものと違って、あくまで「パズル」として以下のような特色があります。


#### 1. コードを提出するわけではない

多くのオンラインジャッジシステムの場合は、入力に対して正しい解を出力するための「コード」を提出することになりますが、Advent of Codeでは提出するのは「自分に用意された入力に対する解」のみです。
その解さえ導出できれば、どんなプログラミング言語を使用しても、あるいはプログラミング言語を使用せずに暗算や手計算で解答しても構いません。
もちろん、実際の問題は人間の処理能力では不可能なくらいの規模の入力が用意されるので、通常は効率的に解を求めるためのコードを書いてコンピュータに計算させることになります。


#### 2. アルゴリズム問題に限らない

多くの問題はアルゴリズムやデータ構造によって解決されるものですが、すべてがそうとも限りません。
非効率と思われるような総当たりが有効な場面があったり、愚直に実行して膨大な計算をすることになる場合もあるかもしれません。数学的な知識が多少必要とされるものがあったり、高度な知識は必要なくただ実装が大変なだけの問題もあったりします。


#### 3. 競技要素もあるがメインではない

12月の開催中は毎日 `EST/UTC-5 00:00` （`JST`日本標準時だと`14:00`） に新しい問題が出題されます。
早く正解したユーザにscoreが付与されランキングが公開されますが、これは毎回上位100人までだけが対象で、ここで上位を狙っていくのはかなり難しいと思います。

全体での [overall learderboard](https://adventofcode.com/2020/leaderboard) とは別に、限られたユーザたちだけでscoreを競う [private leaderboard](https://adventofcode.com/2020/leaderboard/private) を作る機能もありますので、競争が好きな人はそれを利用してみるのも良いでしょう。


## 楽しみ方は人それぞれ

基本的にはパズルを解いていって、星50個を集めることが目標になります。

厳格に正しいコードを書いたり他人と競ったりすることにこだわらず、自分のペースでゆっくり楽しみながら解いていくと良いと思います。
新しい言語を習得するための練習として慣れないプログラミング言語で挑戦してみるのも良いかもしれません。

どうしても解き方が分からないときには [Reddit](https://www.reddit.com/r/adventofcode/) で他の解答者のコードを見て参考にしても構いません。
自力で解いた後で他の人がどう解いているのかを知るために上記のRedditを覗いてみるのも良いと思います。

[Reddit](https://www.reddit.com/r/adventofcode/) では様々な解答例の他にも、解答を導く過程を可視化することを楽しんでいたりマイナーな言語や奇抜な方法を使って解いている人がいたり、様々な楽しみ方を発見することができます。


## 本書について

私は2019, 2020のAdvent of CodeをRustの習得目的で最初はRustで解いてみました。
その後、2020のものをPythonでも解いてみて、それぞれの言語の違いを楽しみました。
Rustでの解答記録は [個人の記事](https://zenn.dev/sugyan) で書いていましたが、本書はそれをPythonで書き直しながらまとめたものになります。

Advent of Codeはまだ日本国内では知名度が低いようで、2020はだいぶ増えたと思いますが日本語圏の参加者はまだまだ少ないように感じます。
サイトがすべて英語でありRedditの議論の場なども英語のため、日本語情報が少ないことがハードルが高く参加しづらい原因の一つかと思っています（実際には機械翻訳を駆使すれば英語が苦手な私でもそれほど問題なく楽しめるのですが）。

本書の情報量はたいしたものではありませんが、問題の概要や考え方や解答例などの日本語情報が少しでもあれば気軽に参加してみる気になる人もいるのでは、と思い、執筆してみました。

本書の存在をきっかけにAdvent of Codeを楽しむ仲間が増えてくれたら嬉しく思います。
