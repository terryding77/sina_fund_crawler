# encoding=utf-8
# !/usr/bin/env python
import Tkinter as tk
import ttk
import tkMessageBox
import os
import thread
from funds_crawler import crawler_all_fund
from fund_net_value_crawler import get_net_value

WINDOW_HEIGHT = 30
ITEM_SHOW_SIZE = 20
WINDOW_WIDTH = 50


class FundNetValueMessageBox(tk.Toplevel):
    def __init__(self, root, symbol_num, sname):
        tk.Toplevel.__init__(self, root)
        self.root = root
        self.resizable(False, False)
        self.symbol_num = symbol_num
        self.protocol('WM_DELETE_WINDOW', self.remove_msg)
        self.withdraw()
        scroll = ttk.Scrollbar(self)
        self.list_box = tk.Listbox(self, yscrollcommand=scroll.set, height=WINDOW_HEIGHT, width=WINDOW_WIDTH)
        scroll.configure(command=self.list_box.yview)
        self.list_box.grid(row=0, column=0)
        scroll.grid(row=0, column=1, sticky=tk.N + tk.S)
        self.title(str(symbol_num) + sname)

    def show(self, force):
        net_values = get_net_value(self.symbol_num, force=force)
        self.list_box.insert(tk.END, "          发布日期               基金净值      累积净值")
        for net_value in net_values:
            self.list_box.insert(tk.END, "%s\t%15.3f\t%15.3f" %
                                 (net_value['fbrq'], float(net_value['jjjz']), float(net_value['ljjz'])))
        self.deiconify()

    def remove_msg(self):
        self.root.__class__.msg_box_dict[self.symbol_num] = None
        self.destroy()


class FundRecord(tk.Frame):
    msg_box_dict = {}
    fund_label_dict = {
        "fund_manager": ["基金经理", 20],
        "jjlx": ["基金类型", 20],
        "nav_date": ["涨跌额", 10],
        "nav_rate": ["增长率", 10],
        "per_nav": ["单位净值", 10],
        "sg_states": ["申购状态", 10],
        "sname": ["基金名称", 25],
        "symbol": ["基金代码", 10],
        "total_nav": ["累积净值", 10],
        "yesterday_nav": ["昨日净值", 10],
    }

    def __init__(self, root=None, fund=None, idx=0):
        tk.Frame.__init__(self, root, height=WINDOW_HEIGHT / ITEM_SHOW_SIZE)
        self.index = idx
        self.fund_obj = fund
        if fund is None:
            self.labels = dict([(name, tk.Label(self, text=value[0], width=value[1])) for name, value in
                                self.__class__.fund_label_dict.items()])
        else:
            self.labels = dict([(name, tk.Label(self, text=fund.get(name, ""), width=value[1])) for name, value in
                                self.__class__.fund_label_dict.items()])
        for i, label in enumerate(self.labels.values()):
            label.grid(row=0, column=i)
        self.labels['symbol'].bind('<Button-1>', self.show_fund)
        self.labels['sname'].bind('<Button-1>', self.show_fund)

    def set_fund(self, fund, idx):
        self.fund_obj = fund
        for name, label in self.labels.items():
            label.config(text=fund[name])
        self.index = idx

    def show_fund(self, event):
        symbol_num = self.fund_obj['symbol']
        sname = self.fund_obj['sname']

        print(symbol_num)
        force = True
        if symbol_num not in self.__class__.msg_box_dict or self.__class__.msg_box_dict[symbol_num] is None:
            msg = FundNetValueMessageBox(self, symbol_num, sname)
            self.__class__.msg_box_dict[symbol_num] = msg
        else:
            msg = self.__class__.msg_box_dict[symbol_num]
            force = False
        msg.show(force)


