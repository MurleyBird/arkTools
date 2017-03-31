import maya.cmds as cmds


class SpaceSwitch():

	def __init__(self):
		print 'Parenting'

	def getNameSpaces(self, influenceA, influenceB, target):
		self.tarNameSpace = target.rpartition(':')[0]
		self.infANameSpace = influenceA.rpartition(':')[0]
		self.infBNameSpace = influenceB.rpartition(':')[0]

	def getXforms(self, influenceA, influenceB, target):
		self.infA_Trans = cmds.xform(influenceA, q = True, ws = True, t = True)
		self.infA_Rot = cmds.xform(influenceA, q = True, ws = True, ro = True)
		self.infB_Trans = cmds.xform(influenceB, q = True, ws = True, t = True)
		self.infB_Rot = cmds.xform(influenceB, q = True, ws = True, ro = True)
		self.target_Trans = cmds.xform(target, q = True, ws = True, t = True)
		self.target_Rot = cmds.xform(target, q = True, ws = True, ro = True)

	def infAToTar(self, influenceA, target):
		cmds.xform(influenceA, ws = True, t = self.target_Trans)
		cmds.xform(influenceA, ws = True, ro = self.target_Rot)
		cmds.parentConstraint(influenceA, target)