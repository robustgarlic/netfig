import pandas as pd 
from jinja2 import *
from colorama import init
from colorama import Fore
import os
import sys
from datetime import datetime

#start time for script
start_time = datetime.now()


#resets colorama colors#
init(autoreset=True)


print(Fore.WHITE + '\n' + '-' * 60)
print(Fore.CYAN +  '\n            Network Configlet Generator')
print(Fore.WHITE + '\n' + '-' * 60)
print(Fore.RED + '\nUsage Example:' + Fore.CYAN + 'netfig.py variables.csv jinjatemplate.j2')

## Define Usage ##
if len(sys.argv) < 3:
    print(Fore.WHITE + '\n' + '*' * 60)
    print('\n')
    print(Fore.RED + 'Try Again. Working Usage Example:' + Fore.CYAN +  'netfig.py variables.csv jinjatemplate.j2')   ##this Script #commands in a list #device type and login type
    print('\n')
    print(Fore.WHITE + '*' * 60)
    print('\n')
    exit()

print('Starting script.....')
## system arguments ##

## define csv variables ##
csv_var = sys.argv[1]

## define jinja template to use ## 
template_var = sys.argv[2]


## reads full csv ##
df = pd.read_csv(csv_var)
data = data.fillna('')
data_list = data.to_dict('records')


## Jinja environment and defining template from sys argument ##
env = Environment(loader=FileSystemLoader(searchpath="."))
template = env.get_template(template_var)


## loop to replace variables based on jinja template and renders accordingly ##
for keys in data_list:
    config = template.render(keys)
    fname = list(keys.values())[0]
    with open(fname + '.txt', 'w') as outputfile:
            outputfile.write(config)


print(Fore.WHITE + "\nTotal Elapsed time: " + str(datetime.now() - start_time))