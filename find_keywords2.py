import pandas as pd
import csv
import os
import thefuzz
from thefuzz import fuzz
from thefuzz import process
import re
import pdbp




def find_keywords(fileName):
    
    fileName = str(fileName)


    df = pd.read_csv(fileName)
    regulation_keys = pd.read_csv('/Users/jaimejacob/Documents/urop/condense_lines_proj/keyword_csvs/keys_regulation.csv')
    regulation_keys = regulation_keys['Words'].tolist()

    eradication_keys = pd.read_csv('/Users/jaimejacob/Documents/urop/condense_lines_proj/keyword_csvs/keys_eradication.csv')
    eradication_keys = eradication_keys['Words'].tolist()

    habitat_keys = pd.read_csv('/Users/jaimejacob/Documents/urop/condense_lines_proj/keyword_csvs/keys_habitat.csv')
    habitat_keys = habitat_keys['Words'].tolist()

    stocking_keys = pd.read_csv('/Users/jaimejacob/Documents/urop/condense_lines_proj/keyword_csvs/keys_stocking.csv')
    stocking_keys = stocking_keys['Words'].tolist()

    #private_keys = ['private']

    eradication =   pd.read_csv('/Users/jaimejacob/Documents/urop/condense_lines_proj/find_keywords2/current/eradication.csv')
    habitat =       pd.read_csv('/Users/jaimejacob/Documents/urop/condense_lines_proj/find_keywords2/current/habitat.csv')
    regulation =    pd.read_csv('/Users/jaimejacob/Documents/urop/condense_lines_proj/find_keywords2/current/regulation.csv')
    stocking =      pd.read_csv('/Users/jaimejacob/Documents/urop/condense_lines_proj/find_keywords2/current/stocking.csv')
    ratios =        pd.read_csv('/Users/jaimejacob/Documents/urop/condense_lines_proj/find_keywords2/ratio_csvs/ratio_100.csv')

    lakeName = fileName.split("/")
    lakeName = str(lakeName[len(lakeName) - 1])

    for index, row in df.iterrows():
        strForRow = str(row[3])
        contents = strForRow.split()
        date = str(row[5])
        in_rec = False
        in_csv = False
        in_csv_eradication = False
        in_csv_regulation  = False
        in_csv_stocking    = False
        in_csv_habitat     = False

        category = ""
        max = 0
        max_word = ""
        new_row = [lakeName, strForRow, date, 0]
        if len(contents) == 1 and contents[0] == 'nan':
            continue

        for i in range(len(eradication_keys) * 2):
            phrase = ''

            if i >= len(eradication_keys):
                a = i - len(eradication_keys)
                phrase = eradication_keys[a].lower()
            else:
                a = i
                phrase = eradication_keys[a]
                
            if phrase in strForRow and not in_csv_eradication:
                eradication.loc[len(eradication)] = new_row
                in_csv = True
                in_csv_eradication = True
        for i in range(len(regulation_keys) * 2):
            phrase = ''

            if i >= len(regulation_keys):
                a = i - len(regulation_keys)
                phrase = regulation_keys[a].lower()
            else:
                a = i
                phrase = regulation_keys[a]

            if phrase in strForRow and not in_csv_regulation:
                regulation.loc[len(regulation)] = new_row
                in_csv = True
                in_csv_regulation = True
        for i in range(len(habitat_keys)): 
            phrase = ''

            if i >= len(habitat_keys):
                a = i - len(habitat_keys)
                phrase = habitat_keys[a].lower()
            else:
                a = i
                phrase = habitat_keys[a]

            if phrase in strForRow and not in_csv_habitat:
                habitat.loc[len(habitat)] = new_row 
                in_csv = True
                in_csv_habitat = True
        for i in range(len(stocking_keys)):
            phrase = ''

            if i >= len(stocking_keys):
                a = i - len(stocking_keys)
                phrase = stocking_keys[a].lower()
            else:
                a = i
                phrase = eradication_keys[a]
            
            phrase = stocking_keys[i]
            if phrase in strForRow and not in_csv_stocking:
                stocking.loc[len(stocking)] = new_row
                in_csv = True
                in_csv_stocking = True

        

        



        for word in contents:            
            if word == "Done" and in_rec == False and not in_csv:
                in_rec = True
                num = contents[0]
                contents = str(row[0])
                new_num = contents[0]
                #if the rows are not cooresponding, try to find matching num 
                #will have to expand the num part bc what ab double digits 
                if num != new_num:
                    found = False;
                    for row in df.iterrows():
                        contents = str(row[0])
                        new_num = contents[0]
                        if new_num == num:
                            found = True;
                            break
                    if not found:
                        break
            else:
                #fuzzy word matching
                #https://www.datacamp.com/tutorial/fuzzy-string-python
                new_row = [lakeName, strForRow, date, 1]
                for word_key in eradication_keys:
                    ratio = fuzz.ratio(word_key, word)
                    if ratio > max:
                        max = ratio
                        category = "eradication"
                        max_word = word
                for word_key in habitat_keys:
                    ratio = fuzz.ratio(word_key, word)
                    if ratio > max:
                        max = ratio
                        category = "habitat"
                        max_word = word
                       
                for word_key in regulation_keys:
                    if word == "5/59.":
                        i = 1
                        #do smth 
                    
                    ratio = fuzz.ratio(word_key, word)
                    if ratio > max:
                        max = ratio
                        category = "regulation"
                        max_word = word

                for word_key in stocking_keys:
                    ratio = fuzz.ratio(word_key, word)
                    if ratio > max:
                        max = ratio
                        category = "stocking"
                        max_word = word

        ratioNewRow = ['', 0, '', 0, ''] 
        if not in_csv and max >= 100:
            if category == "eradication":
                eradication.loc[len(eradication)] = new_row
                ratioNewRow = [max, 1, 'eradication', len(eradication), max_word]
            elif category == "stocking":
                stocking.loc[len(stocking)] = new_row
                ratioNewRow = [max, 1, 'stocking', len(stocking), max_word]

            elif category == "regulation":
                regulation.loc[len(regulation)] = new_row
                ratioNewRow = [max, 1, 'regulation', len(regulation), max_word]

            elif category == "habitat":
                habitat.loc[len(habitat)] = new_row 
                ratioNewRow = [max, 1, 'habitat', len(habitat), max_word]
            else:                
                ratioNewRow = [max, 0, 'NA', 0, 'NA']  
        else: 
            ratioNewRow = [max, 0, 'NA', 0, "NA"]
        ratios.loc[len(ratios)] = ratioNewRow;

    eradication.to_csv('/Users/jaimejacob/Documents/urop/condense_lines_proj/find_keywords2/current/eradication.csv', encoding='utf-8', index = False)
    habitat.to_csv('/Users/jaimejacob/Documents/urop/condense_lines_proj/find_keywords2/current/habitat.csv', encoding='utf-8', index = False)
    stocking.to_csv('/Users/jaimejacob/Documents/urop/condense_lines_proj/find_keywords2/current/stocking.csv', encoding='utf-8', index = False)
    regulation.to_csv('/Users/jaimejacob/Documents/urop/condense_lines_proj/find_keywords2/current/regulation.csv', encoding='utf-8', index = False)
    ratios.to_csv('/Users/jaimejacob/Documents/urop/condense_lines_proj/find_keywords2/ratio_csvs/ratio_100.csv', encoding='utf-8', index = False)

    #end of find keywords

