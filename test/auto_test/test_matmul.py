from src.compiler import Compiler

def test():
    # テスト用のソースコードを読み込む
    with open("test/sample/basic/matmul.py", "r") as f:
        code = f.read()

    # コンパイラのインスタンスを作成し、実行
    result = Compiler(code,False,False).get_result_fullpath()
    assert result == "79\n"
