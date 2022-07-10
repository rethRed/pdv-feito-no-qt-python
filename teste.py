import sqlite3,os


c = os.getcwd()








banco = sqlite3.connect(fr"{c}\\DataBase\\produtos.db",check_same_thread=False)

cursor = banco.cursor()

tempo = cursor.execute("select date('now','localtime','start of year')").fetchall()[0][0]


for i in range(12):


    print(cursor.execute(''' 





    ''').fetchall())






