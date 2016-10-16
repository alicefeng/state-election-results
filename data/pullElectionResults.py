# -*- coding: utf-8 -*-
"""
Title: pullElectionResults.py

Description:
This program scrapes UC Santa Barbara's American Presidency Project
site for past presidential election results.  It records the share
of votes received by the Republican and Democratic candidate (and any
third party candidates who received a significant number of votes) by
state for every election since 1968.  It also notes the party of the
victor in a dataframe.

Input: none

Output: state_election_results.csv (Note: this file will require a little
manual editing afterwards due to a few odd election quirks.)

Created on Sun Sep 18 16:57:35 2016

@author: Alice
"""

import urllib, bs4
import pandas as pd

state_list = ['Alaska',
        'Alabama',
        'Arkansas',
        'Arizona',
        'California',
        'Colorado',
        'Connecticut',
        'Dist. of Col.',
        'Delaware',
        'Florida',
        'Georgia',
        'Hawaii',
        'Iowa',
        'Idaho',
        'Illinois',
        'Indiana',
        'Kansas',
        'Kentucky',
        'Louisiana',
        'Massachusetts',
        'Maryland',
        'Maine',
        'Michigan',
        'Minnesota',
        'Missouri',
        'Mississippi',
        'Montana',
        'North Carolina',
        'North Dakota',
        'Nebraska',
        'New Hampshire',
        'New Jersey',
        'New Mexico',
        'Nevada',
        'New York',
        'Ohio',
        'Oklahoma',
        'Oregon',
        'Pennsylvania',
        'Puerto Rico',
        'Rhode Island',
        'South Carolina',
        'South Dakota',
        'Tennessee',
        'Texas',
        'Utah',
        'Virginia',
        'Vermont',
        'Washington',
        'Wisconsin',
        'West Virginia',
        'Wyoming'
]

years = ['1964', '1968', '1972', '1976', '1980', '1984', '1988', '1992', 
         '1996', '2000', '2004', '2008', '2012']

results = []

# fetch election results table from each election's site
for year in years:
    url = 'http://www.presidency.ucsb.edu/showelection.php?year=' + year
    html = urllib.urlopen(url).read()
    soup = bs4.BeautifulSoup(html, "lxml")
    
    # grab table rows from results table
    if year == '1976':
        elec_table = soup.select('.ver11 > tr')
    else:
        elec_table = soup.select('.elections_states > tr')
    
    for row in elec_table:
        text = row.getText().split('\n') # split on carriage return for state 
                                         # names that have multiple words            
        if text[1].rstrip('*') in state_list:
            state = text[1].rstrip('*').encode('utf_8')
            if year in ['1964', '1976', '2008', '2012']:
                dem_pct = float(text[4].rstrip('%').encode('utf_8'))
                rep_pct = float(text[7].rstrip('%').encode('utf_8'))
                third_pct = 0
            elif year in ['1968', '1980', '2000']:
                rep_pct = float(text[4].rstrip('%').encode('utf_8'))
                dem_pct = float(text[7].rstrip('%').encode('utf_8'))
                third_pct = float(text[10].rstrip('%').encode('utf_8'))
            elif year in ['1992', '1996']:
                dem_pct = float(text[4].rstrip('%').encode('utf_8'))
                rep_pct = float(text[7].rstrip('%').encode('utf_8'))
                third_pct = float(text[10].rstrip('%').encode('utf_8'))
            else:
                rep_pct = float(text[4].rstrip('%').encode('utf_8'))
                dem_pct = float(text[7].rstrip('%').encode('utf_8'))
                third_pct = 0
#            print year, state, dem_pct, rep_pct
            results.append({'Year': year, 'State': state, 'Dem_pct': dem_pct,
                            'Rep_pct': rep_pct, 'Third_pct': third_pct})
                            
# convert results into pandas dataframe
data = pd.DataFrame(results)
data['Year'].value_counts().sort_index() # check that we have 51 results for each election year

# note which party won
data['Winner'] = ''
data.loc[(data['Dem_pct'] > data['Rep_pct']) & (data['Dem_pct'] > data['Third_pct']), 'Winner'] = 'Democrat'
data.loc[(data['Rep_pct'] > data['Dem_pct']) & (data['Rep_pct'] > data['Third_pct']), 'Winner'] = 'Republican'
data.loc[(data['Third_pct'] > data['Rep_pct']) & (data['Third_pct'] > data['Dem_pct']), 'Winner'] = 'Third Party'

# export data to csv
data.to_csv('state_election_results.csv', index=False)

# get winner's share in one column
data['winner_share'] = 0
data.loc[(data['Winner'] == 'Democrat'),'winner_share'] = data['Dem_pct']
data.loc[(data['Winner'] == 'Republican'), 'winner_share'] = data['Rep_pct']
data.loc[(data['Winner'] == 'Third Party'), 'winner_share'] = data['Third_pct']

data.sort_values(['State', 'Year'])
