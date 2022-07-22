import sys
sys.path.append('../')
from module import make_data


def setup_data(filename: str, skip_row:int):
    make_data(filename, skip_row)


if __name__ == '__main__':
    filename = sys.argv[1]
    skip_row = int(sys.argv[2]) if len(sys.argv) > 2 else 0
    make_data(filename, skip_row)