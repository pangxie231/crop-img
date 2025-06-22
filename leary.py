import tkinter as tk

def main():
  root = tk.Tk()
  root.geometry('800x800')
  
  left_frame = tk.Frame(root, width=300)
  left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0,1))

  right_frame = tk.Frame(root, width=500)
  right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

  root.mainloop()

if __name__ == "__main__":
  main()