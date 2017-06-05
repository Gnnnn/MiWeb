#coding=utf-8
import MySQLdb
import jieba
import jieba.analyse


def searcharticle(words):
    jieba.analyse.set_stop_words('stopword.txt')
    jieba.load_userdict('dict_test.txt')
    print(words)
    tags = jieba.analyse.extract_tags(words)
    print(tags)
    sum = len(tags)
    keywords = ''
    for tag in tags:
        tag = ('').join(tag)
        keywords = keywords + tag + ' '
    db = MySQLdb.connect("localhost", "root", "fan123456", "miweb", charset="utf8")
    may = db.cursor()
    may.execute("""alter table article engine=MyISAM""")
    try:
        may.execute("""ALTER TABLE article ADD FULLTEXT INDEX index_keyword (keyword)""")
    except:
        pass
    db.commit()
    may.execute("""SELECT id,MATCH (keyword) AGAINST ('%s') as title_score FROM article WHERE MATCH (keyword) AGAINST ('%s') order by title_score DESC"""%(keywords,keywords))
    tt = may.fetchall()
    return tt,tags



#tt, tags = searcharticle('仿真 团队 需要 可以 发展 代码 ')
#print tt
#print tags[0]