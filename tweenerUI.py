from maya import cmds


def tween(percentage, obj=None, attrs=None, selection=True):
    # No object is given and no object is selected, function can't run
    if not obj and not selection:
        raise ValueError("No object given to tween")

    # No object is specified, so get first object in selection
    if not obj:
        obj = cmds.ls(selection=True)[0]

    # List all attributes that are keyable
    if not attrs:
        attrs = cmds.listAttr(obj, keyable=True)

    currentTime = cmds.currentTime(query=True)

    for attr in attrs:
        # create full attribute name
        attrFull = '%s.%s' % (obj, attr)

        # get list of all keyframes for given attribute
        keyframes = cmds.keyframe(attrFull, query=True)

        # if no keyframes continue
        if not keyframes:
            continue

        # loop over frames, if frame is before current time, add it to the list
        previousKeyframes = [frame for frame in keyframes if frame < currentTime]

        # loop over frames, if frame is after current time, add it to the list
        laterKeyframes = [frame for frame in keyframes if frame > currentTime]

        if not previousKeyframes and not laterKeyframes:
            continue

        # find the closest frame to current time
        previousFrame = max(previousKeyframes) if previousKeyframes else None
        nextFrame = min(laterKeyframes) if laterKeyframes else None

        if not previousFrame or not nextFrame:
            continue

        # get the values
        previousValue = cmds.getAttr(attrFull, time=previousFrame)
        nextValue = cmds.getAttr(attrFull, time=nextFrame)

        # find out the difference, and the weighted difference using input param percentage
        difference = nextValue - previousValue
        weightedDifference = (difference * percentage) / 100.0

        currentValue = previousValue + weightedDifference

        # add the required keyframe
        cmds.setKeyframe(attrFull, time=currentTime, value=currentValue)


class TweenWindow(object):
    # static variable
    windowName = "TweenerWindow"

    def show(self):
        # if window already exists, delete the previous one and create a new one
        if cmds.window(self.windowName, query=True, exists=True):
            cmds.deleteUI(self.windowName)

        cmds.window(self.windowName)

        self.buildUI()

        cmds.showWindow()

    def buildUI(self):
        column = cmds.columnLayout()
        cmds.text(label="Use the slider to set the tween amount")
        row = cmds.rowLayout(numberOfColumns=2)
        self.slider = cmds.floatSlider(min=0, max=100, value=50, step=1, changeCommand=tween)
        cmds.button(label="Reset", command=self.reset)

        cmds.setParent(column)
        cmds.button(label="Close", command=self.close)

    def close(self, *args):
        cmds.deleteUI(self.windowName)

    def reset(self, *args):
        cmds.floatSlider(self.slider, edit=True, value=50)
