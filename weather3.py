import os
from pathlib import Path
import folium
import osmnx as ox
import pandas as pd

query = "Nakamuraku,Nagoya,Aichi,Japan"
outdir = Path(query.replace(",", "_"))
outdir.mkdir(exist_ok=True)

# ネットワーク取得
G = ox.graph_from_place(query, network_type="drive")

# Folium地図作成（ベース）
fmap = ox.plot_graph_folium(G)

# 始点・経由点・終点を含む地点リスト（lat, lon）
points = [
    (35.18253738854321, 136.85996828365532),  # 始点
    (35.175, 136.87),                         # 経由点1（例）
    (35.168, 136.875),                        # 経由点2（例）
    (35.16163249834248, 136.8824509819242)   # 終点
]

# 各地点に対応する最寄りノード取得（X=lon, Y=latの順）
nodes = [ox.distance.nearest_nodes(G, X=pt[1], Y=pt[0]) for pt in points]

# 複数区間の経路を連結
full_route = []
for i in range(len(nodes) - 1):
    segment = ox.shortest_path(G, nodes[i], nodes[i+1])
    if i > 0:
        # つなげるときに重複ノードは除く
        segment = segment[1:]
    full_route.extend(segment)

# 経路を赤色で描画
fmap = ox.plot_route_folium(G, full_route, route_map=fmap, color="red")

# 地点マーカー追加（始点・終点は特別表示）
for i, pt in enumerate(points):
    tooltip = "start" if i == 0 else "end" if i == len(points)-1 else f"via {i}"
    folium.Marker(location=pt, tooltip=tooltip).add_to(fmap)

# 結果HTML保存
fmap.save(outdir / "route_with_waypoints.html")

# 経路ノードの座標をCSV保存
route_coords = [(G.nodes[n]['y'], G.nodes[n]['x']) for n in full_route]
df_route = pd.DataFrame(route_coords, columns=['latitude', 'longitude'])
df_route.to_csv(outdir / "route_with_waypoints_nodes.csv", index=False)
