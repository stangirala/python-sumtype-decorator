from sum_type_decorator import check_match_decorator, Enum
from collections import namedtuple

MurderByNumbers = Enum('one', 'two', 'three')

print('\n---Will throw exception')

@check_match_decorator(MurderByNumbers)
def bad_match_enum(enum):
    if enum == 'one':
        pass
    elif enum == 'two':
        pass

if __name__ == '__main__':
    EnumStruct = namedtuple('EnumStruct', ['tag', 'data'])
    k = EnumStruct(tag='one', data={})
    bad_match_enum(k)
