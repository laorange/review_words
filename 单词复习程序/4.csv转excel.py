import pandas as pd


def csv_to_xlsx_pd():
    csv = pd.read_csv('单词列表.csv', encoding='utf-8')
    csv.to_excel('单词列表excel.xlsx', sheet_name='data')


if __name__ == '__main__':
    csv_to_xlsx_pd()