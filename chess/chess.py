from bs4 import BeautifulSoup
from duckduckgo_search import DDGS
# from googlesearch import search
import os
from progressbar import progressbar
# from progress.bar import Bar
import requests
import shutil

up = "---\n\n---\n"

r = requests.get("https://www.thechesswebsite.com/chess-openings/")
# r = requests.get("https://www.tiobe.com/tiobe-index/")

ddgs = DDGS()

soup = BeautifulSoup(r.text, 'html.parser')

container = soup.find_all(id="cb-container")[1]

list = container.find_all('a')[0:20]

if not os.path.isfile('index.md'):
    chat = ddgs.chat('"Value of Openings in Chess"')
    with open('index.md', 'w+') as main_file:
        main_file.write(up)
        main_file.write("# Value of Openings\n\n")
        main_file.write(chat)
        main_file.write("\n\n[opening list](opening_list)")

if not os.path.isfile('opening_list.md'):
    with open('opening_list.md', 'w+') as list_file:
        list_file.write(up)
        list_file.write("# List of Openings:\n\n")
        for gambit in progressbar(list):
            name = gambit.find("h5").text
            code = name.replace(' ', '-')
            
            # break

            search = ddgs.text(f'"{name}"',max_results=1)
            list_file.write(f"[{code}]: {gambit.find("img")["src"]} \n#### [{name}](openings/{name.replace(' ', '_')}):\n\n![{name}][{code}] \n\n")
            list_file.write(f"{search[0]['body']}\n\n\n")

else:
    skip = 0
    with open('new_list.md', 'w+') as new, open('opening_list.md') as old:
        for line in old:
            try:
                if line[1] == '#':
                    skip += 1
            except:
                ()
            new.write(line)
        for gambit in progressbar(list[skip:-1]):
            name = gambit.find("h5").text
            code = name.replace(' ', '-')
            # break
            try:
                search = ddgs.text(f'"{name}"',max_results=1)
            except Exception as e:
                shutil.move('new_list.md', 'opening_list.md')
                raise e
            
            new.write(f"[{code}]: {gambit.find("img")["src"]} \n#### [{name}](openings/{name.replace(' ', '_')}):\n\n![{name}][{code}] \n\n")
            new.write(f"{search[0]['body']}\n\n\n")

    shutil.move('new_list.md', 'opening_list.md')
                

for gambit in progressbar(list):
    name = gambit.find("h5").text
    if not os.path.isfile(f"openings/{name.replace(' ', '_')}.md"):
        chat = ddgs.chat(f'Tell me about chess opening "{name}"')
        with open(f"openings/{name.replace(' ', '_')}.md", "w+") as gambit_file:
            gambit_file.write(up)
            gambit_file.write(f"# {name}\n\n")
            gambit_file.write(chat)
# print(f"Amount of fails: {fails}.")




# result = ddgs.text(f'"{list[0]}"', max_results=1)
# print(result[0]["body"])