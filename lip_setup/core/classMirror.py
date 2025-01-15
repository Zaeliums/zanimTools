import maya.cmds as cmds

def add_mirrored_selection():
    # Get the selected objects in the scene
    selected = cmds.ls(selection=True)
    
    if not selected:
        cmds.warning("No objects selected.")
        return
    
    mirrored_selection = []

    for obj in selected:
        if obj.startswith("L_"):  # If the object starts with "L_"
            mirrored_obj = obj.replace("L_", "R_", 1)  # Replace "L_" with "R_"
            if cmds.objExists(mirrored_obj):
                mirrored_selection.append(mirrored_obj)
        elif obj.startswith("R_"):  # If the object starts with "R_"
            mirrored_obj = obj.replace("R_", "L_", 1)  # Replace "R_" with "L_"
            if cmds.objExists(mirrored_obj):
                mirrored_selection.append(mirrored_obj)

    # Add mirrored objects to the selection, avoiding duplicates
    if mirrored_selection:
        selected.extend(mirrored_selection)
        selected = list(set(selected))  # Remove duplicates
    
    cmds.select(selected)  # Update the selection with original + mirrored objects
