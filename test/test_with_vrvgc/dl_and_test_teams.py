'''
`cd` into this file's directory!
'''

import os

def h1(s: str):
    print()
    print()
    print(f' {s.strip()} '.center(120, '-'))
    print()

# this_dir = os.path.dirname(__file__)

h1('running download scripts (based on tourneys.txt)')

os.system('download_team_urls.py')
os.system('download_teams.py')


h1('testing')

os.system('test_teams.py')