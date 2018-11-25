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
        
