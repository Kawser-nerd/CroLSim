from Tkinter import *
import tkFileDialog
import os
from xml.etree.ElementTree import Element, SubElement, Comment, ElementTree
from validators import url
from BeautifulSoup import BeautifulSoup
import urllib2
import sys


reload(sys)
sys.setdefaultencoding('utf-8')


root = Tk()
root.minsize(width=200, height=200)


def Button_OnClick():
    if len(entry1.get()) != 0:
        if url(entry1.get()):
            # page = requests.get(entry1.get())
            # tree = html.fromstring(page.content)
            # com = tree.xpath('//div[@class="body"]/text()')
            entry1['state'] = 'disabled'
            page_link = entry1.get()
            html_page = urllib2.urlopen(page_link)
            soup = BeautifulSoup(html_page)
            with open('links.txt', 'a') as f:
                for link in soup.findAll('a'):
                    temp_link = str(link.get('href'))
                    if "http:/" not in temp_link:
                        inner_link = page_link + "/../" + link.get('href')    # page link reformulation
                        print(inner_link)
                        f.writelines(inner_link)
                        f.writelines('\n')
                        html_page = urllib2.urlopen(inner_link)
                        soup1 = BeautifulSoup(html_page)
                        for link1 in soup1.findAll('a'):
                            inner_link1 = inner_link + "/../" + link1.get('href')    # page link reformulation
                            f.writelines(inner_link1)
                            f.writelines('\n')
                    else:
                        continue
        else:
            entry1.delete(0, 'end')
            entry1.insert(0, "Enter Valid Url")
    else:
        entry1.delete(0, 'end')
        entry1.insert(0, "enter Url")


def Button_OnClick2():
    if len(entry2.get()) != 0:
        top = Element(entry2.get())
        comment = Comment('Extracted Function Document for' + entry2.get())
        top.append(comment)
        with open('links.txt') as f:
            for visited_link in f:
                try:
                    html_page = urllib2.urlopen(visited_link)
                    print(visited_link)
                    soup = BeautifulSoup(html_page)
                    # soup = BeautifulSoup(open('test.html'))
                    for tag in soup.findAll('div', attrs={"class": "section"}):
                        if tag.find('p') is not None:
                            # tag_id = u''.join(tag.get('id')).encode('utf-8').strip()
                            print tag.get('id')
                            div_id = SubElement(top, tag.get('id'))
                            # tag_id_text = u''.join(tag.find('p').text).encode('utf-8').strip()
                            print tag.find('p').text
                            div_id.text = tag.find('p').text
                        else:
                            continue
                except urllib2.HTTPError as err:
                    print err.code
                    print visited_link
                    continue
                except urllib2.URLError as urlerr:
                    print urlerr.message
                    continue
        tree = ElementTree(top)
        tree.write(entry2.get() + '.xml')
    else:
        entry2.insert(0, "Enter Project Name")


def Button_OnClick3():
    root.withdraw()
    sys.exit(None)


def elements_equal(e1, e2):
    if type(e1) != type(e2):
        return False
    if e1.tag != e1.tag: return False
    if e1.text != e2.text: return False
    if e1.tail != e2.tail: return False
    if e1.attrib != e2.attrib: return False
    if len(e1) != len(e2): return False
    return all([elements_equal(c1, c2) for c1, c2 in zip(e1, e2)])


def Button_OnClick4():
    path = tkFileDialog.askopenfilename()
    selected_file_name = os.path.basename(path)
    tree = ElementTree()
    tree.parse(path)
    tree_root = tree.getroot()
    prev = None
    #for page in tree_root:  # iterate over pages
    #    print page
    for page in tree_root:
        print page
        elems_to_remove = []
        for elem in page:
            print elem
            if elements_equal(elem, prev):
                print("found duplicate: %s" % elem.text)  # equal function works well
                elems_to_remove.append(elem)
                continue
            prev = elem
        for elem_to_remove in elems_to_remove:
            page.remove(elem_to_remove)
    tree.write(selected_file_name)


topFrame = Frame(root)
topFrame.pack()
bottomFrame = Frame(root)
bottomFrame.pack(side=BOTTOM)

label1 = Label(topFrame, text="Enter the URL for Extraction")
label1.pack(padx=10, pady=10)
entry1 = Entry(topFrame)
entry1.pack(padx=20, pady=10)
button1 = Button(topFrame, text="Link Extraction", fg="green", command=Button_OnClick)
button1.pack(fill=X, padx=10, pady=10)
label2 = Label(topFrame, text="Enter name of the Project Extracted")
label2.pack(padx=10, pady=10)
entry2 = Entry(topFrame)
entry2.pack(padx=20, pady=10)
button2 = Button(topFrame, text="HTML Extraction", fg="green", command=Button_OnClick2)
button2.pack(fill=X, padx=10, pady=10)
button3 = Button(topFrame, text="Exit", fg="green", command=Button_OnClick3)
button3.pack(fill=X, padx=10, pady=10)
button4 = Button(topFrame, text="Duplication Removal", fg="Blue", command=Button_OnClick4)
button4.pack(fill=X, padx=10, pady=10)


# Need to work before of this #
root.mainloop()



