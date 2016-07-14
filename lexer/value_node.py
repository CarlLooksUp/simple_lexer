from parse_tree import *
from boolean_node import *
from string_node import *
from array_node import *

class ValueNode(ParseTree):
    def __init__(self, content):
        self.children = []
        self.parse(content)

    def parse(self, content):
        if self.eof(content) or self.find_boolean(content) \
                                   or self.find_string(content) \
                                   or self.array(content):
            self.print_tree()
        else:
            raise ParseError("Malformed value", content)

    def find_boolean(self, content):
        BooleanNode.match_and_recurse(self, re.compile(r"(true|false)"), content.lstrip())

    def find_string(self, content):
        if content[0] == "'":
            closing_quote = re.search(r"(^|[^\\])((\\\\)*)(')", content[1:])
            if closing_quote:
                quote_idx = closing_quote.end(4)
                self.add(StringNode(content[1:quote_idx]))
                self.parse(content[quote_idx+1:])
            else:
                return False
        else:
            return False

    def find_array(self, content):
        if content[0] == "[":
           array, cursor = ArrayNode.create_and_parse(content[1:])
        if array_match:
            self.add(ArrayNode(array_match.group(1)))
        else:
            return False

    def find_array_end(self, content):
