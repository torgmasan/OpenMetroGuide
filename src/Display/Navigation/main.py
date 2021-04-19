"""This is the module from which the program is to be run.

INSTRUCTIONS:
    The project_report.pdf contains a subsection titled 'Instructions'
    that provides a detailed understanding, with pictures, of a
    successful working and how to go about using the application.

NOTES:
    - The arrows in the second window (if cities are already present in the dataset)
      are for visual aid and not clickable. ALL NAVIGATION IN HOME IS THROUGH ARROW
      KEYS.
    - To proceed to the next step/window, pressing the enter/return key will suffice.
      The exceptions to this is the final step of creating/editing the map. After making
      the changes required, CLOSE the window. The data is auto-saved in the database.
"""
from src.Display.Navigation.home import run_home

if __name__ == '__main__':
    run_home()
