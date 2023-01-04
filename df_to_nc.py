# Transform DataFrame into NetCDF (.nc) file. Run first process_database.py

import netCDF4
import os
import datetime as dt
import numpy as np

data1 = d_w[['Port', 'Barca', 'Kg', 'Vol', 'Fusta', 'MO',
         'Plastics', 'Olis', 'Algues', 'Altres', 'Total',
         'Ruta', 'Ajuntament', 'Comentaris', 'PortCheck',
         'BarcaCheck', 'RutaCheck', 'Lat1', 'Lon1', 'Km_dist',
        'Data', 'Illa']]
data2 = d_w[['Port', 'Barca', 'Kg', 'Vol', 'Fusta', 'MO',
         'Plastics', 'Olis', 'Algues', 'Altres', 'Total',
         'Ruta', 'Ajuntament', 'Comentaris', 'PortCheck',
         'BarcaCheck', 'RutaCheck', 'Lat2', 'Lon2', 'Km_dist',
        'Data', 'Illa']]
data2 = data2.rename(columns={'Lat2':'Lat1', 'Lon2':'Lon1'})
data_merged = pd.concat([data1, data2], axis=0).sort_index(axis=0)
dm=data_merged
dm2022=data_merged[data_merged['Data'].dt.year == 2022]
# Data path
data_path = r'C:\Users\Diego\PycharmProjects\pythonProject'

# Create NetCDF File
output_nc = os.path.join(data_path, 'prueba2.nc')
nc = netCDF4.Dataset(output_nc, 'w')

# Global attributes
nc.title = 'Marine-debris'
nc.summary = ('Files containing daily data from ABAQUA marine debris collecting service in Balearic Islands from 2005'
              ' until 2022 during summer months (May - Sept). Data from 2010, 2011 and 2022 are missing')
nc.keywords = 'Marine debris'
nc.source = 'https://www.hydroshare.org/resource/24792a48a6394dcba52da62fa324ae40/'
nc.Conventions = 'CF-1.6'
nc.institution = 'Agencia Balear del Agua y la Calidad Ambiental (ABAQUA)'
nc.history = '{0} creation of marine debris kg netcdf file.'.format(
              dt.datetime.now().strftime("%Y-%m-%d")
             )
lat_dim = nc.createDimension('latitude', 270)
lon_dim = nc.createDimension('longitude', 448)
tim_dim = nc.createDimension('time', 122)

# Create variables
lat_var = nc.createVariable('latitude', np.float64, ('latitude'))
lat_var.units = 'degrees_north'
lat_var.standard_name = 'latitude'
lat_var.axis = 'Y'

lon_var = nc.createVariable('longitude', np.float64, ('longitude'))
lon_var.units = 'degrees_east'
lon_var.standard_name = 'longitude'
lon_var.axis = 'X'

time_var = nc.createVariable('time', np.int32, ('time'))
time_var.standard_name = 'time'
time_var.calendar = 'gregorian'
time_var.time_step = 'Daily'
time_var.units = 'Seconds since 2022-06-01 00:00:00'
time_var.axis = 'T'

crs_var = nc.createVariable('crs', np.int8, ())
crs_var.standard_name = 'crs'
crs_var.grid_mapping_name = 'latitude_longitude'
crs_var.crs_wkt = ("GEOGCS['GCS_WGS_1984',DATUM['D_WGS_1984',"
                   "SPHEROID['WGS_1984',6378137.0,298.257223563]],"
                   "PRIMEM['Greenwich',0.0],"
                   "UNIT['Degree',0.0174532925199433]]")

et_var = nc.createVariable('ET', np.float64, ('time', 'latitude', 'longitude'),
                           fill_value=9999)
et_var.units = 'kg/day'
et_var.long_name = 'Kilograms of marine debris'
et_var.short_name = 'kg_debris'
et_var.grid_mapping = 'crs'

# Load values: time
date_2022 = int((dt.datetime(2022,6,1) - dt.datetime(1970,1,1)).total_seconds())
# date_200906 = int((dt.datetime(2009,6,1) - dt.datetime(1970,1,1)).total_seconds())
# date_201306 = int((dt.datetime(2013,6,1) - dt.datetime(1970,1,1)).total_seconds())
# time_values = [date_200506, date_200906, date_201306]
time_var[:] = date_2022

lat_values = np.arange(39.2650, 39.939463, 0.0025)
lon_values = np.arange(2.3426, 3.462243, 0.0025)

lat_var[:] = lat_values
lon_var[:] = lon_values
dm2022=dm2022[['Data','Lat1','Lon1','Kg']]
# dm2022=dm2022[['Data','Lat1','Lon1','Kg']].to_dict()

latitude = sorted(list(set(dm2022['Lat1'])))
longitude = sorted(list(set(dm2022['Lon1'])))
time = sorted(list(set(dm2022['Data'])))

for line in dm2022:
        m = (np.abs(lon_values - longitude).argmin())
        n = (np.abs(lat_values - latitude).argmin())
        et_var[0, n, m] = line['Kg']


