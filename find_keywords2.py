"""
Creating Functions to Modify/Organize CSVs for Modeling.

Jaime Jacob
"""

import pandas as pd
import os
from thefuzz import fuzz
import re

# Finding keywords in each CSV file
def find_keywords(fileName):
    """Original Function to Sort the Lines into various management category CSVs."""
    
    fileName = str(fileName) # Ensure filename is a string

    # The Keys for each CSV come from the manual list created from going through CSVs
    df = pd.read_csv(fileName) # use Pandas dataframe to do categorizing

    # Put each file into a respective dataframe for analysis to make keyword CSVs to compare 
    regulation_keys = pd.read_csv('/Users/jaimejacob/Documents/urop/condense_lines_proj/keyword_csvs/keys_regulation.csv')
    regulation_keys = regulation_keys['Words'].tolist()

    eradication_keys = pd.read_csv('/Users/jaimejacob/Documents/urop/condense_lines_proj/keyword_csvs/keys_eradication.csv')
    eradication_keys = eradication_keys['Words'].tolist()

    habitat_keys = pd.read_csv('/Users/jaimejacob/Documents/urop/condense_lines_proj/keyword_csvs/keys_habitat.csv')
    habitat_keys = habitat_keys['Words'].tolist()

    stocking_keys = pd.read_csv('/Users/jaimejacob/Documents/urop/condense_lines_proj/keyword_csvs/keys_stocking.csv')
    stocking_keys = stocking_keys['Words'].tolist()

    # Pull the management CSVs and put them into dataframes to append entries
    eradication =   pd.read_csv('/Users/jaimejacob/Documents/urop/condense_lines_proj/find_keywords2/current/eradication.csv')
    habitat =       pd.read_csv('/Users/jaimejacob/Documents/urop/condense_lines_proj/find_keywords2/current/habitat.csv')
    regulation =    pd.read_csv('/Users/jaimejacob/Documents/urop/condense_lines_proj/find_keywords2/current/regulation.csv')
    stocking =      pd.read_csv('/Users/jaimejacob/Documents/urop/condense_lines_proj/find_keywords2/current/stocking.csv')
    ratios =        pd.read_csv('/Users/jaimejacob/Documents/urop/condense_lines_proj/find_keywords2/ratio_csvs/ratio_100.csv')

    # Find the lakename of the file 
    lakeName = fileName.split("/")
    lakeName = str(lakeName[len(lakeName) - 1])

    # Iterate through each card, check for key words to organize each line
    for index, row in df.iterrows():
        strForRow = str(row[3]) # Records Column
        contents = strForRow.split() # Split entry by each word per whitespace
        date = str(row[5]) # Date Column

        # Variables to track different conditions
        in_rec = False # In reccomendations column
        in_csv = False # Entry has been added to a management CSV
        # Which CSV it has been added to
        in_csv_eradication = False 
        in_csv_regulation  = False
        in_csv_stocking    = False
        in_csv_habitat     = False

        category = ""
        max = 0
        max_word = ""
        new_row = [lakeName, strForRow, date, 0] # Empty row to modify to append to management CSVs
        # If there is nothing in the entry, do not include it
        if len(contents) == 1 and contents[0] == 'nan':
            continue

        # Check for both capitalized and all lower case versions of each keyword
        for i in range(len(eradication_keys) * 2):
            phrase = '' # Eradication keyword

            # Check if there is an eradication keyword
            # Phrase keeps track of the key word(s) that were flagged in this entry
            # Checking the key words vs the entry so that the phrases could be longer than one word
            if i >= len(eradication_keys):
                a = i - len(eradication_keys)
                phrase = eradication_keys[a].lower()  # lowercase
            else:
                a = i
                phrase = eradication_keys[a] # Capitalized 
                
            if phrase in strForRow and not in_csv_eradication: # do not append if already in csv
                # Add new row to eradication CSV
                eradication.loc[len(eradication)] = new_row
                in_csv = True
                in_csv_eradication = True
        # Check for regulation keywords
        for i in range(len(regulation_keys) * 2):
            phrase = ''

            if i >= len(regulation_keys):
                a = i - len(regulation_keys)
                phrase = regulation_keys[a].lower() # lowercase
            else:
                a = i
                phrase = regulation_keys[a]

            if phrase in strForRow and not in_csv_regulation: # do not append if already in csv
                # Add new row to regulation CSV
                regulation.loc[len(regulation)] = new_row
                in_csv = True
                in_csv_regulation = True
        # Check for habitat key words
        for i in range(len(habitat_keys)): 
            phrase = ''

            if i >= len(habitat_keys):
                a = i - len(habitat_keys)
                phrase = habitat_keys[a].lower() # lowercase 
            else:
                a = i
                phrase = habitat_keys[a]

            if phrase in strForRow and not in_csv_habitat: # do not append if already in csv
                # Add new row to habitat CSV
                habitat.loc[len(habitat)] = new_row 
                in_csv = True
                in_csv_habitat = True
        # Check for stocking key words
        for i in range(len(stocking_keys)):
            phrase = ''

            if i >= len(stocking_keys):
                a = i - len(stocking_keys)
                phrase = stocking_keys[a].lower() # lowercase
            else:
                a = i
                phrase = eradication_keys[a]
            
            phrase = stocking_keys[i]
            if phrase in strForRow and not in_csv_stocking: # do not append if already in csv
                # Add to stocking CSV
                stocking.loc[len(stocking)] = new_row
                in_csv = True
                in_csv_stocking = True

        # If 'Done' or some other terminating keyword are in the line - indicates no action was recorded
        # Handling this by moving to the reccomendations column to find the corresponding action that was taken
        for word in contents:            
            if word == "Done" and in_rec == False and not in_csv:
                in_rec = True
                num = contents[0]
                contents = str(row[0])
                new_num = contents[0]
                # If the rows are not cooresponding, try to find matching num in Reccommendations column
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
                # Fuzzy word matching
                # https://www.datacamp.com/tutorial/fuzzy-string-python
                # https://pypi.org/project/thefuzz/
                # Finds the category with the highest ratio, max starts at 0
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

        # Threshold changes based on card from the R shiny app analysis, 100 is a placeholder 
        # https://9emauh-jaime-jacob.shinyapps.io/project/
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

    # Put new categorized dataframes into CSVs
    eradication.to_csv('/Users/jaimejacob/Documents/urop/condense_lines_proj/find_keywords2/current/eradication.csv', encoding='utf-8', index = False)
    habitat.to_csv('/Users/jaimejacob/Documents/urop/condense_lines_proj/find_keywords2/current/habitat.csv', encoding='utf-8', index = False)
    stocking.to_csv('/Users/jaimejacob/Documents/urop/condense_lines_proj/find_keywords2/current/stocking.csv', encoding='utf-8', index = False)
    regulation.to_csv('/Users/jaimejacob/Documents/urop/condense_lines_proj/find_keywords2/current/regulation.csv', encoding='utf-8', index = False)
    ratios.to_csv('/Users/jaimejacob/Documents/urop/condense_lines_proj/find_keywords2/ratio_csvs/ratio_100.csv', encoding='utf-8', index = False)

    # End of find keywords

