import maya.cmds as cmds
from functools import partial
from importlib import import_module
import os

class arkTools_UI:

	def __init__(self, *args):
		currentMenus = cmds.window('MayaWindow', q = True, ma = True)
		for c in currentMenus:
			if c == 'arkTools_Menu':
				cmds.deleteUI('arkTools_Menu', m = True)

		arkMenu = cmds.menu('arkTools_Menu', l = 'Ark Tools', to = True, p = 'MayaWindow')
		cmds.menuItem(l = 'Space Switcher', p =  arkMenu, command = self.ui)

		self.arkUiElements = {}
		self.arkUiInfo = {}
		

		
	def ui(self, *args):
		windowName = 'arkSpaceSwitchWindow'
		if cmds.window(windowName, exists = True):
			cmds.deleteUI(windowName)

		
		windowHeight = 400
		windowWidth = 303
		buttonHeight = 200
		buttonWidth = 150

		self.arkUiElements['window'] = cmds.window(windowName, w = windowWidth, h = windowHeight, t = 'ARK Space Switch V 1.0', sizeable = True, mnb = True)

		self.arkUiElements['mainColLayout'] = cmds.columnLayout("mainColLayout", w = windowWidth, adj = True)
 
		self.arkUiElements['optionsTabLayout'] = cmds.tabLayout('optionsTabs', w = windowWidth)

		self.arkUiElements['spacesLayout'] = cmds.rowColumnLayout('spacesLayout', numberOfColumns = 2, columnWidth = [(1, windowWidth/2), (2, windowWidth/2)], p =self.arkUiElements['optionsTabLayout'])

		cmds.showWindow(self.arkUiElements['window'])




