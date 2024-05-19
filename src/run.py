import sys
import time
from src.compiler import Compiler

class CommandError(Exception):
    pass

def execute_phase(message, function):
    start_time = time.time()
    function()
    end_time = time.time()
    print(message)
    print(f"  --> Completed in {end_time-start_time:.4f} seconds")

def main():
    execute_mode = None
    debug_mode = False
    show_ast = False
    transpile_mode = False
    file_path = None

    # コマンドライン引数の処理
    # 統合したら...
        # index = 0 - vython
        # index = 1 - 実行モード T(ranspile),I(nterpret),Other..
        # としたい
    execute_mode = "vythonT"
    try:
        if execute_mode == "vythonT":
            for arg in sys.argv[1:]:
                if arg in ["--debug", "-d"]:
                    debug_mode = True
                elif arg == "--ast":
                    show_ast = True
                elif arg == "--wo":
                    transpile_mode = True
                else:
                    if file_path is not None:
                        print("Too many arguments. Please specify only one file name.")
                        sys.exit(1)
                    file_path = arg
        elif execute_mode == "test":
            for arg in sys.argv[1:]:
                pass
        # elif execute_mode == "vython":
        #     pass
        else:
            raise CommandError(f"Unknown command: {execute_mode}")
    except CommandError as e:
        print(f"Error: {e}")
        sys.exit(1)

    # execute_modeに従った実行を行う
    if execute_mode == "vythonT":
        # 変換するコードを取得
        try:
            with open(file_path, "r") as file:
                code = file.read()
        except FileNotFoundError:
            print(f"The specified file '{file_path}' was not found.")
            sys.exit(1)
        except Exception as e:
            print(f"An error occurred while opening the file: {e}")
            sys.exit(1)

        compiler = Compiler(code, transpile_mode, show_ast, debug_mode)

        # 各フェーズの実行
        execute_phase("[Phase 1] Prase to lark-vython AST", lambda: compiler.parse())
        execute_phase("[Phase 2] Transpile lark-vython AST to Python AST", lambda: compiler.transpile())
        execute_phase("[Phase 3] Unparse Python AST", lambda: compiler.unparse())
        execute_phase("[Phase 4] Execution", lambda: compiler.execute())
        print(f"[Result]:\n{compiler.get_result()}")
