if 5>2:
    print("5 is greater than 2")
x=3
y=2
print("x is greater than y")

x = "awesome"

def myfunc():
  print("Python is " + x)

myfunc()


price_str=input("请输入苹果的价格: ")
weight_str=input("请输入苹果的重量: ")
price=float(price_str)
weight=float(weight_str)
total_price=price*weight
print("苹果的总价是: ", total_price)
price = float(input("请输入苹果的价格: "))
weight = float(input("请输入苹果的重量: ")) 
money = price * weight
print("当前苹果的单价为: %.2f,重量为:%.2f,总价：%.2f" % (price, weight, money))
scale = 10.23
print("数据比例是 %.2f%%" % (scale*100))
