__author__ = 'roberto'

from gi.repository import Gtk


def prop_map(widget):
    # print(prop.name, prop.value_type, prop, dir(prop))
    return {prop.name: [prop.value_type, prop, dir(prop)] for prop in widget.props}


def printObjProps(widget):
    props = prop_map(widget)
    for prop in sorted(props.keys()):
        print(prop)


class MainWindow(Gtk.Window):
    """properties:

        label.set_label("Hello World") label.set_property("label" ,"Hello World")
        label.get_label() label.get_property("label")

    """

    DEFAULT_SIZE_X = 400
    DEFAULT_SIZE_Y = 200

    def set_top(self, widget):
        self.top = widget
        self.add(self.top)

    def vbox(self, spacing=2):
        return Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=spacing)

    def hbox(self, spacing=2):
        return Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=spacing)

    def grid(self):
        return Gtk.Grid()

    def init_voice(self, label="Open explorer", button_label="Open", event=None):
        """Creates a ListBoxRow """

        row = Gtk.ListBoxRow()

        # line: 1 - 2
        hbox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=50)
        row.add(hbox)

        # 1
        vbox1 = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        hbox.pack_start(vbox1, True, True, 0)

        # 2
        #vbox2 = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        #hbox.pack_start(vbox2, True, True, 0)

        # Label -> 1
        label1 = Gtk.Label(label, xalign=0)
        vbox1.pack_start(label1, True, True, 0)

        # Button -> 2
        button = Gtk.Button(button_label)
        button.props.valign = Gtk.Align.CENTER
        button.set_size_request(40, 20)
        if event:
            button.connect("clicked", event)
        hbox.pack_start(button, False, True, 0)

        return row

    def __init__(self):

        # Init window: title, size, top level component (grid)
        Gtk.Window.__init__(self, title="Management interface")
        self.set_default_size(self.DEFAULT_SIZE_X, self.DEFAULT_SIZE_Y)
        self.set_top(self.grid())

        #self.base = self.hbox(1)
        #self.title = self.vbox(1)
        #self.text = self.hbox(1)
        #self.options = Gtk.Grid()
        #self.options.set_homogeneous(False)

        # Header: title, subtitle, no close button, base size, horizontal expand
        self.header = Gtk.HeaderBar(title="Window text")
        self.header.set_subtitle("Sample Window text")
        self.header.props.show_close_button = False
        self.header.set_size_request(400, 50)
        self.header.set_hexpand(True)

        # Put header on grid
        self.top.attach(self.header, 0, 0, 1, 1)

        # List of items: no selection
        self.items = Gtk.ListBox()
        self.items.set_selection_mode(Gtk.SelectionMode.NONE)

        # Put list on grid
        self.top.attach(self.items, 0, 1, 1, 1)

        # row = Gtk.ListBoxRow()
        # hbox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=50)
        # row.add(hbox)
        # vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        # hbox.pack_start(vbox, True, True, 0)
        #
        # label1 = Gtk.Label("Open explorer", xalign=0)
        # vbox.pack_start(label1, True, True, 0)
        #
        # button = Gtk.Button("Open")
        # button.props.valign = Gtk.Align.CENTER
        # button.set_size_request(40, 20)
        # hbox.pack_start(button, False, True, 0)

        self.items.add(self.init_voice("Start explorer"))
        self.items.add(self.init_voice("Start manager", event=self.open_manager))

        # self.label = Gtk.Label(label="Insert text below")
        # self.top.attach(self.label, 0, 1, 1, 1)
        #
        # self.entry = Gtk.Entry()
        # self.entry.set_text("insert here")
        # self.top.attach(self.entry, 0, 2, 1, 1)
        #
        # self.push_button = Gtk.Button(label="Push")
        # self.push_button.set_border_width(10)
        # self.push_button.connect("clicked", self.on_push_button_clicked)
        # self.options.attach(self.push_button, 0, 0, 1, 1)
        #
        # self.button_pop = Gtk.Button(label="Pop")
        # self.button_pop.set_border_width(10)
        # self.button_pop.connect("clicked", self.on_pop_button_clicked)
        # self.options.attach(self.button_pop, 1, 0, 1, 1)
        #
        # self.top.attach(self.options, 0, 3, 1, 1)


    def on_push_button_clicked(self, widget):
        print("Pushing {}".format(self.entry.get_text()))

    def on_pop_button_clicked(self, widget):
        print("Popping {}".format(self.entry.get_text()))

    def open_manager(self, widget):
        print("open manager")
        w = Gtk.Window(title="Manager")
        w.set_modal(True)
        w.set_default_size(400, 400)

        g = self.grid()
        w.add(g)

        store = Gtk.TreeStore(str, int, bool)

        iter1 = store.append(None, row=["aaa", 4324, False])
        iter2 = store.append(None, row=["bbb", 18347, False])
        iter3 = store.append(None, row=["ccc", 89789, False])

        iter11 = store.append(iter1, row=["aaa", 4324, False])
        iter12 = store.append(iter1, row=["bbb", 18347, False])
        iter13 = store.append(iter1, row=["ccc", 89789, False])


        #print(store.get_path(iter1))
        #print(store.get_path(iter2))
        #print(store.get_path(iter3))

        tree = Gtk.TreeView(store)
        tree.set_hexpand(True)
        tree.set_vexpand(True)

        # single column - single data x column
        #renderer = Gtk.CellRendererText()
        #column = Gtk.TreeViewColumn("Files", renderer, text=0)
        #tree.append_column(column)

        # single column - double data x column
        #column = Gtk.TreeViewColumn("Files")
        #name = Gtk.CellRendererText()
        #size = Gtk.CellRendererText()
        #column.pack_start(name, True)
        #column.pack_start(size, True)
        #column.add_attribute(name, "text", 0)
        #column.add_attribute(size, "text", 1)
        #tree.append_column(column)

        # double column - single data x column
        renderer = Gtk.CellRendererToggle()
        renderer.connect("toggled", self.on_cell_toggled)
        column_toggle = Gtk.TreeViewColumn("Select", renderer, active=2)
        tree.append_column(column_toggle)
        renderer = Gtk.CellRendererText()
        column = Gtk.TreeViewColumn("File name", renderer, text=0)
        column.set_sort_column_id(0)
        tree.append_column(column)
        renderer = Gtk.CellRendererText()
        column = Gtk.TreeViewColumn("Size", renderer, text=1)
        column.set_sort_column_id(1)
        tree.append_column(column)

        select = tree.get_selection()
        select.connect("changed", self.on_tree_selection_changed)

        g.attach(tree, 0, 0, 1, 1)

        w.show_all()

        self.store = store

    def on_cell_toggled(self, widget, path):

        print(self.store[path][2])

        self.store[path][2] = not self.store[path][2]

    def on_tree_selection_changed(self, selection):
        model, treeiter = selection.get_selected()
        if treeiter != None:
            print("You selected", model[treeiter][0])


if __name__ == '__main__':

    win = MainWindow()  # Empty window creation
    # Event - win.disconnect(handler_id) - win.disconnect_by_func(Gtk.main_quit)
    handler_id = win.connect("delete-event", Gtk.main_quit)  # toplevel window is closed -> return from Gtk.main()

    win.show_all()  # display the window

    Gtk.main()  # Processing loop