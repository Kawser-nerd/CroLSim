import textmining
import csv
import math
from scipy import linalg, dot, spatial
import numpy
from nltk import tokenize, stem
from nltk.corpus import stopwords
import os
import string
import porterstemmer


tdm = textmining.TermDocumentMatrix()
counter = 0


def term_document_matrix(path):
    f = open(path, 'r')
    content = f.readlines()
    content = ''.join([i for i in content if not i.isdigit()])
    content = stop_words_stemming(content)
    print(content)
    tdm.add_doc(content)


def csv_file_to_matrix(path):
    with open(path, 'r') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        list_of_list = []
        j = 0
        lines = [line for line in csv_reader]
        for i in range(len(lines)):
            list_ = []
            if len(lines) <= i + j:
                break
            first = lines[i + j][0]
            while first == lines[i + j][0]:
                list_.append(lines[i + j][2])
                j += 1
                if len(lines) <= i + j:
                    break
            j -= 1
            list_of_list.append(list(map(float, list_)))
    return list_of_list


def tfidfTransform(matrix):
    """ Apply TermFrequency(tf)*inverseDocumentFrequency(idf) for each matrix element.
            This evaluates how important a word is to a document in a corpus

            With a document-term matrix: matrix[x][y]
                tf[x][y] = frequency of term y in document x / frequency of all terms in document x
                idf[x][y] = log( abs(total number of documents in corpus) / abs(number of documents with term y)  )
            Note: This is not the only way to calculate tf*idf
        """
    matrix_float = numpy.zeros(matrix.shape)
    document_Total = len(matrix)
    rows, cols = matrix.shape
    for row in xrange(0, rows):  # For each document
        wordTotal = reduce(lambda x, y: x + y, matrix[row])
        for col in xrange(0, cols):  # For each term
            # For consistency ensure all self.matrix values are floats
            matrix[row][col] = float(matrix[row][col])
            if matrix[row][col] != 0:
                term_document_occurences = __getTermDocumentOccurences(col, matrix)
                term_frequency = matrix[row][col] / float(wordTotal)
                inverse_document_frequency = math.log(abs(document_Total / float(term_document_occurences)))
                # print(term_document_occurences, term_frequency, inverse_document_frequency, term_frequency *
                # inverse_document_frequency)
                matrix_float[row][col] = term_frequency * inverse_document_frequency
                # print(matrix_float[row][col])
    return matrix_float


def __getTermDocumentOccurences(col, matrix):
    """ Find how many documents a term occurs in"""
    term_document_occurances = 0
    rows, cols = matrix.shape
    for n in xrange(0, rows):
        if matrix[n][col] > 0:  # Term appears in document
            term_document_occurances += 1
    return term_document_occurances


def lsa(matrix):
    rows, cols = matrix.shape
    # Sigma comes out as a list rather than a matrix
    u, sigma, vt = linalg.svd(matrix)
    # Dimension reduction, build SIGMA'
    # for index in xrange((rows - 1), rows):
    #    sigma[index] = 0
    # Reconstruct MATRIX'
    transformed_matrix = dot(dot(u, linalg.diagsvd(sigma, len(matrix), len(vt))), vt)
    return transformed_matrix


def cosine_similar(matrix):
    rows, cols = matrix.shape
    matrix_cosine = numpy.zeros((rows, rows), dtype=numpy.float64)
    for n in xrange(0, rows):
        software_1 = matrix[n]
        for p in xrange(0, rows):
            software_2 = matrix[p]
            print(spatial.distance.cosine(software_1, software_2))
            matrix_cosine[n][p] = 1 - spatial.distance.cosine(software_1, software_2)
            # print(matrix_cosine[n][p])
    return matrix_cosine


def stop_words_stemming(doc):
    stop_words = set(stopwords.words('english'))
    stop_words.update(['.', ',', '"', '?', '!', ':', ';', '(', ')', '[', ']', '{', '}', '#', '1', '2', '3', '4',
                       '5', '6', '7', '8', '9', '0', 'int', 'float', 'long', '=', '`', "''", "``", "==", '+', '-', '*'])
    term_list = []
    porter = stem.porter.PorterStemmer()
    doc = doc.lower()
    doc = doc.replace('.', ' ')
    doc = doc.replace('/', ' ')
    for term in tokenize.word_tokenize(doc):
        if term not in stop_words:
            term1 = porter.stem(term)
            term_list.append(term1)
    term_list = ' '.join(term_list)
    # term_list = set((term for term in term_list))  # duplicate remove
    # print(term_list)
    return term_list
    # for term in doc:
    #    print(term)
    #    term_list = [porter.stem(i.lower()) for i in tokenize.wordpunct_tokenize(term) if i.lower() not in stop_words]
    # return term_list


def word_vector_index(doc):
    vector_index = {}
    offset = 0
    for term in doc:
        vector_index[term] = offset
        offset += 1
    print(vector_index)
    return vector_index


def vector_create(path):
    projects = os.listdir(path)
    doc_array = []
    for f in projects:
        files = os.listdir(os.path.join(path, f))
        if 'Source_Join.txt' in files:
            vf = open(os.path.join(path, f, 'Source_Join.txt'), 'r')
            doc = vf.read().replace('\n', ' ')
            print(doc)
            doc_array.append(doc)
        doc_array.append('\n')
    # print(doc_array)
    doc = ' '.join(doc_array)
    doc.lower()
    doc = doc.split(" ")
    doc = stop_words_stemming(doc)
    vector_index = word_vector_index(doc)
    matrix = [vector_count(doc, vector_index) for doc in doc_array]
    print(matrix)
    return matrix


def vector_count(doc, vector_index):
    vector_len = len(vector_index)
    vector = [0] * vector_len
    for term in doc:
        t = vector_index[term]
        print(t)
        vector[t] += 1
    return vector






