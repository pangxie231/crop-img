from gui.app import App
import tkinter as tk

def main():
  root = tk.Tk()
  root.geometry('800x640')
  app = App(root)
  root.mainloop()

if __name__ == "__main__":
  main()