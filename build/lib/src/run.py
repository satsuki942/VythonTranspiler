import sys
import time
import ast
from src.vython_parser import Parser
from src.transpiler import Transpiler
from src.compiler import Compiler

def execute_phase(message, function):
    start_time = time.time()
    function()
    end_time = time.time()
    print(message)
    print(f"  --> Completed in {end_time-start_time:.4f} seconds")

def main():
    debug_mode = False
    show_ast = False
    transpile_mode = False
    file_path = None

    # コマンドライン引数の処理
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


    # # Vython ASTをLarkで作成したParserを用いて生成        
    # start = time.time()
    # vythonTree = Parser(debug_mode = False).parse(code)
    # end = time.time()
    # generate_vythonTree_time = end - start

    # # 生成したVython ASTをPython ASTに変換
    # start = time.time()
    # pythonTree = Transpiler(debug_mode, transpile_mode).transform(vythonTree)
    # end = time.time()
    # transpile_vythonTree_time = end - start

    # # Python ASTをPythonプログラムにUnparse
    # start = time.time()
    # pythonProgram = ast.unparse(pythonTree)
    # end = time.time()
    # unparse_pythonTree_time = end - start

    # # 結果をtmp.log/output.pyに表示
    # with open('output.py', 'w') as log:
    #     print("# [Unparse Python AST]",file=log)
    #     print(pythonProgram,file=log)
        
    # with open('tmp.log', 'w') as log:
    #     print(f"[step1] Generating vythonAST: {generate_vythonTree_time:.4f} seconds",file=log)
    #     print(f"{vythonTree}",file=log)
    #     print("",file=log)

    #     print(f"[step2] Transpiling vythonAST to PythonAST: {transpile_vythonTree_time:.4f} seconds",file=log)
    #     print("",file=log)

    #     print(f"[step3] Unparsing PythonAST: {unparse_pythonTree_time:.4f} seconds",file=log)
    #     print("",file=log)

    #      # Python Programの実行
    #     start = time.time()
    #     exec(pythonProgram,globals())
    #     end = time.time()
    #     executing_pythonProgram_time = end - start

    #     print(f"[step4] Execute Python Program: {executing_pythonProgram_time:.4f} seconds",file=log)
    #     print("",file=log)

    #     if show_ast:
    #         print("[Python AST]: ",file=log)
    #         print(ast.dump(pythonTree,False,indent=4),file=log)
