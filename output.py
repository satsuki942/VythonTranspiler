# [Unparse Python AST]
import re

def re_match(self):
    cn = self.__class__.__name__
    pattern = '([A-Za-z_0-9]+)_v_([0-9]+)'
    matchRe = re.fullmatch(pattern, cn)
    if matchRe:
        class_name = matchRe[1]
        version_number = matchRe[2]
        return (class_name, version_number)
    else:
        raise TypeError('Inappropriate Class Name')

def __vt_init__(self):
    self.vt = []
    cv_pair = re_match(self)
    self.vt.append((cv_pair[0], cv_pair[1], False))
    return

def checkCompatibility(left, right):
    for x in left.vt:
        if x[2]:
            print('debug')
            c = x[0]
            v = x[1]
            for y in right.vt:
                if y[0] == c and y[1] != v:
                    raise TypeError(f'Inconsistent Version Usage:\nComparing {c}!{v} and {c}!{y[1]} values')
    for y in right.vt:
        if y[2]:
            c = y[0]
            v = y[1]
            for x in left.vt:
                if (x[0] == c) & (x[1] != v):
                    raise TypeError(f'Inconsistent Version Usage:\nComparing {c}!{x[1]} and {c}!{v} values')
    return

def is_include(left, c, v, b):
    for x in left:
        if (x[0] == c) & (x[1] == v) & (x[2] == b):
            return True
    return False

def insert(value, c, v, b):
    for x in value.vt:
        if x[0] == c and x[1] == v:
            value.vt.remove(x)
        value.vt.append((c, v, b))
    return

def append(left, right):
    left.vt
    right.vt
    for x in left.vt:
        cx = x[0]
        vx = x[1]
        bx = x[2]
        if is_include(right.vt, cx, vx, bx):
            left.vt.remove(x)
    for y in right.vt:
        left.vt.append(y)
    return

def incompat(self, value):
    cv_pair = re_match(self)
    insert(value, cv_pair[0], cv_pair[1], True)
    return

class Primitive_Bool_v_0:

    def __init__(self, value):
        self.value = value
        __vt_init__(self)

    def __repr__(self):
        return f'{self.value}'

    def equal(left, right):
        return left.value == right.value

    def nequal(left, right):
        return left.value != right.value

    def __eq__(left, right):
        return left.binary(right, 'eq')

    def __ne__(left, right):
        return left.binary(right, 'ne')

    def __and__(left, right):
        return left.binary(right, 'and')

    def __or__(left, right):
        return left.binary(right, 'or')

    def binary(left, right, op):
        checkCompatibility(left, right)
        match op:
            case 'and':
                result = Primitive_Bool_v_0(left.value & right.value)
            case 'or':
                result = Primitive_Bool_v_0(left.value | right.value)
            case 'eq':
                result = Primitive_Bool_v_0(left.value == right.value)
            case 'ne':
                result = Primitive_Bool_v_0(left.value != right.value)
        append(result, left)
        append(result, right)
        return result

class Primitive_Number_v_0:

    def __init__(self, value):
        self.value = value
        __vt_init__(self)

    def __repr__(self):
        return f'{self.value}'

    def equal(left, right):
        return left.value == right.value

    def nequal(left, right):
        return left.value != right.value

    def __add__(left, right):
        return left.binary(right, 'add')

    def __sub__(left, right):
        return left.binary(right, 'sub')

    def __mul__(left, right):
        return left.binary(right, 'mul')

    def __div__(left, right):
        return left.binary(right, 'div')

    def __floordiv__(left, right):
        return left.binary(right, 'floordiv')

    def __mod__(left, right):
        return left.binary(right, 'mod')

    def __eq__(left, right):
        return left.binary(right, 'eq')

    def __ne__(left, right):
        return left.binary(right, 'ne')

    def __lt__(left, right):
        return left.binary(right, 'lt')

    def __gt__(left, right):
        return left.binary(right, 'gt')

    def __le__(left, right):
        return left.binary(right, 'le')

    def __ge__(left, right):
        return left.binary(right, 'ge')

    def __and__(left, right):
        return left.binary(right, 'and')

    def __or__(left, right):
        return left.binary(right, 'or')

    def binary(left, right, op):
        checkCompatibility(left, right)
        match op:
            case 'add':
                result = Primitive_Number_v_0(left.value + right.value)
            case 'sub':
                result = Primitive_Number_v_0(left.value - right.value)
            case 'mul':
                result = Primitive_Number_v_0(left.value * right.value)
            case 'div':
                result = Primitive_Number_v_0(left.value / right.value)
            case 'mod':
                result = Primitive_Number_v_0(left.value % right.value)
            case 'floordiv':
                result = Primitive_Number_v_0(left.value // right.value)
            case 'and':
                result = Primitive_Bool_v_0(left.value & right.value)
            case 'or':
                result = Primitive_Bool_v_0(left.value | right.value)
            case 'eq':
                result = Primitive_Bool_v_0(left.value == right.value)
            case 'ne':
                result = Primitive_Bool_v_0(left.value != right.value)
            case 'lt':
                result = Primitive_Bool_v_0(left.value < right.value)
            case 'gt':
                result = Primitive_Bool_v_0(left.value > right.value)
            case 'le':
                result = Primitive_Bool_v_0(left.value <= right.value)
            case 'ge':
                result = Primitive_Bool_v_0(left.value >= right.value)
        append(result, left)
        append(result, right)
        return result

class Primitive_String_v_0:

    def __init__(self, value):
        self.value = value
        __vt_init__(self)

    def __repr__(self):
        return f'{self.value}'

    def equal(left, right):
        return left.value == right.value

    def nequal(left, right):
        return left.value != right.value

    def __add__(left, right):
        return left.binary(right, 'add')

    def __eq__(left, right):
        return left.binary(right, 'eq')

    def __ne__(left, right):
        return left.binary(right, 'ne')

    def __lt__(left, right):
        return left.binary(right, 'lt')

    def __gt__(left, right):
        return left.binary(right, 'gt')

    def __le__(left, right):
        return left.binary(right, 'le')

    def __ge__(left, right):
        return left.binary(right, 'ge')

    def __and__(left, right):
        return left.binary(right, 'and')

    def __or__(left, right):
        return left.binary(right, 'or')

    def binary(left, right, op):
        checkCompatibility(left, right)
        match op:
            case 'add':
                result = Primitive_String_v_0(left.value + right.value)
            case 'and':
                result = Primitive_Bool_v_0(left.value & right.value)
            case 'or':
                result = Primitive_Bool_v_0(left.value | right.value)
            case 'eq':
                result = Primitive_Bool_v_0(left.value == right.value)
            case 'ne':
                result = Primitive_Bool_v_0(left.value != right.value)
            case 'lt':
                result = Primitive_Bool_v_0(left.value < right.value)
            case 'gt':
                result = Primitive_Bool_v_0(left.value > right.value)
            case 'le':
                result = Primitive_Bool_v_0(left.value <= right.value)
            case 'ge':
                result = Primitive_Bool_v_0(left.value >= right.value)
        append(result, left)
        append(result, right)
        return result

class A_v_1:

    def __init__(self, value):
        self.value = value
        __vt_init__(self)

class A_v_2:

    def __init__(self, value):
        self.value = value
        __vt_init__(self)
a1 = A_v_1(Primitive_Number_v_0(1.0))
a2 = A_v_2(Primitive_Number_v_0(3.0))
print(Primitive_String_v_0('"hi"'))
print(a1.value + a2.value)