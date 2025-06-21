import tkinter as tk
from tkinter import Tk, Frame, LEFT, RIGHT, BOTH, X, Y, Label, Button, filedialog, ttk, messagebox
from PIL import Image, ImageTk, ImageDraw
from psd_tools import PSDImage

class App:
  def __init__(self, root: Tk):
    self.root = root

    self.image_cache = {}
    self.layer_map = {}

    main_frame = Frame(root)
    main_frame.pack(fill=BOTH, expand=True)

    # 左侧区域
    layer_frame = Frame(main_frame, width=200)
    layer_frame.pack(side=LEFT, fill=Y)

    self.tree = ttk.Treeview(layer_frame, selectmode='extended')
    self.tree.heading("#0", text="图层名称")
    self.tree.pack(fill=BOTH, expand=True)
    self.tree.bind("<<TreeviewSelect>>", self.on_layer_select)


    # 右侧
    right_frame = Frame(main_frame)
    right_frame.pack(side=RIGHT, fill=BOTH, expand=True)

    self.full_preview_label = Label(right_frame)
    self.full_preview_label.pack(pady=5)

    bottom_frame = Frame(right_frame)
    bottom_frame.pack(fill=BOTH, expand=True)

    # 左：选中图层预览
    selected_frame = Frame(bottom_frame)
    selected_frame.pack(side=LEFT, fill=BOTH, expand=True)
    self.selected_preview_label = Label(selected_frame)
    self.selected_preview_label.pack(pady=5)

    # 右：待切区域
    pending_frame = Frame(bottom_frame)
    pending_frame.pack(side=LEFT, fill=BOTH, expand=True)

    control_frame = Frame(root)
    control_frame.pack(fill=X)
    open_button = Button(control_frame, text='导入PSD', command=self.load_psd)
    open_button.pack(side=LEFT, padx=5, pady=5)

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
      self.full_preview_label.config(image=tk_image)
      self.image_cache['full'] = tk_image  # 必须缓存
      self.build_tree(self.psd, parent="")


  def build_tree(self, group, parent=""):
    for layer in group:
      if not layer.is_visible():
        continue  # 跳过不可见图层

      # 在 Treeview 中添加图层项
      node_id = self.tree.insert(parent, 'end', text=layer.name)

      # 建立节点 ID 到 layer 的映射，方便后续操作
      self.layer_map[node_id] = layer

      # 如果是图层组，递归添加其子图层
      if layer.is_group():
        self.build_tree(layer, parent=node_id)

  def on_layer_select(self, event):
    selected = self.tree.selection()
    print('self',list(selected))
    if not selected:
      return
    
    node_id = selected[0]
    layer = self.layer_map.get(node_id)
    if not layer:
      return
    
    try:
      image = layer.composite()
      image.thumbnail((800, 800))
      tk_image = ImageTk.PhotoImage(image)
      self.image_cache['selected'] = tk_image  # 防止被回收
      self.selected_preview_label.config(image=tk_image, text='')
    except Exception as e:
      messagebox.showerror("渲染失败", f"图层无法渲染：{e}")



