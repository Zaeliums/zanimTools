from zanimTools.module_reloader import reset_session_for_script
import os
import sys

import maya.cmds as cmds
from zanimTools.rig_setup.core.scene_data import NamingConvention
from zanimTools.rig_setup.ui.main_menu import MainMenu

# Add the scripts folder to the system path
scripts_path = os.path.join(os.path.expanduser("~"), "documents", "maya", "scripts")
if scripts_path not in sys.path:
    sys.path.append(scripts_path)


# Import the main menu function
def show():

    if cmds.window("rigSetupUI", exists=True):
        cmds.deleteUI("rigSetupUI")
    naming_convention = NamingConvention()
    my_window = MainMenu(naming_convention)
