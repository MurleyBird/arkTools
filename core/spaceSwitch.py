import maya.cmds as cmds


class SpaceSwitchTPV():


    def __init__(self):
        print 'Space Switch Initialized'

    def getXforms(self, influenceA, influenceB, target):
        self.infA_Trans = cmds.xform(influenceA, q = True, ws = True, t = True)
        self.infA_Rot = cmds.xform(influenceA, q = True, ws = True, ro = True)
        self.infB_Trans = cmds.xform(influenceB, q = True, ws = True, t = True)
        self.infB_Rot = cmds.xform(influenceB, q = True, ws = True, ro = True)
        self.target_Trans = cmds.xform(target, q = True, ws = True, t = True)
        self.target_Rot = cmds.xform(target, q = True, ws = True, ro = True)
        return self.infA_Trans, self.infA_Rot, self.infB_Trans, self.infB_Rot, self.target_Trans, self.target_Rot

    def removeCons(self, influenceA, influenceB, customA, customB, target):
        cons = []
        targets = [influenceA, influenceB, customA, customB, target]
        for t in targets:
            tarCons = cmds.listRelatives(t, c = True, typ = 'parentConstraint')
            tarConsType = cmds.nodeType(tarCons)
            if tarConsType == 'parentConstraint':
                cons.append(tarCons[0])
            else:
                print 'No Constraint  Detected'

        if len(cons) > 0:
            for c in cons:
                cmds.delete(c)

    def removeProjCons(self, influenceA, influenceB, customA, customB, targets):
        cons = []
        projectiles = []
        name = targets.split(',')
        for n in name:
            projectiles.append(n)
        for p in projectiles:
            tarCons = cmds.listRelatives(p, c = True, typ = 'parentConstraint')
            tarConsType = cmds.nodeType(tarCons)
            if tarConsType == 'parentConstraint':
                cons.append(tarCons[0])
            else:
                print 'No Constraint  Detected'

        if len(cons) > 0:
            for c in cons:
                cmds.delete(c)

    def infToTar(self, influenceA, influenceB, customA, customB, target):
        self.getXforms(influenceA, influenceB, target)
        self.removeCons(influenceA, influenceB, customA, customB, target)
        cmds.xform(influenceA, ws = True, t = self.target_Trans)
        cmds.xform(influenceA, ws = True, ro = self.target_Rot)
        cmds.parentConstraint(influenceA, target)

    def infToTarToI(self, influenceA, influenceB, customA, customB, target):
        self.getXforms(influenceA, influenceB, target)
        self.removeCons(influenceA, influenceB, customA, customB, target)
        self.infToTar(influenceA, influenceB, customA, customB, target)
        cmds.parentConstraint(target, customA, mo = True)

    def weaponInf(self, influenceA, influenceB, customA, customB, target):
        self.getXforms(influenceA, influenceB, target)
        self.removeCons(influenceA, influenceB, customA, customB, target)
        cmds.parentConstraint(target, customA, mo = True)
        cmds.parentConstraint(target, customB, mo = True)

    def projToI(self, influence, influenceB, customA, customB, targets):
        projectiles = []
        currentTime = cmds.currentTime(q = True)
        name = targets.split(',')
        for n in name:
            projectiles.append(n)
        for p in projectiles:
            self.getXforms(influence, influenceB, p)
            currentCons = cmds.parentConstraint(influence, p, mo = True)
            currentAlias = cmds.parentConstraint(currentCons, q = True, wal = True)
            for c in currentAlias:
                if currentAlias.index(c) == 0:
                    cmds.setKeyframe(currentCons[0], v = 1, t = currentTime, at = c)
                elif currentAlias.index(c) != 0:
                    cmds.setKeyframe(currentCons[0], v = 1, t = currentTime-1, at =  currentAlias[currentAlias.index(c)-1])
                    cmds.setKeyframe(currentCons[0], v = 0, t = currentTime, at =  currentAlias[currentAlias.index(c)-1])
                    cmds.setKeyframe(currentCons[0], v = 0, t = currentTime-1, at =  c)
                    cmds.setKeyframe(currentCons[0], v = 1, t = currentTime, at =  c)
            print currentAlias