import multiprocessing
import sys

from . import run_client

if __name__ == "__main__":
    multiprocessing.freeze_support()
    run_client(*sys.argv[1:])
