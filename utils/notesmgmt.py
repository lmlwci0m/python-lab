__author__ = 'roberto'


class Note:
    def __init__(self):
        self.note = None
        self.title = None
        self.tag = None
        self.parent = None


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

            note.notes = elems_thr[1].strip()

            notes.append(note)

    return notes


if __name__ == '__main__':

    filename = "notes.txt"

    notes = get_notes(filename)

    for note in notes:

        print("------------------------------------------------------------------\n{} [{}]\n{}\n{}".format(note.title,
                                                                                                           note.parent,
                                                                                                           note.tag,
                                                                                                           note.notes))