class FundBoxFrame(ttk.Frame):
    def __init__(self, root=None):
        ttk.Frame.__init__(self, root, height=WINDOW_HEIGHT, width=WINDOW_WIDTH)
        self.funds = crawler_all_fund()
        self.root = root
        global ITEM_SHOW_SIZE
        ITEM_SHOW_SIZE = min(ITEM_SHOW_SIZE, len(self.funds))
        self.fund_frames = []
        self.fund_show_first_index = 0
        FundRecord(self, None).grid(row=0, column=0)
        for i, fund in enumerate(self.funds[self.fund_show_first_index:self.fund_show_first_index + ITEM_SHOW_SIZE]):
            self.fund_frames.append(FundRecord(self, fund, i))
            self.fund_frames[-1].grid(row=i + 1, column=0)

    def yview(self, action, *args):
        if action == tk.SCROLL and len(args) >= 2 and args[1] == tk.UNITS:
            step = int(args[0])
            tmp = self.fund_show_first_index + step
            if (tmp < 0 and step == -1) or (tmp + ITEM_SHOW_SIZE >= len(self.funds) and step == 1):
                return
            self.fund_show_first_index += step
        if action == tk.MOVETO and len(args) >= 1:
            f = min(1, max(0, float(args[0])))
            self.fund_show_first_index = min(len(self.funds) - ITEM_SHOW_SIZE - 1, int(f * len(self.funds)))
        for i, fund in enumerate(self.fund_frames):
            fund.set_fund(self.funds[i + self.fund_show_first_index], i + self.fund_show_first_index)
        self.root.scroll.set(max(0, self.fund_frames[0].index * 1.0 / len(self.funds)),
                             min(1, self.fund_frames[-1].index * 1.0 / len(self.funds)))


class MainGui(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        self.menu = tk.Menu(self.winfo_toplevel())
        self.menu.add_command(label="Crawl All!", command=self.process_all)
        self.menu.add_command(label="Open Folder!", command=self.open)
        self.menu.add_command(label="About!", command=self.about)
        self.config(menu=self.menu)
        self.title('fund crawler')
        self.fund_box_frame = FundBoxFrame(self)
        self.resizable(False, False)
        self.fund_box_frame.grid(row=1, column=0)
        self.scroll = ttk.Scrollbar(self, command=self.fund_box_frame.yview)
        self.scroll.set(0, min(0.1, ITEM_SHOW_SIZE * 1.0 / len(self.fund_box_frame.funds)))
        self.scroll.grid(row=1, column=1, sticky=tk.N + tk.S)  # side=tk.RIGHT, fill=tk.Y)
        self.progress_frame = ttk.Frame(self)
        self.progress_bar = ttk.Progressbar(self.progress_frame)
        self.progress_label = ttk.Label(self.progress_frame, text="Crawler Begin !")
        self.process_mark = True

    def process_all(self):
        print('process all !')
        force = tkMessageBox.askyesno("force crawl or not", "Do you want to refresh exist data when crawling? ")
        print('is force update? ' + str(force))
        self.menu.delete("Crawl All!")
        self.menu.insert_command(index=0, label="Stop Crawl", command=self.stop_crawl)
        self.progress_frame.grid(row=3)
        self.progress_label.grid(row=0, column=0)
        self.progress_bar.grid(row=0, column=1)
        thread.start_new_thread(self.crawl, (self.fund_box_frame.funds, force))

    def crawl(self, funds, force=False):
        for i, fund in enumerate(funds):
            if not self.process_mark:
                break
            symbol_num = fund['symbol']
            get_net_value(symbol_num, force=force)
            self.progress_label.config(text=symbol_num)
            self.progress_bar.config(value=100 * i / len(funds))
        self.progress_label.config(text='crawl finish!' if self.process_mark else "crawl stopped! ")
        self.menu.insert_command(0, label="Crawl All!", command=self.process_all)
        self.process_mark = True

    def stop_crawl(self):
        self.menu.delete("Stop Crawl")
        import time
        time.sleep(2)
        self.process_mark = False

    @staticmethod
    def about():
        about_str = "Author is Terry Ding (terryding77@gmail.com)\n" \
                    "Idea made by Huan Ding"
        tkMessageBox.showinfo("about", about_str)
        print(about_str)

    @staticmethod
    def open():
        print('Open folder ./')
        os.startfile(os.path.abspath('./'))


if __name__ == "__main__":
    root = MainGui()
    root.mainloop()
