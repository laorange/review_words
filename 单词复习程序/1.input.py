import time
import tkinter as tk
import tkinter.messagebox as tkm #弹窗库

#translate
import random
import requests
import json
import hashlib

root = tk.Tk()
root.withdraw()

t_now = time.gmtime()
date_str = time.strftime('%Y.%m.%d', t_now)
with open('data\\N_YEAR.data') as N_YEAR:
    n_year = N_YEAR.read()
    ls_DATA = n_year.split(',')
    N_YEAR.close()

word_ls = []
translation_ch_ls = []
translation_en_ls = []
eff_rev_ls = []
x_times_ls = []
last_rev_date_ls = []
d_position_ls = []

with open('data//百度翻译_appid&密钥.txt', encoding='UTF-8') as id_key:
    id_key_ls = id_key.readlines()
    appid = id_key_ls[0].strip().split('：')[1]
    key = id_key_ls[1].strip().split('：')[1]


#清空'在这里导入单词.txt'
def clear():
    rps = tkm.askquestion(title='Finally', message="是否清空\n'在这里导入单词.txt'中的现有内容?") #resurn 'yes' or 'no'
    if rps == 'yes':
        with open('在这里导入单词.txt', 'wt', encoding='UTF-8') as clear_target:
            clear_target.write('')
            clear_target.close()
        tkm.showinfo('提示', "完成!")


def translate(q, f='fra', to='zh', appid=appid, key=key):#, appid='20200526000471661', key='7BrvzDUh0TzlcYSQ0sMP'
    def md5_sign(s):
        return hashlib.md5(s.encode('utf8')).hexdigest()
    url = "http://api.fanyi.baidu.com/api/trans/vip/translate"
    salt = random.randint(32768, 65536) #salt='1435660288'
    finial_str = '%s%s%s%s' % (appid, q, salt, key)
    sign = md5_sign(finial_str)
    params = {
        'q': q,
        'from': f,
        'to': to,
        'appid': appid,
        'salt': salt,
        'sign': sign,
    }
    try:
        res_json = requests.get(url, params=params).json()
        res = res_json['trans_result'][0]["dst"]
        return res
    except Exception as e:
        print(e)
        return ''


try:
    with open('data\\单词数据.data', encoding='UTF-8') as data:
        all_data = data.readlines()
        i = 0
        for word_data in all_data:
            word_data = word_data.strip()
            word_data_ls = word_data.split(',')
            word_ls.append(word_data_ls[0])
        data.close()

    with open('在这里导入单词.txt', encoding='UTF-8') as source:
        word_today = source.readlines()

        if len(word_today) == 0:
            raise TabError  # '在这里导入单词.txt'为空

        with open('data\\单词数据.data', 'at', encoding='UTF-8') as data:
            compete = 0
            progress = 1
            for word in word_today:
                print('\r当前进度:{}/{}'.format(progress, len(word_today)), end='')
                progress += 1
                word = word.strip()
                if word in word_ls:
                    compete += 1
                    continue
                translation_ch = translate(word)
                time.sleep(1) #百度翻译api限制
                translation_en = translate(word, to='en')
                time.sleep(1) #百度翻译api限制
                data.write(word+','+translation_ch+','+translation_en+',0,0,' + date_str + ',0' + '\n')

            if compete == len(word_today):
                raise IndentationError  # 这些单词已经添加过了,随便用的错误类型
            elif compete > 0:
                print('\n本次想要添加的{}个单词中有{}个单词已在列表中,已忽略\n成功添加了{}个单词!'.format(len(word_today),
                                                                         compete, len(word_today)-compete))

            data.close()
        source.close()
    word_ls.clear()

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

    with open('单词列表.csv', 'wt', encoding='UTF-8') as ls:
        ls.write('num,word,tran_ch,tran_en,eff_rev,x_times,interval\n')
        for i in range(len(word_ls)):
            ls.write(str(i+1) + ',')
            ls.write(word_ls[i] + ',' + translation_ch_ls[i] + ',' + translation_en_ls[i] + ','
                     + eff_rev_ls[i] + ',' + x_times_ls[i] + ',' + d_position_ls[i] + '\n')
        ls.close()
        tkm.showinfo('提示', "成功导入数据\n可在'单词列表'中查看")


except IndentationError:
    tkm.showinfo('提示', "这些单词已经添加过了哟\n已忽略本次操作")
    clear()

except TabError:
    tkm.showerror('ERROR', "文档'在这里导入单词.txt'为空\n请输入内容")

except IOError:
    tkm.showerror('ERROR', "IOError:请检查相关文档的存在性")

except Exception as e:
    tkm.showerror('ERROR', e)

else:
    clear()
