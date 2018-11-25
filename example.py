from sum_type_decorator import check_match_decorator, Enum

MurderByNumbers = Enum('one', 'two', 'three')

@check_match_decorator(MurderByNumbers)
def match_enum(enum):
    if enum == 'one':
        pass
    elif enum == 'two':
        pass
    elif enum == 'three':
        pass

# Will throw exception
@check_match_decorator(MurderByNumbers)
def bad_match_enum(enum):
    if enum == 'one':
        pass
    elif enum == 'two':
        pass
