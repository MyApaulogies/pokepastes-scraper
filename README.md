
# pokepastes-scraper

A simple library that converts a Pokemon team from https://pokepast.es to an object in Python.

### Usage 

Let's say we want to use [Gavin Michael's team](https://pokepast.es/5c46f9ec443664cb), which he used to win the [Oceania world championships](https://victoryroadvgc.com/2023-ocic/). Simply call `team_from_url`:

```python
import pokepastes_scraper as pastes

team = pastes.team_from_url("https://pokepast.es/5c46f9ec443664cb")

for mon in team.members:
    print(f"{mon.species} with {mon.item}")
```

Output: 

```
Iron Hands with Assault Vest
Amoonguss with Sitrus Berry
Pelipper with Focus Sash
Palafin with Mystic Water
Baxcalibur with Dragon Fang
Dragonite with Lum Berry
```

For a detailed example output of `team_from_url`, see `test/example.py` and `test/example_team.json`.

### Installation
`pip install -U pokepastes-scraper`



Tested in python 3.11, but likely compatible with 3.7+.