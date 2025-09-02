# # 用户输入数字
# num1 = float(input("请输入第一个数字: "))
# num2 = float(input("请输入第二个数字: "))
# # 计算和
# sum_result = num1 + num2
# # 输出结果
# print("两个数字的和是: ", sum_result)

# num = float(input("请输入一个数字: "))
# num_sqrt = num ** 0.5
# print('%.3f 的平方根是 %.3f' % (num, num_sqrt))
# -*- coding: UTF-8 -*-
 
# Filename : test.py
# author by : www.runoob.com
 
# 计算实数和复数平方根
# 导入复数数学模块
 
# import cmath
 
# num = int(input("请输入一个数字: "))
# num_sqrt = cmath.sqrt(num)
# print('{0} 的平方根为 {1:0.3f}+{2:0.3f}j'.format(num ,num_sqrt.real,num_sqrt.imag))
# -*- coding: UTF-8 -*-
 
# Filename : test.py
# author by : www.runoob.com
 
 
# a = float(input('输入三角形第一边长: '))
# b = float(input('输入三角形第二边长: '))
# c = float(input('输入三角形第三边长: '))
 
# # 计算半周长
# s = (a + b + c) / 2
 
# # 计算面积
# area = (s*(s-a)*(s-b)*(s-c)) ** 0.5
# print('三角形面积为 %0.2f' %area)
# import math

# def calculate_circle_area(radius):
#     return math.pi * radius ** 2

# # 示例
# radius = 5
# area = calculate_circle_area(radius)
# print(f"半径为 {radius} 的圆的面积是 {area}")
# import random

# random_number = random.random()
# print(random_number)
# -*- coding: UTF-8 -*-
 
# Filename : test.py
# author by : www.runoob.com
 
# 生成 0 ~ 9 之间的随机数
 
# 导入 random(随机数) 模块
# import random
 
# print(random.randint(0,9))
# -*- coding: UTF-8 -*-
 
# Filename : test.py
# author by : www.runoob.com
 
# # 九九乘法表
# for i in range(1, 10):
#     for j in range(1, i+1):
#         print('{}x{}={}\t'.format(j, i, i*j), end='')
#     print()
# -*- coding: UTF-8 -*-
 
# # Python 斐波那契数列实现
 
# # 获取用户输入数据
# nterms = int(input("你需要几项？"))
 
# # 第一和第二项
# n1 = 0
# n2 = 1
# count = 2
 
# # 判断输入的值是否合法
# if nterms <= 0:
#    print("请输入一个正整数。")
# elif nterms == 1:
#    print("斐波那契数列：")
#    print(n1)
# else:
#    print("斐波那契数列：")
#    print(n1,",",n2,end=" , ")
#    while count < nterms:
#        nth = n1 + n2
#        print(nth,end=" , ")
#        # 更新值
#        n1 = n2
#        n2 = nth
#        count += 1
num = int(input("请输入一个数字: "))
 
# 初始化变量 sum
sum = 0
# 指数
n = len(str(num))
 
# 检测
temp = num
while temp > 0:
   digit = temp % 10
   sum += digit ** n
   temp //= 10
 
# 输出结果
if num == sum:
   print(num,"是阿姆斯特朗数")
else:
   print(num,"不是阿姆斯特朗数")