import tkinter as tk
import tkinter.messagebox
import os


class Panel(tkinter.Tk):
    """
    基本的GUI界面，能够完成模型训练和图像的检测
    """""

    # 初始化
    def __init__(self):
        """
        初始化函数，定义了类成员
        :return: 无返回值
        """""
        super().__init__()
        self.cancel = None
        self.time = None
        self.countdown_info3 = None
        self.countdown = None
        self.countdown_info2 = None
        self.countdown_info1 = None
        self.info6 = None
        self.interval_opt = None
        self.interval_default = None
        self.interval_opts_default = None
        self.wait_default = None
        self.delay_default = None
        self.help = None
        self.start_count = None
        self.do_test = None
        self.info5 = None
        self.interval = None
        self.interval_unit = None
        self.interval_info = None
        self.wait = None
        self.wait_unit = None
        self.wait_info = None
        self.delay_info = None
        self.delay_unit = None
        self.info4 = None
        self.delay = None
        self.info3 = None
        self.info2 = None
        self.info1 = None
        self.title("自动化测量")
        self.geometry("380x600")
        self.layout()
        self.template = ""
        self.stop_flag = False

    # 布局设计
    def layout(self):
        """
        进行GUI的布局设计
        :return: 无返回值
        """""
        # 说明文字
        self.info1 = tk.Label(self, text="使用须知：")
        self.info1.place(x=00, y=0)
        self.info2 = tk.Label(self, text="①确认测试程序已经正确配置")
        self.info2.place(x=60, y=20)
        self.info3 = tk.Label(self, text="②至少手动执行过一次测试（为了确定数据的保存位置）")
        self.info3.place(x=60, y=40)
        self.info4 = tk.Label(self, text="---------------------------------------------------------------------------")
        self.info4.place(x=00, y=60)

        # 指令间隔调整区域
        self.delay_info = tk.Label(self, text="指令间隔时间（默认无需调整，当电脑较卡时可尝试调大）")
        self.delay_info.place(x=5, y=80)
        self.delay_unit = tk.Label(self, text="ms")
        self.delay_unit.place(x=45, y=100)
        self.delay_default = tk.StringVar(value="500")
        self.delay = tk.Entry(self, width=5, textvariable=self.delay_default)
        self.delay.place(x=5, y=100)

        # 等待时间调整区域
        self.wait_info = tk.Label(self, text="测量等待时间（取决于选择的测量范围和需要测试的点位数，默认6s）")
        self.wait_info.place(x=5, y=140)
        self.wait_unit = tk.Label(self, text="s")
        self.wait_unit.place(x=45, y=160)
        self.wait_default = tk.StringVar(value="6")
        self.wait = tk.Entry(self, width=5, textvariable=self.wait_default)
        self.wait.place(x=5, y=160)

        # 间隔时间调整区域
        self.interval_info = tk.Label(self, text="间隔时间（默认60 minutes）")
        self.interval_info.place(x=5, y=200)
        interval_opts = [
            'seconds',
            'minutes',
            'hours'
        ]
        self.interval_opt = tk.StringVar(value="minutes")
        self.interval_unit = tk.OptionMenu(self, self.interval_opt, *interval_opts)
        self.interval_unit.place(x=45, y=220)
        self.interval_default = tk.StringVar(value="60")
        self.interval = tk.Entry(self, width=5, textvariable=self.interval_default)
        self.interval.place(x=5, y=225)

        # 说明文字2
        self.info5 = tk.Label(self, text="---------------------------------------------------------------------------")
        self.info5.place(x=00, y=260)

        # 测试按钮
        self.do_test = tk.Button(self, text="测试一下", command=self.test)
        self.do_test.place(x=50, y=320)
        # 执行按钮
        self.start_count = tk.Button(self, text="开始执行", command=self.start_test)
        self.start_count.place(x=150, y=320)
        # 帮助按钮
        self.help = tk.Button(self, text="程序说明", command='')
        self.help.place(x=250, y=320)

        # 说明文字3
        self.info6 = tk.Label(self, text="---------------------------------------------------------------------------")
        self.info6.place(x=00, y=380)

        # 倒计时界面
        self.countdown_info1 = tk.Label(self, text="距离下次测量还有：")
        self.countdown_info1.place(x=50, y=400)
        self.countdown_info2 = tk.Label(self, text="秒")
        self.countdown_info2.place(x=250, y=400)
        self.countdown = tk.StringVar(self, value="0")
        self.countdown_info3 = tk.Label(self, textvariable=self.countdown)
        self.countdown_info3.place(x=180, y=400)
        self.cancel = tk.Button(self, text="结束目前任务", command=self.cancel_task)
        self.cancel["state"] = "disable"
        self.cancel.place(x=140, y=450)

    # 测试过程
    def test(self):
        """
        更新脚本，并执行一次测试
        :return: 无返回值
        """""
        self.validate_numbers()
        self.generate_file()
        if not os.path.exists("temp.ahk"):
            return tk.messagebox.showerror("软件错误", "软件错误，请联系开发者")
        os.system("AutoHotkey.exe ./temp.ahk")

    # 执行过程
    def start_test(self):
        """
        更新脚本，并开始自动测试
        :return: 无返回值
        """""
        self.validate_numbers()
        self.generate_file()
        if not os.path.exists("temp.ahk"):
            return tk.messagebox.showerror("软件错误", "软件错误，请联系开发者")
        # 设置结束标志为假
        self.stop_flag = False
        # 开始进行倒计时
        self.run()

    # 倒计时部分
    def run(self):
        """
        倒计时开始函数，于该处计算倒计时初始值
        :return: 无返回值
        """""
        # 更新按钮状态，防止指令冲突
        self.cancel["state"] = "normal"
        self.do_test["state"] = "disable"
        # 计算倒计时
        interval = self.interval.get()
        interval_opt = self.interval_opt.get()
        if interval_opt == "seconds":
            self.time = int(interval)
        if interval_opt == "minutes":
            self.time = int(interval) * 60
        if interval_opt == "hours":
            self.time = int(interval) * 3600
        self.countdown.set(str(self.time))
        # 执行倒计时更新
        self.do_countdown()
        print("一次执行结束")

    # 数字合法性验证函数
    def validate_numbers(self):
        """
        数字合法性验证函数，于该处验证时间输入文本框的合法性
        :return: 无返回值
        """""
        delay = self.delay.get()
        wait = self.wait.get()
        interval = self.interval.get()
        if (not delay.isdigit()) or (not wait.isdigit()) or (not interval.isdigit()):
            return tk.messagebox.showerror("数字错误", "请在该输入框输入纯数字")

    # 脚本文件生成函数
    def generate_file(self):
        """
        脚本文件生成函数，于该处生成自动测量用的 AHK 脚本文件
        :return: 无返回值
        """""
        delay = self.delay.get()
        wait = self.wait.get()
        new_wait = str(int(wait) * 1000)
        if not os.path.exists("AHKTemplate"):
            return tk.messagebox.showerror("软件错误", "缺少 AHKTemplate 模板，请联系开发者")
        template = open("./AHKTemplate", encoding="utf-8")
        commands = template.readlines()
        template.close()
        new_commands = []
        for line in commands:
            if line.startswith(';'):
                continue
            if line.endswith("<delay>\n"):
                new_commands.append("Sleep " + delay + "\n")
                continue
            if line.endswith("<wait>\n"):
                new_commands.append("Sleep " + new_wait + "\n")
                continue
            new_commands.append(line)
        # 删除已有文件
        if os.path.exists("temp.ahk"):
            os.remove("temp.ahk")
        new_file = open("./temp.ahk", encoding="utf-8", mode="w")
        new_file.writelines(new_commands)
        new_file.close()

    # 倒计时更新函数
    def do_countdown(self):
        """
        倒计时更新函数，于该处更新倒计时并执行倒计时结束后操作
        :return: 无返回值
        """""
        # 倒计时自减
        self.time -= 1

        # 显示新的倒计时
        self.countdown.set(str(self.time))

        # 倒计时判断，未结束则递归
        if self.time > 0 and not self.stop_flag:
            self.after(1000, self.do_countdown)
        else:
            # 倒计时结束，执行脚本，并重新开始倒计时
            if self.time <= 0:
                os.system("AutoHotkey.exe ./temp.ahk")
                self.run()

    # 倒计时取消函数
    def cancel_task(self):
        """
        倒计时取消函数，于该处取消倒计时
        :return: 无返回值
        """""
        # 将结束标志设置为真
        self.stop_flag = True
        # 修改按钮状态
        self.cancel["state"] = "disable"
        self.do_test["state"] = "normal"
