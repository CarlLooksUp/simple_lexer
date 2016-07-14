from parse_tree import LeafNode

class BooleanNode(LeafNode):
    def get_value(self):
        return self.value == "true"
