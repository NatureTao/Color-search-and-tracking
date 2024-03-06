import sys
import threading
from tkinter.messagebox import askyesno
import ctypes
import PIL
import customtkinter
import numpy as np
from imageColorSerch import color_search

global target_color, screenshot, difference_lv, isStarted,target_xy
target_color = (254, 43, 51)  # 默认搜索RGB
target_xy = (0,0)  # 目标偏移xy
screenshot = (710, 290, 1210, 790)  # 截图范围 大
# screenshot = (916, 494, 1005, 574)  # 截图范围 小
difference_lv = 10  # 相差RBG数值
isStarted = False
'''加载罗技驱动'''
try:
    gm = ctypes.CDLL(r'./ghub_device.dll')
    gmok = gm.device_open() == 1
    if not gmok:
        print('未安装ghub或lgs驱动!')
    else:
        print("初始化成功!")
except FileNotFoundError:
    print("缺少文件")
class childThreadGUI(object):



    def __init__(self, root):
        values = ["红色", "黄色", "紫色","蓝色(AIMLABS)"] #颜色标签
        self.root = root
        customtkinter.set_default_color_theme("green")
        root.minsize(600, 500)
        root.maxsize(600, 500)
        root.title('桃园月色')
        root.iconbitmap("images/peach.ico")
        self.image = PIL.Image.open("images/600x500.png")
        self.background_image = customtkinter.CTkImage(self.image, size=(600, 500))
        self.bg_lbl = customtkinter.CTkLabel(root, text="", image=self.background_image)
        self.bg_lbl.place(x=0, y=0)
        self.logo_label = customtkinter.CTkLabel(root, text="敌人颜色", font=customtkinter.CTkFont(size=20, weight="bold"),
                                            width=140, text_color="black")
        self.logo_label.grid(row=1, column=1, padx=14, pady=(10, 1))
        self.optionmenu = customtkinter.CTkOptionMenu(root, values=values,
                                                 command=self.optionmenu_callback)
        self.optionmenu.place(relx=0.14, rely=0.1, anchor="n")
        """ 点击右上角关闭窗体弹窗事件 """
        self.root.protocol('WM_DELETE_WINDOW', lambda: self.thread_it(self.clos_window))
        """ 操作按钮 """
        self.button = customtkinter.CTkButton(master=root, text="启动", command=lambda:self.thread_it(self.button_function_start), width=80)
        self.button.place(relx=0.5, rely=0.9, anchor=customtkinter.CENTER)
        '''上面是用户界面'''

        '''这里是颜色RBG数值存放地'''
    def optionmenu_callback(self,choice):
        global target_color,target_xy
        if choice == "红色":
            target_color = (249,148,146)
            target_xy = (150, -14)
        if choice == "紫色":
            target_color = (255, 144, 255)
            target_xy = (5, 1)
        if choice == "黄色":
            target_color = (0, 0, 0)
        if choice == "蓝色(AIMLABS)":
            target_color = (21,214,217)
            target_xy = (1,1)
        # print("查找-->",target_color)
    def button_function_start(self):
        global target_xy
        print("=====启动=====")
        global isStarted
        customtkinter.CTkButton.configure(self.button, text="关闭", command=lambda:self.thread_it(self.button_function_end))
        isStarted = True

        while isStarted:

            if not isStarted:
                break

            self.coord = color_search(target_color,screenshot,difference_lv=10)
            if self.coord is not None:
                #调用平滑计算
                self.mouse_xy(self.coord,target_xy)


    def button_function_end(self):
        print("=====关闭=====")
        global isStarted
        isStarted = False
        customtkinter.CTkButton.configure(self.button, text="启动", command=lambda:self.thread_it(self.button_function_start))



    def clos_window(self):
        ans = askyesno(title='桃园月色v1.1警告', message='是否确定退出程序？\n是则退出，否则继续！')
        if ans:
            self.root.destroy()
            sys.exit()
        else:
            return None

    def thread_it(self, func, *args):
        """ 将函数打包进线程 """
        self.myThread = threading.Thread(target=func, args=args)
        self.myThread.setDaemon(True)  # 主线程退出就直接让子线程跟随退出,不论是否运行完成。
        self.myThread.start()



    def mouse_xy(slef,coord,target_xy):
        abs_move = True #是否绝对移动
        A = [960,540]
        if (A[0]-coord[0] < 10 or coord[0] - A[0] < 10 ):
             # num_points 是平滑次数
            curves = bezier_curve(A,(coord[0]+target_xy[0],coord[1]+target_xy[1]),2)
            for curve in curves:
                if gmok:
                    gm.moveR(int(curve[0]-A[0]+target_xy[0]), int(curve[1]-A[1]+target_xy[1]), abs_move)
                    # gm.moveR(int(curve[0] - A[0]), int(curve[1] - A[1]), abs_move)
                    print("平滑移动-->",curve)


#平滑代码1
# def bezier_curve(A, B, num_points):
#     steps = np.linspace(0, 1, num_points)
#     path = np.array([[A[0] + step * (B[0] - A[0]), A[1] + step * (B[1] - A[1])] for step in steps])
#     return path

#平滑代码2
def bezier_curve(A, B, num_points):
    accel_rate = 0.01#加速
    decel_rate = 0.1 #减速
    A = np.array(A)
    B = np.array(B)
    dist = np.linalg.norm(B - A)
    path = []
    for t in np.linspace(0, 1, num_points):
        if t < 0.5:
            current_pos = A + (B - A) * t + 0.5 * accel_rate * t ** 2
        else:
            current_pos = A + (B - A) * t - 0.5 * decel_rate * (1 - t) ** 2

        path.append(current_pos)

    return np.array(path)











