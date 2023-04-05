
import pokepastes_scraper as pastes
import os, jsonpickle

team = pastes.team_from_url('https://pokepast.es/5c46f9ec443664cb')
this_dir = os.path.dirname(__file__)
with open(f'{this_dir}/pickletest_team.json', 'w') as f:
    f.write(jsonpickle.encode(team))