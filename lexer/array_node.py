from parse_tree import *
import value_node

class ArrayNode(value_node.ValueNode):
    def __init__(self):
        self.children = []

    @classmethod
    def create_and_parse(cls, content):
        anode = cls()
        
