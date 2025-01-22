import maya.cmds as cmds


def show_warning_popup(control, mirrored_control):
    result = cmds.confirmDialog(
        title='Warning',
        message='Selected controller {} is driving {}. If continuing without mirroring behavior, {} will be disconnected. Continue?'.format(
            control, mirrored_control, mirrored_control),
        button=['Cancel', 'Continue and disconnect', 'Continue and mirror behavior'],
        defaultButton='Continue and disconnect',
        cancelButton='Cancel',
        dismissString='Cancel'
    )
    return result
