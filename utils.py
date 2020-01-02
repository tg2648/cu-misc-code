"""
Utility functions
"""

# Standard library imports
import sys


def progress_bar(n, n_max):
    sys.stdout.write('\r')
    j = (n + 1) / n_max
    sys.stdout.write("[%-20s] %d%%" % ('='*int(j*20), j*100))
    sys.stdout.flush()