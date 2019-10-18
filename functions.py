def neighborhood (tree, radius):

    # Subset dataframe for the tree's site
    dat_site = dat[dat['plot_code'] == dat[dat['cross_ID'] == tree]['plot_code']]

    # Set tree location
    x = dat_site[dat_site['cross_ID'] == tree]['x']
    y = dat_site[dat_site['cross_ID'] == tree]['y']

    # Find square neighborhood based on radius
    neigh = dat_site[(dat_site['x'] > x - radius) & (dat_site['x'] < x + radius) & (dat_site['y'] > y - radius) & (dat_site['y'] < y + radius)]

    # Narrow neighborhood to actual radius
    neigh['dist'] = ((neigh['x'] - x)**2 + (neigh['y'] - y)**2)**.5
    neigh = neigh[neigh['dist'] <= radius]

    # Find proportion evergreen trees
    neigh_known = neigh[neigh['Phenology'].isna() == False]
    prop_ever = neigh_known[neigh_known['Phenology'] == "evergreen"].shape[0] / neigh_known.shape[0]

    # Assess confidence based on known phenologies
    confidence = neigh_known.shape[0] / neigh.shape[0]



    return;
