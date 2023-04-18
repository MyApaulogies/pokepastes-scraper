
import pokepastes_scraper as pastes
import os

team = pastes.team_from_url('https://pokepast.es/5c46f9ec443664cb')
this_dir = os.path.dirname(__file__)
with open(f'{this_dir}/example_team.json', 'w') as f:
    f.write(team.to_json())

for mon in team.members:
    print(f'{mon.species} with {mon.item or "no item"} (Tera: {mon.tera_type})')
    for move in mon.moveset:
        print('-', move)