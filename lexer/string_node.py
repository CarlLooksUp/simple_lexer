from parse_tree import *

class StringNode(ParseTree):
    def __init__(self, content=None):
        self.children = []
        self.value = content

    def get_value(self):
        return str(self)

    def __str__(self):
        return "".join("%s" % str(x) for x in self.children)

class LiteralNode(TreeNode):
    pass

class EscapedNode(TreeNode):
    def __str__(self):
        return self.value.decode('string_escape')

    def get_value(self):
        return str(self)
