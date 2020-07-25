import pymysql

dbparams = {
            'host':'127.0.0.1',
            'user':'root',
            'password':'mysqlroot',
            'port':3306,
            'database':'jianshu',
            'charset':'utf8',
        }
conn = pymysql.connect(**dbparams)
cursor = conn.cursor()

sql = "insert into article(id,title,content,author,article_id,origin_url) values(null,%s,%s,%s,%s,%s)"
cursor.execute(sql,('title','content','author','article_id','origin_url'))
conn.commit()