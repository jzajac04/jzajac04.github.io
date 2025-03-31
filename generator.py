import sys
from bs4 import BeautifulSoup
from duckduckgo_search import DDGS
import os
from progressbar import progressbar
import requests
import shutil
import time
import yaml

JEKYLL_HEADER = "---\n"
LIST_HEADER = JEKYLL_HEADER + "layout: list\n"

def index_generator(config):
    if not os.path.isfile(f'{config["path"]}/index.md'):
        with open('example/index copy.md') as example_file:
            chat = DDGS().chat(f'Write about {config["topic"]} and then reformat it to look something like this(DONT ADD ANYTHING ABOVE and change Opening List to {config["list_name"]}):{example_file.read()}')
            with open(f'{config["path"]}/index.md', 'w+') as index_file:
                index_file.write(chat)

def gambit_generator(config, item_list):
    ddgs = DDGS()
    for item in progressbar(item_list):
        name = item.find('h5').text
        path = name.replace(' ', '_')
        
        if not os.path.isfile(f"{config["path"]}/list/{path}.md"):
            time.sleep(3)
            # continue
            chat = ddgs.chat(f'Tell me about chess opening "{name}"')
            with open(f"{config["path"]}/list/{path}.md", "w+") as item_file:
                item_file.write(f"""---
layout: default
title: { name }
nav:
    -   path: /
        text: Home
    -   path: /{ config["path"] }
        text: { config["name"] }
    -   path: /{config["path"]}/list
        text: {config["list_name"]}
---
{chat}
""")

def list_generator(config, item_list):
    skip = 0
    with open(f'{config["path"]}/new_list.md', 'w+') as new_list_file:
        if not os.path.isfile(f'{ config["path"] }/list.md'):
            new_list_file.write(f"""---
layout: list
title: { config["list_name"] }
nav:
    -   path: /
        text: Home
    -   path: /{ config["path"] }
        text: { config["name"] }
list:
""")
        else:
            with open(f'{config["path"]}/list.md') as old_list_file:
                lines = old_list_file.readlines()
                skip = -2
                for line in lines[:-1]:
                    try:
                        if line[4] == '-':
                            skip += 1
                    except:
                        pass
                    new_list_file.write(line)
        for item in progressbar(item_list[skip:]):
            # if skip > 0:
            #     skip -= 1
            #     continue
            name = item.find(config["item"]).text
            path = name.replace(' ', '_')
            try:
                search = DDGS().chat(f"Tell me only about {config["name"]} {name} (max 400 characters long without \" or :)")
            except Exception as e:
                new_list_file.write('---')
                shutil.move(f'{config["path"]}/new_list.md', f'{config["path"]}/list.md')
                raise e
            time.sleep(5)
            new_list_file.write(f"""    -   img: {item.find('img')['src']}
        title: {name}
        text: {search}
        path: {path}
""")
        new_list_file.write('---')
        shutil.move(f'{config["path"]}/new_list.md', f'{config["path"]}/list.md')


def simple_fix(config, item_list):
    for item in progressbar(item_list):
        name = item.find('h5').text
        path = name.replace(' ', '_')
        if not os.path.isfile(f"{config["path"]}/list/{path}.md"):
            with open(f"{config["path"]}/list/{path}.md", "w+") as new_item_file:
                new_item_file.write(f"""---
layout: default
title: { name }
nav:
    -   path: /
        text: Home
    -   path: /{ config["path"] }
        text: { config["name"] }
    -   path: /{config["path"]}/list
        text: {config["list_name"]}
---
# """)            
#                 skip = 4
#                 for line in old_item_file:
#                     if skip > 0:
#                         skip-=1
#                         continue
#                     new_item_file.write(line)
        # time.sleep(1)
        # shutil.move(f"{config["path"]}/list/{path}_new.md", f"{config["path"]}/list/{path}.md")

def main():
    args = sys.argv[1:]
    for option in args:
        with open(f'{option}/config.yaml') as config_file:
            config = yaml.safe_load(config_file)
            r = requests.get(config["link"])
            soup = BeautifulSoup(r.text, 'html.parser')
            item_list = soup.find_all(id=config["list_cont_id"])[config["list_cont_nr"]].find_all(config["list"])
            # break
            # index_generator(config)
            # gambit_generator(config, item_list)
            # list_generator(config, item_list)
            simple_fix(config, item_list)

if __name__ == '__main__':
    main()
