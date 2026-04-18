class obj():
    enable = False

obj1 = obj()
obj2 = obj()

print(obj1.enable)

obj.enable = True

print(obj1.enable)