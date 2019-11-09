import os
import nltk
from gensim.models.keyedvectors import KeyedVectors
from DocSim import DocSim
import gc
import multiprocessing as mp
from Initialization import *


docs = []
listofFiles = os.listdir(dataFolder)
is_noun = lambda pos: pos[:2] == 'NN'
is_verb = lambda pos: pos[:2] == 'VB'
# word vector learning
'''
print "loading the model"
w2v_model = KeyedVectors.load_word2vec_format(modelPath, binary=True)
ds = DocSim(w2v_model)
'''
'''
class MyThread(threading.Thread):

    def __init__(self, name, sourceDoc, targetDoc):
        threading.Thread.__init__(self)
        self.name = name
        self.sourceDoc = sourceDoc
        self.targetDoc = targetDoc

    def w2vDocSimilarity(self):
        w2vDocSimilarity(self.sourceDoc, self.targetDoc)

    def run(self):
        print("starting Thread " + self.name)              # "Thread-x started!"
        self.w2vDocSimilarity()
        print("finished Thread " + self.name)              # "Thread-x finished!"
        gc.collect()
        if threading.active_count == 6:
            threading.Thread.join()
'''


def w2vDocSimilarity(dataFiles):
    sourceDoc = dataFiles[0]
    sourceVec = dataFiles[1]
    targetDoc = dataFiles[2]
    targetVec = dataFiles[3]
    global count
    global comparison
    global threshHold
    global clones
    print 'comparison: ' + str(comparison)
    comparison += 1
    print "Working on: " + sourceDoc + ' ' + targetDoc
    simScore = calculate_vector_similarity(sourceVec, targetVec)
    print "simscore: " + str(simScore)
    if simScore >= threshHold:
        '''
        ws.write(count, 0, sourceDoc)
        ws.write(count, 1, targetDoc)
        ws.write(count, 2, str(simScore))
        '''

        row = []
        row.append(sourceDoc)
        row.append(targetDoc)
        row.append(str(simScore))
        '''
        clones.append(row)
        count += 1
        print "count: " + str(count)
        '''
        return row
    gc.collect()


def calculate_vector_similarity(vector1, vector2):
    csim = np.dot(vector1, vector2) / (np.linalg.norm(vector1) * np.linalg.norm(vector2))
    if np.isnan(np.sum(csim)):
        return 0
    return csim

'''
# verbs nouns selection
for desFiles in listofFiles:
    if desFiles.endswith('.txt'):
        if os.stat(os.path.join(dataFolder, desFiles)).st_size != 0:
            docs.append(desFiles)
            print('working: ' + desFiles)

            f = open(os.path.join(dataFolder, desFiles))
            lines = f.read()
            f.close()
            tokenized = nltk.word_tokenize(lines)
            nouns = [word for (word, pos) in nltk.pos_tag(tokenized) if is_noun(pos)]
            verbs = [word for (word, pos) in nltk.pos_tag(tokenized) if is_verb(pos)]

            with open(os.path.join(dataFolder, desFiles), 'w') as f:
                for word in nouns:
                    f.write(word + ' ')
                for word in verbs:
                    f.write(word + ' ')
            f.close()

print('Docs are ready')
gc.collect()
print "Preparing Vector Data with Multiprocessing"



def create_vector(fileName):
    ds.create_vector(fileName)

#dataFilesForVector = tuple(docs)

number_workers = mp.cpu_count()
print ('number of workers: ' + str(number_workers))
pool = mp.Pool(number_workers)
pool.map(create_vector, docs)
pool.close()
pool.join()

print ('Vector Creation Finished')
gc.collect()
'''

# Comparison Steps

dataFiles = []
docs = []
listofFiles = os.listdir(dataFolder)
for desFiles in listofFiles:
    if desFiles.endswith('.npy'):
        if os.stat(os.path.join(dataFolder, desFiles)).st_size != 0:
            docs.append(desFiles)
            print('working: ' + desFiles)

# array creation
for i in range(len(docs)):
    for j in range((i+1), len(docs)):
        row = []
        row.append(docs[i])
        row.append(np.load(os.path.join(dataFolder, docs[i])))
        row.append(docs[j])
        row.append(np.load(os.path.join(dataFolder, docs[j])))
        dataFiles.append(row)
print ("Datafiles are ready. Total Comparison: " + str(len(dataFiles)))

poolValues = tuple(dataFiles)

number_workers = mp.cpu_count()
print ('number of workers: ' + str(number_workers))
pool = mp.Pool(number_workers)
p = pool.map(w2vDocSimilarity, poolValues)
pool.close()
pool.join()
row = 0
print len(p)

clones = filter(partial(is_not, None), p)

print len(clones)

for sourceDoc, targetDoc, simScore in clones:
    ws.write(row, 0, sourceDoc)
    ws.write(row, 1, targetDoc)
    ws.write(row, 2, simScore)
    row += 1

wb.close()


'''
# Comparison with threading
for i in range(0, len(docs)):
    for j in range(i + 1, len(docs)):
        sourceDoc = docs[i]
        targetDoc = docs[j]
        gc.collect()
        mythread = MyThread(str(j % 6), sourceDoc, targetDoc)           # Thread Starts
        mythread.start()
'''







