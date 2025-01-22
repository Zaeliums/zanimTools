import inspect
from os.path import dirname
import sys


# This function resets the session for the script
# It has a flag to let you specify the userPath you want to clear out
# By default, it assumes the userPath is the directory of the running script (__file__)
def reset_session_for_script(user_path=None):
    if user_path is None:
        user_path = dirname(__file__)
    # Convert this to lower just for a clean comparison later
    user_path = user_path.lower()

    to_delete = []
    # Iterate over all the modules that are currently loaded
    for key, module in sys.modules.items():
        # There's a few modules that are going to complain if you try to query them
        # ,so I've popped this into a try/except to keep it safe
        try:
            # Use the "inspect" library to get the module_file_path that the current module was loaded from
            module_file_path = inspect.getfile(module).lower()

            # Don't try and remove the startup script, that will break everything
            if module_file_path == __file__.lower():
                continue

            # If the module's filepath contains the userPath, add it to the list of modules to delete
            if module_file_path.startswith(user_path):
                print(f"Removing {key}")
                to_delete.append(key)
        except Exception as e:
            # Log the exception message for debugging purposes
            print(f"Error inspecting module {key}: {e}")
            pass

    # If we'd deleted the module in the loop above, it would have changed the size of the dictionary and
    # broken the loop. So now we go over the list we made and delete all the modules
    for module in to_delete:
        del sys.modules[module]

#########################################
