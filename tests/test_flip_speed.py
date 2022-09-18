import numpy as np
import sys, time



def flip1(l: list, width: int = 32, height: int = 24) -> list:
    frame = np.array(l)
    frame = frame.reshape((height, width))
    frame = np.flip(frame, 1)
    frame = frame.reshape(-1)

    return frame


def flip2(l: list, width: int = 32, height: int = 24) -> list:
    start = 0
    end = width
    for i in range(height):
        l[start:end] = l[start:end][::-1]
        start += width
        end += width

    return l

def test(width: int = 32, height: int = 24, tests: int = 1000, pr_flag: bool = False):
    # execute both functions 1000 times, print average time
    times = []
    l_final = []
    for i in range(tests):
        l = [i for i in range(width * height)]
        start = time.monotonic()
        l_final = flip1(l, width=width, height=height)
        times.append(time.monotonic() - start)

    # print first row
    if pr_flag:
        print(l_final[:width])
    print(f'flip1, james\' versionß: {np.mean(times)}')
    times = []
    for i in range(tests):
        l = [i for i in range(width * height)]
        start = time.monotonic()
        l_final = flip2(l, width=width, height=height)
        times.append(time.monotonic() - start)
        # print first row
    if pr_flag:
        print(l_final[:width])
    print(f'flip2, Alex\'s version: {np.mean(times)}')

if __name__ == '__main__':
    # take values from command line: width, height, tests
    if len(sys.argv) >= 4:
        width = int(sys.argv[1])
        height = int(sys.argv[2])
        tests = int(sys.argv[3])
        if len(sys.argv) == 5:
            # 0 is false, 1 is true
            pr_flag = bool(int(sys.argv[4]))
    else:
        width = 32
        height = 24
        tests = 1000
        pr_flag = False

    print(f'Executing tests with width: {width}, height: {height}, tests: {tests}')
    test(width=width, height=height, tests=tests, pr_flag=pr_flag)