from maya import cmds

SUFFIXES = {
    "mesh": "geo",
    "joint": "jnt",
    "camera": None,
    "ambientLight": "lgt"
}

DEFAULT_SUFFIX = "grp"


def rename(selection=False):
    """
    Renames any object with correct suffix from the suffix dictionary
    :param selection: If True, use the currently selected items
    :return:List of all objects that the function was operated on
    """

    # selection equals all selected items
    objects = cmds.ls(selection=selection, dag=True, long=True)

    if selection and not objects:
        raise RuntimeError("You don't have any objects selected.")

    # By sorting the selection list by the number of "|" chartacters, I make sure children objects come before parents
    objects.sort(key=lambda x: x.count('|'), reverse=True)

    # remove long form and get only the name of the obj, find the object type of each obj
    for obj in objects:
        shortName = obj.split("|")[-1]
        children = cmds.listRelatives(obj, children=True, fullPath=True) or []

        if len(children) == 1:
            child = children[0]
            objType = cmds.objectType(child)
        else:
            objType = cmds.objectType(obj)

        # add appropriate suffix to each object
        suffix = SUFFIXES.get(objType, DEFAULT_SUFFIX)
        if not suffix:
            continue

        if obj.endswith('_'+suffix):
            continue

        # generate new name
        newName = "%s_%s" % (shortName, suffix)

        # rename each
        cmds.rename(obj, newName)

        index = objects.index(obj)
        objects[index] = obj.replace(shortName, newName)

    return objects
