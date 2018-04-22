# from __future__ import absolute_import
# from __future__ import division
# from __future__ import unicode_literals
# from __future__ import print_function


import re


def main():
    pattern = re.compile(r'Errors:(.*?)\s1')
    pattern2 = re.compile(r'Test\s10')
    pattern3 = re.compile(r'Errors:(.*)\s{4}1')
    pattern4 = re.compile(r'Pass(.*?)100%')
    print("Searching")
    with open("SerialBusLog.csv", 'r') as _f:
        for _line in _f:

            _match = pattern3.search(_line)
            # print(_match)
            if _match is not None:
                print(_match.group())
                print()
                # print("Found!")
                # break


if __name__ == "__main__":
    main()
