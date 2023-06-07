'''
basic idea:
- pastes = downloaded 1.8k Pokepastes
- modeled = pastes
    |> run team_from_html on each of them
    |> somehow convert to text file that exactly matches format of original pokepast.es page, minus images
- actual = pastes |> extract raw text from each page
- make sure modeled and actual are exactly the same

the differences in the actual vs expected should show flaws in scraping system


TODO:

- make test.py update team_urls.txt instead of just creating another
- make master script that runs all these scripts
- git commit lol

'''


import os
from bs4 import BeautifulSoup
from pokepastes_scraper import PokepastesMon, PokepastesTeam, team_from_html


# excluding attrs in the nickname/name/gender/item line
ordered_attrs = (
    ('ability', 'Ability'),
    ('level', 'Level'),
    ('shiny', 'Shiny'),
    ('happiness', 'Happiness'),
    ('pokeball', 'Pokeball'),
    # ('dynamax_level', 'Dynamax Level'), # idk
    # ('gigantamax', 'Gigantamax'), # idk
    ('tera_type', 'Tera Type'),
    ('evs', 'EVs'),
    ('nature', 'Nature'),
    ('ivs', 'IVs'),
)

ordered_stats = (
    'HP',
    'Atk',
    'Def',
    'SpA',
    'SpD',
    'Spe',
)


# includes newline at the end
def create_name_line(mon: PokepastesMon):
    res = mon.species if not mon.nickname else f'{mon.nickname} ({mon.species})'

    if mon.gender:
        res += f' ({mon.gender})'
    if mon.item:
        res += f' @ {mon.item}'

    return res + '\n'


def create_ivs_line(mon: PokepastesMon):
    stat_words = []
    for stat in ordered_stats:
        val = getattr(mon.ivs, stat)
        if val != None and val != 255:
            stat_words.append(f'{val} {stat}')
    
    if len(stat_words) == 0:
        return ''
    return 'IVs: ' + ' / '.join(stat_words) + '\n'


def create_evs_line(mon: PokepastesMon):
    stat_words = []
    for stat in ordered_stats:
        val = getattr(mon.evs, stat)
        if val:
            stat_words.append(f'{val} {stat}')

    if len(stat_words) == 0:
        return ''
    return 'EVs: ' + ' / '.join(stat_words) + '\n'


def create_move_list(mon: PokepastesMon, squish_dashes: bool):
    if squish_dashes:
        return '\n'.join(f'-{move}' for move in mon.moveset)
    else:
        return '\n'.join(f'- {move}' for move in mon.moveset)


def mon_to_text(mon: PokepastesMon, squish_dashes: bool):
    res = create_name_line(mon)
    for attr, attr_name in ordered_attrs:
        a = getattr(mon, attr)
        if not a:
            continue
        
        if attr == 'evs':
            res += create_evs_line(mon)
            continue
        if attr == 'nature':
            res += f'{a.capitalize()} Nature\n'
            continue
        if attr == 'ivs':
            res += create_ivs_line(mon)
            continue
        if attr == 'shiny':
            if mon.shiny:
                res += 'Shiny: Yes\n'
            continue

        res += f'{attr_name}: {a}\n'
    
    res += create_move_list(mon, squish_dashes)
    
    return res



def team_to_text(team: PokepastesTeam, squish_dashes=False):
    return '\n'.join(mon_to_text(mon, squish_dashes) for mon in team.members)


def html_to_text(raw_html: str):
    soup = BeautifulSoup(raw_html, 'html.parser')
    lines = [line.strip() for line in soup.text.splitlines() if line.strip()]

    # i == the last line that contains a move (i.e. starts with a '-')
    i = 0
    for line in reversed(lines):
        if line.startswith('-'):
            squish_dashes = not line.startswith('- ')
            break
        i += 1

    # ignore first line, and ignore everything after last attack
    return '\n'.join(lines[1:-i]), squish_dashes

def test_team(raw_html: str) -> bool:

    actual, squish_dashes = html_to_text(raw_html)


    team = team_from_html(raw_html)
    expected = team_to_text(team, squish_dashes)

    return actual == expected




if __name__ == "__main__":
    this_dir = os.path.dirname(__file__)

    no = yes = ctr = 0
    for filename in os.scandir(f'{this_dir}{os.sep}team_pages'):
        with open(filename, encoding='utf-8') as f:
            ctr += 1
            if not test_team(f.read()):
                print('fail:', filename)
                no += 1
            else:
                yes += 1
    
    print()
    print(f'out of {ctr} tests:')
    print(f'- {yes} passed')
    print(f'- {no} failed')