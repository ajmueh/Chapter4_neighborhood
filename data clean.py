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
dat = census.merge(habit, on = 'species', how = 'left')

# Create comparable tree ID
dat['cross_ID'] = dat['plot_code'] + '_' + dat['tree_tag'].astype(str)
growth['cross_ID'] = growth['plot_code'] + '_' + growth['tree_tag'].astype(str)



### Check for spelling mismatches

#dat[dat['Phenology'].isna() == False].shape

spec1_nomatch = dat[dat['Phenology'].isna()]['species']
spec1_nomatch = spec1_nomatch.unique()
spec2_nomatch = habit[habit['species'].isin(dat['species']) == False]['species']
