import pytest
from lexer.parse_tree import *
from lexer.value_node import *
from lexer.boolean_node import *
from lexer.string_node import *

@pytest.fixture
def p():
    return ValueNode()

def test_find_boolean_true(p):
    p.find_boolean("true")
    assert p.children[0].get_value() == True

def test_find_boolean_false(p):
    p.find_boolean("false")
    assert p.children[0].get_value() == False

def test_find_string(p):
    p.find_string("'i am a string'")
    assert len(p.children) == 1
    assert isinstance(p.children[0], StringNode)
    assert p.children[0].children[0].value == "i"

def test_find_string_escaped(p):
    p.find_string(r"'i \\\''")
    assert isinstance(p.children[0].children[2], EscapedNode)
    assert p.children[0].children[2].get_value() == r"\\"
    assert p.children[0].children[3].get_value() == r"\'"

def test_find_string_error(p):
    with pytest.raises(ParseError) as errInfo:
        p.find_string(r"'I can\'t even'")
    assert errInfo.value.msg == "Malformed string"

def test_string_output(p):
    p.find_string(r"'char \\ a \''")
    assert str(p.children[0]) == r"char \ a '"

def test_array(p):
    p.find_array("[true, true, false, false]")
    assert isinstance(p.children[0], ArrayNode)
