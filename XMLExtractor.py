'''

import xml.etree.ElementTree as ET
import os
import re


cwd = os.getcwd()
xmlReader = open(os.path.join(cwd, 'Corpus/JHotDraw54b1_functions.xml'), 'r').read()

tree = ET.fromstring(re.sub(r"(<\?xml[^>]+\?>)", r"\1<root>", xmlReader) + "</root>")
for node in tree.iter('entry'):
    print('\n')
    for elem in node.iter():
        if not elem.tag==node.tag:
            print("{}: {}".format(elem.tag, elem.text))

'''

from bs4 import BeautifulSoup
import os
import shutil


fileName = 'JHotDraw54b1_functions.xml' # Change the name of the file to extract

cwd = os.getcwd()
xmlReader = open(os.path.join(cwd, 'Corpus/' + fileName))

soup = BeautifulSoup(xmlReader, "lxml")
fragments = soup.find_all('source')
folderName = fileName.split('.')[0]
print folderName
projectPath = os.path.join(cwd, 'Corpus/' + folderName)
if os.path.exists(projectPath):
    shutil.rmtree(projectPath)
os.makedirs(projectPath)

count = 0
for f in fragments:
    fragmentName = folderName + 'fragment_' + str(count)
    with open(os.path.join(projectPath, fragmentName), 'w+') as frg:
        methodBlock = f.text
        frg.write(methodBlock)
    frg.close()
    count += 1


