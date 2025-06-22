import tkinter as tk
from tkinter import Tk, Frame, LEFT, RIGHT, BOTH, X, Y, Label, Button, filedialog, ttk, messagebox
from PIL import Image, ImageTk, ImageDraw
from psd_tools import PSDImage

class App:
  def __init__(self, root: Tk):
    self.root = root

    self.image_cache = {}
    
    main_frame = Frame(root, width=800, height=600)
    main_frame.pack(fill=BOTH, expand=True)

    self.frame_left(main_frame)
    self.frame_right(main_frame)


    control_frame = Frame(root)
    control_frame.pack(fill=X)
    open_button = Button(control_frame, text='导入PSD', command=self.load_psd)
    open_button.pack(side=LEFT, padx=5, pady=5)

  # 左边设计稿展示
  def frame_left(self, main):
    frame = tk.Frame(main, width=400, height=600, bg='yellow')
    frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
    self.psd_preview = tk.Canvas(frame, cursor='cross')
    self.psd_preview.pack(fill=tk.BOTH, expand=True)

    # 选区功能
    self.init_crop_reactangle()
    
  def init_crop_reactangle(self):
    self.start_x = None
    self.start_y = None
    self.start_id = None

    self.psd_preview.bind("<ButtonPress-1>", self.on_press)
    self.psd_preview.bind("<B1-Motion>", self.on_drag)


  def on_press(self, event):
    self.start_x = event.x
    self.start_y = event.y

    self.rect_id = self.psd_preview.create_rectangle(self.start_x, self.start_y, self.start_x, self.start_y, outline='red', width=2)
  def on_drag(self, event):
    self.psd_preview.coords(self.rect_id, self.start_x, self.start_y, event.x, event.y)
  
  # def on_release(self, event):



  # 右侧 
  def frame_right(self, main):
    frame = tk.Frame(main, bg='red')
    frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
    self.frame_rt(frame)
    self.frame_rb(frame)

  # 右上
  def frame_rt(self, parent):
    frame = tk.Frame(parent, bg='purple')
    frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

  # 右下
  def frame_rb(self, parent):
    frame = tk.Frame(parent, bg='skyblue')
    frame.pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True)

  def load_psd(self):
    file_path = filedialog.askopenfilename(
      title='选择psd文件',
      filetypes=[("PSD 文件", "*.psd *.psb")]
    )

    if file_path:
      self.psd = PSDImage.open(file_path)
      full_image = self.psd.composite()
      full_image.thumbnail((600, 600))
      tk_image = ImageTk.PhotoImage(full_image)
      self.psd_preview.create_image(0,0, anchor=tk.NW, image=tk_image)
      self.image_cache['full'] = tk_image  # 必须缓存




