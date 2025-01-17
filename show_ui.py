from lip_setup.core.className import namingConvention
import maya.cmds as cmds


# Reload relevant modules before showing the UI
import zanimTools.lip_setup.core.classLips
import zanimTools.lip_setup.core.className
import zanimTools.lip_setup.ui.main_window


# Reload all relevant modules
reload(zanimTools.lip_setup.core.classLips)
reload(zanimTools.lip_setup.core.className)
reload(zanimTools.lip_setup.core)
reload(zanimTools.lip_setup.ui.main_window)
reload(zanimTools.lip_setup.ui)
reload(zanimTools.lip_setup)

# Import the show_lip_setup_ui function
from zanimTools.lip_setup.ui.main_window import mainWindow

def show():
    if cmds.window("rigSetupUI", exists=True):
        cmds.deleteUI("rigSetupUI")
    naming_convention = namingConvention()
    myWindow = mainWindow(naming_convention)
