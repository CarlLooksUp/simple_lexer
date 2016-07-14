import pytest
from lexer.parse_tree import *
from lexer.string_node import *
from lexer.lexer import Lexer

@pytest.fixture
def l():
    return Lexer()

def test_boolean_parse_true(l):
    tree = l.parse("true")
    assert tree.children[0].get_value() == True

def test_boolean_parse_false(l):
    tree = l.parse("false")
    assert tree.children[0].get_value() == False

def test_string_parse(l):
    tree = l.parse("'i am a string'")
    assert len(tree.children) == 1
    assert isinstance(tree.children[0], StringNode)
    assert tree.children[0].children[0].value == "i"

def test_string_parse_escape(l):
    tree = l.parse(r"'i \\\''")
    assert isinstance(tree.children[0].children[2], EscapedNode)
    assert tree.children[0].children[2].get_value() == "\\"
    assert tree.children[0].children[3].get_value() == "'"

def test_string_parse_error(l):
    with pytest.raises(ParseError) as errInfo:
        tree = l.parse(r"'I can\'t even'")
    assert errInfo.value.msg == "Invalid string character"

def test_string_output(l):
    tree = l.parse(r"'char \\ a \''")
    assert tree.output() == r"char \ a '"

def test_empty_string(l):
    tree = l.parse(r"''")
    assert tree.output() == "" 

def test_unterminated_string(l):
    with pytest.raises(ParseError) as errInfo:
        tree = l.parse(r"'i forgot the last quote")
    assert errInfo.value.msg == "Unterminated string"

def test_array(l):
    tree = l.parse("[true, true, false, false]")
    assert isinstance(tree.children[0], ArrayNode)
    assert tree.children[0].get_value() == [True, True, False, False]

def test_mixed_array(l):
    tree = l.parse("[['help', 'me'], true, 'mega man', '[stuff]']")
    assert tree.children[0].get_value() == [["help", "me"], True, "mega man", "[stuff]"]

def test_empty_array(l):
    tree = l.parse("[]")
    assert tree.output() == []

def test_array_delim_error(l):
    with pytest.raises(ParseError) as errInfo:
        tree = l.parse(r"true, false")
    assert errInfo.value.msg == "Invalid syntax"

def test_generic_syntax_error(l):
    with pytest.raises(ParseError) as errInfo:
        tree = l.parse(r"no statement")
    assert errInfo.value.msg == "Invalid syntax"

def test_case_1(l):
    tree = l.parse("'datto is hiring'")
    assert tree.output() == "datto is hiring"

def test_case_2(l):
    tree = l.parse(r"[true, 'true', '\'d\' is for \'datto\'']")
    assert tree.output() == [True, "true", "'d' is for 'datto'"]
