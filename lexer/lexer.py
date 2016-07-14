from parse_tree import *
from string_node import *
from string_cursor import StringCursor
import re

#Regex patterns for syntax matching
LITERAL = re.compile(r"([a-z \,\[\]])")
ESCAPED = re.compile(r"(\\'|\\\\)")
BOOL = re.compile(r"(true|false)")
DELIMITER = re.compile(r"\, ")

#Module lexer, containing parsing functions for simple syntax code
class Lexer:
    def parse(self, content):
        context = ParseTree()
        sc = StringCursor(content) 

        #loop over the 'code', considering one character at a time.
        #some instructions require looking ahead, and will call 
        #StringCursor.read() to do so
        while not sc.end():
            char = sc.read_one()

            #find array nodes
            if char == "[":
                array = ArrayNode()
                context.add(array)
                context = array 

            elif (DELIMITER.match(sc.read()) and 
                  isinstance(context, ArrayNode)):
                #skip past the delimiter if it's in the right context
                sc.increment(DELIMITER.match(sc.read()).end(0)-1)

            #close array nodes
            elif char == "]" and isinstance(context, ArrayNode):
                context = context.parent

            #find string nodes. population handled by parse_string()
            elif char == "'":
                snode = StringNode()
                sc.increment()
                self.parse_string(snode, sc) #increments StringCursor
                context.add(snode)

            elif BOOL.match(sc.read()):
                match = BOOL.match(sc.read())
                context.add(BooleanNode(match.group(1)))
                sc.increment(match.end(1)-1)

            else:
                raise ParseError("Invalid syntax", char)
            sc.increment() #move to next character

        return context #return full parse tree 

    def parse_string(self, context, sc):
        char = sc.read_one()
        
        #starting after opening quote, looking for closing quote
        while char is not "'": 
            if LITERAL.match(char):
                l = LiteralNode(char)
                context.add(l)
                sc.increment()
            else:
                match = ESCAPED.match(sc.read())
                if match:
                    e = EscapedNode(match.group(1))
                    context.add(e)
                    sc.increment(match.end(1)) #skips over escaped quotes
                else:
                    raise ParseError("Invalid string character", char)
            
            #raise error if we run out of characters before string ends
            if sc.end():
                raise ParseError("Unterminated string", '')
            else:
                char = sc.read_one() 


if __name__ == "__main__":
    input_ = r"'datto is hiring'"
    print Lexer().parse(input_).output()
