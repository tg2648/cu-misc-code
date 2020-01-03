"""
Utility to query LDAP

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
    OUTPUT_FILE
"""

# Standard library imports
import os
import sys
import csv
import json
from pathlib import Path

# Third party imports
from dotenv import load_dotenv
from ldap3 import Server, Connection, SUBTREE

# Local application imports
sys.path.append(str(Path(__file__).parent.parent.resolve()))  # Add parent directory to sys.path to import utils.py
# from utils import progress_bar


class LDAPConnection(object):
    """Summary line.

    Longer class description...

    Class Attributes:
        attrlist (tuple -> str): LDAP attributes of interest

    Instance Attributes:
        server_url (str): LDAP server URL
        ldap_base (str): LDAP base dn
        keys (list -> str): List of keys that will be searched
        search_results (dict -> dict): JSON-like dictionary with key-value pairs as `'key': {'attr': 'attr_value'}`
    """

    attrlist = (
        'uid',
        'sn',
        'givenName',
        'title',
        'ou',
        'title;x-role-2',
        'ou;x-role-2',
        'title;x-role-3',
        'ou;x-role-3',
        'mail'
    )

    def __init__(self, server_url, ldap_base):
        self.server_url = server_url
        self._server = Server(self.server_url)
        self._conn = Connection(self._server)
        self.ldap_base = ldap_base
        self.keys = []
        self.search_results = {}

    def search(self, keys, key_type):
        """Performs an LDAP search

        Populates a JSON-like dictionary. If attribute is not present, writes 'n/a'.

        {
            'key1': {
                'attr1': attr1_value,
                'attr2': attr2_value,
            },
            'key2': {
                'attr1': attr1_value,
                'attr2': attr2_value,
            },
        }

        Args:
            keys (list): Keys to search, may contain duplicates.
            key_type (str): What the key represents (uni, email, etc.)
        """
        self.keys = keys  # Save keys for writing out operations

        with self._conn as c:
            for key in set(keys):  # Operate on a set to remove duplicates
                c.search(self.ldap_base, f"({key_type}={key})", search_scope=SUBTREE, attributes=self.attrlist)
                if c.response:  # Non-matches return empty lists
                    response = c.response[0]['attributes']  # Response is a list of dictionaries
                    self.search_results[key] = {}
                    for attr in self.attrlist:
                        if response[attr]:  # Each attribute is a list of strings
                            self.search_results[key][attr] = response[attr][0]
                        else:
                            self.search_results[key][attr] = 'n/a'
                else:
                    for attr in self.attrlist:
                        self.search_results[key][attr] = 'n/a'

    def to_csv(self, path):
        """
        Writes search results to a csv file. Preserves duplicates if `keys` contained duplicate values.
        Each row is a key from `keys`, each column is an attribute value.

        Requires an environment variable `LDAP_OUTPUT` with a valid path.
        """
        with open(path, 'w', newline='') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=self.attrlist)
            writer.writeheader()
            for key in self.keys:
                writer.writerow(self.search_results[key])

    def to_json(self, path):
        """
        Writes search results as JSON. Requires an environment variable `LDAP_OUTPUT` with a valid path.
        """
        with open(path, 'w') as jsonfile:
            jsonfile.write(json.dumps(self.search_results))

    def to_print(self):
        """
        Prints in a friendly format
        """
        str_out = []
        for key in self.keys:
            str_out.append(f'{key}:')
            for attr in self.attrlist:
                str_out.append(f'\t{attr}: {self.search_results[key][attr]}')
            str_out.append('')

        print('\n'.join(str_out))


if __name__ == "__main__":

    BASEDIR = Path(__file__).parent.resolve()
    env_path = BASEDIR / '.env'
    load_dotenv(dotenv_path=env_path)

    with open(os.getenv('LDAP_INPUT'), 'r') as f_in:
        keys = [line.rstrip() for line in f_in]

    ldap = LDAPConnection(server_url=os.getenv('LDAP_SERVER'), ldap_base=os.getenv('LDAP_BASE'))
    ldap.search(keys=keys, key_type='uni')
    ldap.to_csv(os.getenv('LDAP_OUTPUT'))