def find_no_stock(fileName):
    fileName = str(fileName)
    df = pd.read_csv(fileName)
    df.loc[:, "NO"] = 0

    for index, row in df.iterrows():
        strForRow = str(row[1])
      #  contents = strForRow.split()
       
        if "no" in strForRow or "not" in strForRow or "No" in strForRow or "Not" in strForRow:
            df.at[index, 'NO'] = 1

    df.to_csv(fileName, encoding='utf-8', index = False)

def find_info_stock(fileName):
    fileName = str(fileName)
    df = pd.read_csv(fileName)
    stock_header = "LAKE NAME,CONTENTS,DATE,FUZZY MATCH,NO,Stage,Num,Species,Trout,Perch,Rock Bass,Walleye,Smallmouth Bass,Pike,Suckers,Largemouth Bass,Bluegill,Bass,Green Sunfish,Bullheads,Pumpkinseed Sunfish,Rainbows,Brook trout,Pike,Panfish,Grayling,Trash,Black Spotted Trout,Montana grayling,Chubs,BrownsHybrid Sunfish,Sea Lamprey,Splake,Salmonid,Common Shiners,Tiger Muskies,Whitefish,Ichthyomyzon,Brown trout,Menominees,Sturgeon"
    stock_header = stock_header.split(",")
    print(stock_header)
    df.loc[:, "Species"] = ""
    df.loc[:, "Stage"] = ""
   # df.loc[:, "Num"] = 0
   # df.columns = stock_header
    for i in range(len(stock_header)):
        if i > 7:
            df.loc[:, stock_header[i]] = 0
   # df.head()

    stock_csv = pd.read_csv('/Users/jaimejacob/Documents/urop/condense_lines_proj/find_keywords2/current/stocking.csv')
   # return


    species_keys = pd.read_csv('/Users/jaimejacob/Documents/urop/condense_lines_proj/keyword_csvs/keys_species.csv')
    species_keys = species_keys['Words'].tolist()

    stage_keys = pd.read_csv('/Users/jaimejacob/Documents/urop/condense_lines_proj/keyword_csvs/keys_stage.csv')
    stage_keys = stage_keys['Words'].tolist()

    for index, row in df.iterrows():
        strForRow = str(row[1])
        species = ""
        stage = ""
        amt = ""
      #  contents = strForRow.split()
       
       # if df.at[index, 'NO'] == 0:

            #clmn = (stock_csv)
        clmn = df.columns.values.tolist()

        if index == 5:
            index = 5
        for i in range(len(clmn)):
            if i >= 7:
                #    header = clmn[i].tolist()
                #    header = clmn[i].split()
                header = [clmn[i], clmn[i].lower()]
                for item in header:
                    if item in strForRow:
                        df.at[index, clmn[i]] = 1
                if df.at[index, clmn[i]] != 1:
                    df.at[index, clmn[i]] = 0
                


           # for word in species_keys:
             #   if word in strForRow:
              #      species += (word + ", ")
                  #  species += ", "
        if species != "":
            df.at[index, 'Species'] = species
        for word in stage_keys:
            if word in strForRow:
                stage += (word + ", ")
                  #  species += ", "
        if stage != "":
            df.at[index, 'Stage'] = stage
            
           # contents = strForRow.split()
           # for word in contents:
             #   if word.isnumeric():
             #       amt += (word + ",")
            #if amt != 0:
        df.at[index, 'Num'] = find_amt(strForRow)



            

    df.to_csv(fileName, encoding='utf-8', index = False)
    return




