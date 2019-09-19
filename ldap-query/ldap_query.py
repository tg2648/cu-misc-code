"""
Available LDAP attributes:

departmentNumber - code of the department, e.g. 400200X
campusphone - campus phone "shortcut", the last 5 digits
sn - last name
ou - full department name
mail - email
givenName - first name
uid - uni
uni - uni
postalAddress - mailing address
cn - full name
telephone number - telephone number
title - title

Add ';x-role-<#>' to the attribute for second/third/etc LDAP entry, for people
with multiple appointments

ENVIRONMENT VARIABLES:
    LDAP_SERVER
    LDAP_BASE
"""

# Standard library imports
import os
import sys
from pathlib import Path

# Third party imports
from dotenv import load_dotenv
import ldap

# Local application imports
sys.path.append(str(Path(__file__).parent.parent.resolve())) # Add parent directory to sys.path to import utils.py
from utils import progress_bar


# Base directory of the script file
basedir = Path(__file__).parent.resolve()

# Load environment variables
env_path = basedir / '.env'
load_dotenv(dotenv_path=env_path)

# initialize connection
con = ldap.initialize(os.getenv('LDAP_SERVER'))
con.simple_bind_s()

# setup information for the query
# base dn:
ldap_base = os.getenv('LDAP_BASE')
# attributes that we are interested in:
attrlist = [
    'sn',
    'givenName',
    'title',
    'ou',
    'sn;x-role-2',
    'givenName;x-role-2',
    'title;x-role-2',
    'ou;x-role-2',
    'sn;x-role-3',
    'givenName;x-role-3',
    'title;x-role-3',
    'ou;x-role-3'
]

query = "(uni=rr222)"

# returns a list of tuples
# each tuple is of the form (dn, attrs)
# since we're querying a single item, get the first and only tuple right away
# since we are interested in attributes, get the second item of the tuple right away
result_attrs = con.search_s(ldap_base, ldap.SCOPE_SUBTREE, query, attrlist)[0][1]

# the keys of attrs are strings, and the associated values are lists of strings
# the strings are byte strings, need to decode first
# s = 'name: {str(givenName[0])} lastname: {str(sn[0])}'.format(**result_attrs)
print(result_attrs['givenName'][0].decode("utf-8"))

# unbind and close connection
con.unbind_s()
