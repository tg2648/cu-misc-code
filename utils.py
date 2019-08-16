"""
Utility functions
"""

# === IMPORTS ===

# Standard library imports
import sys

# === FUNCTION DEFINITIONS ===

def progress_bar(n, n_max):
    sys.stdout.write('\r')
    j = (n + 1) / n_max
    sys.stdout.write("[%-20s] %d%%" % ('='*int(j*20), j*100))
    sys.stdout.flush()