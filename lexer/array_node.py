from parse_tree import *
import value_node

class ArrayNode(value_node.ValueNode):
    def __init__(self, content):
        self.children = []
        self.parse(content, first=True)

    def parse(self, content, first=False):
        if not first:
            content = content.lstrip(", ")
        super.parse(content)
