from Initialization import *
import os
import re


class DocSim(object):
    def __init__(self, w2v_model , stopwords=[]):
        self.w2v_model = w2v_model
        self.stopwords = stopwords

    def vectorize(self, doc):
        """Identify the vector values for each word in the given document"""
        doc = doc.lower()
        words = [w for w in doc.split(" ") if w not in self.stopwords]
        word_vecs = []
        for word in words:
            try:
                vec = self.w2v_model[word]
                word_vecs.append(vec)
            except KeyError:
                # Ignore, if the word doesn't exist in the vocabulary
                pass

        # Assuming that document vector is the mean of all the word vectors
        # PS: There are other & better ways to do it.
        vector = np.mean(word_vecs, axis=0)
        return vector

    def _cosine_sim(self, vecA, vecB):
        """Find the cosine similarity distance between two vectors."""
        csim = np.dot(vecA, vecB) / (np.linalg.norm(vecA) * np.linalg.norm(vecB))
        if np.isnan(np.sum(csim)):
            return 0
        return csim

    def calculate_similarity(self, source_doc, target_docs=[], threshold=0):
        """Calculates & returns similarity scores between given source document & all
        the target documents."""
        if isinstance(target_docs, str):
            target_docs = [target_docs]

        source_vec = self.vectorize(source_doc)
        results = []
        for doc in target_docs:
            target_vec = self.vectorize(doc)
            sim_score = self._cosine_sim(source_vec, target_vec)
            if sim_score > threshold:
                results.append({
                    'score' : sim_score,
                    'doc' : doc
                })
            # Sort results by score in desc order
            results.sort(key=lambda k : k['score'] , reverse=True)

        return results

    def calculate_doc_similarity(self, source_doc, target_doc, threshold=0):
        """Calculates & returns similarity scores between given source document & all
        the target documents."""

        source_vec = np.load(os.path.join(dataFolder, source_doc))
        target_vec = np.load(os.path.join(dataFolder, target_doc))
        sim_score = self._cosine_sim(source_vec, target_vec)
        # del source_vec
        # del target_vec
        # gc.collect()

        return sim_score

    def create_vector(self, fileName):
        """Identify the vector values for each word in the given document and write it is a file"""
        doc = open(os.path.join(dataFolder, fileName)).read()
        doc = doc.lower()
        words = [w for w in doc.split(" ") if w not in self.stopwords]
        word_vecs = []
        for word in words:
            try:
                vec = self.w2v_model[word]
                word_vecs.append(vec)
            except KeyError:
                # Ignore, if the word doesn't exist in the vocabulary
                pass
        vector = np.mean(word_vecs, axis=0)  # Vector Created

        fileName = re.sub('_description.txt', '', fileName)
        fileName = fileName + '.npy'
        np.save(os.path.join(dataFolder, fileName), vector)
        print (fileName + ' saved. ')