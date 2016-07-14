import re

class ParseTree:

    def __init__(self):
        self.children = []

    def add(self, node):
        self.children.append(node)

    def print_tree(self):
        return ""

    def eof(self, content):
        return content.strip() == ""

    def clear(self):
        self.children = []


class LeafNode:
    def __init__(self, value_):
        self.value = value_

    def get_value(self):
        return self.value

    @classmethod
    def match_and_recurse(cls, target, pattern, content):
        match = pattern.match(content)
        if match:
            target.add(cls(match.group(1)))
            return target.parse(content[match.end(1):])
        else:
            return False

    def __str__(self):
        return str(self.value)


class ParseError(Exception):
    def __init__(self, msg, content):
        self.msg = msg
        self.content = content

    def __str__(self):
        return "{0} \n Parsing: {1}".format(self.msg, self.content)
