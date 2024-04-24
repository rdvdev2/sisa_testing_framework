from enum import Enum, auto


class AssertionType(Enum):
    MEMORY = auto()


class Assertion(object):

    def __init__(self, a_type, dir, val):    
        self.a_type = a_type
        self.dir = dir
        self.val = val


    def from_line(line: str):
        assertions = []
        if line.startswith('Mem'):
            if line[6] == ':':
                address1 = int(line[4:6], 16)
                value1 = line[13:15].upper()
                assertions.append(Assertion(AssertionType.MEMORY, address1, value1))

                address2 = int(line[7:9], 16)
                value2 = line[15:17].upper()
                assertions.append(Assertion(AssertionType.MEMORY, address2, value2))
            else:
                address = int(line[4:6], 16)
                vale = line[10:12]

        return assertions


    def passes(self, dumps):
        match self.a_type:
            case AssertionType.MEMORY:
                dir = self.dir ^ 1
                got = dumps['memory'][int(dir / 2)][dir % 2 * 2:dir % 2 * 2 + 2]
                return got == self.val

        return False


    def describe_failure(self, dumps):
        match self.a_type:
            case AssertionType.MEMORY:
                dir = self.dir ^ 1
                got = dumps['memory'][int(dir / 2)][dir % 2 * 2:dir % 2 * 2 + 2]
                return f"Failed MEMORY assertion at {hex(self.dir)}. Expected {self.val}, got {got}."
