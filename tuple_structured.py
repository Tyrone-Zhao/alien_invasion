# 只包含一个元素的元组会被python识别错误
tuple = ("apple")
print (tuple[0])
print (type(tuple))

# 加逗号识别正确
tuple = ("apple",)
print (tuple[0])
print (type(tuple))

# 负数索引和分片索引
tuple = ("value1", "value2", "value3", "value4")
print (tuple)
print (tuple[1:3])
print (tuple[-1])
print (tuple[-2])
print (tuple[0:-2])
print (tuple[2:-2])

# 二元元组
fruit1 = ("apple", "banana")
fruit2 = ("grape", "orange")
tuple = (fruit1, fruit2)
print (tuple)
print ("tuple[0][1] =", tuple[0][1])
print ("tuple[1][1] =", tuple[1][1])
#print ("tuple[1][1] =", tuple[1][2])

# 元组的打包和解包
# 打包
tuple = ("apple", "banana", "grape", "orange")
# 解包
a, b, c, d = tuple
print (a, b, c, d)

# 元组的遍历
tuple = (("apple", "banana"), ("grape", "orange"), ("watermelon",), ("grapefruit",))
for i in range(len(tuple)):
    print ("tuple[%d]: " % i)
    for j in range(len(tuple[i])):
        print (tuple[i][j])
    print()

# 直接使用 for in 遍历元组
tuple = (("apple", "banana"), ("grape", "orange"), ("watermelon",), ("grapefruit",))
for i in tuple:
    for j in i:
        print(j)