#!/usr/bin/env python
# -*- coding: utf-8 -*-

import jieba
import mysql.connector

class WordSeg(object):

    db = 'lagou'
    user = 'root'
    passwd = ''

    def __init__(self):
        self.dbc = mysql.connector.connect(
                user = self.user,
                passwd = self.passwd,
                host = 'localhost',
                database = self.db
                )
        self.cursor = self.dbc.cursor()
        self.cursor.execute('set names utf8')
        self.load_ignoring()

    # XXX this class should not hold other objects,
    # or else it will not be called.
    # see this link for details:
    # http://eli.thegreenplace.net/2009/06/12/safely-using-destructors-in-python
    def __del__(self):
        self.cursor.close()
        self.dbc.close()

    def load_ignoring(self):
        query = "select word from ignored_word"
        self.cursor.execute(query)
        ignored = {}
        for word in self.cursor:
            ignored[word[0]] = 1
        self.ignored_words = ignored

    def segment(self):
        query = "select job_desc from job_desc"
        self.cursor.execute(query)

        all_jd = ''
        for jd in self.cursor:
            all_jd = all_jd + jd[0]

        counter = {}
        for seg in jieba.cut(all_jd):
            seg = seg.lower()
            if seg in self.ignored_words:
                continue
            if seg not in counter:
                counter[seg] = 0
            else:
                counter[seg] = counter[seg] + 1

        for (word, cnt) in counter.iteritems():
            self.cursor.execute(
                    "insert into word_frequency (word, cnt) values (%s, %s)",
                    (word, cnt)
                    )

if '__main__' == __name__:
    ws = WordSeg()
    ws.segment()
