import ast
import os
import code_comment
import fnmatch
import re


class CallCollector(ast.NodeVisitor):
    def __init__(self):
        self.calls = []
        self._current = []
        self._in_call = False

    def visit_Call(self, node):
        self._current = []
        self._in_call = True
        self.generic_visit(node)

    def visit_Attribute(self, node):
        if self._in_call:
            self._current.append(node.attr)
        self.generic_visit(node)

    def visit_Name(self, node):
        if self._in_call:
            self._current.append(node.id)
            self.calls.append('.'.join(self._current[::-1]))
            # Reset the state
            self._current = []
            self._in_call = False
        self.generic_visit(node)


def API_Extraction(project, filepath, directory):
    projectname = project + '_api.txt'
    projectPath = os.path.join(directory, projectname)
    if os.path.isfile(projectPath):
        fileCreate = open(projectPath, 'a+')
    else:
        fileCreate = open(projectPath, 'w+')

    fileRead = open(filepath).readlines()  # Source code read
    for line in fileRead:
        if re.search('^import', line):
            fileCreate.write(line)
            fileCreate.write('\n')

    fileRead = open(filepath).read()  # Source code read
    tree = ast.parse(fileRead)   # ASTree Generation
    cc = CallCollector()
    cc.visit(tree)
    nodes = cc.calls
    for n in nodes:
        fileCreate.write(n)
        fileCreate.write('\n')
    fileCreate.close()


def Comment_Extraction(project, filepath, directory):
    projectname = project + '_comment.txt'
    projectPath = os.path.join(directory, projectname)
    # fileRead = open(filepath).read()  # Source code read
    if os.path.isfile(projectPath):
        fileCreate = open(projectPath, 'a+')
    else:
        fileCreate = open(projectPath, 'w+')

    comments = code_comment.extract(filepath)
    for comm in comments:
        fileCreate.write(comm.body_str)
        fileCreate.write(' ')
    fileCreate.close()


def ReadMe_Extraction(project, directory):
    projectname = project + '_readme.txt'
    projectPath = os.path.join(directory, projectname)
    if os.path.isfile(projectPath):
        fileCreate = open(projectPath, 'a+')
    else:
        fileCreate = open(projectPath, 'w+')
    projectFolder = os.path.join(directory, project)
    for file in os.listdir(projectFolder):
        if fnmatch.fnmatch(file.lower(), 'readme.*'):
            fileRead = open(os.path.join(projectFolder, file)).read()
            fileCreate.write(fileRead)





