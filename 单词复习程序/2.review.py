#review.py
import time
import random
import tkinter as tk
import tkinter.messagebox as tkm #弹窗库

#translate
#import requests
#import json
#import hashlib

import matplotlib.pyplot as plt
from matplotlib.pyplot import MultipleLocator  # 从pyplot导入MultipleLocator类，这个类用于设置刻度间隔

root = tk.Tk()
root.withdraw()

#全局变量
i = 0
N = 0
pass_code = 0
today_count = 0  # 本次有效复习的次数

day_ls = []
day_ls_temp = []
day_count_ls = []
day_count_ls_temp = []

word_ls = []
translation_ch_ls = []
translation_en_ls = []
eff_rev_ls = []
x_times_ls = []
last_rev_date_ls = []
d_position_ls = []


class TaskV4:
    def __init__(self, month):
        """?"""
        self.month = month
        self.file = "data\\day_count\\" + self.month + '.data'

    def day_count_to_ls(self):
        try:
            with open(self.file, 'at'):
                pass
            with open(self.file) as dcd:
                days = dcd.readlines()
                for day in days:
                    if day == '':
                        continue
                    day = day.strip()
                    # if day[0:7] == self.month:
                    day_ls_temp.append(day.split(':')[0])
                    day_count_ls_temp.append(day.split(':')[1])

            first_day_this_month = self.month + '.01'
            month_index = N_YEAR_DATA_ls.index(first_day_this_month)
            for d in range(32):
                day_temp = N_YEAR_DATA_ls[month_index+d]
                if day_temp[:7] != self.month:
                    break
                if day_temp in day_ls_temp:
                    day_ls.append(day_temp)
                    day_count_ls.append(day_count_ls_temp[day_ls_temp.index(day_temp)])
                else:
                    day_ls.append(day_temp)
                    day_count_ls.append('0')
                if day_temp == date_str:
                    break

        except FileExistsError:
            print("错误！数据文件不存在")

        except Exception as e:
            print(e)

    def png_after_review(self):
        #if date_str in day_ls:

        day_count_ls[day_ls.index(date_str)] = str(eval(day_count_ls[day_ls.index(date_str)]) + today_count)

        #else:
        #    day_ls.append(date_str)
        #    day_count_ls.append(str(today_count))

        today_task.update_data()

        day_count_ls_eval = list(map(int, day_count_ls))
        day_max = int(date_str[-2:])
        count_max = max(day_count_ls_eval)

        def cut_day(day):
            if day[-2] == '0':
                return day[-1]
            else:
                return day[-2:]

        day_ls_cut = list(map(cut_day, day_ls))
        # print(day_count_ls)
        # print(day_count_ls_eval)

        #plt.title("有效复习单词个数统计图", fontsize=fs)
        x_label = today_task.month
        table = x_label+" 有效复习单词个数统计图"
        plt.axis([-1, day_max, -1, count_max+1])

        x_major_locator = MultipleLocator(1)
        y_major_locator = MultipleLocator(1)
        ax = plt.gca()
        # ax为两条坐标轴的实例
        ax.xaxis.set_major_locator(x_major_locator)
        # 把x轴的主刻度设置为1的倍数
        ax.yaxis.set_major_locator(y_major_locator)
        # 把y轴的主刻度设置为1的倍数

        plt.xlabel(table, fontproperties='SimHei', fontsize=12)
        #plt.xlabel(x_label, fontproperties='SimHei', fontsize=12)
        #plt.ylabel('当日有效复习单词个数', fontsize=12)
        plt.plot(day_ls_cut, day_count_ls_eval, 'ob--')
        plt.grid(True)

        #plt.figure(figsize=(2, 1))  # 图像大小

        name = '统计图\\' + date_str[:7] + '.png'
        plt.savefig(name, dpi=600)  # 生成PNG文件
        #plt.show()

    def update_data(self):
        with open(self.file, 'wt') as dcd_new:
            for i_day in range(len(day_ls)):
                dcd_new.write(day_ls[i_day]+':'+day_count_ls[i_day]+'\n')


t_now = time.gmtime()
date_str = time.strftime('%Y.%m.%d', t_now)
try:
    with open('data\\N_YEAR.data') as N_YEAR:
        n_year = N_YEAR.read()
        N_YEAR_DATA_ls = n_year.split(',')
        N_YEAR.close()
except IOError:
    tkm.showerror('ERROR', "IOError:请检查N_YEAR.data的存在性")

today_task = TaskV4(date_str[:7])
today_task.day_count_to_ls()


def ls_clear():
    word_ls.clear()
    translation_ch_ls.clear()
    translation_en_ls.clear()
    eff_rev_ls.clear()
    x_times_ls.clear()
    last_rev_date_ls.clear()
    d_position_ls.clear()


def get_info():
    try:
        ls_clear()
        with open('data\\单词数据.data', encoding='UTF-8') as data:
            all_data = data.readlines()
            for word_data in all_data:
                word_data = word_data.strip()
                word_data_ls = word_data.split(',')
                word_ls.append(word_data_ls[0])
                translation_ch_ls.append(word_data_ls[1])
                translation_en_ls.append(word_data_ls[2])
                eff_rev_ls.append(word_data_ls[3])
                x_times_ls.append(word_data_ls[4])
                last_rev_date_ls.append(word_data_ls[5])
                d_position_ls.append(word_data_ls[6])
            data.close()
    except IOError:
        tkm.showerror('ERROR', "IOError:请检查相关文档的存在性")


