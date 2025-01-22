from reload_modules import reset_session_for_script
from rig_setup.core.scene_data import namingConvention
import maya.cmds as cmds
from rig_setup.ui.main_menu import mainMenu

reset_session_for_script(r"C:\Users\ZaDus\Documents\maya\scripts\zanimTools")
# Import the main menu function


def show():
    if cmds.window("rigSetupUI", exists=True):
        cmds.deleteUI("rigSetupUI")
    naming_convention = namingConvention()
    my_window = mainMenu(naming_convention)
