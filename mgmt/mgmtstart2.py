__author__ = 'roberto'

from gi.repository import Gtk


def printObjProps(widget):
    for prop in widget.props:
        print(prop.name, prop.value_type, prop, dir(prop))


class MainWindow(Gtk.Window):

    DEFAULT_SIZE_X = 400
    DEFAULT_SIZE_Y = 200

    def set_top(self, widget):
        self.top = widget
        self.add(self.top)

    def vbox(self, spacing=2):
        return Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=spacing)

    def hbox(self, spacing=2):
        return Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=spacing)

    def __init__(self):
        Gtk.Window.__init__(self, title="Management interface")

        self.set_default_size(self.DEFAULT_SIZE_X, self.DEFAULT_SIZE_Y)

        # self.box = Gtk.Box(spacing=2)  # Horizontal box
        # self.add(self.box)  # top level window child
        # self.set_top(Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=2))
        self.set_top(self.hbox(2))

        self.button = Gtk.Button(label="Push")
        self.button.connect("clicked", self.on_button_clicked)
        #self.box.add(self.button)
        self.top.pack_start(self.button, True, True, 0)

        # label.set_label("Hello World") label.set_property("label" ,"Hello World")
        # label.get_label() label.get_property("label")
        #self.label = Gtk.Label(label="Hello World", angle=25, halign=Gtk.Align.END)
        self.label = Gtk.Label(label="Hello World")
        #self.box.add(self.label)
        self.top.pack_start(self.label, True, True, 0)

    def on_button_clicked(self, widget):
        print("Hello World")


if __name__ == '__main__':

    win = MainWindow()  # Empty window creation
    # Event - win.disconnect(handler_id) - win.disconnect_by_func(Gtk.main_quit)
    handler_id = win.connect("delete-event", Gtk.main_quit)  # toplevel window is closed -> return from Gtk.main()

    win.show_all()  # display the window

    Gtk.main()  # Processing loop