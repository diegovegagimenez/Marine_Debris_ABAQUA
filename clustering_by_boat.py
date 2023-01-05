## for data
import numpy as np
import pandas as pd
## for plotting
import matplotlib.pyplot as plt
import seaborn as sns
## for geospatial
import folium
# import geopy
## for machine learning
from sklearn import preprocessing, cluster
import scipy
## for deep learning
# import minisom
from geopy.geocoders import Nominatim
import webbrowser
webbrowser.open(r'https://towardsdatascience.com/clustering-geospatial-data-f0584f0b04ec')  # REFFERENCE WEB

geolocator = Nominatim(user_agent="MyCoder")
zona = geolocator.reverse("39.4555555, 3.2955555") #  Cales de Mallorca, Manacor, Llevant, Illes Balears, Espa�a, (39.4652049, 3.279857, 0.0))
location = [39.6155555, 3.0255555]  # Center of Mallorca
x, y = "Lat1", "Lon1"
color = "Barca"
size = "Kg"
popup = "Ruta"
idx = list(range(5219*2))
dtf = dm2022[['Kg','Barca','Lat1','Lon1','Ruta']].set_index(pd.Index(idx))    #Añadir Lat2,Lon2 si es necesario
data = dtf.copy()

## create color column
lst_colors=["red","green","orange","blue","yellow","pink","white","black","gray","brown"]
lst_elements = sorted(list(dtf[color].unique()))
data["color"] = data[color].apply(lambda x:
                lst_colors[lst_elements.index(x)])
## create size column (scaled)
scaler = preprocessing.MinMaxScaler(feature_range=(3,15))
data["size"] = scaler.fit_transform(
               data[size].values.reshape(-1,1)).reshape(-1)

## initialize the map with the starting location
map_ = folium.Map(location=location, tiles="openstreetmap",
                  zoom_start=10, control_scale=True)

## add points Lat1 Lon1
data.apply(lambda row: folium.CircleMarker(
           location=[row[x],row[y]], popup=row[popup],
           color=row["color"], fill=True,
           radius=row["size"]).add_to(map_), axis=1)

## add html legend
legend_html = """<div style="position:fixed; bottom:10px; left:10px;border:2px solid
                black; z-index:9999; font-size:14px;">&nbsp;<b>"""+color+""":</b><br>"""
for i in lst_elements:
     legend_html = legend_html+"""&nbsp;<i class="fa fa-circle 
     fa-1x" style="color:"""+lst_colors[lst_elements.index(i)]+"""">
     </i>&nbsp;"""+str(i)+"""<br>"""
legend_html = legend_html+"""</div>"""
map_.get_root().html.add_child(folium.Element(legend_html))

map_.save("out5.html")
webbrowser.open(r'C:\Users\Diego\PycharmProjects\pythonProject\out5.html')


# CLUSTERING

# Getting the right K using Elbow method

X = dtf[["Lat1", "Lon1"]]
max_k = 10
## iterations
distortions = []
for i in range(1, max_k+1):
    if len(X) >= i:
       model = cluster.KMeans(n_clusters=i, init='k-means++', max_iter=300, n_init=10, random_state=0)
       model.fit(X)
       distortions.append(model.inertia_)

## best k: the lowest derivative
k = [i*100 for i in np.diff(distortions,2)].index(min([i*100 for i
     in np.diff(distortions,2)]))

## plot
fig, ax = plt.subplots()
ax.plot(range(1, len(distortions)+1), distortions)
ax.axvline(k, ls='--', color="red", label="k = "+str(k))
ax.set(title='The Elbow Method', xlabel='Number of clusters',
       ylabel="Distortion")
ax.legend()
ax.grid(True)
plt.show()

# We can try with k = 5 so that the K-Means algorithm will find 5 theoretical centroids. In addition,
# I will identify the real centroids too (the closest observation to the cluster center).

k = 5
model = cluster.KMeans(n_clusters=k, init='k-means++')
X = dtf[["Lat1","Lon1"]]

## clustering
dtf_X = X.copy()
dtf_X["cluster"] = model.fit_predict(X)
## find real centroids
closest, distances = scipy.cluster.vq.vq(model.cluster_centers_,
                     dtf_X.drop("cluster", axis=1).values)
dtf_X["centroids"] = 0
for i in closest:
    dtf_X["centroids"].iloc[i] = 1
## add clustering info to the original dataset
dtf[["cluster","centroids"]] = dtf_X[["cluster","centroids"]]
dtf.sample(5)

