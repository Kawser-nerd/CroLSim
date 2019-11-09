import xlsxwriter
import numpy as np
from functools import partial
from operator import is_not
from nltk.tokenize import word_tokenize
import os


threshHold = 0.90
dataFolder = "/home/sr-p2irc-big14/grive/test_jhot"
modelPath = "/home/sr-p2irc-big14/grive/Tester_Word/GoogleNews-vectors-negative300.bin.gz"
wb = xlsxwriter.Workbook('Clones90.xlsx')
ws = wb.add_worksheet('Clones')

clones = []

count = 0
comparison = 0
