class ABC():
    pass

class BCD(ABC):
    pass

a = BCD()

print(type(a) == ABC)