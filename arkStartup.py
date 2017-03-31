import maya.cmds as cmds
import os

print 'ARK Startup'

cmds.currentUnit( linear = 'cm')
print 'Setting units to Centimeters'

cmds.currentUnit( time = 'ntsc')
print 'Setting time to NTSC 30 fps'

os.environ["ARK_DATA"] = os.environ["ARK_TOOLS"]

import ui.switchUi as sUi
reload(sUi)
sUi.arkTools_UI()