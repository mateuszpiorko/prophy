import model
from collections import namedtuple

Action = namedtuple("Action", ["action", "params"])

def parse(filename):
    """
    Parses file and extracts from it all operations which will be perform
        :param filename: path to parch file
        :type filename: string

        :return: list with action which will be perform
        :rtype: list
    """
    def make_item(line):
        words = line.split()
        name, action = words[:2]
        params = words[2:]
        return name, Action(action, params)
    patches = {}
    for name, action in (make_item(line) for line in open(filename) if line.strip()):
        patches.setdefault(name, []).append(action)
    return patches

def patch(nodes, patches):
    """
    Performs operations from patch file
        :param nodes: all elements from model
        :type nodes: list

        :param patches: actions from patch file
        :type patches: dictionary 
    """
    for node in nodes:
        actions = patches.get(node.name, [])
        for patch in actions:
            _apply(node, patch)

def _apply(node, patch):
    action = _actions.get(patch.action)
    if not action:
        raise Exception("Unknown action: %s %s" % (node.name, patch))
    action(node, patch)

def _type(node, patch):
    if not isinstance(node, model.Struct):
        raise Exception("Can change field only in struct: %s %s" % (node.name, patch))

    if len(patch.params) != 2:
        raise Exception("Change field must have 2 params: %s %s" % (node.name, patch))
    name, tp = patch.params

    i, member = next((x for x in enumerate(node.members) if x[1].name == name), (None, None))
    if not member:
        raise Exception("Member not found: %s %s" % (node.name, patch))

    p1, _, p3, p4, p5, p6 = node.members[i]
    node.members[i] = model.StructMember(p1, tp, p3, p4, p5, p6)

def _insert(node, patch):
    if not isinstance(node, model.Struct):
        raise Exception("Can insert field only in struct: %s %s" % (node.name, patch))

    if len(patch.params) != 3:
        raise Exception("Change field must have 3 params: %s %s" % (node.name, patch))
    index, name, tp = patch.params

    if not _is_int(index):
        raise Exception("Index is not a number: %s %s" % (node.name, patch))
    index = int(index)

    node.members.insert(index, model.StructMember(name, tp, None, None, None, None))

def _remove(node, patch):
    if not isinstance(node, model.Struct):
        raise Exception("Can remove field only in struct: %s %s" % (node.name, patch))

    if len(patch.params) != 1:
        raise Exception("Remove field must have 1 param: %s %s" % (node.name, patch))
    name, = patch.params

    i, member = next((x for x in enumerate(node.members) if x[1].name == name), (None, None))
    if not member:
        raise Exception("Member not found: %s %s" % (node.name, patch))

    del node.members[i]

def _dynamic(node, patch):
    if not isinstance(node, model.Struct):
        raise Exception("Can change field only in struct: %s %s" % (node.name, patch))

    if len(patch.params) != 2:
        raise Exception("Change field must have 2 params: %s %s" % (node.name, patch))
    name, len_name = patch.params

    i, member = next((x for x in enumerate(node.members) if x[1].name == name), (None, None))
    if not member:
        raise Exception("Member not found: %s %s" % (node.name, patch))

    p1, p2, _, _, _, _ = node.members[i]
    node.members[i] = model.StructMember(p1, p2, True, len_name, None, None)

def _greedy(node, patch):
    if not isinstance(node, model.Struct):
        raise Exception("Can change field only in struct: %s %s" % (node.name, patch))

    if len(patch.params) != 1:
        raise Exception("Change field must have 1 params: %s %s" % (node.name, patch))
    name, = patch.params

    i, member = next((x for x in enumerate(node.members) if x[1].name == name), (None, None))
    if not member:
        raise Exception("Member not found: %s %s" % (node.name, patch))

    p1, p2, _, _, _, _ = node.members[i]
    node.members[i] = model.StructMember(p1, p2, True, None, None, None)

def _static(node, patch):
    if not isinstance(node, model.Struct):
        raise Exception("Can change field only in struct: %s %s" % (node.name, patch))

    if len(patch.params) != 2:
        raise Exception("Change field must have 2 params: %s %s" % (node.name, patch))
    name, size = patch.params

    if not _is_int(size):
        raise Exception("Size is not a number: %s %s" % (node.name, patch))

    i, member = next((x for x in enumerate(node.members) if x[1].name == name), (None, None))
    if not member:
        raise Exception("Member not found: %s %s" % (node.name, patch))

    p1, p2, _, _, _, _ = node.members[i]
    node.members[i] = model.StructMember(p1, p2, True, None, size, None)

def _limited(node, patch):
    if not isinstance(node, model.Struct):
        raise Exception("Can change field only in struct: %s %s" % (node.name, patch))

    if len(patch.params) != 2:
        raise Exception("Change field must have 2 params: %s %s" % (node.name, patch))
    name, len_array = patch.params

    i, member = next((x for x in enumerate(node.members) if x[1].name == len_array), (None, None))
    if not member:
        raise Exception("Array len member not found: %s %s" % (node.name, patch))

    i, member = next((x for x in enumerate(node.members) if x[1].name == name), (None, None))
    if not member:
        raise Exception("Member not found: %s %s" % (node.name, patch))

    p1, p2, _, _, p3, _ = node.members[i]
    node.members[i] = model.StructMember(p1, p2, True, len_array, p3, None)


_actions = {'type': _type,
            'insert': _insert,
            'remove': _remove,
            'greedy': _greedy,
            'static': _static,
            'limited': _limited,
            'dynamic': _dynamic}

def _is_int(s):
    try:
        int(s)
        return True
    except ValueError:
        return False