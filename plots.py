###=================================###
#           Import settings
###=================================###

import matplotlib.pyplot as plt
import matplotlib.pylab as pl
import matplotlib.patches as mpatches
from matplotlib.colors import LinearSegmentedColormap
import pandas as pd
import numpy as np
import os

# Set color gradient
col = LinearSegmentedColormap.from_list('name', ['#de5d54','#58f57f'])

###====================================================###
#   Assess effect of growth on variable neighborhoods
###====================================================###

# Find neigbhorhoods of different sizes
trees2 = census_tot.copy()
neighborhood(trees2, radius = 2)
trees2 = trees2[(trees2.growth_rate_mm.isna() == False) & (trees2.conf >= 0.75) & (trees2.prop_evergreen.isna() == False) & (trees2.Phenology == "evergreen")]

trees5 = census_tot.copy()
neighborhood(trees5, radius = 5)
trees5 = trees5[(trees5.growth_rate_mm.isna() == False) & (trees5.conf >= 0.75) & (trees5.prop_evergreen.isna() == False) & (trees5.Phenology == "evergreen")]

trees8 = census_tot.copy()
neighborhood(trees8, radius = 8)
trees8 = trees8[(trees8.growth_rate_mm.isna() == False) & (trees8.conf >= 0.75) & (trees8.prop_evergreen.isna() == False) & (trees8.Phenology == "evergreen")]

# Create figure
fig = plt.figure()

plt.subplot(1,3,1)
plt.scatter(trees2.prop_evergreen, trees2.growth_rate_mm, color = "black")
plt.title("2m Neighborhood")

plt.subplot(1,3,2)
plt.scatter(trees5.prop_evergreen, trees5.growth_rate_mm, color = "black")
plt.title("5m Neighborhood")

plt.subplot(1,3,3)
plt.scatter(trees8.prop_evergreen, trees8.growth_rate_mm, color = "black")
plt.title("8m Neighborhood")

fig.savefig("./figures/neighborhood_comp.pdf", bbox_inches = 'tight')