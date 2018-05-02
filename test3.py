# -*- coding: utf-8 -*-
import tkinter as tk
import time
import threading
def showother():
	otherFrame.update()
	otherFrame.deiconify()
	hide_thd()
def delaysHideOther():
    time.sleep(5)
    otherFrame.withdraw()
def hide_thd():
    threading.Thread(target = delaysHideOther).start()
root = tk.Tk()
otherFrame = tk.Toplevel()
otherFrame.withdraw()
otherFrame.attributes('-toolwindow', True)
otherFrame.geometry('150x50')
tk.Label(otherFrame, text="5秒后关闭!", width=50).pack()
root.geometry('150x80')
tk.Button(root, text='显示弹窗', width=10, command=showother).pack()
root.mainloop()