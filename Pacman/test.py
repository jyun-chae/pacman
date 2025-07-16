class ABC():
    pass


b = ABC()
a = [b, 2, 3]
del a[0]

print(a)