from reload_modules import resetSessionForScript
from rig_setup.core.scene_data import namingConvention
import maya.cmds as cmds


resetSessionForScript("C:\Users\ZaDus\Documents\maya\scripts\zanimTools")
# Import the main menu function
from zanimTools.rig_setup.ui.main_menu import mainMenu

def show():
    if cmds.window("rigSetupUI", exists=True):
        cmds.deleteUI("rigSetupUI")
    naming_convention = namingConvention()
    myWindow = mainMenu(naming_convention)
