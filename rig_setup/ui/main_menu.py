import maya.cmds as cmds
from zanimTools.rig_setup.core.module_lips import create_lip_nodes


class MainMenu:

    def __init__(self, naming_convention):

        self.naming_convention = naming_convention
        self.is_mirror_behavior = None
        self.window = cmds.window("rigSetupUI", title="Rig Setup Tool", widthHeight=(400, 600))
        cmds.columnLayout(adjustableColumn=True, columnAlign="center")
        self.tabs = cmds.tabLayout(innerMarginWidth=5, innerMarginHeight=5)

        # Dictionary to store UI elements and their corresponding naming convention attributes
        self.ui_elements = {}

        # Name Convention Tab
        tab_naming = cmds.columnLayout(adjustableColumn=True, columnAlign="center")
        cmds.tabLayout(self.tabs, edit=True, tabLabel=[(tab_naming, "Naming Convention")])

        # Naming Convention Collapsable Section
        cmds.frameLayout(label="Naming Convention Rules", font="boldLabelFont", collapsable=True)

        self.ui_elements['side_l'] = cmds.textFieldGrp(label="Side Left Prefix:",
                                                       text=self.naming_convention.side_l)
        self.ui_elements['side_r'] = cmds.textFieldGrp(label="Side Right Prefix:",
                                                       text=self.naming_convention.side_r)
        self.ui_elements['side_c'] = cmds.textFieldGrp(label="Side Center Prefix:",
                                                       text=self.naming_convention.side_c)
        self.ui_elements['side_index'] = cmds.intFieldGrp(label="Index Number For Side Name:",
                                                          value1=self.naming_convention.side_index)

        self.ui_elements['pos_top_name'] = cmds.textFieldGrp(label="Position Top Name:",
                                                             text=self.naming_convention.pos_top_name)
        self.ui_elements['pos_bot_name'] = cmds.textFieldGrp(label="Position Bot Name:",
                                                             text=self.naming_convention.pos_bot_name)
        self.ui_elements['pos_corner_name'] = cmds.textFieldGrp(label="Position Corner Name:",
                                                                text=self.naming_convention.pos_corner_name)
        self.ui_elements['pos_mid_name'] = cmds.textFieldGrp(label="Position Mid Name:",
                                                             text=self.naming_convention.pos_mid_name)
        self.ui_elements['pos_front_name'] = cmds.textFieldGrp(label="Position Front Name:",
                                                               text=self.naming_convention.pos_front_name)
        self.ui_elements['pos_back_name'] = cmds.textFieldGrp(label="Position Back Name:",
                                                              text=self.naming_convention.pos_back_name)
        self.ui_elements['pos_index'] = cmds.intFieldGrp(label="Index Number For Pos Name:",
                                                         value1=self.naming_convention.pos_index)

        self.ui_elements['type_joint'] = cmds.textFieldGrp(label="Type Joint:",
                                                           text=self.naming_convention.type_joint)
        self.ui_elements['type_control'] = cmds.textFieldGrp(label="Type Control:",
                                                             text=self.naming_convention.type_control)
        self.ui_elements['type_Group'] = cmds.textFieldGrp(label="Type Group:",
                                                           text=self.naming_convention.type_group)
        self.ui_elements['type_locator'] = cmds.textFieldGrp(label="Type Locator:",
                                                             text=self.naming_convention.type_locator)
        self.ui_elements['type_follicle'] = cmds.textFieldGrp(label="Type Follicle:",
                                                              text=self.naming_convention.type_follicle)
        self.ui_elements['type_index'] = cmds.intFieldGrp(label="Index Number For Type:",
                                                          value1=self.naming_convention.type_index)

        cmds.setParent("..")  # End of Naming Convention Collapsable Section

        # Rig Joint Names Collapsable Section
        cmds.frameLayout(label="Rig Joint Names", font="boldLabelFont", collapsable=True)

        self.ui_elements['jaw01_jnt'] = cmds.textFieldGrp(label="Jaw 01 Joint Name:",
                                                          text=self.naming_convention.jaw01_jnt)
        cmds.setParent("..")  # End of Rig Joint Names Collapsable Section
        cmds.setParent("..")  # End of Name Convention Tab

        # Facial Tab
        tab_facial = cmds.columnLayout(adjustableColumn=True)
        cmds.tabLayout(self.tabs, edit=True, tabLabel=[(tab_facial, "Facial")])

        # Jaw Fields Collapsable Section
        cmds.frameLayout(label="Jaw Fields", font="boldLabelFont", collapsable=True)

        self.ui_elements['jaw_joint_reference'] = cmds.textFieldGrp(label="Jaw Joint Reference:",
                                                                    text=self.naming_convention.jaw_joint_reference)
        self.ui_elements['jaw_control'] = cmds.textFieldGrp(label="Jaw Control:",
                                                            text=self.naming_convention.jaw_control)
        cmds.setParent("..")  # End of Jaw Fields collapsable Section

        # Mirror Behavior Checkbox Section
        cmds.frameLayout(label="Mirror Behavior Field", font="boldLabelFont")

        self.ui_elements['mirror_behavior'] = cmds.checkBox(label="Mirror Behavior", value=False,
                                                            changeCommand=self.refresh_mirror_behavior)
        cmds.setParent("..")  # End of Mirror Behavior Checkbox Section

        # Build Lip Nodes Button Section
        cmds.button(label="Build Lip Nodes", command=self.build_lip_nodes)
        cmds.setParent("..")  # End of Build Lip Nodes Button Section
        cmds.setParent("..")  # End of Facial Tab

        # Save Settings Section (below tabs)
        cmds.button(label="Save Settings", command=self.save_settings)

        cmds.showWindow(self.window)

    # Define what the button "save settings" does
    def save_settings(self, *args):
        """Store the current UI values into the storage node."""
        self.naming_convention.set_attr("jaw_joint",
                                        cmds.textFieldGrp(self.ui_elements["jaw_joint"], query=True, text=True))
        self.naming_convention.set_attr("jaw_control",
                                        cmds.textFieldGrp(self.ui_elements["jaw_control"], query=True, text=True))
        self.naming_convention.set_attr("side_l",
                                        cmds.textFieldGrp(self.ui_elements["side_l"], query=True, text=True))
        self.naming_convention.set_attr("side_r",
                                        cmds.textFieldGrp(self.ui_elements["side_r"], query=True, text=True))
        self.naming_convention.set_attr("side_c",
                                        cmds.textFieldGrp(self.ui_elements["side_c"], query=True, text=True))
        self.naming_convention.set_attr("pos_top_name",
                                        cmds.textFieldGrp(self.ui_elements["pos_top_name"], query=True, text=True))
        self.naming_convention.set_attr("pos_bot_name",
                                        cmds.textFieldGrp(self.ui_elements["pos_bot_name"], query=True, text=True))
        self.naming_convention.set_attr("pos_corner_name",
                                        cmds.textFieldGrp(self.ui_elements["pos_corner_name"], query=True, text=True))

        self.naming_convention.set_attr("mirror_behavior",
                                        str(cmds.checkBox(self.ui_elements["mirror_behavior"], query=True, value=True)))

        # Update scene_data dynamically
        self.naming_convention.update_naming_convention()
        cmds.warning("Settings saved for this scene!")

    # Add a button to run lip setup
    def build_lip_nodes(self, *args):
        """Make sure the latest UI values are used before running the lip setup."""
        # Save settings to update naming convention
        self.save_settings()
        # Run lip setup
        create_lip_nodes(
            self.naming_convention,
            is_mirror_behavior=self.naming_convention.mirror_behavior == 'True'
        )

    def refresh_mirror_behavior(self, *args):
        self.is_mirror_behavior = cmds.checkBox(self.ui_elements['mirror_behavior'], query=True, value=True)
        print(self.is_mirror_behavior)