def find_amt(text):
    #https://www.w3schools.com/python/python_regex.asp
   # fileName = str(fileName)
   # df = pd.read_csv(fileName)    
    

        # Regular expression pattern to match different number formats
    pattern = r'\d+(?:,\d+)?|\d+/\d+'
  #  pattern = r'\d+(?:,\d+)?(?:\s\d+/\d+)?'
    #\d+: match 1+ ints
    #(?:,\d+)?: optionally, match a comma followed by one or more digits
    #|: OR
    #\d+/\d+: match a fraction, where one or more digits are separated by a forward slash



# Find all matches in the text
    matches = re.findall(pattern, text)


    amt = 0
    for i in range(len(matches)):
        matches[i] = matches[i].replace(',', '').strip()
       
    for match in matches:
        match = int(match)
        if match > 99 and (match > 1999 or match <= 1900):
            amt += match
            print("Match:", match, " | Amt: ",  amt)

         
    return amt


def find_info(fileName, headers):
    fileName = str(fileName)
    df = pd.read_csv(fileName)
    #habitat_header = list(df.columns)
    print (headers)
    headers = headers.split(",")
    print(headers)

  
    for i in range(len(headers)):
        if i > 4:
            df.loc[:, headers[i]] = 0
 

    for index, row in df.iterrows():
        strForRow = str(row[1])
  
        clmn = df.columns.values.tolist()

   
        for i in range(len(clmn)):
            if i >= 4:
 
                header = [clmn[i], clmn[i].lower()]
                for item in header:
                    if item in strForRow:
                        df.at[index, clmn[i]] = 1
                if df.at[index, clmn[i]] != 1:
                    df.at[index, clmn[i]] = 0
                

    df.to_csv(fileName, encoding='utf-8', index = False)
    return

