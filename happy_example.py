from sum_type_decorator import check_match_decorator, Enum
from collections import namedtuple

MurderByNumbers = Enum('one', 'two', 'three')


@check_match_decorator(MurderByNumbers)
def match_enum(enum_struct):
    if enum_struct.tag == 'one':
        print('for tag one')
    elif enum_struct.tag == 'two':
        print('for tag two')
    elif enum_struct.tag == 'three':
        print('for tag three')

if __name__ == '__main__':
    EnumStruct = namedtuple('EnumStruct', ['tag', 'data'])
    k = EnumStruct(tag='one', data={})
    match_enum(k)