# Finding instances where there was not any stocking done.
# Example of an entry that would not be included after running this function - 'No stocking this year'. 
def find_no_stock(fileName):
    """Find termintating keywords."""
    fileName = str(fileName)
    df = pd.read_csv(fileName)
    df.loc[:, "NO"] = 0

    for index, row in df.iterrows():
        strForRow = str(row[1])

        if "no" in strForRow or "not" in strForRow or "No" in strForRow or "Not" in strForRow:
            df.at[index, 'NO'] = 1

    df.to_csv(fileName, encoding='utf-8', index = False)

# Flags species using the same mechanism as finding keywords. Species list comes from the same method that the keywords were found. 
def find_info_stock(fileName):
    """Find species stocked, amount, in each line in the stocking CSV."""

    fileName = str(fileName)
    find_no_stock(fileName) # Make sure to mark where there was no stocking done 
    df = pd.read_csv(fileName) # Create dataframe to modify
    # Colum Names - include all of the keyword species pulled out from the manual QAQC
    stock_header = "LAKE NAME,CONTENTS,DATE,FUZZY MATCH,NO,Stage,Num,Species,Are_species,Trout,Perch,Rock Bass,Walleye,Smallmouth Bass,Pike,Suckers,Largemouth Bass,Bluegill,Bass,Green Sunfish,Bullheads,Pumpkinseed Sunfish,Rainbows,Brook trout,Pike,Panfish,Grayling,Trash,Black Spotted Trout,Montana grayling,Chubs,BrownsHybrid Sunfish,Sea Lamprey,Splake,Salmonid,Common Shiners,Tiger Muskies,Whitefish,Ichthyomyzon,Brown trout,Menominees,Sturgeon,Salmon"
    stock_header = stock_header.split(",") # create a list of headers
    df.loc[:, "Species"] = "" # set column to standard null value
    df.loc[:, "Stage"] = "" # set column to standard null value
    df.loc[:, "Are_species"] = 0 # set column to standard null value

    # set species column to standard null value
    for i in range(len(stock_header)):
        if i > 7:
            df.loc[:, stock_header[i]] = 0

    # Pull species keys and create a list
    species_keys = pd.read_csv('/Users/jaimejacob/Documents/urop/condense_lines_proj/keyword_csvs/keys_species.csv')
    species_keys = species_keys['Words'].tolist()

    # Pull stage keys and create a list
    # Stage refers to stage in development, EX. fingerling, adult, etc
    stage_keys = pd.read_csv('/Users/jaimejacob/Documents/urop/condense_lines_proj/keyword_csvs/keys_stage.csv')
    stage_keys = stage_keys['Words'].tolist()

    # Iterate through each row in dataframe to find species & stage
    for index, row in df.iterrows():
        strForRow = str(row[1])
        species = ""
        stage = ""

        clmn = df.columns.values.tolist()

        for i in range(len(clmn)):
            if i >= 7:
                header = [clmn[i], clmn[i].lower()] # to check for capitalized and all lower case

                # check if keyword in the contents of the entry 
                for item in header:
                    if item in strForRow:
                        df.at[index, clmn[i]] = 1
                        df.at[index, 'Are_species'] = 1
                if df.at[index, clmn[i]] != 1:
                    df.at[index, clmn[i]] = 0
        if species != "":
            df.at[index, 'Species'] = species

        # If no species, look to entry above and copy contents, due to the dates possibly being seperated and thus the species not explicitly recorded
        if df.at[index, 'Are_species'] == 0:
            cur = index - 1
            while cur >= 0:
                if df.at[cur, "'LAKE NAME'"] == df.at[index, "'LAKE NAME'"]:
                    if df.at[cur, 'Are_species'] == 1: 
                        contents = df.at[index, " 'CONTENTS'"]
                        date = df.at[index, " 'DATE'"]
                        df.loc[index] = df.loc[cur]
                        df.at[index, " 'CONTENTS'"] = contents
                        df.at[index, " 'DATE'"] = date
                        df.at[index, 'Are_species'] = 1
                        break
                else:
                    break
                cur = cur - 1
        for word in stage_keys:
            if word in strForRow:
                stage += (word + ", ")
        if stage != "":
            df.at[index, 'Stage'] = stage

        df.at[index, 'Num'] = find_amt(strForRow)
    df.to_csv(fileName, encoding='utf-8', index = False)
    return