def seperate_years(fileName):
    pattern = r'(?:\d{1}[19]\d{2}|\d{1,2}/\d{1,2}/\d{2}|\d{1,2}/\d{2})'
# \d{1}[19]\d{2}: Match a sequence of digits representing a four-digit number in the range from 1900 to 1999.
# \d{1,2}/\d{1,2}/\d{2}: Dates in the format "m/d/yy" or "mm/dd/yy".
# \d{1,2}/\d{2}: Dates in the format "m/yy" or "mm/yy".
    df = pd.read_csv(fileName)
    new_df = pd.DataFrame(columns=df.columns)

    for index, row in df.iterrows():
        #breakpoint()
        contents = str(row[1])
        #contents = strForRow.split()
        #print("Contents: ", contents)
        #contents = contents[1]
        years = re.findall(pattern, contents)
        #breakpoint()
        contents_split = re.split(pattern, contents)
        #print("Years:", years)
        #print("Contents split:", contents_split)  
        #breakpoint()  
        if len(contents_split) == 1:
            # breakpoint()
            row =pd.DataFrame([row.tolist()], columns=df.columns)
            new_df = pd.concat([new_df, row], ignore_index=True)
            continue

        for i in range(len(contents_split)):
            new_row_data = []
            if contents_split[i].isspace() or contents_split[i] == '.' or contents_split[i] == '-' or contents_split[i] == ';' or contents_split[i] == '. ' or contents_split[i] == '&':
                continue
            for j in range(len(df.columns)):
                if j != 1 and j != 2:
                    new_row_data.append(row[j])
                elif j == 1:
                    
                    new_row_data.append(contents_split[i])
                else: #i == 2
                    if i < len(years):
                        new_row_data.append(years[i])
                    else:
                        new_row_data.append('')
            #print("New Row Data:", new_row_data)
            #new_df = new_df.append(pd.DataFrame([new_row_data], columns=df.columns), ignore_index=True)
            new_row = pd.DataFrame([new_row_data], columns=df.columns)
            #print("Shape of df1:", new_df.shape)
            #print("Shape of df2:", new_row.shape)
            new_df = pd.concat([new_df, new_row], ignore_index=True)
        #breakpoint()
        # if len(contents_split) == 0:
        #     new_df.append(pd.DataFrame([row], columns=df.columns), ignore_index=True)
    new_df.to_csv('test.csv', encoding='utf-8', index = False)

                



    
       






text = "1947- 1,200 1948- 3,000 1949- none planted 1950-spring 3000 (A), fall 2100 (A)"
sentence = "In the year 1900, the population was 1,900, and the ratio was 7/34."
text = """ 4. Stocked 2,431 fingerling walleyes  " 14,999 11 " 7/74  11 880 " 11 7/77  " 2,500 " " 7/76 """
##text = """ 1. (Cont'd) 7,800 - 1949;2200 -1950;  5000 - 1951;10,000 - 1952 ; 5000 -  1953 . Good returns.  Lake biologically inventoried in  summer of 1953. Rainbow trout taken  in nets.  3, 4. Lake stocked annually with  5,000 legal rainbow. Planted  in 2 groups (1957-1962)--4,000  in spring, 1, 000 in fall. 1956  plant was only 1, 000 fall-planted  trout. """
#matches = find_amt(text)

   # print(f"Number: {number}")
