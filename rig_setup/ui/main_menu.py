import maya.cmds as cmds
from zanimTools.rig_setup.core.module_lips import create_lip_nodes


class MainMenu:

    def __init__(self, naming_convention):

        self.naming_convention = naming_convention
        self.is_mirror_behavior = None
        self.window = cmds.window("rigSetupUI", title="Rig Setup Tool", widthHeight=(400, 600))
        cmds.columnLayout(adjustableColumn=True)
        self.tabs = cmds.tabLayout(innerMarginWidth=5, innerMarginHeight=5)

        # Define a settings node name
        self.settings_node = "rigSetupSettings"

        # Ensure the settings node exists in the scene
        if not cmds.objExists(self.settings_node):
            cmds.createNode("transform", name=self.settings_node)

        # Name Convention Tab
        tab_naming = cmds.columnLayout(adjustableColumn=True)
        cmds.tabLayout(self.tabs, edit=True, tabLabel=[(tab_naming, "Naming Convention")])
        cmds.frameLayout(label="Naming Convention", font="boldLabelFont", collapsable=True)

        self.side_l_textbox = cmds.textFieldGrp(label="Side Left Prefix:",
                                                text=self.load_attribute(self.settings_node, "side_l", "L"))
        self.side_r_textbox = cmds.textFieldGrp(label="Side Right Prefix:",
                                                text=self.load_attribute(self.settings_node, "side_r", "R"))
        self.side_c_textbox = cmds.textFieldGrp(label="Side Center Prefix:",
                                                text=self.load_attribute(self.settings_node, "side_c", "C"))
        self.pos_top_name_textbox = cmds.textFieldGrp(label="Position Top Name:",
                                                      text=self.load_attribute(self.settings_node, "pos_top_name",
                                                                               "Top"))
        self.pos_bot_name_textbox = cmds.textFieldGrp(label="Position Bot Name:",
                                                      text=self.load_attribute(self.settings_node, "pos_bot_name",
                                                                               "Bot"))
        self.pos_corner_name_textbox = cmds.textFieldGrp(label="Position Corner Name:",
                                                         text=self.load_attribute(self.settings_node, "pos_corner_name",
                                                                                  "Corner"))

        cmds.setParent("..")
        cmds.setParent("..")

        # Facial tab
        tab_facial = cmds.columnLayout(adjustableColumn=True)
        cmds.tabLayout(self.tabs, edit=True, tabLabel=[(tab_facial, "Facial")])
        # Jaw Fields Section
        cmds.frameLayout(label="Jaw Fields", font="boldLabelFont", collapsable=True)

        self.jaw_joint_textbox = cmds.textFieldGrp(label="Jaw Joint:",
                                                   text=self.load_attribute(self.settings_node, "jaw_joint", ""))
        self.jaw_control_textbox = cmds.textFieldGrp(label="Jaw Control:",
                                                     text=self.load_attribute(self.settings_node, "jaw_control", ""))
        cmds.setParent("..")

        # Mirror Behavior Checkbox
        cmds.frameLayout(label="Mirror Behavior Field", font="boldLabelFont")

        self.mirror_behavior_checkbox = cmds.checkBox(label="Mirror Behavior", value=False,
                                                      changeCommand=self.refresh_mirror_behavior)
        cmds.setParent("..")

        cmds.button(label="Build Lip Nodes", command=self.build_lip_nodes)
        cmds.setParent("..")

        cmds.setParent("..")
        # Add a button always visible under the tabs to save settings
        cmds.button(label="Save Settings", command=self.save_settings)

        cmds.showWindow(self.window)

    # Helper to save attributes
    def save_attribute(self, node, attr_name, value):
        if not cmds.attributeQuery(attr_name, node=node, exists=True):
            cmds.addAttr(node, longName=attr_name, dataType="string")
        cmds.setAttr("{}.{}".format(node, attr_name), value, type="string")

    # Helper to load attributes
    def load_attribute(self, node, attr_name, default=""):
        if cmds.attributeQuery(attr_name, node=node, exists=True):
            return cmds.getAttr("{}.{}".format(node, attr_name))
        return default

    # Define what the button "save settings" does
    def save_settings(self, *args):
        self.save_attribute(self.settings_node, "jaw_joint",
                            cmds.textFieldGrp(self.jaw_joint_textbox, query=True, text=True))
        self.save_attribute(self.settings_node, "jaw_control",
                            cmds.textFieldGrp(self.jaw_control_textbox, query=True, text=True))
        self.save_attribute(self.settings_node, "side_l",
                            cmds.textFieldGrp(self.side_l_textbox, query=True, text=True))
        self.save_attribute(self.settings_node, "side_r",
                            cmds.textFieldGrp(self.side_r_textbox, query=True, text=True))
        self.save_attribute(self.settings_node, "side_c",
                            cmds.textFieldGrp(self.side_c_textbox, query=True, text=True))
        self.save_attribute(self.settings_node, "pos_top_name",
                            cmds.textFieldGrp(self.pos_top_name_textbox, query=True, text=True))
        self.save_attribute(self.settings_node, "pos_bot_name",
                            cmds.textFieldGrp(self.pos_bot_name_textbox, query=True, text=True))
        self.save_attribute(self.settings_node, "pos_corner_name",
                            cmds.textFieldGrp(self.pos_corner_name_textbox, query=True, text=True))
        self.save_attribute(self.settings_node, "mirror_behavior",
                            str(cmds.checkBox(self.mirror_behavior_checkbox, query=True, value=True)))
        cmds.warning("Settings saved for this scene!")

    # Add a button to run lip setup
    def build_lip_nodes(self, *args):
        jaw_joint = cmds.textFieldGrp(self.jaw_joint_textbox, query=True, text=True)
        jaw_control = cmds.textFieldGrp(self.jaw_control_textbox, query=True, text=True)

        # Get naming convention fields
        side_l = cmds.textFieldGrp(self.side_l_textbox, query=True, text=True)
        side_r = cmds.textFieldGrp(self.side_r_textbox, query=True, text=True)
        side_c = cmds.textFieldGrp(self.side_c_textbox, query=True, text=True)
        pos_top_name = cmds.textFieldGrp(self.pos_top_name_textbox, query=True, text=True)
        pos_bot_name = cmds.textFieldGrp(self.pos_bot_name_textbox, query=True, text=True)
        pos_corner_name = cmds.textFieldGrp(self.pos_corner_name_textbox, query=True, text=True)

        # Dynamically query the mirror behavior checkbox
        self.is_mirror_behavior = cmds.checkBox(self.mirror_behavior_checkbox, query=True, value=True)

        # Run the lip setup logic
        create_lip_nodes(
            self.naming_convention,
            is_mirror_behavior=self.is_mirror_behavior,  # Pass this dynamically
        )

    def refresh_mirror_behavior(self, *args):
        self.is_mirror_behavior = cmds.checkBox(self.mirror_behavior_checkbox, query=True, value=True)
        print(self.is_mirror_behavior)