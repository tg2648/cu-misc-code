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
    INPUT_FILE
"""

# Standard library imports
import os
import sys
from pathlib import Path

# Third party imports
from dotenv import load_dotenv
from ldap3 import Server, Connection, SUBTREE


# Base directory of the script file
basedir = Path(__file__).parent.resolve()

# Load environment variables
env_path = basedir / '.env'
load_dotenv(dotenv_path=env_path)

# LDAP attributes we are interested in
attrlist = [
    'sn',
    'givenName',
    'title',
    'ou',
    'title;x-role-2',
    'ou;x-role-2',
    'title;x-role-3',
    'ou;x-role-3'
]

server = Server(os.getenv('LDAP_SERVER'))
conn = Connection(server)
conn.bind()
ldap_base = os.getenv('LDAP_BASE')

# Load unis to be queried, stripping trailing characters (such as newlines)
with open(os.getenv('INPUT_FILE'), 'r') as f_in:
    unis = [line.rstrip() for line in f_in]

# Assemble a list of headers by inserting uni to the attribute list and joining with separators
headers = ['UNI'] + attrlist
headers = ','.join(headers)
headers = headers + '\n'

with open(os.getenv('OUTPUT_FILE'), 'w') as f_out:
    # first write the headers
    f_out.writelines(headers)

    # then loop through unis in the input file
    for uni in unis:
        # start the output with a uni (first column)
        output = [uni]
        # query LDAP
        conn.search(ldap_base, f"(uid={uni})", search_scope=SUBTREE, attributes=attrlist)
        
        # non-matches return empty lists
        if len(conn.response) > 0:
            # since there should only be one match on uni, get the first response and then its attributes as a dict
            query_result = conn.response[0]['attributes']
            # loop through the result dictionary, get the attributes of interest, and join with separators before writing
            # enclosed in quotes to escape potential commas in titles, etc.
            # the value of each attribute is a list, need to select the underlying fist element
            for i in range(len(attrlist)):
                selected_attr = query_result[attrlist[i]]
                if len(selected_attr) > 0:
                    output.append(f"\"{selected_attr[0]}\"")
                else:
                    output.append('"n/a"')

            # append newline after all attributes were parsed and write to file
            output.append('\n')
        else:
            # if non-match, then fill with n/a's
            for i in attrlist:
                output.append("n/a") 

        f_out.writelines(','.join(output))

# Close the LDAP connection
conn.unbind()