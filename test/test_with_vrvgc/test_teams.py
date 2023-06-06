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



