"""
High Level Execution.

Jaime Jacob
"""
import find_keywords2
import pandas as pd
import csv
import os
import thefuzz
from thefuzz import fuzz
from thefuzz import process
import re
import pdbp

# Execuiting find keywords function
path_of_directory = '/Users/jaimejacob/Documents/urop/condense_lines_proj/end_result'
lst = os.listdir(path_of_directory) # your directory path
for files in os.listdir(path_of_directory):
        if files.endswith('.csv'):
            name = '/Users/jaimejacob/Documents/urop/condense_lines_proj/end_result/' + str(files)
            # find_keywords2.find_keywords(name)
# find_keywords2.find_no_stock('/Users/jaimejacob/Documents/urop/condense_lines_proj/find_keywords2/split_by_species.csv')
#find_info_stock('/Users/jaimejacob/Documents/urop/condense_lines_proj/find_keywords2/current/stocking.csv')


#Stocking headers - 'LAKE NAME',CONTENTS',DATE',FUZZY MATCH',NO,Stage,Num,Species,"Trout, trout","Perch, perch","Rock Bass, rock bass","Walleye, walleye","Smallmouth Bass, smallmouth bass","Pike, pike","Suckers, suckers","Largemouth Bass, largemouth bass","Bluegill, bluegill","Bass, bass","Green Sunfish, green sunfish","Bullheads, bullheads","Pumpkinseed Sunfish, pumpkinseed sunfish","Rainbows, rainbows","Brook trout, brook trout","Pike, pike.1","Panfish, panfish","Grayling, grayling","Trash, trash","Black Spotted Trout, black spotted trout","Montana grayling, montana grayling","Chubs, chubs","Browns, browns","Hybrid Sunfish, hybrid sunfish","Sea Lamprey, sea lamprey","Splake, splake","Salmonid, salmonid","Common Shiners, common shiners","Tiger Muskies, tiger muskies","Whitefish, whitefish","Ichthyomyzon, ichthyomyzon","Brown trout, brown trout","Menominees, menominees","Sturgeon, sturgeon"
habitat_header = "LAKE NAME,CONTENTS,DATE,FUZZY MATCH,Install,Phosphate,Fertilizer,Transplant vegetation,Hollow Square Shelters,Bushel piles of gravel,Brush Shelters,Clear brush,Rock & gravel filter dam,Self - cleaning screen,Filter dam,Gravel,Filling,Transfer forage species to basin,Long crib,Low-head dams,Shelters,dam,Marsh,Establish,Artificial,Shelters,Brush,Rock,Screen,Basin,Crib"

#find_info('/Users/jaimejacob/Documents/urop/condense_lines_proj/find_keywords2/current/habitat.csv', habitat_header)


reg_header = "LAKE NAME,CONTENTS,DATE,FUZZY MATCH,Remove size restriction,Acquire public fishing site,Prohibit use of live minnows for bait,Commercial fisherman to trap net,Discontinue commercial trap netting,Remove size limit,Open to fishing,Acquire land for public access,Opened,Remove all restrictions,Commercial minnow seining,Restriction,Site,Bait,Fishermen,Netting,Limit,Seining,Access,Fishing"
#find_info('/Users/jaimejacob/Documents/urop/condense_lines_proj/find_keywords2/current/regulation.csv', reg_header)

eradication_header = "LAKE NAME,CONTENTS,DATE,FUZZY MATCH,Chemically reclaim,Rotenone,Kill,Chemical Renovation,Poisoned,Toxaphene,Repoisioning,Fish-Tox,Lethal,Manually remove,Removed,Antimycin,Chemical reclamation,Eradicate,Manually thin,Toxicant,Remove,Derris,Manual removal,Poison,Chemical,Chemically reclaim,Thin"
#find_info('/Users/jaimejacob/Documents/urop/condense_lines_proj/find_keywords2/current/eradication.csv', eradication_header)

#seperate_years('/Users/jaimejacob/Documents/urop/condense_lines_proj/find_keywords2/current/stocking.csv')
#find_keywords2.find_info_stock('/Users/jaimejacob/Documents/urop/condense_lines_proj/find_keywords2/split_by_species.csv')

#find_keywords2.split_by_species('/Users/jaimejacob/Documents/urop/condense_lines_proj/find_keywords2/split_by_species.csv')
#find_keywords2.summarize('/Users/jaimejacob/Documents/urop/condense_lines_proj/find_keywords2/split_by_species.csv')

find_keywords2.format_years('/Users/jaimejacob/Documents/urop/condense_lines_proj/find_keywords2/current/eradication.csv', '/Users/jaimejacob/Documents/urop/condense_lines_proj/find_keywords2/formatted_years/formatted_years_eradication.csv')
find_keywords2.format_years('/Users/jaimejacob/Documents/urop/condense_lines_proj/find_keywords2/current/habitat.csv', '/Users/jaimejacob/Documents/urop/condense_lines_proj/find_keywords2/formatted_years/formatted_years_habitat.csv')
find_keywords2.format_years('/Users/jaimejacob/Documents/urop/condense_lines_proj/find_keywords2/current/regulation.csv', '/Users/jaimejacob/Documents/urop/condense_lines_proj/find_keywords2/formatted_years/formatted_years_regulation.csv')