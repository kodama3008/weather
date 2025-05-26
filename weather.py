## pip　インストール
# !pip install osmnx folium
# !pip uninstall osmnx
# !pip install "osmnx==1.9.4"

import os
from pathlib import Path
import folium
import osmnx as ox
import pandas as pd

query = "Nakamuraku,Nagoya,Aichi,Japan"
outdir = Path(query.replace(",", "_"))
outdir.mkdir(exist_ok=True)

# 1. ネットワーク取得
G = ox.graph_from_place(query, network_type="drive")

# 2. Folium で可視化
fmap = ox.plot_graph_folium(G)

# 3. 最短経路
start_pt = (35.18253738854321, 136.85996828365532)  # (lat, lon)
end_pt   = (35.16163249834248, 136.8824509819242)
start_nd = ox.distance.nearest_nodes(G, X=start_pt[1], Y=start_pt[0])
end_nd   = ox.distance.nearest_nodes(G, X=end_pt[1],   Y=end_pt[0])
route    = ox.shortest_path(G, start_nd, end_nd)

# 4. 経路を赤で描画
fmap = ox.plot_route_folium(G, route, route_map=fmap, color="red")
folium.Marker(location=start_pt, tooltip="start").add_to(fmap)
folium.Marker(location=end_pt,   tooltip="end").add_to(fmap)
fmap.save(outdir / "shortest_path.html")

# 5. 最短経路をcsvで格納
route_coords = [(G.nodes[n]['y'], G.nodes[n]['x']) for n in shortest_path]
df_route = pd.DataFrame(route_coords, columns=['latitude', 'longitude'])
df_route.to_csv(outdir_path / "shortest_path_nodes.csv", index=False)
