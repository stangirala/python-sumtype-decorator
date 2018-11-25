import ast
import _ast
import inspect
import functools

class Enum(object):
    def __init__(self, *args): 
        for arg in args:
            assert type(arg) is str

        self.enum_list = list(args)

def state_machine(node, enum_to_check):
    assert type(node) is _ast.Module

    module_children = list(ast.iter_child_nodes(node))
    assert len(module_children) == 1

    function_node = module_children[0]
    enum_var = _get_enum_name_from_function_node(function_node.args)

    assert len(function_node.body) == 1
    enum_match_list = _get_enum_match_list_to_check(function_node.body[0], enum_var)

    assert enum_to_check.enum_list == enum_match_list, \
        ('enum list: expected, actual,', enum_to_check.enum_list, enum_match_list)

    return True

def _get_enum_name_from_function_node(node):
    assert type(node) is _ast.arguments
    assert len(node.args) == 1
    assert node.defaults == []
    assert node.kwarg is None
    assert node.vararg is None

    return node.args[0].id

def _get_enum_match_list_to_check(node, enum_var):
    itr_node = node
    enum_match_list = []
    while True:
        assert type(itr_node) is _ast.If

        test_expression = itr_node.test
        assert type(test_expression) is _ast.Compare

        left = test_expression.left
        if type(left) is _ast.Name:
            assert left.id == enum_var
        elif type(left) is _ast.Attribute:
            assert left.value.id == enum_var
        else:
            print(ast.dump(left))
            assert 'if expression type was neither Name not Attribute'

        assert len(test_expression.ops) == 1
        assert type(test_expression.ops[0]) is _ast.Eq

        assert len(test_expression.comparators) == 1
        assert type(test_expression.comparators[0]) is _ast.Str
        enum_match_list.append(test_expression.comparators[0].s)
        # ignore the match body

        if len(itr_node.orelse) == 0:
            break
        itr_node = itr_node.orelse[0]

    return enum_match_list

def check_match_decorator(enum_to_check):
    assert enum_to_check

    def actual_decorator(func):
        source = inspect.getsource(func)
        parse_tree = ast.parse(source=source, filename='raw_source')

        assert state_machine(node=parse_tree, enum_to_check=enum_to_check)

        return func
    return actual_decorator
