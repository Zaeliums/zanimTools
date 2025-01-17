#import maya.cmds as cmds

def add_mirrored_selection(side_l, side_r):
    # Get the selected objects in the scene
    selected = cmds.ls(selection=True)
    
    if not selected:
        cmds.warning("No objects selected.")
        return
    
    mirrored_selection = []

    for obj in selected:
        if obj.startswith(side_l):  # If the object starts with "L_"
            mirrored_obj = obj.replace(side_l, side_r, 1)  # Replace "L_" with "R_"
            if cmds.objExists(mirrored_obj):
                mirrored_selection.append(mirrored_obj)
        elif obj.startswith(side_r):  # If the object starts with "R_"
            mirrored_obj = obj.replace(side_r, side_l, 1)  # Replace "R_" with "L_"
            if cmds.objExists(mirrored_obj):
                mirrored_selection.append(mirrored_obj)

    # Add mirrored objects to the selection, avoiding duplicates
    if mirrored_selection:
        selected.extend(mirrored_selection)
        selected = list(set(selected))  # Remove duplicates
    
    cmds.select(selected)  # Update the selection with original + mirrored objects

def get_mirrored_selection(control="L_eye01_CTL", side_l="L", side_r="R", separator="_", side_index=0):
    # Change affected controller for its mirrored counterpart 

    # Find side indication in control's name
    control_tokens = control.split(separator)
    print("control tokens=",control_tokens)

    for i, token in enumerate(control_tokens):
        print("index,token=",i,token)
        if token == side_l:
            token = side_r
            print("token=",token)
            control_tokens[side_index] = token
            break
        elif token == side_r:
            token = side_l
            print("token=",token)
            control_tokens[side_index] = token
            break

    print("control tokens=",control_tokens)
    mirrored_control = separator.join(control_tokens)

    return mirrored_control


print(get_mirrored_selection())