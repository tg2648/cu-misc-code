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


from ldap3 import Server, Connection, SUBTREE, AUTO_BIND_NONE
server = Server(os.getenv('LDAP_SERVER'))

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

ldap_base = os.getenv('LDAP_BASE')

conn = Connection(server)
conn.bind()
conn.search(ldap_base, '(uni=tg2648)', search_scope=SUBTREE, attributes=attrlist)
conn.unbind()
print(conn.response)