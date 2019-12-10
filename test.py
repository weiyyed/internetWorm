import collections

import re


def fun():
    for i in range(5):
        yield{
            x:i,
            y:i+1
        }
if __name__=="__main__":
    x=re.search("#([A-Z_]{0-10}).*","hse_injob_deal#HSE_WORKTASK_INJOB_MgetDutyShiftingDict:['交接班']")
    print(x)