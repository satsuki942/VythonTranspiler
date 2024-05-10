class A!1:
    def __init__(self,n):
        self.num = n

    def m(self,r):
        return self.num + r

class A!2:
    def __init__(self,n):
        self.num = n
    
    def m(self,r):
        result = self.num+r
        # incompatの時だけ困る
        incompat(self,result)
        return result

a1 = A!2(4)
print(a1.vt)
a2 = A!1(3)
print(a2.vt)
n1 = a1.m(5)
print(n1.vt)
# ここがおかしい
n2 = a2.m(1)
print(n2.vt)
n3 = n1+n2
print(n3.vt)

print(n3)


