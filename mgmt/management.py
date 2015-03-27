import logging

__author__ = 'roberto'

import wx

from .frameutils import ManagementMainFrame


class ManagementApp(wx.App):
    """Implementation of an app. A main frame is provided.

        starting:

        __init__() -> OnInit()


    """

    ON_INIT_OK = True
    MAIN_FRAME_INIT = None

    def __init__(self, script_path, logging_manager, *args, **kwargs):
        self.main_frame = self.MAIN_FRAME_INIT  # This is the main frame (wx.Frame implementation)
        self.script_path = script_path
        self.logging_manager = logging_manager
        self.logger = self.logging_manager.get_logger(__name__)

        self.logger.debug("Starting initialization")
        super(ManagementApp, self).__init__(*args, **kwargs)

    def init_main_frame(self):
        """Initialization of the main frame. The implementations must set parent as None."""

        self.main_frame = ManagementMainFrame(self)

    def show_main_frame(self):
        """Centering and calling Show on main frame."""

        self.logger.debug("Centering main frame")
        self.main_frame.Centre()

        self.logger.debug("Showing main frame")
        self.main_frame.Show()

    def start_loop(self):
        """Start loop for application object."""

        self.MainLoop()

    def OnInit(self):
        """OnInit event implementation. Init the main frame and show it."""

        self.logger.debug("Executing OnInit method")

        self.init_main_frame()
        self.show_main_frame()

        #for widget in self.main_frame.widget_list:
        #    self.logger.debug(widget)

        self.logger.debug("Returning ON_INIT_OK")

        return self.ON_INIT_OK


def start_managerment_app(script_path, logging_manager):
    """Main call to management app."""

    return ManagementApp(script_path, logging_manager, redirect=False)