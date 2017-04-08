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
		self.rightHand = '*:ctrl_R_weaponJnt'
		self.leftHand = '*:ctrl_L_weaponJnt'
		self.customR = '*:c_Rht_arm_customSpace'
		self.customL = '*:c_Lft_arm_customSpace'
		

		
	def ui(self, *args):
		windowName = 'arkSpaceSwitchWindow'
		if cmds.window(windowName, exists = True):
			cmds.deleteUI(windowName)

		
		windowHeight = 200
		windowWidth = 600
		buttonHeight = 50
		buttonWidth = 100

		self.arkUiElements['window'] = cmds.window(windowName, w = windowWidth, h = windowHeight, t = 'ARK Space Switch V 1.0', sizeable = True, mnb = True)

		self.arkUiElements['mainColLayout'] = cmds.columnLayout("mainColLayout", w = windowWidth, adj = True)

		self.arkUiElements['targetInput'] = cmds.frameLayout('targetInputFrame', w = windowWidth, l = 'Weapon Input', cll = True, p = self.arkUiElements['mainColLayout'])

		self.arkUiElements['textFieldLayout'] = cmds.rowColumnLayout("textFieldLayout", numberOfColumns = 3, columnWidth = [(1, windowWidth/3), (2, windowWidth/3), (3, windowWidth/3)], p = self.arkUiElements['targetInput'])
		
		cmds.text(l = 'Target Weapon Name:', p = self.arkUiElements['textFieldLayout'])

		self.arkUiElements['inputText'] = cmds.textField('weaponTextField', pht = 'Target Weapon Name', w = (windowWidth/3)-3, p = self.arkUiElements['textFieldLayout'])

		self.arkUiElements['weaponNameCall'] = cmds.button('WeapNameCall', w = buttonWidth, h = buttonHeight/2, l = 'Get Weapon Name', p = self.arkUiElements['textFieldLayout'], c = partial(self.nameInput, self.arkUiElements['inputText']))

		cmds.text(l = 'Target Projectile Name:', p = self.arkUiElements['textFieldLayout'])

		self.arkUiElements['inputProjText'] = cmds.textField('projTextField', pht = 'Target Projectile Name', w = (windowWidth/3)-3, p = self.arkUiElements['textFieldLayout'])

		self.arkUiElements['projNameCall'] = cmds.button('projNameCall', w = buttonWidth, h = buttonHeight/2, l = 'Get Projectile Name', p = self.arkUiElements['textFieldLayout'], c = partial(self.nameInput, self.arkUiElements['inputProjText']))

		cmds.text(l = 'Target Chamber Name:', p = self.arkUiElements['textFieldLayout'])

		self.arkUiElements['inputProjChamberText'] = cmds.textField('projChamberTextField', pht = 'Target Chamber Name', w = (windowWidth/3)-3, p = self.arkUiElements['textFieldLayout'])

		self.arkUiElements['chamNameCall'] = cmds.button('chamNameCall', w = buttonWidth, h = buttonHeight/2, l = 'Get Chamber Name', p = self.arkUiElements['textFieldLayout'], c = partial(self.nameInput, self.arkUiElements['inputProjChamberText']))

		self.arkUiElements['spacesLayout'] = cmds.rowColumnLayout('Assignments', numberOfColumns = 2, columnWidth = [(1, windowWidth/2), (2, windowWidth/2)], p =self.arkUiElements['mainColLayout'])

		self.arkUiElements['OperationsFrame'] = cmds.frameLayout('OperationsFrame', w = windowWidth, l = 'Operations', cll = True, p = self.arkUiElements['mainColLayout'])

		self.arkUiElements['operationsLayout'] = cmds.rowColumnLayout('Assignments', numberOfColumns = 2, columnWidth = [(1, windowWidth/2), (2, windowWidth/2)], p = self.arkUiElements['OperationsFrame'])

		self.arkUiElements['buttonA'] = cmds.button('WeapToRHand', w = buttonWidth, h = buttonHeight, l = 'Right Hand', p = self.arkUiElements['operationsLayout'], c = self.rightSpace)

		self.arkUiElements['buttonB'] = cmds.button('WeapToLHand', w = buttonWidth, h = buttonHeight, l = 'Left Hand', p = self.arkUiElements['operationsLayout'], c = self.leftSpace)

		self.arkUiElements['buttonC'] = cmds.button('2HWeapToRHand', w = buttonWidth, h = buttonHeight, l = '2H Right Hand', p = self.arkUiElements['operationsLayout'], c = self.right2HWeap)

		self.arkUiElements['buttonD'] = cmds.button('2HWeapToLHand', w = buttonWidth, h = buttonHeight, l = '2H Left Hand', p = self.arkUiElements['operationsLayout'], c = self.left2HWeap)

		self.arkUiElements['buttonE'] = cmds.button('WeaponDriver', w = buttonWidth, h = buttonHeight, l = 'Weapon Driver', p = self.arkUiElements['operationsLayout'], c = self.weapInf)

		self.arkUiElements['buttonF'] = cmds.button('Detach', w = buttonWidth, h = buttonHeight, l = 'Detach', bgc = (1,0.2,0.2), p = self.arkUiElements['operationsLayout'], c = self.detach)

		self.arkUiElements['buttonG'] = cmds.button('ProjectileAttachL', w = buttonWidth, h = buttonHeight, l = 'Projectile L', p = self.arkUiElements['operationsLayout'], c = self.projL)

		self.arkUiElements['buttonH'] = cmds.button('ProjectileAttachR', w = buttonWidth, h = buttonHeight, l = 'Projectile R', p = self.arkUiElements['operationsLayout'], c = self.projR)

		self.arkUiElements['buttonI'] = cmds.button('ProjectileAttachW', w = buttonWidth, h = buttonHeight, l = 'Projectile Weapon', p = self.arkUiElements['operationsLayout'], c = self.projW)

		self.arkUiElements['buttonJ'] = cmds.button('ProjectileDetach', w = buttonWidth, h = buttonHeight, l = 'Projectile Detach', bgc = (1,0.2,0.2), p = self.arkUiElements['operationsLayout'], c = self.projDetach)


		cmds.showWindow(self.arkUiElements['window'])


	def nameInput(self, slot, *args):
		name = cmds.ls(sl = True)
		for n in name:
			cmds.textField(slot, e = True, it = n, ip = 0)
			if name.index(n) != len(name)-1:
				cmds.textField(slot, e = True, it = ',', ip = 0)

	def weaponQuery(self):
		name = cmds.textField(self.arkUiElements['inputText'], q = True, text = True)
		return name
	
	def projQuery(self):
		projs = []
		projs.append(cmds.textField(self.arkUiElements['inputProjText'], q = True, text = True))
		return projs

	def chamberQuery(self):
		chamber = cmds.textField(self.arkUiElements['inputProjChamberText'], q = True, text = True)
		return chamber

	def rightSpace(self, *args):
		print 'SwitchingSpaces'
		import core.spaceSwitch as switch
		reload(switch)
		switch = switch.SpaceSwitchTPV()
		self.target = self.weaponQuery()
		print self.target
		switch.infToTar(self.rightHand, self.leftHand, self.customL, self.customR, self.target)

	def leftSpace(self, *args):
		print 'SwitchingSpaces'
		import core.spaceSwitch as switch
		reload(switch)
		switch = switch.SpaceSwitchTPV()
		self.target = self.weaponQuery()
		print self.target
		switch.infToTar(self.leftHand, self.rightHand, self.customL, self.customR, self.target)

	def right2HWeap(self, *args):
		print 'SwitchingSpaces'
		import core.spaceSwitch as switch
		reload(switch)
		switch = switch.SpaceSwitchTPV()
		self.target = self.weaponQuery()
		print self.target
		switch.infToTarToI(self.rightHand, self.leftHand, self.customL, self.customR, self.target)

	def left2HWeap(self, *args):
		print 'SwitchingSpaces'
		import core.spaceSwitch as switch
		reload(switch)
		switch = switch.SpaceSwitchTPV()
		self.target = self.weaponQuery()
		print self.target
		switch.infToTarToI(self.leftHand, self.rightHand, self.customR, self.customL, self.target)

	def detach(self, *args):
		print 'Detaching'
		import core.spaceSwitch as switch
		reload(switch)
		switch = switch.SpaceSwitchTPV()
		self.target = self.weaponQuery()
		print self.target
		switch.removeCons(self.rightHand, self.leftHand, self.customL, self.customR, self.target)

	def weapInf(self, *args):
		print 'SwitchingSpaces'
		import core.spaceSwitch as switch
		reload(switch)
		switch = switch.SpaceSwitchTPV()
		self.target = self.weaponQuery()
		print self.target
		switch.weaponInf(self.rightHand, self.leftHand, self.customL, self.customR, self.target)

	def projL(self, *args):
		print 'SwitchingSpaces'
		import core.spaceSwitch as switch
		reload(switch)
		switch = switch.SpaceSwitchTPV()
		self.targets = self.projQuery()[0]
		print self.targets
		switch.projToI(self.leftHand, self.rightHand, self.customL, self.customR, self.targets)

	def projR(self, *args):
		print 'SwitchingSpaces'
		import core.spaceSwitch as switch
		reload(switch)
		switch = switch.SpaceSwitchTPV()
		self.targets = self.projQuery()[0]
		print self.targets
		switch.projToI(self.rightHand, self.leftHand, self.customL, self.customR, self.targets)

	def projW(self, *args):
		print 'SwitchingSpaces'
		import core.spaceSwitch as switch
		reload(switch)
		switch = switch.SpaceSwitchTPV()
		self.targets = self.projQuery()[0]
		self.chamber = self.chamberQuery()
		print self.targets
		switch.projToI(self.chamber, self.leftHand, self.customL, self.customR, self.targets)

	def projDetach(self, *args):
		print 'Detaching'
		import core.spaceSwitch as switch
		reload(switch)
		switch = switch.SpaceSwitchTPV()
		self.targets = self.projQuery()[0]
		print self.targets
		switch.removeProjCons(self.rightHand, self.leftHand, self.customL, self.customR, self.targets)
