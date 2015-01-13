__author__ = 'roberto'

import wx

from .frameutils import ManagementMainFrame


class ManagementApp(wx.App):
    """Implementation of an app. A main frame is provided."""

    ON_INIT_OK = True
    MAIN_FRAME_INIT = None

    def __init__(self, script_path, *args, **kwargs):
        self.main_frame = self.MAIN_FRAME_INIT  # This is the main frame (wx.Frame implementation)
        self.script_path = script_path

        super(ManagementApp, self).__init__(*args, **kwargs)


    def init_main_frame(self):
        """Initialization of the main frame. The implementations must set parent as None."""

        self.main_frame = ManagementMainFrame(self)

    def show_main_frame(self):
        """Call Show on main frame."""

        self.main_frame.Centre()
        self.main_frame.Show()

    def start_loop(self):
        """Start loop for application object."""

        self.MainLoop()

    def OnInit(self):
        """OnInit event implementation. Init the main frame and show it."""

        self.init_main_frame()
        self.show_main_frame()

        return self.ON_INIT_OK


def start_managerment_app(script_path):
    """Main call to management app."""

    return ManagementApp(script_path, redirect=False)