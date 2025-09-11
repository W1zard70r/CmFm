import os

import requests
# import sys, os
#
# # setting path
# sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
#
# # importing
# from Chords_site.models import Song
from ..models import Song

import pkgutil
sp = ['..']
moduls = pkgutil.iter_modules(sp)
print(*moduls, sep = '\n')







async def Get_Song_Info(song_link: str) -> Song:
    response = requests.get(song_link)
    print(response)

Get_Song_Info("https://amdm.ru/akkordi/bond_s_knopkoy/189069/ten/")