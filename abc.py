# listdemo = ['Google','Runoob', 'Taobao']
# # 将列表中各字符串值为键，各字符串的长度为值，组成键值对
# newdict = {k:len(k) for k in listdemo}
# print(newdict)
 
# import sys         # 引入 sys 模块
 
# list=[1,2,3,4]
# it = iter(list)    # 创建迭代器对象
 
# while True:
#     try:
#         print (next(it), end=' ') # 使用 next() 函数获取迭代器的下一个值  
#     except StopIteration:
#         sys.exit()
class MyNumbers:
  def __iter__(self):
    self.a = 1
    return self
 
  def __next__(self):
    x = self.a
    self.a += 1
    return x
 
myclass = MyNumbers()
myiter = iter(myclass)
 
print(myiter.__next__())  # 输出 1
print(next(myiter))  # 输出 2  
print(myiter.__next__())  # 输出 3
print(myiter.__next__())  # 输出 4
print("5. 返回主菜单")
