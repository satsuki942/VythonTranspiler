import time
import ast
from src.vython_parser import Parser
from src.transpiler import Transpiler

class Compiler:
    def __init__(self, vythonCode, transpile_mode, show_ast, debug_mode=False, ):
        self.debug_mode = debug_mode
        self.show_ast = show_ast
        self.transpile_mode = transpile_mode
        self.vythonCode = vythonCode
        self.vythonaAST = None
        self.pythonAST = None
        self.pythonCode = None
        self.result = None
    
    def parse(self):
        if self.debug_mode:
            print(f"File Content:\n{self.vythonCode}")
        self.vythonaAST = Parser(debug_mode = False).parse(self.vythonCode)
        if self.debug_mode:
            print(self.vythonaAST)
    
    def transpile(self):
        self.pythonAST = Transpiler(self.debug_mode, self.transpile_mode).transform(self.vythonaAST)
        if self.show_ast:
            print(ast.dump(self.pythonAST,False,indent=4))

    def unparse(self):
        self.pythonCode = ast.unparse(self.pythonAST)
        if self.debug_mode:
            with open('output.py', 'w') as log:
                print("# [Unparse Python AST]",file=log)
                print(self.pythonCode, file=log)

    def execute(self):
        exec(self.pythonCode,globals())