def update_data1():
    try:
        with open('data\\单词数据.data', 'wt', encoding='UTF-8') as data_nw:
            for p in range(len(word_ls)):
                d_position_ls[p] = str(N_YEAR_DATA_ls.index(date_str) - N_YEAR_DATA_ls.index(last_rev_date_ls[p]))
                data_nw.write(word_ls[p] + ',' + translation_ch_ls[p] + ',' + translation_en_ls[p] + ','
                              + eff_rev_ls[p]+','+x_times_ls[p]+','+last_rev_date_ls[p]+','+d_position_ls[p]+'\n')
            data_nw.close()
    except IOError:
        tkm.showerror('ERROR', "IOError:请检查相关文档的存在性")


def show_info_ask_n():
    global N, pass_code
    tkm.showinfo('提示', '请在隔壁小黑框输入\n计划复习多少个单词')
    N = input('今天想复习多少个单词?\n(请输入一个正整数):')
    while 1:
        global pass_code
        if not N.isdigit():
            pass_code = 0
        elif eval(N) <= 0:
            pass_code = 0
        elif eval(N)-eval(N)//1 != 0:
            pass_code = 0
        else:
            pass_code = 1
            break
        N = input('输入的格式错误，请重新输入\n请输入一个正整数:')
    N = eval(N)
    print('(请不要关闭小黑框,否则程序会终止哟)\n')
    tkm.showinfo('提示', '好的，现在开始')


get_info()
update_data1()
show_info_ask_n()
ls_clear()
get_info()

i = 0   #开始背单词后的计数


def one_review():
    global i
    global today_count  # 本次有效复习的计数
    p_num = random.randint(0, len(word_ls)-1)
    prob_draw = 0.8**(eval(eff_rev_ls[p_num]) - eval(x_times_ls[p_num])) + 0.01*eval(d_position_ls[p_num])
    if random.random() < prob_draw:
        prob_draw_str = '{:.2f}'.format(100*prob_draw)
        translation_zh = translation_ch_ls[p_num]
        translation_en = translation_en_ls[p_num]  #appid='20200526000471949', key='DWc3xD5IT2iDpsl1I7hF')
        rps = tkm.askquestion(title=word_ls[p_num]+'_weight:'+prob_draw_str+'%',
                              message=word_ls[p_num]+'，认识吗?\n完全清楚请选"是"\n否则请选"否"')
        if rps == 'yes':
            eff_rev_ls[p_num] = str(eval(eff_rev_ls[p_num])+1)
            last_rev_date_ls[p_num] = date_str
            today_count += 1
        if rps == 'no':
            rps2 = tkm.askquestion(title='参考翻译:',
                                   message='CH：'+translation_zh+'\nEN：'+translation_en+'\n模糊请选"是"\n完全没印象请选"否"')
            if rps2 == 'yes':
                x_times_ls[p_num] = str(round(eval(x_times_ls[p_num]) + 0.1, 1))
            if rps2 == 'no':
                x_times_ls[p_num] = str(eval(x_times_ls[p_num])+1)
        print(word_ls[p_num]+'\nCH：'+translation_zh+'\nEN：'+translation_en+'\n')

    else:
        i = i - 1


def review(n):
    global i
    while i < n:
        one_review()
        i += 1

    today_task.png_after_review()

    tkm.showinfo('提示', "完成!")


def update():
    with open('data\\单词数据.data', 'wt', encoding='UTF-8') as data_nw:
        for p in range(len(word_ls)):
            d_position_ls[p] = str(N_YEAR_DATA_ls.index(date_str) - N_YEAR_DATA_ls.index(last_rev_date_ls[p]))
            data_nw.write(word_ls[p] + ',' + translation_ch_ls[p] + ',' + translation_en_ls[p] + ','
                          + eff_rev_ls[p]+','+x_times_ls[p]+','+last_rev_date_ls[p]+','+d_position_ls[p]+'\n')
        data_nw.close()


def update_data2list():
    ls_clear()
    with open('data\\单词数据.data', encoding='UTF-8') as data:
        all_data = data.readlines()
        for word in all_data:
            word = word.strip()
            word_data_ls = word.split(',')
            word_ls.append(word_data_ls[0])
            translation_ch_ls.append(word_data_ls[1])
            translation_en_ls.append(word_data_ls[2])
            eff_rev_ls.append(word_data_ls[3])
            x_times_ls.append(word_data_ls[4])
            last_rev_date_ls.append(word_data_ls[5])
            d_position_ls.append(word_data_ls[6])
        data.close()

    with open('单词列表.csv', 'wt', encoding='UTF-8') as ls:
        ls.write('num,word,tran_ch,tran_en,eff_rev,x_time,interval\n')
        for ni in range(len(word_ls)):
            ls.write(str(ni+1) + ',')
            ls.write(word_ls[ni] + ',' + translation_ch_ls[ni] + ',' + translation_en_ls[ni] + ','
                     + eff_rev_ls[ni] + ',' + x_times_ls[ni] + ',' + d_position_ls[ni] + '\n')
        ls.close()


review(N)
update()
update_data2list()
