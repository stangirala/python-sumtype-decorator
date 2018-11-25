A simple decorator that checks the matching arms for all cases of a Sum Type. This
is similar to ML-style pattern matching without the Type Deconstruction. 

Here's a happy example which will fail on an Assertion if one of the if branches
are missing,
```
MurderByNumbers = Enum('one', 'two', 'three')

@check_match_decorator(MurderByNumbers)
def match_enum(enum):
    if enum == 'one':
        pass
    elif enum == 'two':
        pass
    elif enum == 'three':
        pass
```

The implementation here is currently limited to matching code that is similar to
the example above where one of the args to `match_enum` is the enum tag and the
rest of the function body is the `if-else` check.
