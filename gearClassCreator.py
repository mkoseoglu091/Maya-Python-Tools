from maya import cmds


class Gear(object):
    """
    Gear object that allows user to create and modify a gear
    """

    def __init__(self):
        """
        sets default values
        """
        self.transform = None
        self.extrude = None
        self.constructor = None

    def createGear(self, teeth=10, length=0.3):
        """
        creates a Gear object
        :param teeth: number of teeth
        :param length: length of each tooth
        :return: void
        """

        # Teeth of a gear are alternating faces
        spans = teeth * 2

        self.transform, self.constructor = cmds.polyPipe(subdivisionsAxis=spans)

        # When alternating faces are selected and ls -sl is inputted to MEL
        # the following range is selected. range(start, end, step)
        sideFaces = range(spans * 2, spans * 3, 2)

        cmds.select(clear=True)

        for face in sideFaces:
            # additivity selects each alternating face
            cmds.select('%s.f[%s]' % (self.transform, face), add=True)

        self.extrude = cmds.polyExtrudeFacet(localTranslateZ=length)[0]

    def changeTeeth(self, teeth=10, length=0.3):
        """
        Modifies the gear
        :param teeth: new teeth
        :param length: lenth of tooth
        :return: void
        """

        # calculates number of faces again
        spans = teeth*2

        # edit flag edits the existing instead of creating a new one
        cmds.polyPipe(self.constructor, edit=True, subdivisionsAxis=spans)

        sideFaces = range(spans*2, spans*3, 2)
        faceNames = []

        for face in sideFaces:
            faceName = 'f[%s]' % (face)
            faceNames.append(faceName)

        cmds.setAttr('%s.inputComponents' % (self.extrude), len(faceNames), *faceNames, type="componentList")

        #ltz is shortform of localTranslateZ
        cmds.polyExtrudeFacet(self.extrude, edit=True, ltz=length)
