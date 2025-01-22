import module_reloader
from rig_setup.core.scene_data import NamingConvention
import maya.cmds as cmds
from rig_setup.ui.main_menu import MainMenu


if __name__ == "__main__":
    module_reloader.reset_session_for_script()    # (r"C:\Users\ZaDus\Documents\maya\scripts\zanimTools")


# Import the main menu function
def show():
    if cmds.window("rigSetupUI", exists=True):
        cmds.deleteUI("rigSetupUI")
    naming_convention = NamingConvention()
    my_window = MainMenu(naming_convention)
