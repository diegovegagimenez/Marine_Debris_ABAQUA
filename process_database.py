# Script for processing Matlab (.mat) files containing daily data from ABAQUA marine debris collecting service
# from 2005 until 2022 during summer months (May - Sept). Data from 2004, 2010 and 2011 are missing.

import pandas as pd
from pymatreader import read_mat

# import warnings
# warnings.simplefilter(action='ignore', category=FutureWarning) #  # import warnings

data = read_mat('G:/Mi unidad/ABAQUA/data/Mallorca2005_2022_concat_dates_illa_cell.mat')
C = pd.DataFrame(data['Mal'])  # data.keys(). Depends on the island we are dealing with ['Mal','Men','Eiv' o 'For'].

# Defining columns names
names = ['Port', 'Barca', 'Kg', 'Vol', 'Fusta', 'MO',
         'Plastics', 'Olis', 'Algues', 'Altres', 'Total',
         'Ruta', 'Ajuntament', 'Comentaris', 'PortCheck',
         'BarcaCheck', 'RutaCheck', 'Lat1', 'Lon1', 'Lat2',
         'Lon2', 'Km_dist', 'Data', 'Illa']
C.columns = names

# Defining column types
strings=['Ajuntament', 'Barca', 'BarcaCheck', 'Comentaris',
         'Illa', 'Port', 'PortCheck', 'Ruta', 'RutaCheck']
floats = ['Kg', 'Vol', 'Fusta', 'MO', 'Plastics',
          'Olis', 'Algues', 'Altres', 'Total']

C[strings] = C[strings].astype(str)  # Change formats
C[floats] = C[floats].apply(pd.to_numeric, errors='coerce', axis=1)

C['Data'] = pd.to_datetime(C['Data'])

# Checking how many records/rows contain keywords in the column of comments
# daywmal = C[C['Comentaris'].str.contains('mal|Mal|MAL')]  # len = 2158
# daywpatro = C[C['Comentaris'].str.contains('Patro|PATRO|patro')]  # len = 134
# daywsortida = C[C['Comentaris'].str.contains('sortida|Sortida|Sortida')]  # = 4
# daywavaria = C[C['Comentaris'].str.contains('avaria|averia|Avaria|Averia|AVARIA|AVERIA')]  # len = 134

# Selecting working days (wdays) and not working days (notwdays)
wdays = C[~C['Comentaris'].str.contains('mal|Mal|MAL|Patro|patro|PATRO|avaria|Avaria|AVARIA|sortida|Sortida|SORTIDA')]
notwdays = C[C['Comentaris'].str.contains('mal|Mal|MAL|Patro|patro|PATRO|avaria|Avaria|AVARIA|sortida|Sortida|SORTIDA')]

# Selecting the boats and the dates on which the service did not operate
notwdays = notwdays[['Barca', 'Data']]

# Adding a new column in C and in notwdays to make possible an extraction of the matching values in both dataframes
notwdays['BarcaData'] = notwdays['Barca'] + notwdays['Data'].astype(str)
C['BarcaData'] = C['Barca'] + C['Data'].astype(str)

d_w = C[~C['BarcaData'].isin(notwdays['BarcaData']) == True]

data1 = d_w[['Port', 'Barca', 'Kg', 'Vol', 'Fusta', 'MO',
         'Plastics', 'Olis', 'Algues', 'Altres', 'Total',
         'Ruta', 'Ajuntament', 'Comentaris', 'PortCheck',
         'BarcaCheck', 'RutaCheck', 'Lat1', 'Lon1', 'Km_dist',
        'Data', 'Illa']] # Mergin Lat1-Lat2 Lon1-Lon2
data2 = d_w[['Port', 'Barca', 'Kg', 'Vol', 'Fusta', 'MO',
         'Plastics', 'Olis', 'Algues', 'Altres', 'Total',
         'Ruta', 'Ajuntament', 'Comentaris', 'PortCheck',
         'BarcaCheck', 'RutaCheck', 'Lat2', 'Lon2', 'Km_dist',
        'Data', 'Illa']]
data2 = data2.rename(columns={'Lat2':'Lat1', 'Lon2':'Lon1'})
dm = pd.concat([data1, data2], axis=0).sort_index(axis=0)

# dm2022=dm[dm['Data'].dt.year == 2022]

# Defining variance for obtaining insights
# def variance(data):
#      # Number of observations
#      n = len(data)
#      # Mean of the data
#      mean = np.nansum(data) / n
#      # Square deviations
#      deviations = [(x - mean) ** 2 for x in data]
#      # Variance
#      variance = np.nansum(deviations) / n
#      return variance

# Insights of the database per year
yrs = list([2005, 2006, 2007, 2008, 2009, 2012, 2013, 2014, 2015, 2016, 2017, 2018, 2019, 2021, 2022])

for yr in yrs:

    globals()['d_w_' + str(yr)] = d_w[d_w['Data'].dt.year == yr]
    globals()['dm' + str(yr)] = dm[dm['Data'].dt.year == yr]
    # GROUP BY BARCA
    globals()['d_w_barca_'+str(yr)] = globals()['d_w_'+str(yr)].groupby(globals()['d_w_'+str(yr)]['Barca']).agg(
        {'Kg': 'sum', 'Vol': 'sum', 'Fusta': 'sum', 'MO': 'sum', 'Plastics': 'sum',
        'Olis': 'sum', 'Algues': 'sum', 'Altres': 'sum', 'Total': 'sum', 'Lat1': 'mean', 'Lon1': 'mean', 'Lat2': 'mean',
        'Lon2': 'mean', 'Km_dist': 'sum'})

    # Efficiency per boat
    globals()['d_w_barca_' + str(yr)]['Eficiencia'] = globals()['d_w_barca_' + str(yr)]['Kg']/globals()['d_w_barca_' + str(yr)]['Km_dist']

    # GROUP BY RUTA
    globals()['d_w_ruta_' + str(yr)] = globals()['d_w_' + str(yr)].groupby(globals()['d_w_' + str(yr)]['Ruta']).agg(
        {'Kg': 'sum', 'Vol': 'sum', 'Fusta': 'sum', 'MO': 'sum', 'Plastics': 'sum',
         'Olis': 'sum', 'Algues': 'sum', 'Altres': 'sum', 'Total': 'sum', 'Lat1': 'mean', 'Lon1': 'mean',
         'Lat2': 'mean', 'Lon2': 'mean', 'Km_dist': 'sum'}).sort_values(by=['Kg'], ascending=False)
    # Obtaining top 5 rutes for each year
    globals()['d_w_ruta_head_' + str(yr)] = globals()['d_w_ruta_' + str(yr)].head(10)



