

import os, sys
from test_teams import html_to_text

filename = sys.argv[1]

this_dir = os.path.dirname(__file__)
with open(f'{this_dir}{os.sep}team_pages{os.sep}{filename}', encoding='utf-8') as f:
    text, _ = html_to_text(f.read())
    print(text)
    print()