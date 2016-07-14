from parse_tree import *

class StringNode(ParseTree):
    def __init__(self, content):
        self.children = []
        self.parse(content)

    def parse(self, content):
        if self.find_literal(content) or self.find_escaped(content) or self.eof(content):
            return True
        else:
            raise ParseError("Malformed string", content)

    def find_literal(self, content):
        return LiteralNode.match_and_recurse(self, re.compile(r"([a-z \,\[\]])"), content)

    def find_escaped(self, content):
        return EscapedNode.match_and_recurse(self, re.compile(r"(\\'|\\\\)"), content)

    def __str__(self):
        output = ""
        for node in self.children:
            output += str(node)
        print output
        return output

class LiteralNode(LeafNode):
    pass

class EscapedNode(LeafNode):
    def __str__(self):
        return self.value.decode('string_escape')
