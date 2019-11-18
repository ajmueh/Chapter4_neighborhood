###===========================###
#   Import Data and Settings
###===========================###

import pandas as pd
import numpy as np
import os

os.chdir("C:/Users/Andrew/Dropbox/Phd/Chapter 4/neighborhood analysis")
execfile("./code/functions.py")

### Read in data

growth = pd.read_table("./data/growth.txt", sep = "\t")
growth = growth[['plot_code','sub_plot','tree_tag','year','month','day','pom_height_m','dbh_nodirection_mm','date','dendrometer_reading_mm','site']]

## Bring in census data and subset for pertinent columns
census = pd.read_table("./data/census.txt", sep = "\t")
census = census[['plotid','plot_code','treeid','tree_tag','sub_plot_t1','x','y','family','genus','species','authority','familyapgid','genusid','speciesid','census_no','census_date','d0','pom','f1']]
census = census[census.tree_tag.isna() == False]
# Convert tag number to integer
census.tree_tag = census.tree_tag.astype(str).astype(float).astype(int)


## Bring in leaf habit info
habit = pd.read_table("./data/phenology.txt", sep = "\t")
habit.rename(columns = {'Species_JA_trimfinalspace':'species'}, inplace = True)

habit_ext = pd.read_table("./data/ouedraogo_phenology.txt", sep = "\t")

###=================================###
#   Merge and create new variables
###=================================###

### Merge phenology data into census
census_tot = census.merge(habit, on = 'species', how = 'left')
census_tot = census_tot.merge(habit_ext, on = 'genus', how = 'left')

# Join phenology data
census_tot.Phenology = census_tot['leaf_habit'].where(census_tot['Phenology'].isna(), other = census_tot['Phenology'])

# Create comparable tree ID
census_tot['cross_ID'] = census_tot['plot_code'] + '_' + census_tot['tree_tag'].astype(str)
growth['cross_ID'] = growth['plot_code'] + '_' + growth['tree_tag'].astype(str)

### Determine DBH growth rates

# Calculate total number of days monitored
date_diff = (census_tot.groupby('cross_ID')['census_date'].max() - census_tot.groupby('cross_ID')['census_date'].min()).reset_index()
date_diff.census_date = date_diff.census_date * 365
date_diff.rename(columns = {'census_date':'days_diff'}, inplace = True)

# Calculate change in dbh from first to last census
dbh_diff = census_tot.groupby('cross_ID')['d0'].max() - census_tot.groupby('cross_ID')['d0'].min()

### Determine dendro growth rates

# Convert variable to date object
growth.date = pd.to_datetime(growth.date)

# Calculate total number of days monitored
date_diff2 = (growth.groupby('cross_ID')['date'].max() - growth.groupby('cross_ID')['date'].min()).reset_index()
date_diff2.date = date_diff2.date.dt.days

# Sum growth increments across study period
growth_tot = growth.groupby("cross_ID")['dendrometer_reading_mm'].sum().reset_index()

# Find growth rate (mm/day)
growth_tot['growth_rate_mm'] = growth_tot.dendrometer_reading_mm / date_diff2.date
# Select for only those trees that have meaningful growth rates
growth_tot = growth_tot[growth_tot.growth_rate_mm < 1000]

### Reduce census data to one observation per tree, either census 4 or 5, to match dates of growth measurements
census_tot = census_tot[(census_tot['census_no'] == 4) | (census_tot['census_no'] == 5)]
census_tot = census_tot.drop_duplicates(subset = "cross_ID")
census_tot = census_tot.reset_index()

### Final merge
## Merge growth data into census data
census_tot = census_tot.merge(growth_tot[['cross_ID','growth_rate_mm']], on = 'cross_ID', how = 'left')
