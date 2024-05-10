import ast
from lark import Token, Transformer, Tree
import copy

global_func_paths = {"src/lib/global_func/global_func.py"}
calling_vt_init_path = "src/lib/helper_func/__calling_vt_init__.py"
calling_vt_append_path = "src/lib/helper_func/__calling_vt_append__.py"
# checking_compatibility_path = ""

primitive_classes = {"src/primitive_lib/Primitive_Bool.py","src/primitive_lib/Primitive_String.py","src/primitive_lib/Primitive_Number.py"}

# larkToIRを参考に実装する
class Transpiler(Transformer):
    def __init__(self, debug_mode=False):
        # 今の所使ってない
        self.debug_mode = debug_mode
            
        # Python ASTに挿入するグローバル関数(VT操作/検査)をASTに変換
        global_func_asts = set()
        for global_func_path in global_func_paths:
            with open(global_func_path,"r") as file:
                global_func_code = file.read()
            global_func_asts.add(ast.parse(global_func_code))
        # トランスパイラインスタンスの属性として保持
        self.global_func_asts = global_func_asts

        # 各メソッド、演算定義の前後に挿入されるヘルパ関数の呼び出しをASTに変換
        # VT初期化関数の呼び出し
        with open(calling_vt_init_path,"r") as file:
            calling_vt_init_code = file.read()
        self.calling_vt_init_ast = ast.parse(calling_vt_init_code).body
        # VT検査関数の呼び出し
        # with open(checking_compatibility_path, "r") as file:
        #   checking_compatibility_code = file.read()
        # self.checking_compatibility_ast = ast.parse(checking_compatibility_code)
        # VT結合関数の呼び出し
        with open(calling_vt_append_path,"r") as file:
            calliing_vt_append_code = file.read()
        self.calling_vt_append_ast = ast.parse(calliing_vt_append_code).body[0]

        # Primitiveクラスの定義をASTに変換
        primitive_class_asts = set()
        for primitive_class in primitive_classes:
            with open(primitive_class,"r") as file:
                primitive_class_code = file.read()
            primitive_class_asts.add(ast.parse(primitive_class_code))
        # トランスパイラインスタンスの属性として保持
        self.primitive_class_asts = primitive_class_asts

    def file_input(self, items):
        body = self._flatten_list(items)
        # Primitiveクラスを挿入
        for primitive_class_ast in self.primitive_class_asts:
            body.insert(0,primitive_class_ast)
        # グローバル関数を挿入: デバッグのため現在はoffにしている
        for global_func_ast in self.global_func_asts:
            body.insert(0,global_func_ast)

        return ast.Module(body=body,type_ignores=[])

    def classdef(self, items):
        name, version, bases, body = items[0], items[1], [], self._flatten_list(items[3:])
        # バージョンの情報もクラス名が持つ
        class_name = str(name) + "_v_" + str(version)

        wrapped_func_list = []
        # basesの中身を検査
        for element in body:
            if isinstance(element,ast.FunctionDef):
                # initializeメソッドAST に VT初期化関数呼び出しAST を挿入
                if(element.name == "__init__"):
                    element.body.append(self.calling_vt_init_ast)
                # メソッドをラップし、VT書き換え関数呼び出しASTを挿入した新しいメソッドASTに変更する
                else:
                    new_method_ast = self.calling_vt_append_ast
                    wrap_func_name = element.name
                    wrapped_func_name = "__wrapped_" + wrap_func_name + "__"
                    formal_args = element.args.args
                    # wrapメソッドのASTを作成
                    new_method_ast.name = wrap_func_name
                    new_method_ast.args = element.args
                    actual_args = []
                    for formal_arg in formal_args:
                        actual_args.append(ast.Name(id=formal_arg.arg,ctx=ast.Load()))
                    new_method_ast.body[0].value.func.attr = wrapped_func_name
                    new_method_ast.body[0].value.args = [actual_args[1]]
                    new_method_ast.body[1].value.args[1]=actual_args[0]
                    # wrappedメソッドのASTを変更
                    element.name = wrapped_func_name
                    # wrapメソッドの配置
                    wrapped_func_list.append(new_method_ast)

        for element in wrapped_func_list:
            body.append(element)

        return ast.ClassDef(name=class_name,bases=[],keywords=[],body=body,decorator_list=[],type_params=[],lineno=0,col_offset=0,end_lineno=0,end_col_offset=0)
    
    def assign_stmt(self, items):
        assign_tree = items[0]
        targets = assign_tree.children[0]
        value = assign_tree.children[1]

        transformed_targets = (
            self.transform(targets) if isinstance(targets, Tree) else targets
        )
        transformed_value = self.transform(value) if isinstance(value, Tree) else value

        return ast.Assign(targets=[transformed_targets], value=transformed_value,lineno=0,col_offset=0,end_lineno=0,end_col_offset=0)

    def expr_stmt(self, items):
        value = items[0]
        transformed_value = self.transform(value) if isinstance(value, Tree) else value
        return ast.Expr(value=transformed_value,lineno=0,col_offset=0,end_lineno=0,end_col_offset=0)
    
    # primitiveを含むASTの変換(新)
    def const_true(self, items):
        value = ast.Constant(True,lineno=0,col_offset=0,end_lineno=0,end_col_offset=0)
        return ast.Call(ast.Name(id="Primitive_Bool_v_0",ctx=ast.Load()),[value],[],lineno=0,col_offset=0,end_lineno=0,end_col_offset=0)
    
    def const_false(self, items):
        value = ast.Constant(False,lineno=0,col_offset=0,end_lineno=0,end_col_offset=0)
        return ast.Call(ast.Name(id="Primitive_Bool_v_0",ctx=ast.Load()),[value],[],lineno=0,col_offset=0,end_lineno=0,end_col_offset=0)
    
    def string(self, items):
        value = items[0]
        transformed_value = self.transform(value) if isinstance(value, Tree) else value
        transformed_value = ast.Constant(transformed_value.value,lineno=0,col_offset=0,end_lineno=0,end_col_offset=0)
        return ast.Call(ast.Name(id="Primitive_String_v_0",ctx=ast.Load()),[transformed_value],[],lineno=0,col_offset=0,end_lineno=0,end_col_offset=0)
    
    def number(self, items):
        value = items[0]
        transformed_value = self.transform(value) if isinstance(value, Tree) else value
        transformed_value = ast.Constant(float(transformed_value.value),lineno=0,col_offset=0,end_lineno=0,end_col_offset=0)
        return ast.Call(ast.Name(id="Primitive_Number_v_0",ctx=ast.Load()),[transformed_value],[],lineno=0,col_offset=0,end_lineno=0,end_col_offset=0)

    def comp_op(self, items):
        value = items[0]
        transformed_value = self.transform(value) if isinstance(value, Tree) else value
        match transformed_value:
            case "==":
                transformed_op = ast.Eq()
            case "!=":
                transformed_op = ast.NotEq()
            case ">":
                transformed_op = ast.Gt()
            case "<":
                transformed_op = ast.Lt()
            case "<=":
                transformed_op = ast.LtE()
            case ">=":
                transformed_op = ast.GtE()
        return transformed_op

    def comparison(self, items):
        # 要素数が適切かどうかのチェック
        size = len(items)
        if(size%2==0 | size<3):
            raise TypeError("Vython->Python: Inappropriate form of comparison")
        
        value_left = items[0]
        transformed_value_l = self.transform(value_left) if isinstance(value_left, Tree) else value_left
        transformed_ops = []
        transformed_comparators = []
        for i in range(1, size):
            if i%2==1:
                op = items[i]
                transformed_op = self.transform(op) if isinstance(op, Tree) else op
                transformed_ops.append(transformed_op)
            else:
                comparator = items[i]
                transformed_comparator = self.transform(comparator) if isinstance(comparator, Tree) else comparator
                transformed_comparators.append(transformed_comparator)
        return ast.Compare(left=transformed_value_l,ops=transformed_ops,comparators=transformed_comparators,lineno=0,col_offset=0,end_lineno=0,end_col_offset=0)
    
    def or_expr(self, items):
        value_left = items[0]
        value_right = items[1]
        transformed_value_l = self.transform(value_left) if isinstance(value_left, Tree) else value_left
        transformed_value_r = self.transform(value_right) if isinstance(value_right, Tree) else value_right
        transformed_values = [transformed_value_l,transformed_value_r]
        return ast.BoolOp(op=ast.Or(), values=transformed_values,lineno=0,col_offset=0,end_lineno=0,end_col_offset=0)
    
    def and_expr(self, items):
        value_left = items[0]
        value_right = items[1]
        transformed_value_l = self.transform(value_left) if isinstance(value_left, Tree) else value_left
        transformed_value_r = self.transform(value_right) if isinstance(value_right, Tree) else value_right
        transformed_values = [transformed_value_l,transformed_value_r]
        return ast.BoolOp(op=ast.And(), values=transformed_values,lineno=0,col_offset=0,end_lineno=0,end_col_offset=0)

    def arith_expr(self, items):
        value_left = items[0]
        op = items[1]
        value_right = items[2]
        transformed_value_l = self.transform(value_left) if isinstance(value_left, Tree) else value_left
        transformed_value_r = self.transform(value_right) if isinstance(value_right, Tree) else value_right
        transformed_op = self.transform(op) if isinstance(op, Tree) else op
        match transformed_op:
            case "+": transformed_op = ast.Add()
            case "-": transformed_op = ast.Sub()
        return ast.BinOp(transformed_value_l,transformed_op,transformed_value_r,lineno=0,col_offset=0,end_lineno=0,end_col_offset=0)

    def term(self, items):
        value_left = items[0]
        op = items[1]
        value_right = items[2]
        transformed_value_l = self.transform(value_left) if isinstance(value_left, Tree) else value_left
        transformed_value_r = self.transform(value_right) if isinstance(value_right, Tree) else value_right
        transformed_op = self.transform(op) if isinstance(op, Tree) else op
        match transformed_op:
            case "*": transformed_op = ast.Mult()
            case "/": transformed_op = ast.Div()
            case "%": transformed_op = ast.Mod()
            case "//": transformed_op = ast.FloorDiv()
        return ast.BinOp(transformed_value_l,transformed_op,transformed_value_r,lineno=0,col_offset=0,end_lineno=0,end_col_offset=0)
    
    def factor(self, items):
        value_left = items[0]
        value_right = items[1]
        transformed_value_l = self.transform(value_left) if isinstance(value_left, Tree) else value_left
        transformed_value_r = self.transform(value_right) if isinstance(value_right, Tree) else value_right
        if(transformed_value_l == "+"):
            op = ast.UAdd()
        else:
            op = ast.USub()
        return ast.UnaryOp(op,transformed_value_r,lineno=0,col_offset=0,end_lineno=0,end_col_offset=0)

    def old_transform():
        return
        # primitiveを含むASTの変換(旧)
        # def const_true(self, items):
        #     return ast.Constant(True,lineno=0,col_offset=0,end_lineno=0,end_col_offset=0)
        
        # def const_false(self, items):
        #     return ast.Constant(False,lineno=0,col_offset=0,end_lineno=0,end_col_offset=0)
        
        # def string(self, items):
        #     value = items[0]
        #     transformed_value = self.transform(value) if isinstance(value, Tree) else value
        #     return ast.Constant(transformed_value.value,lineno=0,col_offset=0,end_lineno=0,end_col_offset=0)
        
        # def number(self, items):
        #     value = items[0]
        #     transformed_value = self.transform(value) if isinstance(value, Tree) else value
        #     return ast.Constant(float(transformed_value.value),lineno=0,col_offset=0,end_lineno=0,end_col_offset=0)

        # def comp_op(self, items):
        #     value = items[0]
        #     transformed_value = self.transform(value) if isinstance(value, Tree) else value
        #     match transformed_value:
        #         case "==":
        #             transformed_op = ast.Eq()
        #         case "!=":
        #             transformed_op = ast.NotEq()
        #         case ">":
        #             transformed_op = ast.Gt()
        #         case "<":
        #             transformed_op = ast.Lt()
        #         case "<=":
        #             transformed_op = ast.LtE()
        #         case ">=":
        #             transformed_op = ast.GtE()
        #     return transformed_op

        # def comparison(self, items):
        #     # 要素数が適切かどうかのチェック
        #     size = len(items)
        #     if(size%2==0 | size<3):
        #         raise TypeError("Vython->Python: Inappropriate form of comparison")
            
        #     value_left = items[0]
        #     transformed_value_l = self.transform(value_left) if isinstance(value_left, Tree) else value_left
        #     transformed_ops = []
        #     transformed_comparators = []
        #     for i in range(1, size):
        #         if i%2==1:
        #             op = items[i]
        #             transformed_op = self.transform(op) if isinstance(op, Tree) else op
        #             transformed_ops.append(transformed_op)
        #         else:
        #             comparator = items[i]
        #             transformed_comparator = self.transform(comparator) if isinstance(comparator, Tree) else comparator
        #             transformed_comparators.append(transformed_comparator)
        #     return ast.Compare(left=transformed_value_l,ops=transformed_ops,comparators=transformed_comparators,lineno=0,col_offset=0,end_lineno=0,end_col_offset=0)
        
        # def or_expr(self, items):
        #     value_left = items[0]
        #     value_right = items[1]
        #     transformed_value_l = self.transform(value_left) if isinstance(value_left, Tree) else value_left
        #     transformed_value_r = self.transform(value_right) if isinstance(value_right, Tree) else value_right
        #     transformed_values = [transformed_value_l,transformed_value_r]
        #     return ast.BoolOp(op=ast.Or(), values=transformed_values,lineno=0,col_offset=0,end_lineno=0,end_col_offset=0)
        
        # def and_expr(self, items):
        #     value_left = items[0]
        #     value_right = items[1]
        #     transformed_value_l = self.transform(value_left) if isinstance(value_left, Tree) else value_left
        #     transformed_value_r = self.transform(value_right) if isinstance(value_right, Tree) else value_right
        #     transformed_values = [transformed_value_l,transformed_value_r]
        #     return ast.BoolOp(op=ast.And(), values=transformed_values,lineno=0,col_offset=0,end_lineno=0,end_col_offset=0)

        # def arith_expr(self, items):
        #     value_left = items[0]
        #     op = items[1]
        #     value_right = items[2]
        #     transformed_value_l = self.transform(value_left) if isinstance(value_left, Tree) else value_left
        #     transformed_value_r = self.transform(value_right) if isinstance(value_right, Tree) else value_right
        #     transformed_op = self.transform(op) if isinstance(op, Tree) else op
        #     match transformed_op:
        #         case "+": transformed_op = ast.Add()
        #         case "-": transformed_op = ast.Sub()
        #     return ast.BinOp(transformed_value_l,transformed_op,transformed_value_r,lineno=0,col_offset=0,end_lineno=0,end_col_offset=0)

        # def term(self, items):
        #     value_left = items[0]
        #     op = items[1]
        #     value_right = items[2]
        #     transformed_value_l = self.transform(value_left) if isinstance(value_left, Tree) else value_left
        #     transformed_value_r = self.transform(value_right) if isinstance(value_right, Tree) else value_right
        #     transformed_op = self.transform(op) if isinstance(op, Tree) else op
        #     match transformed_op:
        #         case "*": transformed_op = ast.Mult()
        #         case "/": transformed_op = ast.Div()
        #         case "%": transformed_op = ast.Mod()
        #         case "//": transformed_op = ast.FloorDiv()
        #     return ast.BinOp(transformed_value_l,transformed_op,transformed_value_r,lineno=0,col_offset=0,end_lineno=0,end_col_offset=0)
        
        # def factor(self, items):
        #     value_left = items[0]
        #     value_right = items[1]
        #     transformed_value_l = self.transform(value_left) if isinstance(value_left, Tree) else value_left
        #     transformed_value_r = self.transform(value_right) if isinstance(value_right, Tree) else value_right
        #     if(transformed_value_l == "+"):
        #         op = ast.UAdd()
        #     else:
        #         op = ast.USub()
        #     return ast.UnaryOp(op,transformed_value_r,lineno=0,col_offset=0,end_lineno=0,end_col_offset=0)

    # elifにはまだ対応していない
    def if_stmt(self, items):
        test = items[0]
        then_body = items[1]
        elifs = items[2]
        else_body = items[3]
        transformed_test = self.transform(test) if isinstance(test, Tree) else test
        transformed_then_body = self.transform(then_body) if isinstance(then_body, Tree) else then_body
        transformed_elifs = self.transform(elifs) if isinstance(elifs, Tree) else elifs
        transformed_else_body = self.transform(else_body) if isinstance(else_body, Tree) else else_body
        return ast.If(transformed_test,transformed_then_body,transformed_else_body,lineno=0,col_offset=0,end_lineno=0,end_col_offset=0)

    def funccall(self, items):
        func, args = items[0], self._flatten_list(items[1:])
        transformed_func = self.transform(func) if isinstance(func, Tree) else func
        return ast.Call(func=transformed_func,args=args,keywords=[],lineno=0,col_offset=0,end_lineno=0,end_col_offset=0)
    
    def funccallwithversion(self, items):
        func, version, args = items[0], items[1], self._flatten_list(items[2:])

        # バージョンの情報もクラス名が持つ
        if isinstance(func,ast.Name):
            func.id = func.id + "_v_" + str(version)
        else:
            raise TypeError("syntax error")
        
        return ast.Call(func=func,args=args,keywords=[],lineno=0,col_offset=0,end_lineno=0,end_col_offset=0)
    
    def version(self, items):
        number = items[0][0]
        return str(number)

    def getattr(self, items):
        value, attr = items[0], items[1]
        transformed_value = self.transform(value) if isinstance(value, Tree) else value
        transformed_attr = self.transform(attr) if isinstance(attr, Tree) else attr
        return ast.Attribute(value=transformed_value, attr=transformed_attr,lineno=0,col_offset=0,end_lineno=0,end_col_offset=0)
    
    def arguments(self, items):
        args = []
        for item in items:
            if isinstance(item, Tree):
                args.append(self.transform(item))
            else:
                args.append(item)
        return args
    
    def var(self, items):
        id = items[0]
        return ast.Name(id=id,ctx=ast.Load(),lineno=0,col_offset=0,end_lineno=0,end_col_offset=0)
    
    def name(self, items):
        id = items[0].value
        return str(id)
    
    def suite(self, items):
        return self._flatten_list(items)

    def parameters(self, items):
        args = []
        for item in items:
            if item is not None:
                args.append(ast.arg(item,lineno=0,col_offset=0,end_lineno=0,end_col_offset=0))
        return ast.arguments(posonlyargs=[],args=args,kwonlyargs=[],kw_defaults=[],defaults=[])

    def funcdef(self, items):
        name, params_tree, _, body = items
        # 'params_tree' が Tree オブジェクトの場合
        if isinstance(params_tree, Tree):
            # params_treeの子ノードから引数を取得
            args = [self.transform(param) for param in params_tree.children]
        else:
            # params_treeがリストでない場合、空の引数リストを設定
            args = params_tree
        return ast.FunctionDef(name=name, args=args, body=self._flatten_list(body),decorator_list=[],type_params=[],lineno=0,col_offset=0,end_lineno=0,end_col_offset=0)

    def return_stmt(self, items):
        value_item = items[0]
        value = (
            self.transform(value_item) if isinstance(value_item, Tree) else value_item
        )
        return ast.Return(value=value,lineno=0,col_offset=0,end_lineno=0,end_col_offset=0)

    def pass_stmt(self, _):
        return ast.Pass(lineno=0,col_offset=0,end_lineno=0,end_col_offset=0)

    # 適切か怪しい
    def const_none(self, _):
        return ast.Constant(None,lineno=0,col_offset=0,end_lineno=0,end_col_offset=0)

    # _flatten_list メソッドの定義
    def _flatten_list(self, l):
        flattened = []
        for item in l:
            if isinstance(item, list):
                flattened.extend([subitem for subitem in item if subitem is not None])
            elif isinstance(item, Tree):
                flattened.append(item)
            elif item is not None:
                flattened.append(item)
        return flattened