# Did not end up using number of fish stocked in final analysis. 
# This function was not used in final analysis.
def find_amt(text):
    """Find quantities of fish stocked per line."""
    # https://www.w3schools.com/python/python_regex.asp
    # fileName = str(fileName)
    # Regular expression pattern to match different number formats
    pattern = r'\d+(?:,\d+)?|\d+/\d+'
    # \d+: match 1+ ints
    # (?:,\d+)?: optionally, match a comma followed by one or more digits
    # |: OR
    # \d+/\d+: match a fraction, where one or more digits are separated by a forward slash
    # Find all matches in the text
    matches = re.findall(pattern, text)
    amt = 0
    for i in range(len(matches)):
        matches[i] = matches[i].replace(',', '').strip()
       
    for match in matches:
        match = int(match)
        if match > 99 and (match > 1999 or match <= 1900):
            amt += match
    return amt


# Pulls out information based upon the keywords for each category. 
# Keywords predetermined via manual QAQC as described for find_keywords function.
def find_info(fileName, headers):
    """Generalized find information function."""
    fileName = str(fileName)
    df = pd.read_csv(fileName)
    headers = headers.split(",")

    for i in range(len(headers)):
        if i > 4:
            df.loc[:, headers[i]] = 0

    for index, row in df.iterrows():
        strForRow = str(row[1])

        clmn = df.columns.values.tolist()

        for i in range(len(clmn)):
            if i >= 4:

                header = [clmn[i], clmn[i].lower()] # check for capitalized and lowercase 
                for item in header:
                    if item in strForRow:
                        df.at[index, clmn[i]] = 1
                if df.at[index, clmn[i]] != 1:
                    df.at[index, clmn[i]] = 0

    df.to_csv(fileName, encoding='utf-8', index = False)
    return

