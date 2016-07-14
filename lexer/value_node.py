from parse_tree import *
from boolean_node import *
from string_node import *
from array_node import *

class ValueNode(ParseTree):
    def __init__(self, content=None):
        self.children = []
        if content:
            self.parse(content)

    def parse(self, content):
        if self.eof(content) or self.find_boolean(content) \
                                   or self.find_string(content) \
                                   or self.array(content):
            return True
        else:
            raise ParseError("Malformed value", content)

    def find_boolean(self, content):
        return BooleanNode.match_and_recurse(self, re.compile(r"(true|false)"), content.lstrip())

    def find_string(self, content):
        if content[0] == "'":
            closing_quote = re.search(r"(^|[^\\])((\\\\)*)(')", content[1:])
            if closing_quote:
                quote_idx = closing_quote.end(4)
                self.add(StringNode(content[1:quote_idx]))
                return self.parse(content[quote_idx+1:])
            else:
                return False
        else:
            return False

    def find_array(self, content):
        if content[0] == "[":
            closing_bracket_idx = self.find_array_end(content)
            self.add(ArrayNode(content[1:closing_bracket_idx]))
            return self.parse(content[closing_bracket_idx:])
        else:
            return False

    def find_array_end(self, content):
        cursor = 1
        open_bracket = 1
        for idx, c in enumerate(content[cursor:]):
            if c == '[':
                open_bracket += 1
            elif c == ']':
                open_bracket -= 1
            if open_bracket == 0:
                cursor = cursor + idx
                return cursor
