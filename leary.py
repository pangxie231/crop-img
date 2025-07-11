import tkinter as tk
from functools import cmp_to_key
from typing import Dict

# def main():
#   root = tk.Tk()
#   root.geometry('800x800')
  
#   left_frame = tk.Frame(root, width=300)
#   left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0,1))

#   right_frame = tk.Frame(root, width=500)
#   right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

#   root.mainloop()

# if __name__ == "__main__":
#   main()



# list = [0,1,2,3,4,5,6,7,8,9,10]
# # a1, a2, a3, a4 = list[0:4]
# # print(a1, a2, a3, a4)

# # print(list[::-1]) 

# list1 = [1,2,3]
# list2 = [4,5,6]
# # print(list1 + list2)
# list4 = [None] * 10
# print(list4)



# 滚动条
# root = tk.Tk()
# root.title('滚动条学习')
# root.geometry('400x180')

# frame1 = tk.Frame(root, width=200)
# frame1.pack(side=tk.LEFT, fill=tk.BOTH)

# sbarx = tk.Scrollbar(frame1, orient=tk.HORIZONTAL)
# sbarx.pack(side=tk.BOTTOM, fill=tk.X)

# sbary = tk.Scrollbar(frame1)
# sbary.pack(side=tk.RIGHT, fill=tk.Y)


# canvas = tk.Canvas(frame1, xscrollcommand= sbarx.set, yscrollcommand=sbary.set)
# canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
# canvas.create_rectangle(40, 20, 240, 222, fill='green')
# canvas.create_rectangle(80, 300, 280, 500, fill='blue')
# canvas.create_rectangle(60, 60, 1000, 580, fill='pink')

# sbarx.config(command=canvas.xview)
# sbary.config(command=canvas.yview)

# canvas.config(scrollregion=canvas.bbox('all'))

# frame2 = tk.Frame(root, width=200)
# frame2.pack(side=tk.LEFT, fill=tk.BOTH)

# root.mainloop()

# x = [2,3,5,4,1]
# # 先判断x > y
# # -1 1, 按照一个坐标轴，-1在左侧，1在右侧
# def compare(x,y):
#   if x > y:
#     return -1
#   if x < y:
#     return 1
#   else:
#     return 0
  
# x.sort(key=cmp_to_key(compare))
# print(x)

# 字符串格式化
# input_name = input('请输入你的姓名:')
# input_age = input('请输入你的年龄:')
# print('Hello %s! You are %s! %%' % (input_name, input_age))


# 字典
# d = dict(age=25, name='lwj')


# if else 三目
# b = False
# print(b if 'True' else 'False')


# 循环
# x = 1
# while x <= 100:
#   print(x)
#   x +=1

# words = ['this', 'is', 'an', 'ex', 'parrot']
# for word in words:
#   print(word)
  
# numbers = [0,1,2,3,4,5,6,7,8,9,10]
# for number in numbers:
#   print(number)

# for n in range(1,10):
#   print(n)

# d = { 'x': 1, 'y': 2, 'z': 3 }
# for key in d:
#   # print(key)
#   print(d.get(key))

# fibs = [0,1]
# for i in range(10):
#   fibs.append(fibs[-2] + fibs[-1])
# print(fibs)

# def hello(name):
#   return 'Hello' + ',' + name + '!'

# print(hello('lwj'))

# def fibs(num):
#   '计算fib'
#   my_list = [0, 1]
#   i = 0
#   while i < num - 2:
#     my_list.append(my_list[-2] + my_list[-1])
#     i += 1
#   return my_list

# print(help(fibs))

# def hello_1(gretting='hello', name='world'):
#   print('%s, %s!' % (gretting, name))

# hello_1(gretting='Hello', name='JG')
# hello_1(name='JG')

# def print_params(*params):
#   print(params)

# print_params()

# def print_params2(title, **params):
#   print(title)
#   print(params)

# print_params2('title', other="jg", name="dg")

# def add(x,y):
#   return x + y
# params = (1,2)
# print(add(*params))

# def add(**d: Dict[str, int]):
#   sum = 0
#   for v in d.values():
#     sum += v
#   return sum
# my_d = {'x': 1, 'y': 2, 'z': 3}
# print(add(**my_d))
    
# 改变全局变量
# x = 1
# def change_global():
#   global x
#   x = x + 1

# change_global()
# print(x)
  
# 递归
# def recursion():
#   return recursion()
# recursion()

def factorial(n):
  if n == 1: return 1
  return n * factorial(n - 1)

print(factorial(10))