# -*- coding: utf-8 -*-
from gensim.utils import simple_preprocess
from gensim.models.doc2vec import Doc2Vec, TaggedDocument, DocvecsArray
from smart_open import smart_open
import os
from tkinter import *
import tkFileDialog


currentFolder = os.getcwd()