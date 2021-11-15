# get-manaba

[Click here for English README](README.md)

[manaba](https://manaba.jp)のさまざまな情報を取得するためのライブラリです。

## アナウンス

- このライブラリは開発者が所属する大学内サービスを運用することを主目的として作られています。他の大学では上手く利用できない可能性がありますのでご注意ください。
- このライブラリの開発者が所属する大学が 2022 年から manaba を利用しなくなります。これに伴い、2022 年 4 月を持ってこのライブラリのサポートは打ち切られ、アーカイブされます。

## 警告および免責事項

- **開発者は、このプロジェクト・ライブラリを使用したことによる問題について一切の責任を負いません。自己責任で利用ください。**
- このライブラリを使用して短時間に多くのリクエストを発行しないでください。

## ドキュメント

- [get-manaba ドキュメント](https://book000.github.io/get-manaba/)

## 要件

- manaba (Tested with `manaba 2.96`)
- Python 3.9+
- [requirements.txt](requirements.txt): `requests`, `beautifulsoup4`

## インストール

PyPI からインストールするか、リポジトリをクローンしてインストールする方法の二つがあります。

### PyPI からインストールする

1. PyPI から get-manaba をインストールする: `pip install -U get-manaba`

## リポジトリをクローンしてインストールする

1. GitHub リポジトリからクローンする: `git clone https://github.com/book000/get-manaba.git`
2. `requirements.txt` から依存パッケージをインストールする: `pip3 install -U -r requirements.txt`
3. get-manaba パッケージをインストールする: `pip install .`

## ライセンス

このプロジェクトのライセンスは [MIT License](LICENSE) です。
