## 概要
ツイッターアカウントのフォロワーのアカウントIDを取得する。
アカウントIDは固有の数字(例: 12345)
これを用いて、2アカウントのフォロワーの重複を調べることが可能である。

## 使用パッケージ
### python3
* requests_oauthlib
https://github.com/requests/requests-oauthlib

### R
* venneuler

## フォルダ構成

* download
* DLusers

### download/
データ入手用ツール群。
主に、アカウントIDの取得に使用する。

#### DLids/
フォロワーidを取得するためのディレクトリ。
以下、内容を順を追って説明する。

##### getIds.py
メインプログラム。

フォロワーIDを取得する。

##### config.py
設定ファイル。

developer.twitter.comを通して得た、開発者向けの認証キーをここで設定する。
```
CONSUMER_KEY        = 'XXXXXXXXXX'
CONSUMER_SECRET     = 'XXXXXXXXXX'
ACCESS_TOKEN        = 'XXXXXXXXXX'
ACCESS_TOKEN_SECRET = 'XXXXXXXXXX'
```
参考)[ツイッターの開発者ブログ](https://blog.twitter.com/developer/ja_jp/topics/tools/2018/jp-new-developer-requirements-to-protect-our-platform.html)

##### screen_name.txt
設定ファイル。

ここでscreen_nameを設定して、getIds.pyで読み込む。

例えば、ツイッター公式([@TwitterJP](https://twitter.com/twitterjp))と
ツイッターAPI([@TwitterAPI](https://twitter.com/TwitterAPI))なら、ファイルの中身は以下のようになる。
```
TwitterJP
TwitterAPI
```

##### ids/
出力先フォルダ。

中に、{screen_name}.txtの形で出力される。

例えば、screen_nameが[TwitterJP](https://twitter.com/twitterjp)なら、
出力ファイルはTwitterJP.txt

#### DLusers/
フォロワーidを取得するためのディレクトリ。
以下、内容を順を追って説明する。

##### getUsers.py
メインプログラム。

##### screen_name.txt
設定ファイル。

ここで設定したscreen_nameのユーザー情報をgetUsers.pyで取得する。

##### update_scName.sh
screen_name.txt を、 DLids/ を参照して更新する。

##### key_list.txt
設定ファイル。

ここで設定したパラメータを外部ファイルに出力する。

どんなパラメータがあるか、公式ドキュメントが確認できない(2019/1/14)。
知りたい方はメインプログラム内でブレーク貼って調べて...

以下、例。

```
screen_name
name
id
```

##### config.py
設定ファイル。

##### users.csv
出力ファイル。

### visualize/
可視化のためのディレクトリ。
以下、内容を順を追って説明する。

#### plot.r
メインプログラム。

得たデータから、ベン図を作成する。
これにより、複数アカウント間のフォロワーの重複を調べる。

調べるアカウントを変更する場合は、ソースを変更しなければならない。

#### users.csv
設定ファイル。

グラフのラベルに使用されている。

#### ids/
データファイルの保存ディレクトリ。

リンクにした方が良いのかもしれない。
