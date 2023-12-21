from enum import Enum


# specify the plan type for FSA
class FSAPlanType(Enum):
    DID_NOT_ELECT = 0
    FSA = 1
    LPF = 2
