class Primitive_Bool_v_0():
    def __init__(self, value):
        self.value = value
        __vt_init__(self)
    
    def __repr__(self):
        return f"{self.value}"
    
    # 検査 & VT書き換えを加える
    def __eq__(left,right):
        return left.binary(right,"eq")
    def __ne__(left,right):
        return left.binary(right,"ne")
    def __and__(left,right):
        return left.binary(right,"and")
    def __or__(left,right):
        return left.binary(right,"or")
    
    def binary(left,right,op):
        checkCompatibility(left,right)
        match op:
            # 論理
            case "and": result = Primitive_Bool_v_0(left.value & right.value)
            case "or": result = Primitive_Bool_v_0(left.value | right.value)
            # 比較
            case "eq": result = Primitive_Bool_v_0(left.value == right.value)
            case "ne": result = Primitive_Bool_v_0(left.value != right.value)
        append(result,left)
        append(result,right)
        return result
    