def seperate_years(fileName, output):
    """Seperate years into various lines for easier analysis of separate stocking events."""
    pattern = r'(?:\d{1}[19]\d{2}|\d{1,2}/\d{1,2}/\d{2}|\d{1,2}/\d{2})'
    # \d{1}[19]\d{2}: Match a sequence of digits representing a four-digit number in the range from 1900 to 1999.
    # \d{1,2}/\d{1,2}/\d{2}: Dates in the format "m/d/yy" or "mm/dd/yy".
    # \d{1,2}/\d{2}: Dates in the format "m/yy" or "mm/yy".
    df = pd.read_csv(fileName)
    new_df = pd.DataFrame(columns=df.columns)

    # Iterate through rows and find instances of the RegEx pattern
    for index, row in df.iterrows():
        contents = str(row[1])
        years = re.findall(pattern, contents)
        # Split based upon instances of years found 
        contents_split = re.split(pattern, contents)

        # No years
        if len(contents_split) == 1:
            row = pd.DataFrame([row.tolist()], columns=df.columns)
            new_df = pd.concat([new_df, row], ignore_index=True)
            continue

        # Check for empty cells in Date field
        for i in range(len(contents_split)):
            new_row_data = []
            is_empty = False
            try:
                df.at[index, "DATE"].isnull()
                is_empty = True
            except:
                try:                    
                    df.at[index, "DATE"].isspace()
                    is_empty = True
                except:
                    is_empty = False
 
            # If date is empty, and there is no content in the content cell, discard entry
            if is_empty and (contents_split[i].isspace() or contents_split[i] == '.' or contents_split[i] == '-' or contents_split[i] == ';' or contents_split[i] == '. ' or contents_split[i] == '&'):
                continue

            # Iterate through rows and appedn to new dataframe split by years
            for j in range(len(df.columns)):
                if j != 1 and j != 2:
                    new_row_data.append(row[j])
                elif j == 1:
                    
                    new_row_data.append(contents_split[i])
                else: #i == 2
                    if i < len(years):
                        new_row_data.append(years[i])
                    else:
                        new_row_data.append(row[j])

            new_row = pd.DataFrame([new_row_data], columns=df.columns)
            new_df = pd.concat([new_df, new_row], ignore_index=True)

    new_df.to_csv(output, encoding='utf-8', index = False)
    
# Split by Species Function - Did not end up using this in final analysis. 
def split_by_species(fileName):
    df = pd.read_csv(fileName)
    new_df = pd.DataFrame(columns=df.columns)

    species_keys = pd.read_csv('/Users/jaimejacob/Documents/urop/condense_lines_proj/keyword_csvs/keys_species.csv')
    species_keys = species_keys['Words'].tolist()

    for index, row in df.iterrows():
        contents = str(row[1])
        new_contents = []
        contents = re.split(" ", contents)
        current_string = ""
        for word in contents:
            if word in species_keys:
                current_string += (" " + word)
                new_contents.append(current_string)
                current_string = ""
            else:
                current_string += (" " + word)
        if current_string != "":
            new_contents.append(current_string)
        # print("NEW CONTENTS:", new_contents)

        for i in range(len(new_contents)):
            new_row_data = []
            for j in range(len(df.columns)):
                new_row_data.append(row[j])
                if j == 1:
                    new_row_data[j] = new_contents[i]
            new_row = pd.DataFrame([new_row_data], columns=df.columns)
            if new_row['NO'][0] == 1:
                continue
            new_df = pd.concat([new_df, new_row], ignore_index=True)
    
    new_df.to_csv(fileName, encoding='utf-8', index = False)

    file_path = os.path.join(os.getcwd(), fileName)

    find_info_stock(file_path)
    
