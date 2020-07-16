import time
import tkinter as tk
import tkinter.messagebox as tkm #弹窗库

root = tk.Tk()
root.withdraw()

word_ls = []
translation_ch_ls = []
translation_en_ls = []
eff_rev_ls = []
x_times_ls = []
last_rev_date_ls = []
d_position_ls = []

t_now = time.gmtime()
date_str = time.strftime('%Y.%m.%d', t_now)
try:
    with open('data\\N_YEAR.data') as N_YEAR:
        n_year = N_YEAR.read()
        ls_DATA = n_year.split(',')
        N_YEAR.close()
except IOError:
    tkm.showerror('ERROR', "IOError:请检查相关文档的存在性")


def get_info():
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


def get_change():
    word_change = input('请输入想要更改的单词:')
    if word_change in word_ls:
        p = word_ls.index(word_change)

        rps1 = tkm.askquestion(title=word_change,
                              message='CH：' + translation_ch_ls[p] + '\nEN：' + translation_en_ls[p]
                                       + '\n是否想要手动修改当前翻译?')
        if rps1 == 'yes':
            rps2 = tkm.askquestion(title=word_change,
                                   message='CH：' + translation_ch_ls[p] + '\nEN：' + translation_en_ls[p]
                                           + "\n修改中文请选'是',修改英文请选'否'")

            if rps2 == 'yes':
                translation_ch_nw = input('当前中文翻译为:'+translation_ch_ls[p]+'\n想要修改成什么？:')
                translation_ch_ls[p] = translation_ch_nw

            if rps2 == 'no':
                translation_en_nw = input('当前英文翻译为:'+translation_en_ls[p]+'\n想要修改成什么？:')
                translation_en_ls[p] = translation_en_nw

    else:
        tkm.showerror('ERROR', "未找到这个单词，请检查后重试")


def update_data():
    with open('data\\单词数据.data', 'wt', encoding='UTF-8') as data_nw:
        for p in range(len(word_ls)):
            d_position_ls[p] = str(ls_DATA.index(date_str) - ls_DATA.index(last_rev_date_ls[p]))
            data_nw.write(word_ls[p] + ',' + translation_ch_ls[p] + ',' + translation_en_ls[p] + ',' + eff_rev_ls[p]
                          + ',' + x_times_ls[p] + ',' + last_rev_date_ls[p] + ',' + d_position_ls[p] + '\n')
        data_nw.close()


def update_data2list():
    with open('单词列表.csv', 'wt', encoding='UTF-8') as ls:
        ls.write('num,word,tran_ch,tran_en,eff_rev,x_time,interval\n')
        for ni in range(len(word_ls)):
            ls.write(str(ni + 1) + ',')
            ls.write(word_ls[ni] + ',' + translation_ch_ls[ni] + ',' + translation_en_ls[ni] + ','
                     + eff_rev_ls[ni] + ',' + x_times_ls[ni] + ',' + d_position_ls[ni] + '\n')
        ls.close()
        tkm.showinfo('提示', "更新完成\n在'单词列表'中可以查看更新后的数据了")


try:
    get_info()
    while True:
        get_change()
        rps = tkm.askquestion(title='是否继续修改', message='是否继续修改?')
        if rps == 'no':
            break
    update_data()
    update_data2list()
except Exception as e:
    tkm.showerror('ERROR', e)
