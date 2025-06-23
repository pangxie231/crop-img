import tkinter as tk

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
root = tk.Tk()
root.title('滚动条学习')
root.geometry('400x180')

frame1 = tk.Frame(root, width=200)
frame1.pack(side=tk.LEFT, fill=tk.BOTH)

sbarx = tk.Scrollbar(frame1, orient=tk.HORIZONTAL)
sbarx.pack(side=tk.BOTTOM, fill=tk.X)

sbary = tk.Scrollbar(frame1)
sbary.pack(side=tk.RIGHT, fill=tk.Y)


canvas = tk.Canvas(frame1, xscrollcommand= sbarx.set, yscrollcommand=sbary.set)
canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
canvas.create_rectangle(40, 20, 240, 222, fill='green')
canvas.create_rectangle(80, 300, 280, 500, fill='blue')
canvas.create_rectangle(60, 60, 1000, 580, fill='pink')

sbarx.config(command=canvas.xview)
sbary.config(command=canvas.yview)

canvas.config(scrollregion=canvas.bbox('all'))

frame2 = tk.Frame(root, width=200)
frame2.pack(side=tk.LEFT, fill=tk.BOTH)

root.mainloop()