#print(matches)



path_of_directory = '/Users/jaimejacob/Documents/urop/condense_lines_proj/end_result'


lst = os.listdir(path_of_directory) # your directory path



for files in os.listdir(path_of_directory):
        if files.endswith('.csv'):
            name = '/Users/jaimejacob/Documents/urop/condense_lines_proj/end_result/' + str(files)
           # find_keywords(name)

#find_no_stock('/Users/jaimejacob/Documents/urop/condense_lines_proj/find_keywords2/current/stocking.csv')
#find_info_stock('/Users/jaimejacob/Documents/urop/condense_lines_proj/find_keywords2/current/stocking.csv')
find_info_stock('/Users/jaimejacob/Documents/urop/condense_lines_proj/find_keywords2/test.csv')


#Stocking headers - 'LAKE NAME',CONTENTS',DATE',FUZZY MATCH',NO,Stage,Num,Species,"Trout, trout","Perch, perch","Rock Bass, rock bass","Walleye, walleye","Smallmouth Bass, smallmouth bass","Pike, pike","Suckers, suckers","Largemouth Bass, largemouth bass","Bluegill, bluegill","Bass, bass","Green Sunfish, green sunfish","Bullheads, bullheads","Pumpkinseed Sunfish, pumpkinseed sunfish","Rainbows, rainbows","Brook trout, brook trout","Pike, pike.1","Panfish, panfish","Grayling, grayling","Trash, trash","Black Spotted Trout, black spotted trout","Montana grayling, montana grayling","Chubs, chubs","Browns, browns","Hybrid Sunfish, hybrid sunfish","Sea Lamprey, sea lamprey","Splake, splake","Salmonid, salmonid","Common Shiners, common shiners","Tiger Muskies, tiger muskies","Whitefish, whitefish","Ichthyomyzon, ichthyomyzon","Brown trout, brown trout","Menominees, menominees","Sturgeon, sturgeon"
habitat_header = "LAKE NAME,CONTENTS,DATE,FUZZY MATCH,Install,Phosphate,Fertilizer,Transplant vegetation,Hollow Square Shelters,Bushel piles of gravel,Brush Shelters,Clear brush,Rock & gravel filter dam,Self - cleaning screen,Filter dam,Gravel,Filling,Transfer forage species to basin,Long crib,Low-head dams,Shelters,dam,Marsh,Establish,Artificial,Shelters,Brush,Rock,Screen,Basin,Crib"

#find_info('/Users/jaimejacob/Documents/urop/condense_lines_proj/find_keywords2/current/habitat.csv', habitat_header)


reg_header = "LAKE NAME,CONTENTS,DATE,FUZZY MATCH,Remove size restriction,Acquire public fishing site,Prohibit use of live minnows for bait,Commercial fisherman to trap net,Discontinue commercial trap netting,Remove size limit,Open to fishing,Acquire land for public access,Opened,Remove all restrictions,Commercial minnow seining,Restriction,Site,Bait,Fishermen,Netting,Limit,Seining,Access,Fishing"
#find_info('/Users/jaimejacob/Documents/urop/condense_lines_proj/find_keywords2/current/regulation.csv', reg_header)

eradication_header = "LAKE NAME,CONTENTS,DATE,FUZZY MATCH,Chemically reclaim,Rotenone,Kill,Chemical Renovation,Poisoned,Toxaphene,Repoisioning,Fish-Tox,Lethal,Manually remove,Removed,Antimycin,Chemical reclamation,Eradicate,Manually thin,Toxicant,Remove,Derris,Manual removal,Poison,Chemical,Chemically reclaim,Thin"
#find_info('/Users/jaimejacob/Documents/urop/condense_lines_proj/find_keywords2/current/eradication.csv', eradication_header)

#seperate_years('/Users/jaimejacob/Documents/urop/condense_lines_proj/find_keywords2/current/stocking.csv')