__author__ = 'roberto'

import wx


class MainFrameUtils(wx.Frame):

    def init_widget_list(self):
        self.widget_list = {self.NAME: self}

    def get_widget(self, name):
        return self.widget_list[name]

    def set_widget(self, name, value):
        self.widget_list[name] = value


class ManagementMainFrame(MainFrameUtils):

    DEFAULT_POS_X = 400
    DEFAULT_POS_Y = 200

    DEFAULT_SIZE_W = 600
    DEFAULT_SIZE_H = 400

    TITLE = "Management app"
    MAIN_FRAME_WIDGET = "main_frame"

    STYLE = wx.DEFAULT_FRAME_STYLE

    MENU_BAR_WIDGET = "menu_bar"

    FILE_MENU_WIDGET = "file_menu"
    FILE_MENU_WIDGET_CAPTION = "&File"

    INFO_MENU_ITEM_WIDGET = "info_menu_item"
    INFO_MENU_ITEM_WIDGET_NAME = "Info"
    INFO_MENU_ITEM_WIDGET_DESC = "DIsplay info"

    QUIT_MENU_ITEM_WIDGET = "quit_menu_item"
    QUIT_MENU_ITEM_WIDGET_NAME = "Quit"
    QUIT_MENU_ITEM_WIDGET_DESC = "Quit application"

    def __init__(self):
        """
        wx.Frame(None, title="Management app",
                         style=wx.MINIMIZE_BOX |
                         wx.MAXIMIZE_BOX |
                         wx.RESIZE_BORDER |
                         wx.SYSTEM_MENU |
                         wx.CAPTION |
                         wx.CLOSE_BOX |
                         wx.CLIP_CHILDREN)

        wx.Frame(
            wx.Window parent,
            int id=-1,
            string title='',
            wx.Point pos = wx.DefaultPosition,
            wx.Size size = wx.DefaultSize,
            style = wx.DEFAULT_FRAME_STYLE,
            string name = "frame")

        """

        # create istself as parent for all widgets
        super(ManagementMainFrame, self).__init__(None,
                                                  id=-1,
                                                  pos=(self.DEFAULT_POS_X, self.DEFAULT_POS_Y),
                                                  size=(self.DEFAULT_SIZE_W, self.DEFAULT_SIZE_H),
                                                  title=self.TITLE,
                                                  name=self.MAIN_FRAME_WIDGET,
                                                  style=self.STYLE)

        self.init_widget_list()
        self.init_menu_bar()

    def init_menu_bar(self):
        """
        Menu bar: initialize wx.MenuBar,
                  set as menubar to frame (frame.SetMenuBar), add to widget list

        Menu: initialize wx.Menu,
              append to menubar (menu_bar.Append), add to widget list

        Menu item: initialize with menu.Append,
                   bind an OnEvent(self, event) handler (frame.Bind), add to widget list

        """

        menu_bar = wx.MenuBar()
        self.SetMenuBar(menu_bar)
        self.set_widget(self.MENU_BAR_WIDGET, menu_bar)

        file_menu = wx.Menu()
        menu_bar.Append(file_menu, self.FILE_MENU_WIDGET_CAPTION)
        self.set_widget(self.FILE_MENU_WIDGET, file_menu)

        info_menu_item = file_menu.Append(wx.ID_ANY,
                                          self.INFO_MENU_ITEM_WIDGET_NAME,
                                          self.INFO_MENU_ITEM_WIDGET_DESC)
        self.Bind(wx.EVT_MENU, self.OnInfo, info_menu_item)
        self.set_widget(self.INFO_MENU_ITEM_WIDGET, info_menu_item)

        # OSX has different system menus !!!
        quit_menu_item = file_menu.Append(wx.ID_ANY,
                                          self.QUIT_MENU_ITEM_WIDGET_NAME,
                                          self.QUIT_MENU_ITEM_WIDGET_DESC)
        self.Bind(wx.EVT_MENU, self.OnQuit, quit_menu_item)
        self.set_widget(self.QUIT_MENU_ITEM_WIDGET, quit_menu_item)

    def OnQuit(self, event):
        self.Close()

    def OnInfo(self, event):
        wx.MessageBox('This is a wxPython application', 'Information message')