import maya.cmds as cmds


def create_lip_nodes(naming_convention, is_mirror_behavior):
    """
    The main logic for setting up the lip system.
    """
    control_list = cmds.ls(sl=True)

    # Check if at least one controller is selected
    if len(control_list) < 1:
        cmds.warning("Please select at least one controller.")
        return

    # Validate mirror behavior conditions
    if is_mirror_behavior:
        # Collect names without side prefixes to check for duplicates
        stripped_names = [ctrl.replace(naming_convention.side_l, "").replace(naming_convention.side_r, "") for ctrl in control_list]
        duplicates = [name for name in stripped_names if stripped_names.count(name) > 1]

        # If any duplicates exist, both sides of the same control are selected
        if duplicates:
            cmds.warning("Mirror Behavior expects only one side of each controller to be selected.")
            return

    def create_nodes_for_selected(control, is_mirror_behavior):

        # Create and name nodes for the selected controllers
        cmds.shadingNode("multiplyDivide", asUtility=True, name=control + "_multi")
        cmds.shadingNode("remapValue", asUtility=True, name=control + "_remap")
        cmds.shadingNode("remapValue", asUtility=True, name=control + "_remap_pressed")
        cmds.shadingNode("plusMinusAverage", asUtility=True, name=control + "_plus")
        # Conditionally create the _inv node if pos_bot_name is in the name
        if naming_convention.pos_bot_name in control:
            cmds.shadingNode("remapValue", asUtility=True, name=control + "_inv")

        cmds.connectAttr(naming_convention.jaw_joint_reference + ".rotate", control + "_multi.input1", force=True)  # Connect Jaw rotate with the multiply node (to allow lip rotation to match jaw rotation)
        cmds.connectAttr(naming_convention.jaw_control + ".StickyLips", control + "_remap_pressed.inputValue", force=True)  # Connect Jaw controller attribute "Sticky Lips" to the input value of the _remap_pressed node

        if naming_convention.pos_bot_name in control:
            cmds.connectAttr(control + "_remap_pressed.outValue", control + "_inv.inputValue", force=True)  # Conditionally connect the _remap_pressed.outValue
            cmds.connectAttr(control + "_remap.outValue", control + "_remap_pressed.outputMax", force=True)  # Conditionally connect _remap outValue to the remap_pressed outputMax
            # Conditionally connect outValue of appropriated node to the input 2 of the multiplier node (to multiply with the jaw rotation)
            cmds.connectAttr(control + "_inv.outValue", control + "_multi.input2X", force=True)
            cmds.connectAttr(control + "_inv.outValue", control + "_multi.input2Y", force=True)
            cmds.connectAttr(control + "_inv.outValue", control + "_multi.input2Z", force=True)
        else:
            cmds.connectAttr(control + "_remap_pressed.outValue", control + "_remap.outputMax", force=True)
            cmds.connectAttr(control + "_remap.outValue", control + "_multi.input2X", force=True)
            cmds.connectAttr(control + "_remap.outValue", control + "_multi.input2Y", force=True)
            cmds.connectAttr(control + "_remap.outValue", control + "_multi.input2Z", force=True)

        cmds.connectAttr(naming_convention.jaw_control + ".StickyTopBot", control + "_remap.inputValue", force=True)  # Connect Jaw controller attribute "Sticky Top Bot" to the input value of the _remap node
        cmds.connectAttr(control + "_multi.output", control + "_plus.input3D[0]", force=True)  # Connect _multi outputs to the correct nodes and into the _drivers
        cmds.connectAttr(control + "_multi.outputX", control + "_driver.rotateX", force=True)
        cmds.connectAttr(control + "_multi.outputY", control + "_driver.rotateY", force=True)
        cmds.connectAttr(naming_convention.jaw_control + ".PressLips", control + "_plus.input3D[1].input3Dz", force=True)  # Connect "Press Lips" attribute with the add node and then this node to the controller_driver
        cmds.connectAttr(control + "_plus.output3Dz", control + "_driver.rotateZ", force=True)

        # If two controllers are selected and shall be controlled by the same system, do so on the second one as well
        if is_mirror_behavior:
            mirrored_control = None  # Initialize mirrored_control
            if control.startswith(naming_convention.side_l):
                mirrored_control = control.replace(naming_convention.side_l, naming_convention.side_r, 1)
                print(f"Mirrored control result: {mirrored_control}, From: {control}")
            elif control.startswith(naming_convention.side_r):
                mirrored_control = control.replace(naming_convention.side_r, naming_convention.side_l, 1)
                print(f"Mirrored control result: {mirrored_control}, From: {control}")

            # Check if mirrored_control was assigned and if the mirrored control exists
            if mirrored_control and cmds.objExists(mirrored_control + "_driver"):
                cmds.connectAttr(control + "_multi.outputX", mirrored_control + "_driver.rotateX", force=True)
                cmds.connectAttr(control + "_multi.outputY", mirrored_control + "_driver.rotateY", force=True)
                cmds.connectAttr(control + "_plus.output3Dz", mirrored_control + "_driver.rotateZ", force=True)
                print(f"Mirrored lip setup completed for: {mirrored_control}")
            else:
                if control.startswith(naming_convention.side_c):
                    print(f"Skipped mirror on {control} because it's in the center.")
                if control.startswith(naming_convention.side_l) or control.startswith(naming_convention.side_r):
                    print(f"Mirrored control could not be set up for: {control}. Check naming conventions or existence.")

        print(f"Lip setup completed for {control}")

    # Process each control in the selection
    for control in control_list:
        create_nodes_for_selected(control, is_mirror_behavior)
    cmds.warning("Lip setup complete")
