#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Author: 52nlpcn@gmail.com
# Copyright 2015 @ NLPJob

import codecs
import sys

from langconv import *
from pinyin import PinYin
py = PinYin()
py.load_word()

def make_word_4tag(word):
    if len(word) == 0:
        return "N"
    if len(word) == 1:
        return "S"
    else:
        tag = "B"
        for w in word[1:len(word)-1]:
            tag += "M"
        tag += "E"
        return tag

def make_mecab_train_data(input_file, output_file):
    input_data = codecs.open(input_file, 'r', 'utf-8')
    output_data = codecs.open(output_file, 'w', 'utf-8')
    for line in input_data.readlines():
        word_list = line.strip().split()
        if len(word_list) == 0: continue
        for word in word_list:
            words = word.split("/")
            pword = py.hanzi2pinyin_split(string=words[0], split='_')
            if pword.strip() == "":
                pword = words[0]
            fword = Converter('zh-hant').convert(words[0])
            tag = make_word_4tag(words[0])
            output_data.write(words[0] + "\t" + words[1][0] + "," +
                    words[1] + "," + tag + "," + str(len(words[0])) + "," +
                    words[0] + "," + pword + "," + fword + "\n")
        output_data.write("EOS\n")
    input_data.close()
    output_data.close()

if __name__ == '__main__':
    if len(sys.argv) < 3:
        print "pls use: python make_mecab_train_data.py input output"
        sys.exit()
    input_file = sys.argv[1]
    output_file = sys.argv[2]
    make_mecab_train_data(input_file, output_file)
