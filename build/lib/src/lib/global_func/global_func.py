import re

def __vt_init__(self):
    self.vt = []
    cn = self.__class__.__name__

    # 正規表現パターン
    # 不正確
    pattern = r'([A-Za-z_0-9]+)_v_([0-9]+)'

    # 正規表現にマッチする部分を検索
    matchRe = re.fullmatch(pattern, cn)

    if matchRe:
        class_name = matchRe[1]  # クラスの名前
        version_number = matchRe[2]  # バージョンの名前
    else:
        raise TypeError("Inappropriate Class Name")
    
    self.vt.append((class_name,version_number,False))
    return

def checkCompatibility(left,right):
    return

def insert(self,c,v,b):
    self.vt.append((c,v,b))
    return

def append(left,right):
    # 以下は見やすくするために行うもの、結合の順序を気にするなら変えた方がいい
    left_vt = left.vt
    right_vt = right.vt
    for x in left_vt:
        cx = x[0]
        vx = x[1]
        bx = x[2]
        for y in right_vt:
            cy = y[0]
            vy = y[1]
            by = y[2]
            if((cx==cy) and (vx == vy) and (bx == by)):
                left_vt.remove(x)      
    # 結合を返す
    left.vt = left_vt + right_vt
    return