import ast
import _ast
import inspect
import functools

class Enum(object):
    def __init__(self, *args): 
        for arg in args:
            assert type(arg) is str

        self.enum_list = list(args)

def state_machine(node, enum_to_check, state='', enum_var=None):
    if state is '':
        assert type(node) is _ast.Module
        state = 'module'
    elif state is 'module':
        assert type(node) is _ast.FunctionDef
        state = 'function'
    elif state is 'function':
        _check_node_for_state_function(node)
        enum_var = node.args[0].id
        state = 'match_branch'
    elif state is 'match_branch':
        enum_match_list = _get_enum_match_list_to_check(
                node=node,
                enum_var=enum_var
        )
        assert enum_to_check.enum_list == enum_match_list, \
                ('enum states expected & actual', enum_to_check.enum_list, enum_match_list)
            
        state = 'done_match'
    elif state is 'done_match':
        # TODO iterate other nodes and verify there isn't an if condition or other
        # code basically
        state = 'done'
    else:
        assert False, 'unknown state'

    return state, enum_var

def _check_node_for_state_function(node):
    assert type(node) is _ast.arguments
    assert len(node.args) == 1
    assert node.defaults == []
    assert node.kwarg is None
    assert node.vararg is None

def _get_enum_match_list_to_check(node, enum_var):
    itr_node = node
    enum_match_list = []
    while True:
        assert type(itr_node) is _ast.If

        test_expression = itr_node.test
        assert type(test_expression) is _ast.Compare

        left = test_expression.left
        assert type(left) is _ast.Name
        assert left.id == enum_var

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


def parse_ast(func):
    source = inspect.getsource(func)
    return ast.parse(source=source, filename='raw_source')

def test_ast(parse_tree, enum_to_check):
    state = ''
    enum_var = None
    for node in ast.walk(parse_tree):
        if state is 'done':
            break
        state, enum_var = state_machine(
                node=node,
                enum_to_check=enum_to_check,
                state=state,
                enum_var=enum_var
        )

    if state is 'done':
        return True
    return False

def check_match_decorator(enum_to_check):
    assert enum_to_check

    def actual_decorator(func):
        parse_tree = parse_ast(func)
        assert test_ast(parse_tree, enum_to_check)
        return func
    return actual_decorator
