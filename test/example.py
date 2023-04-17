# requires: pip install jsonpickle

import pokepastes_scraper as pastes
import os

team = pastes.team_from_url('https://pokepast.es/5c46f9ec443664cb')
thisdir = os.path.dirname(__file__)
with open(f'{thisdir}/example_team.json', 'w') as f:
    f.write(team.to_json())

for mon in team.members:
    print(f'{mon.species} with {mon.item or "no item"}')