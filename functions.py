
###=================================###
#     Neighborhood calc function      #
###=================================###

def neighborhood (dat, radius):

    ## Set up new variables in data
    dat['prop_evergreen'] = 0
    dat['conf'] = 0
    dat['neighbors_num'] = 0

    ## Set up loop for each observation
    for i in range(0,dat.shape[0]):

        # Grab ith row
        tree = dat.iloc[i,]

        # Subset data for the tree's site (only look at the relevant neighborhood)
        dat_site = dat[dat['plot_code'] == tree['plot_code']]

        # Find neighborhood in square based on radius to reduce # of distance calculations
        neigh = dat_site[(dat_site['x'] > tree['x'] - radius) & (dat_site['x'] < tree['x'] + radius) & (dat_site['y'] > tree['y'] - radius) & (dat_site['y'] < tree['y'] + radius)]
        neigh = neigh[neigh['cross_ID'] != tree['cross_ID']]

        # Narrow neighborhood to actual radius
        neigh['dist'] = ((neigh['x'] - tree['x'])**2 + (neigh['y'] - tree['y'])**2)**.5
        neigh = neigh[neigh['dist'] <= radius]

        # Find proportion evergreen trees
        neigh_known = neigh[neigh['Phenology'].isna() == False]

        ## Parse various data scenarios
        # Check to see if the phenology of any neighbors are known
        if neigh_known.shape[0] > 0:
            # Determine the proportion of evergreens
            prop_ever = neigh_known[neigh_known['Phenology'] == "evergreen"].shape[0] / neigh_known.shape[0]

            # Assess confidence based on known phenologies
            confidence = neigh_known.shape[0] / neigh.shape[0]

            # Update proportion evergreen and confidence
            dat.loc[i, 'conf'] = confidence
            dat.loc[i,'prop_evergreen'] = prop_ever

        # If no neighbor phenologies are know, check to see if the tree is alone
        elif neigh.shape[0] == 0:
            # Set confidence to 1, assign NA to proportion evergreen (there is no neighborhood)
            dat.loc[i, 'conf'] = 1
            dat.loc[i, 'prop_evergreen'] = None

        # If no neighbor phenologies are known, but there is a neighborhood
        else:
            # Set confidence to 0, assign NA to proportion evergreen (can't tell)
            dat.loc[i, 'conf'] = 0
            dat.loc[i, 'prop_evergreen'] = None


        dat.loc[i,'neighbors_num'] = neigh.shape[0]


    return;