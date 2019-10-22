import pandas as pd
import numpy as np
import os

os.chdir("C:/Users/Andrew/Dropbox/Phd/Chapter 4/neighborhood analysis")

### Read in data

growth = pd.read_table("./data/growth.txt", sep = "\t")
growth = growth[['plot_code','sub_plot','tree_tag','year','month','day','pom_height_m','dbh_nodirection_mm','date','dendrometer_reading_mm','site']]

## Bring in census data and subset for pertinent columns
census = pd.read_table("./data/census.txt", sep = "\t")
census = census[['plotid','plot_code','treeid','tree_tag','sub_plot_t1','x','y','family','genus','species','authority','familyapgid','genusid','speciesid','census_no','census_date','d0','pom','f1']]

## Bring in leaf habit info
habit = pd.read_table("./data/phenology.txt", sep = "\t")
habit.rename(columns = {'Species_JA_trimfinalspace':'species'}, inplace = True)


### Merge datasets together

## Merge phenology data into census

census_tot = census.merge(habit, on = 'species', how = 'left')

# Create comparable tree ID
census_tot['cross_ID'] = census_tot['plot_code'] + '_' + census_tot['tree_tag'].astype(str)
growth['cross_ID'] = growth['plot_code'] + '_' + growth['tree_tag'].astype(str)

# Reduce to one observation per tree, either census 4 or 5, to match dates of growth measurements
census_tot = census_tot[(census_tot['census_no'] == 4) | (census_tot['census_no'] == 5)]
census_tot = census_tot.drop_duplicates(subset = "cross_ID")
census_tot = census_tot.reset_index()


