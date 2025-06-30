import tkinter as tk
from tkinter import Tk, Frame, LEFT, RIGHT, BOTH, X, Y, Label, Button, filedialog, ttk, messagebox
from PIL import Image, ImageTk, ImageDraw
from psd_tools import PSDImage
import threading
from typing import Dict, List
from utils.matcher import get_match_degree, crop_transparent_edges

class App:
  def __init__(self, root: Tk):
    self.root = root

    # tk_image
    self.image_cache = {}
    # pil_image
    self.pil_image = {}
    # 预览器的pil_image
    self.preview_pil_image: Dict[str, Image.Image] = {}
    # 裁剪区的image
    self.crop_image: Dict[str, ImageTk.PhotoImage] = {}
    
    self.psd: PSDImage = None
    
    main_frame = Frame(root, width=800, height=600)
    main_frame.pack(fill=BOTH, expand=True)

    self.frame_left(main_frame)
    self.frame_right(main_frame)


    control_frame = Frame(root)
    control_frame.pack(fill=X)
    open_button = Button(control_frame, text='导入PSD', command=self.load_psd)
    open_button.pack(side=LEFT, padx=5, pady=5)
    
    split_button = Button(control_frame, text='切割图片', command=self.split_layer)
    split_button.pack(side=tk.LEFT, padx=5, pady=5)
    
    matcher_button = Button(control_frame, text='匹配', command=self.matcher_preview)
    matcher_button.pack(side=tk.LEFT, padx=5, pady=5)

  # 切割图层
  def split_layer(self):
    self.psd.save('example.png')
    for layer in self.psd:
      image = layer.composite()
      print(layer.name)
      # image.save('testimg' + '/' + layer.name + '.png')

  # 左边设计稿展示
  def frame_left(self, main):
    frame = tk.Frame(main, bg='yellow')
    frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
    self.left_frame = frame

    
    vbar = tk.Scrollbar(frame, orient=tk.VERTICAL)
    vbar.pack(side=tk.RIGHT, fill=Y)
    hbar = tk.Scrollbar(frame, orient=tk.HORIZONTAL)
    hbar.pack(side=tk.BOTTOM, fill=X)

    vbar.get()

    self.psd_preview = tk.Canvas(frame, cursor='cross')
    self.psd_preview.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
    vbar.config(command=self.psd_preview.yview)
    hbar.config(command=self.psd_preview.xview)
    

    self.psd_preview.config(xscrollcommand=hbar.set, yscrollcommand=vbar.set)

    # 选区功能
    self.init_crop_reactangle()
    
  def init_crop_reactangle(self):
    self.start_x = None
    self.start_y = None
    self.start_id = None
    
    self.rect_id = None
    self.buttons_frame_id = None

    self.psd_preview.bind("<ButtonPress-1>", self.on_press)
    self.psd_preview.bind("<B1-Motion>", self.on_drag)
    self.psd_preview.bind('<ButtonRelease-1>', self.on_release)
    

  # 纠正偏移量
  def adjust_coords(self, *args):
    dx = self.psd_preview.canvasx(0)
    dy = self.psd_preview.canvasy(0)

    if len(args) == 2:
      x, y= args
      return x + dx, y+dy
    elif len(args) == 4:
      x1, y1, x2, y2 = args
      return x1 + dx, y1 + dy, x2 + dx, y2 + dy
    else:
      raise ValueError('必须传入两个或四个坐标')
      

  def on_press(self, event):
    if self.rect_id:
      self.psd_preview.delete(self.rect_id)
      self.rect_id = None
    if self.buttons_frame_id:
      self.psd_preview.delete(self.buttons_frame_id)
      self.buttons_frame_id = None
    
    
    # 鼠标的位置
    self.start_x = event.x
    self.start_y = event.y

    self.rect_id = self.psd_preview.create_rectangle(*self.adjust_coords(self.start_x, self.start_y, self.start_x, self.start_y), outline='red', width=2)
  def on_drag(self, event):
    
    self.psd_preview.coords(self.rect_id, *self.adjust_coords(self.start_x, self.start_y, event.x, event.y))
  
  def on_release(self, event):

    x1, y1 = self.start_x, self.start_y
    x2, y2 = event.x, event.y
    x1, x2 = sorted([x1, x2])
    y1, y2 = sorted([y1, y2])
    
    self.create_buttons(x2, y2)
  def create_buttons(self, x, y):

    frame = tk.Frame(self.root)
    
    ok_btn = tk.Button(frame, text='确定', command=self.ok_crop)
    ok_btn.pack(side=tk.LEFT)

    cancel_btn = tk.Button(frame, text='取消', padx=5, command=self.cancel_crop)
    cancel_btn.pack(side=tk.LEFT, padx=5)

    frame.update_idletasks()
    frame_width = frame.winfo_reqwidth()
    self.buttons_frame_id = self.psd_preview.create_window(*self.adjust_coords(x - frame_width - 8, y + 8), anchor=tk.NW, window=frame)

  def ok_crop(self):
    if not self.rect_id:
      return
    
    x1, y1, x2, y2 = map(int, self.psd_preview.coords(self.rect_id))

    cropped_img = self.pil_image['full'].crop((x1, y1, x2, y2))
    self.preview_pil_image[self.rect_id] = cropped_img
    tk_img = ImageTk.PhotoImage(cropped_img)
    self.image_cache[self.rect_id] = tk_img
    tk.Label(self.previews_frame, image=tk_img).pack(side=tk.LEFT)
    
    self.cancel_crop()
    
    
  
  def cancel_crop(self):
    if self.rect_id:
      self.psd_preview.delete(self.rect_id)
      self.rect_id = None
    if self.buttons_frame_id:
      self.psd_preview.delete(self.buttons_frame_id)
      self.buttons_frame_id = None

  # 右侧 
  def frame_right(self, main):
    frame = tk.Frame(main, bg='red')
    frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
    self.frame_rt(frame)
    self.frame_rb(frame)

  # 右上
  def frame_rt(self, parent):
    frame = tk.Frame(parent, bg='purple')
    self.previews_frame = frame
    frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

  # 右下
  def frame_rb(self, parent):
    frame = tk.Frame(parent, bg='skyblue')
    self.crop_frame = frame
    frame.pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True)
    
  
  # 匹配函数
  def matcher_preview(self):
    # 把pil_image的图片和大图中的图层进行比较
    mathers: List[Image.Image] = []

    for preview_key in self.preview_pil_image:
      # 获取预览区图片
      preview_image = self.preview_pil_image[preview_key]
      
      max_num: float = 0
      max_image: Image.Image = None
      for layer in self.psd:
        image = crop_transparent_edges(layer.composite())
        match_num = get_match_degree(preview_image, image)

        # mathers.append(image)
        if match_num > max_num:
          max_num = match_num
          max_image = image
        
      mathers.append(max_image)
  
    self.render_crop_images(mathers)
  
  # 获取psd所有图层，过滤掉不展示的
  # def psd_layers(self, layer: PSDImage):
    
    
  def render_crop_images(self, images: List[Image.Image]):
    for i, img in enumerate(images):
      tk_image = ImageTk.PhotoImage(img)
      self.image_cache['crop' + str(i)] = tk_image

      label = tk.Label(self.crop_frame, image=tk_image)
      label.pack(side=tk.LEFT)

  def load_psd(self):
    def on_finish():
      print('读取成功!')
    
    def task():
      print('task is call')
      file_path = filedialog.askopenfilename(
      title='选择psd文件',
      filetypes=[("PSD 文件", "*.psd *.psb")]
    )
      if file_path:
        self.psd = PSDImage.open(file_path)
        full_image = self.psd.composite()
        # full_image.thumbnail((600, 600))
        self.pil_image['full'] = full_image
        tk_image = ImageTk.PhotoImage(full_image)
        self.psd_preview.create_image(0,0, anchor=tk.NW, image=tk_image)
        self.psd_preview.config(scrollregion=self.psd_preview.bbox('all'))
        self.image_cache['full'] = tk_image  # 必须缓存
        self.root.after(0, lambda: on_finish)
      
    print('load_psd is call')
    t1 = threading.Thread(target=task, name='load_psd')
    t1.start()
    # t1.join()
      




