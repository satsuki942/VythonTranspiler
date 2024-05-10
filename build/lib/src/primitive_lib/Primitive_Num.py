class Primitive_Num():
    def __init__(self, value):
        self.value = value
    def __add__(left,right):
        # 検査 & VT書き換えを加える
        result = left.value + right.value
        return Primitive_Num(result)
    def __eq__(left,right):
        result = left.value == right.value
        return Primitive_Bool(result)

