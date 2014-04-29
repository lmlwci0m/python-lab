import os

__author__ = 'roberto'

import xml.etree.ElementTree as ET


class Note:
    def __init__(self):
        self.notes = ''
        self.title = ''
        self.tag = ''
        self.parent = ''

    def to_note(self):
        return """###Title:{0:s}
###Parent:{1:s}
###Tag:{2:s}
###Notes:{3:s}""".format(self.title, self.parent, self.tag, self.notes)

    def to_xml(self):
        tags = "\n".join(["        <tag>{}</tag>".format(tag) for tag in self.tag.split("|")])
        return """<note>
    <title>{0:s}</title>
    <parent>{1:s}</parent>
    <tags>
{2:s}
    </tags>
    <notes><![CDATA[""".format(self.title, self.parent, tags) + self.notes + """]]></notes>
</note>
"""


def get_notes(filepath):

    notes = []

    with open(filepath) as f:

        for x in f.read().split("###Title:")[1:]:

            note = Note()

            elems = x.split("###Parent:")

            note.title = elems[0].strip()

            elems_sec = elems[1].split("###Tag:")

            note.parent = elems_sec[0].strip()

            elems_thr = elems_sec[1].split("###Notes:")

            note.tag = elems_thr[0].strip()

            note.notes = elems_thr[1]

            notes.append(note)

    return notes


def get_notes_xml(filename):

    notes = []

    tree = ET.parse(filename)
    root = tree.getroot()

    #print(root.tag)

    for child in root:
        #print((" " * 4) + child.tag)
        note = Note()
        for subchild in child:

            #print((" " * 8) + subchild.tag)
            if subchild.tag == 'title':
                note.title = str(subchild.text) if subchild.text else ''
            elif subchild.tag == 'parent':
                note.parent = str(subchild.text) if subchild.text else ''
            elif subchild.tag == 'notes':
                note.notes = str(subchild.text) if subchild.text else ''
            elif subchild.tag == 'tags':
                note.tag = "|".join([str(tagchild.text) for tagchild in subchild])
        notes.append(note)

    return notes


def write_to_xml(notes, filename):

    with open(filename, "w") as f:
        f.write('<?xml version="1.0" encoding="UTF-8"?>\n')
        f.write('<notelist>')
        for note in notes:
            f.write(note.to_xml())
        f.write('</notelist>')


def write_to_notes(notes, filename):

    with open(filename, "w") as f:
        for note in notelist:
            f.write(note.to_note())


if __name__ == '__main__':

    basepath = ""

    filename = os.path.join(basepath, "notes.txt")
    xmlfilename = os.path.join(basepath, "notes.xml")
    backfilename = os.path.join(basepath, "notesback.txt")

    notes = get_notes(filename)

    write_to_xml(notes, xmlfilename)

    notelist = get_notes_xml(xmlfilename)

    write_to_notes(notelist, backfilename)

#    for note in notes:
#
#        print("------------------------------------------------------------------\n{} [{}]\n{}\n{}".format(note.title,
#                                                                                                           note.parent,
#                                                                                                           note.tag,
#                                                                                                           note.notes))