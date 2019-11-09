from semanticpy.vector_space import VectorSpace
documents = []


def vector_document_mapping(path):
    f = open(path, 'r')
    content = f.read().replace('\n', ' ')
    content = ''.join([i for i in content if not i.isdigit()])
    # content = '"' + content + '"'
    content = content.replace('"""', '')
    content = content.replace('"', '')
    content = content.replace('#', '')
    stop_words = ['.', ',', '"', '?', '!', ':', ';', '(', ')', '[', ']', '{', '}', '#', '1', '2', '3', '4', "'"
                '5', '6', '7', '8', '9', '0', 'int', 'float', 'long', '=', '`', "''", "``", "==", '+', '-', '*', '/']
    for stop in stop_words:
        content = content.rstrip(stop)
    documents.append(content)


class VectorSpaceCreate():
    def __init__(self):
        self.documents = documents


    def vector_space_mapping(self):
        v = VectorSpace(self.documents)
        matrix = v.collection_of_document_term_vectors
        return matrix


def matrix_value(matrix):
    return matrix


