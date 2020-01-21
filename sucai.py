import requests
import xlrd

flbrd = "词库.xlsx"
ws = xlrd.open_workbook(flbrd)
sheet_names = ws.sheet_names()

sheet_num = 2
wp = ws.sheet_by_name(sheet_names[sheet_num])
row_num = wp.nrows

for i in range(0, row_num):
    word = wp.cell_value(i, 0)
    word = word.lower()
    # url = "https://ssl.gstatic.com/dictionary/static/sounds/oxford/" + word + "--_gb_1.mp3"
    url = "http://dict.youdao.com/dictvoice?type=1&audio=" + word
    r = requests.get(url)
    print(r.status_code)
    if r.status_code == 404:
        print(word)
        continue
    path = "C:/Users/14114/Downloads/" + word + ".mp3"
    with open(path, "wb") as f:
        f.write(r.content)
    f.close()
print('complete')