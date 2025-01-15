import maya.cmds as cmds

def create_lip_nodes(jawJoint, jawControl, side_l, side_r, side_c, name_top, name_bot, name_corner, is_mirror_behavior):
    """
    The main logic for setting up the lip system.
    """
    controlList = cmds.ls(sl=1)

    # Check if at least one controller is selected
    if len(controlList) < 1:
        cmds.warning("Please select at least one controller.")
        return

    # Validate mirror behavior conditions
    if is_mirror_behavior:
        # Collect names without side prefixes to check for duplicates
        stripped_names = [ctrl.replace(side_l, "").replace(side_r, "") for ctrl in controlList]
        duplicates = [name for name in stripped_names if stripped_names.count(name) > 1]

        # If any duplicates exist, both sides of the same control are selected
        if duplicates:
            cmds.warning("Mirror Behavior expects only one side of each controller to be selected.")
            return

            
    def create_nodes_for_selected(control, is_mirror_behavior):


        # Create and name nodes for the selected controllers
        cmds.shadingNode ("multiplyDivide", au=1, n=control + "_multi") 
        cmds.shadingNode ("remapValue", au=1, n=control + "_remap") 
        cmds.shadingNode ("remapValue", au=1, n=control + "_remap_pressed") 
        cmds.shadingNode ("plusMinusAverage", au=1, n=control + "_plus") 
        # Conditionally create the _inv node if name_bot is in the name
        if name_bot in control:
            cmds.shadingNode("remapValue", au=1, n=control + "_inv")

        # Connect Jaw rotate with the multiply node (to allow lip rotation to match jaw rotation)
        cmds.connectAttr (jawJoint + ".rotate", control + "_multi.input1", f=1) 

        # Connect Jaw controller attribute "Sticky Lips" to the input value of the _remap_pressed node 
        cmds.connectAttr (jawControl + ".StickyLips", control + "_remap_pressed.inputValue", f=1) 

        # Conditionally connect the _remap_pressed.outValue
        if name_bot in control:
            cmds.connectAttr(control + "_remap_pressed.outValue", control + "_inv.inputValue", f=1)
        else:
            cmds.connectAttr(control + "_remap_pressed.outValue", control + "_remap.outputMax", f=1)

        # Connect Jaw controller attribute "Sticky Top Bot" to the input value of the _remap node
        cmds.connectAttr (jawControl + ".StickyTopBot", control + "_remap.inputValue", f=1)

        # Conditionnally connect _remap outValue to the remap_pressed outputMax
        if name_bot in control:
            cmds.connectAttr (control + "_remap.outValue", control + "_remap_pressed.outputMax", f=1) 

        # Conditionnally connect outValue of appropriated node to the input 2 of the multiplier node (to multiply with the jaw rotation)
        if name_bot in control:
            cmds.connectAttr (control + "_inv.outValue", control + "_multi.input2X", f=1) 
            cmds.connectAttr (control + "_inv.outValue", control + "_multi.input2Y", f=1) 
            cmds.connectAttr (control + "_inv.outValue", control + "_multi.input2Z", f=1) 
        else:
            cmds.connectAttr (control + "_remap.outValue", control + "_multi.input2X", f=1) 
            cmds.connectAttr (control + "_remap.outValue", control + "_multi.input2Y", f=1) 
            cmds.connectAttr (control + "_remap.outValue", control + "_multi.input2Z", f=1) 

        # cmds.setAttr(control + "_remap.inputMin", offsetValue) 
        # cmds.setAttr(control + "_remap.inputMax", offsetValue + 1)

        # Connect _multi outputs to the correct nodes and into the _drivers
        cmds.connectAttr (control + "_multi.output", control + "_plus.input3D[0]", f=1) 

        cmds.connectAttr (control + "_multi.outputX", control + "_driver.rotateX", f=1) 
        cmds.connectAttr (control + "_multi.outputY", control + "_driver.rotateY", f=1) 

        # Connect "Press Lips" attribute with the add node and then this node to the controller_driver
        cmds.connectAttr (jawControl + ".PressLips", control + "_plus.input3D[1].input3Dz", f=1) 

        cmds.connectAttr (control + "_plus.output3Dz", control + "_driver.rotateZ", f=1) 

        # If two controllers are selected and shall be controlled by the same system, do so on the second one as well
        if is_mirror_behavior: 
            mirrored_control = None # Initialize mirrored_control
            if control.startswith(side_l):
                mirrored_control = control.replace(side_l, side_r, 1) 
                print("Mirrored control result: {},".format(mirrored_control)+ " From: {}".format(control))
            elif control.startswith(side_r):
                mirrored_control = control.replace(side_r, side_l, 1)
                print("Mirrored control result: {},".format(mirrored_control)+ " From: {}".format(control))

            # Check if mirrored_control was assigned and if the mirrored control exists
            if mirrored_control and cmds.objExists(mirrored_control + "_driver"):
                cmds.connectAttr (control + "_multi.outputX", mirrored_control + "_driver.rotateX", f=1)
                cmds.connectAttr (control + "_multi.outputY", mirrored_control + "_driver.rotateY", f=1)
                cmds.connectAttr (control + "_plus.output3Dz", mirrored_control + "_driver.rotateZ", f=1) 
                print("Mirrored lip setup completed for: {}".format(mirrored_control))
            else:
                if control.startswith(side_c): 
                    print("Skipped mirror on {} because it's in the center.".format(control))
                if control.startswith(side_l or side_r):
                    print("Mirrored control could not be set up for: {}. Check naming conventions or existence.".format(control))

        print("Lip setup completed for {}".format(control))

    # Process each control in the selection
    
    for control in controlList:
        create_nodes_for_selected(control, is_mirror_behavior)
    cmds.warning("Lip setup complete")



