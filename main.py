import time

import customtkinter

from childThreadGUI import childThreadGUI

if __name__ == '__main__':
    root = customtkinter.CTk()  # 创建窗口容器
    root.attributes("-topmost",1)
    gui = childThreadGUI(root)
    root.mainloop()