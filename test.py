from sum_type_decorator import check_match_decorator, Enum

MurderByNumbers = Enum('one', 'two', 'three')

def match_enum(enum):
    if enum == 'one':
        pass
    elif enum == 'two':
        pass
    elif enum == 'three':
        pass

def test_happy():
    check_match_decorator(MurderByNumbers)(match_enum)

def bad_match_enum(enum):
    if enum == 'one':
        pass
    elif enum == 'two':
        pass

def test_sad():
    try:
        check_match_decorator(MurderByNumbers)(bad_match_enum)
        assert False
    except AssertionError:
        pass
        
def match_enum_with_extra_code(enum):
    if enum == 'one':
        pass
    elif enum == 'two':
        pass
    elif enum == 'three':
        pass

    k = lambda x: None
    k()
    return None

def test_match_enum_with_extra_code():
    try:
        check_match_decorator(MurderByNumbers)(bad_match_enum)
        assert False
    except AssertionError:
        pass
