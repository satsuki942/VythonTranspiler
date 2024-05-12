How to Install/Run

## vythonトランスパイラのインストール。
    - プロジェクトルートで以下を実行
```sh
pip install .
```
## コンパイル & 実行
`vythonT` で `test/sample.py` をコンパイル・実行するには、以下を実行してください。
```sh
vythonT test/sample.py
```

`vython` コンパイラはオプションで詳細な情報を出力可能です。

```sh
vython --debug test/sample.py # tmp.logにログを出力 / output.pyにunparseしたpythonプログラムを出力
vython -d test/sample.py
```

```sh
vython --ast test/sample.py # tmp.logにPython ASTを出力
```

```sh
vython --wo test/sample.py # 値にVersion情報を付加しないPythonプログラムASTにトランスパイルして実行する
```
