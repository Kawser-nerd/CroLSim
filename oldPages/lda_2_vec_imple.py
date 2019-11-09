import os
import pickle
from lda2vec import preprocess, Corpus
import numpy
from mudablue import stop_words_stemming


result_folder = '/home/kwnafi/PycharmProjects/MudaBlue/Results'


def text_prep(text_doc, count):
    text_doc = [digit_removal(d) for d in text_doc]
    text_doc = [stop_word_removal(d) for d in text_doc]
    maxlength_doc = 80000
    text_doc = [unicode(clean(d)) for d in text_doc]
    print(text_doc)
    tokens, vocab = preprocess.tokenize(text_doc, maxlength_doc, merge=False, n_threads=4)
    print(tokens, vocab)
    corpus = Corpus()
    corpus.update_word_count(tokens)
    corpus.finalize()
    compact = corpus.to_compact(tokens)
    pruned = corpus.filter_count(compact, min_count=50)
    bow = corpus.compact_to_bow(pruned)
    clean_data = corpus.subsample_frequent(pruned)
    doc_ids = numpy.arange(pruned.shape[0])
    flattened, (doc_ids,) = corpus.compact_to_flat(pruned, doc_ids)
    assert flattened.min() >= 0
    pickle.dump(vocab, open(os.path.join(result_folder, str(count) + 'vocab.pkl'), 'w'))
    pickle.dump(corpus, open(os.path.join(result_folder, str(count) + 'corpus.pkl'), 'w'))
    numpy.save("flattened", flattened)
    numpy.save("doc_ids", doc_ids)
    numpy.save("pruned", pruned)
    numpy.save("bow", bow)


def clean(line):
    bad = set(["ax>", '`@("', '---', '===', '^^^'])
    return ' '.join(w for w in line.split() if not any(t in w for t in bad))


def stop_word_removal(line):
    return stop_words_stemming(line)


def digit_removal(line):
    return ' '.join([i for i in line.split() if not i.isdigit()])
