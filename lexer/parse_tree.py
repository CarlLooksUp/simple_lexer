import re

class ParseTree:
    def __init__(self):
        self.children = []

    def add(self, node):
        self.children.append(node)
        node.parent = self

    def output(self):
        if len(self.children) == 1:
            return self.children[0].get_value()
        else:
            return [x.get_value() for x in self.children] 


class TreeNode(ParseTree):
    def __init__(self, value=None):
        self.value = value
        self.children = []

    def get_value(self):
        return self.value

    def __str__(self):
        return str(self.value)

class BooleanNode(TreeNode):
    def __init__(self, value):
         self.value = (value == "true")

class ArrayNode(TreeNode):
    def get_value(self):
        return [x.get_value() for x in self.children]

class ParseError(Exception):
    def __init__(self, msg, content):
        self.msg = msg
        self.content = content

    def __str__(self):
        return "{0} \n Parsing: {1}".format(self.msg, self.content)
