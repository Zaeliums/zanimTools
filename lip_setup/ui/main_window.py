import maya.cmds as cmds
from zanimTools.lip_setup.core.classLips import create_lip_nodes

class mainWindow: 

    if cmds.window("rigSetupUI", exists=True):
        cmds.deleteUI("rigSetupUI")
        
    def __init__(self):
                
        self.window = cmds.window("rigSetupUI", title="Rig Setup Tool", widthHeight=(400, 600))
        cmds.columnLayout(adjustableColumn=True)
        self.tabs = cmds.tabLayout(innerMarginWidth=5, innerMarginHeight=5)
        
        # Define a settings node name
        settings_node = "rigSetupSettings"
    
        # Ensure the settings node exists in the scene
        if not cmds.objExists(settings_node):
            cmds.createNode("transform", name=settings_node)
        
        # Helper to save attributes
        def save_attribute(node, attr_name, value):
            if not cmds.attributeQuery(attr_name, node=node, exists=True):
                cmds.addAttr(node, longName=attr_name, dataType="string")
            cmds.setAttr("{}.{}".format(node, attr_name), value, type="string")
        
        # Helper to load attributes
        def load_attribute(node, attr_name, default=""):
            if cmds.attributeQuery(attr_name, node=node, exists=True):
                return cmds.getAttr("{}.{}".format(node, attr_name))
            return default
            
        # Define what the button "save settings" does
        def save_settings(*args):
            save_attribute(settings_node, "jawJoint", cmds.textFieldGrp(jaw_fields["jawJoint"], query=True, text=True))
            save_attribute(settings_node, "jawControl", cmds.textFieldGrp(jaw_fields["jawControl"], query=True, text=True))
            save_attribute(settings_node, "side_l", cmds.textFieldGrp(naming_convention_fields["side_l"], query=True, text=True))
            save_attribute(settings_node, "side_r", cmds.textFieldGrp(naming_convention_fields["side_r"], query=True, text=True))
            save_attribute(settings_node, "side_c", cmds.textFieldGrp(naming_convention_fields["side_c"], query=True, text=True))
            save_attribute(settings_node, "name_top", cmds.textFieldGrp(naming_convention_fields["name_top"], query=True, text=True))
            save_attribute(settings_node, "name_bot", cmds.textFieldGrp(naming_convention_fields["name_bot"], query=True, text=True))
            save_attribute(settings_node, "name_corner", cmds.textFieldGrp(naming_convention_fields["name_corner"], query=True, text=True))
            save_attribute(settings_node, "mirror_behavior", str(cmds.checkBox(mirror_behavior_checkbox, query=True, value=True)))
            cmds.warning("Settings saved for this scene!")
        
        # Name Convention Tab
        tab_naming = cmds.columnLayout(adjustableColumn=True)
        cmds.tabLayout(self.tabs, edit=True, tabLabel=[tab_naming, "Naming Convention"])
        cmds.frameLayout(label="Naming Convention", font="boldLabelFont", collapsable=True)
        
        naming_convention_fields = {}
        naming_convention_fields["side_l"] = cmds.textFieldGrp(label="Side Left Prefix:", text=load_attribute(settings_node, "side_l", "L"))
        naming_convention_fields["side_r"] = cmds.textFieldGrp(label="Side Right Prefix:", text=load_attribute(settings_node, "side_r", "R"))
        naming_convention_fields["side_c"] = cmds.textFieldGrp(label="Side Center Prefix:", text=load_attribute(settings_node, "side_c", "C"))
        naming_convention_fields["name_top"] = cmds.textFieldGrp(label="Position Top Name:", text=load_attribute(settings_node, "name_top", "Top"))
        naming_convention_fields["name_bot"] = cmds.textFieldGrp(label="Position Bot Name:", text=load_attribute(settings_node, "name_bot", "Bot"))
        naming_convention_fields["name_corner"] = cmds.textFieldGrp(label="Position Corner Name:", text=load_attribute(settings_node, "name_corner", "Corner"))
        
        cmds.setParent("..")
        cmds.setParent("..")
    
        # Facial tab
        tab_facial = cmds.columnLayout(adjustableColumn=True)
        cmds.tabLayout(self.tabs, edit=True, tabLabel=[tab_facial, "Facial"])
        # Jaw Fields Section
        cmds.frameLayout(label="Jaw Fields", font="boldLabelFont", collapsable=True)
        
        jaw_fields = {}
        jaw_fields["jawJoint"] = cmds.textFieldGrp(label="Jaw Joint:", text=load_attribute(settings_node, "jawJoint", ""))
        jaw_fields["jawControl"] = cmds.textFieldGrp(label="Jaw Control:", text=load_attribute(settings_node, "jawControl", ""))
        cmds.setParent("..")
       
        # Mirror Behavior Checkbox
        cmds.frameLayout(label="Mirror Behavior Field", font="boldLabelFont")
        def print_is_mirror_behavior(is_mirror_behavior):
            is_mirror_behavior = cmds.checkBox(mirror_behavior_checkbox, query=True, value=True)
            print is_mirror_behavior
            
        mirror_behavior_checkbox = cmds.checkBox(label="Mirror Behavior", value=False, changeCommand=print_is_mirror_behavior)
        cmds.setParent("..")
        
    
        # Add a button to run lip setup
        def build_lip_nodes(*args):
            jaw_joint = cmds.textFieldGrp(jaw_fields["jawJoint"], query=True, text=True)
            jaw_control = cmds.textFieldGrp(jaw_fields["jawControl"], query=True, text=True)
            
            # Get naming convention fields
            side_l = cmds.textFieldGrp(naming_convention_fields["side_l"], query=True, text=True)
            side_r = cmds.textFieldGrp(naming_convention_fields["side_r"], query=True, text=True)
            side_c = cmds.textFieldGrp(naming_convention_fields["side_c"], query=True, text=True)
            name_top = cmds.textFieldGrp(naming_convention_fields["name_top"], query=True, text=True)
            name_bot = cmds.textFieldGrp(naming_convention_fields["name_bot"], query=True, text=True)
            name_corner = cmds.textFieldGrp(naming_convention_fields["name_corner"], query=True, text=True)
    
            # Dynamically query the mirror behavior checkbox
            is_mirror_behavior = cmds.checkBox(mirror_behavior_checkbox, query=True, value=True)
            
            # Run the lip setup logic
            create_lip_nodes(
                jawJoint=jaw_joint,
                jawControl=jaw_control,
                side_l=side_l,
                side_r=side_r,
                side_c=side_c,
                name_top=name_top,
                name_bot=name_bot,
                name_corner=name_corner,
                is_mirror_behavior=is_mirror_behavior,  # Pass this dynamically
            )
    
        cmds.button(label="Build Lip Nodes", command=build_lip_nodes)
        cmds.setParent("..")
        
        cmds.setParent("..")
        # Add a button always visible under the tabs to save settings
        cmds.button(label="Save Settings", command=save_settings)
        
        cmds.showWindow(self.window)
       
    