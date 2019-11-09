'''
from astdump import dumpattrs as dat
import ast

root = ast.parse('2+2')

print root

print ast.dump(root, include_attributes=True)

'''


'''
import ast

class MyVisitor(ast.NodeVisitor):
    def visit_Str(self, node):
        print('String Node: "' + node.s + '"')

class MyTransformer(ast.NodeTransformer):
    def visit_Str(self, node):
        return ast.Str('str: ' + node.s)


parsed = ast.parse("print('Hello World')")
MyTransformer().visit(parsed)
MyVisitor().visit(parsed)




def partition(alist,first,last):
   pivotvalue = alist[first]
   leftmark = first+1
   rightmark = last

   done = False
   while not done:
       while leftmark <= rightmark and alist[leftmark] <= pivotvalue:
           leftmark = leftmark + 1
       while alist[rightmark] >= pivotvalue and rightmark >= leftmark:
           rightmark = rightmark -1
       if rightmark < leftmark:
           done = True
       else:
           temp = alist[leftmark]
           alist[leftmark] = alist[rightmark]
           alist[rightmark] = temp
   temp = alist[first]
   alist[first] = alist[rightmark]
   alist[rightmark] = temp
   return rightmark

MyTransformer().visit(parsed)
MyVisitor().visit(parsed)

a = int(input("enter first number: "))
b = int(input("enter second number: "))

sum = a + b

print("sum:", sum)
'''

import ast
from pprint import pprint


def main():
    with open("/home/sr-p2irc-big14/Desktop/CloneData/AtCoder/abc001/A/4924321.py", "r") as source:
        tree = ast.parse(source.read())

    analyzer = Analyzer()
    analyzer.visit(tree)
    analyzer.report()


class Analyzer(ast.NodeVisitor):
    def __init__(self):
        self.stats = {"import": [], "from": []}

    def visit_Import(self, node):
        for alias in node.names:
            self.stats["import"].append(alias.name)
        self.generic_visit(node)

    def visit_ImportFrom(self, node):
        for alias in node.names:
            self.stats["from"].append(alias.name)
        self.generic_visit(node)

    def report(self):
        pprint(self.stats)


if __name__ == "__main__":
    main()

