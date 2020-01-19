from app.models import Word
import xlrd
import sqlite3


db = sqlite3.connect("app.db")
flbrd = "词库.xlsx"
ws = xlrd.open_workbook(flbrd)
sheet_names = ws.sheet_names()

sheet_num = 1
word_subject = sheet_names[sheet_num]
wp = ws.sheet_by_name(sheet_names[sheet_num])
row_num = wp.nrows

print(db.execute("select word from Word where word = 'apple'") )
print(Word.query.filter(Word.word=='apple'))
for i in range(0, row_num):
    word = wp.cell_value(i, 0)
    word = word.lower()
    if len(Word.query.filter_by(word=word).all()):
        continue
    new_word = Word()
    attr = {}
    attr['word'] = word
    attr['meaning'] = wp.cell_value(i,1)
    attr['word_subject'] = word_subject
    new_word.set_attr(attr)
    db.session.add(new_word)
    db.session.commit()