## plot
fig, ax = plt.subplots()
sns.scatterplot(x="Lat1", y="Lon1", data=dtf,
                palette=sns.color_palette("bright",k),
                hue='cluster', size="centroids", size_order=[1,0],
                legend="brief", ax=ax).set_title('Clustering(k=+str(k)+)')
th_centroids = model.cluster_centers_
ax.scatter(th_centroids[:,0], th_centroids[:,1], s=50, c='black',
           marker="x")

model = cluster.AffinityPropagation()
k = dtf["cluster"].nunique()
sns.scatterplot(x="Lat1", y="Lon1", data=dtf,
                palette=sns.color_palette("bright",k),
                hue='cluster', size="centroids", size_order=[1,0],
                legend="brief").set_title('Clustering k='+str(k))


# X = dtf[["Lat1","Lon1"]]
# map_shape = (4,4)
# ## scale data
# scaler = preprocessing.StandardScaler()
# X_preprocessed = scaler.fit_transform(X.values)
# ## clustering
# model = minisom.MiniSom(x=map_shape[0], y=map_shape[1],
#                         input_len=X.shape[1])
# model.train_batch(X_preprocessed, num_iteration=100, verbose=False)
# ## build output dataframe
# dtf_X = X.copy()
# dtf_X["cluster"] = np.ravel_multi_index(np.array(
#       [model.winner(x) for x in X_preprocessed]).T, dims=map_shape)
# ## find real centroids
# cluster_centers = np.array([vec for center in model.get_weights()
#                             for vec in center])
# closest, distances = scipy.cluster.vq.vq(model.cluster_centers_,
#                                          X_preprocessed)
# dtf_X["centroids"] = 0
# for i in closest:
#     dtf_X["centroids"].iloc[i] = 1
# ## add clustering info to the original dataset
# dtf[["cluster","centroids"]] = dtf_X[["cluster","centroids"]]
# ## plot
# k = dtf["cluster"].nunique()
# fig, ax = plt.subplots()
# sns.scatterplot(x="Lat1", y="Lon1", data=dtf,
#                 palette=sns.color_palette("bright",k),
#                 hue='cluster', size="centroids", size_order=[1,0],
#                 legend="brief", ax=ax).set_title('Clustering (k='+str(k)+')')
# th_centroids = scaler.inverse_transform(cluster_centers)
# ax.scatter(th_centroids[:,0], th_centroids[:,1], s=50, c='black',
#            marker="x")


# Independently from the algorithm you used to cluster the data, now you have a dataset with two
# more columns (“cluster”, “centroids”). We can use that to visualize the clusters on the map,
# and this time I’m going to display the centroids as well using a marker.

x, y = "Lat1", "Lon1"
color = "cluster"
size = "Kg"
popup = "Ruta"
marker = "centroids"
data = dtf.copy()
## create color column
lst_elements = sorted(list(dtf[color].unique()))
lst_colors = ['#%06X' % np.random.randint(0, 0xFFFFFF) for i in
              range(len(lst_elements))]
data["color"] = data[color].apply(lambda x:
                lst_colors[lst_elements.index(x)])
## create size column (scaled)
scaler = preprocessing.MinMaxScaler(feature_range=(3,15))
data["size"] = scaler.fit_transform(
               data[size].values.reshape(-1,1)).reshape(-1)
## initialize the map with the starting location
map_ = folium.Map(location=location, tiles="openstreetmap",
                  zoom_start=11)
## add points
data.apply(lambda row: folium.CircleMarker(
           location=[row[x],row[y]], popup=row[popup],
           color=row["color"], fill=True,
           radius=row["size"]).add_to(map_), axis=1)
## add html legend
legend_html = """<div style="position:fixed; bottom:10px; left:10px; border:2px solid black;
                z-index:9999; font-size:14px;">&nbsp;<b>"""+color+""":</b><br>"""
for i in lst_elements:
     legend_html = legend_html+"""&nbsp;<i class="fa fa-circle 
     fa-1x" style="color:"""+lst_colors[lst_elements.index(i)]+"""">
     </i>&nbsp;"""+str(i)+"""<br>"""
legend_html = legend_html+"""</div>"""
map_.get_root().html.add_child(folium.Element(legend_html))
## add centroids marker
lst_elements = sorted(list(dtf[marker].unique()))
data[data[marker]==1].apply(lambda row:
           folium.Marker(location=[row[x],row[y]],
           popup=row[marker], draggable=False,
           icon=folium.Icon(color="black")).add_to(map_), axis=1)
## plot the map
map_.save("map_mal_2022_5k.html")
webbrowser.open(r'C:\Users\Diego\PycharmProjects\pythonProject\map_mal_2022_5k.html')
