from tweenerUI import tween
from gearClassCreator import Gear
from maya import cmds


class BaseWindow(object):
    """
    A base window UI object, used as an abstract class.
    """
    # static variable
    windowName = "BaseWindow"

    def show(self):
        # if window already exists, delete the previous one and create a new one
        if cmds.window(self.windowName, query=True, exists=True):
            cmds.deleteUI(self.windowName)

        cmds.window(self.windowName)

        self.buildUI()

        cmds.showWindow()

    def buildUI(self):
        pass

    def close(self, *args):
        cmds.deleteUI(self.windowName)

    def reset(self, *args):
        pass


class TweenerUI(BaseWindow):
    """
    Inherits from BaseWindow, an animation tweener UI object. Users can use the slider between two keyframes to tween
    """

    windowName = "TweenerWindow"

    def buildUI(self):
        column = cmds.columnLayout()
        cmds.text(label="Use the slider to set the tween amount")
        row = cmds.rowLayout(numberOfColumns=2)
        self.slider = cmds.floatSlider(min=0, max=100, value=50, step=1, changeCommand=tween)
        cmds.button(label="Reset", command=self.reset)

        cmds.setParent(column)
        cmds.button(label="Close", command=self.close)

    def reset(self, *args):
        cmds.floatSlider(self.slider, edit=True, value=50)


class GearUI(BaseWindow):
    """
    A UI component for the Gear creation and modification process. Inherits BaseWindow, and uses the gearClassCreator
    """

    windowName = "GearWindow"

    def __init__(self):
        self.gear = None

    def buildUI(self):
        column = cmds.columnLayout()
        cmds.text(label="Use the slider to modify the gear")

        cmds.rowLayout(numberOfColumns=4)
        self.label = cmds.text(label="10")
        self.slider = cmds.intSlider(min=5, max=30, value=10, step=1, dragCommand=self.modifyGear)
        cmds.button(label="Make Gear", command=self.makeGear)
        cmds.button(label="Reset", command=self.reset)

        cmds.setParent(column)
        cmds.button(label="Close", command=self.close)

    def makeGear(self, *args):
        teeth = cmds.intSlider(self.slider, query=True, value=True)

        self.gear = Gear()
        self.gear.createGear(teeth=teeth)

    def modifyGear(self, teeth):
        if self.gear:
            self.gear.changeTeeth(teeth=teeth)

        cmds.text(self.label, edit=True, label=teeth)

    def reset(self, *args):
        self.gear = None
        cmds.intSlider(self.slider, edit=True, value=10)
        cmds.text(self.label, edit=True, label=10)
