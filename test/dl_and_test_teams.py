'''
`cd` into this file's directory!
'''

import os

def h1(s: str):
    print()
    print()
    print(f' {s.strip()} '.center(120, '-'))
    print()

this_dir = os.path.dirname(__file__)

h1(f'running download scripts (based on tourneys.txt)')

os.system(f'{this_dir}{os.sep}download_team_urls.py')
os.system(f'{this_dir}{os.sep}download_teams.py')


h1('testing')

os.system(f'{this_dir}{os.sep}test_teams.py')