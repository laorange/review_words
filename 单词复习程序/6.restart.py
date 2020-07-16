import tkinter as tk
import tkinter.messagebox as tkm #弹窗库

root = tk.Tk()
root.withdraw()

continue_num = 0

try:
    rps1 = tkm.askquestion(title='提示', message='该操作将清空所有现有数据,确认吗')
    if rps1 == 'yes':
        rps2 = tkm.askquestion(title='提示', message='该操作无法撤销,将清空所有现有数据\n确认吗?')
        if rps2 == 'yes':
            continue_num = 1
    if continue_num == 1:
        with open('单词列表.csv', 'wt', encoding='UTF-8') as ls:
            ls.write('')
            ls.close()
        with open('data\\单词数据.data', 'wt', encoding='UTF-8') as data:
            data.write('')
            data.close()
        tkm.showinfo('提示', "已清空当前所有数据")

except:
    tkm.showerror('ERROR', "程序发生未知错误")
