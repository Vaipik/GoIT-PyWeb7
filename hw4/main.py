from threading import Thread
import sys

from sorter import sorter


if __name__ == '__main__':
    sorter(sys.argv[1:])
