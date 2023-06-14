

import os, sys
from test_teams import html_to_text, team_to_text, team_from_html

# filename = sys.argv[1]
filename = '0d7c5ddc58ce9eb3.html'

this_dir = os.path.dirname(__file__)
with open(f'{this_dir}{os.sep}team_pages{os.sep}{filename}', encoding='utf-8') as f:
    html = f.read()
    team = team_from_html(html)
    print(team_to_text(team))

    # print()
    # print(team.members[2].gender)
    print()