# Finds sum of count columns to find counts on instances of various events
def summarize(fileName):
    df = pd.read_csv(fileName)

    for col in df.columns:
        try:
            df[col] = pd.to_numeric(df[col])
        except ValueError:
            print(f"Column '{col}' contains non-numeric values that cannot be converted.")

    print(df.dtypes)
    sum_of_columns = df.sum(numeric_only=True)
    print(sum_of_columns)
    sum_df = pd.DataFrame(sum_of_columns).T
    sum_df.to_csv('df_summary.csv', encoding='utf-8', index = False)

# Formatting years in the CSV files for analysis in R
def format_years(fileName, outputFile):

    # Captures formats like '7/76' 
    pattern1 = r'^\s*(\d{1,2})/(\d{1,2})\s*$'

    # Captures formats like '7/7/76'
    pattern2 = r'^\s*(\d{1,2})/(\d{1,2})/(\d{1,2})\s*$'

    # Captures formats like '5-25'
    pattern3 = r'^\s*(\d{1,2})-(\d{1,2})\s*$'

    # Captures formats like '9-5-25'
    pattern4 = r'^\s*(\d{1,2})-(\d{1,2})-(\d{1,2})\s*$'

    # Captures formats like ' '82 '
    pattern5 = r"^\s*'(\d{1,2})\s*$"

    # Other patterns not accounted for: 71&72, Fall/1950
    df = pd.read_csv(fileName)
    num_exceptions = 0

    # Looks for dates in the entry, uses that as the DATE column
    for index, row in df.iterrows():
        dates = None
        date = str(row[2])

        dates2 = re.search(pattern2, date)
        dates4 = re.search(pattern4, date)
        if dates2:
            dates = dates2
        elif dates4:
            dates = dates4

        if dates:
            date = dates.group(3)
            date = '19' + str(date)
            date = int(date)
            df.at[index, "DATE"] = date
            continue 
    
        if not dates:
            dates1 = re.search(pattern1, date)
            dates3 = re.search(pattern3, date)
            if dates1: 
                dates = dates1
            elif dates3:
                dates = dates3
            if dates:
                date = dates.group(2)
                date = '19' + str(date)
                date = int(date)
                df.at[index, "DATE"] = date
                continue 

        dates5 = re.search(pattern5, date)

        if dates5:
            date = dates5.group(1)
            date = '19' + str(date)
            date = int(date)
            df.at[index, "DATE"] = date
            continue 

        if not dates:
            try:
                if not date == 'nan':
                    df.at[index, "DATE"] = int(row[2])
                else: 
                    df.at[index, "DATE"] = None
            except:
                num_exceptions = num_exceptions + 1
            continue

    print('FILE:', fileName)
    # Num exceptions are instances where the date column does not follow any of the formats specified 
    print('Exceptions:', num_exceptions)
    df.to_csv(outputFile, encoding='utf-8', index = False)

# Discards instances in the stocking CSV where the negative keywords are present indicating no stocking was completed
def filter_stocking(fileName, outputFile):
    df = pd.read_csv(fileName)

    new_df = pd.DataFrame(columns=df.columns)
    for index, row in df.iterrows():
        if df.at[index, 'NO'] == 1:
            continue 
        # if both the date and information column is blank, do not include row
        elif pd.isna(row['DATE']) and pd.isna(row['CONTENTS']):
            continue
        elif pd.isna(row['CONTENTS']):
            continue
        else:
            #new_row = pd.DataFrame([new_row_data], columns=df.columns)
            #new_df.pd.con
            row_new = pd.DataFrame([row.tolist()], columns=df.columns)
            new_df = pd.concat([new_df, row_new], ignore_index=True)
            # new_df = pd.concat([new_df, df.at[index]], ignore_index=True)

    new_df.to_csv(outputFile, encoding='utf-8', index = False)
