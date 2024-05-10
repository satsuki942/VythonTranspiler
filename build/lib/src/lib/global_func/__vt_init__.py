import re

def __vt_init__(self):
    self.vt = []
    cn = self.__class__.__name__

    # 正規表現パターン
    # 不正確
    pattern = r"__(\w+)_v_(\d)__"

    # 正規表現にマッチする部分を検索
    match = re.match(pattern, cn)

    if match:
        class_name = match.group(1)  # クラスの名前
        version_number = int(match.group(2))  # バージョンの名前
    else:
        raise TypeError("Inappropriate Class Name")
    
    self.vt.append((class_name,version_number,False))
    return
    
