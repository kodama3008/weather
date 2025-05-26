from pathlib import Path
import folium
import osmnx as ox
import pandas as pd

class RoutePlanner:
    def __init__(self, place: str, network_type: str = "drive"):
        self.place = place
        self.network_type = network_type
        self.G = None
        self.nodes = []
        self.route = []
    
    def load_graph(self):
        """指定エリアの道路ネットワークを取得"""
        self.G = ox.graph_from_place(self.place, network_type=self.network_type)
    
    def find_nearest_nodes(self, points: list[tuple[float, float]]):
        """地点リスト(lat, lon)からグラフ上の最寄りノードリストを保存"""
        if self.G is None:
            raise RuntimeError("Graph is not loaded. Call load_graph() first.")
        self.nodes = [ox.distance.nearest_nodes(self.G, X=pt[1], Y=pt[0]) for pt in points]
    
    def calculate_route(self):
        """複数ノードを順に結ぶ最短経路を計算して保存"""
        if not self.nodes:
            raise RuntimeError("Nearest nodes not found. Call find_nearest_nodes() first.")
        full_route = []
        for i in range(len(self.nodes) - 1):
            segment = ox.shortest_path(self.G, self.nodes[i], self.nodes[i+1])
            if i > 0:
                segment = segment[1:]  # 重複ノード削除
            full_route.extend(segment)
        self.route = full_route
    
    def save_route_csv(self, filepath: Path):
        """経路ノードの緯度経度をCSVで保存"""
        if not self.route:
            raise RuntimeError("Route is not calculated. Call calculate_route() first.")
        route_coords = [(self.G.nodes[n]['y'], self.G.nodes[n]['x']) for n in self.route]
        df = pd.DataFrame(route_coords, columns=['latitude', 'longitude'])
        df.to_csv(filepath, index=False)
    
    def plot_route(self, points: list[tuple[float, float]]) -> folium.Map:
        """経路と地点をFolium地図に描画しMapオブジェクトを返す"""
        if not self.route:
            raise RuntimeError("Route is not calculated. Call calculate_route() first.")
        fmap = ox.plot_graph_folium(self.G)
        fmap = ox.plot_route_folium(self.G, self.route, route_map=fmap, color="red")
        for i, pt in enumerate(points):
            tooltip = "start" if i == 0 else "end" if i == len(points)-1 else f"via {i}"
            folium.Marker(location=pt, tooltip=tooltip).add_to(fmap)
        return fmap

from pathlib import Path
from route_planner import RoutePlanner

def main():
    query = "Nakamuraku,Nagoya,Aichi,Japan"
    points = [
        (35.18253738854321, 136.85996828365532),  # 始点
        (35.175, 136.87),                         # 経由点1
        (35.168, 136.875),                        # 経由点2
        (35.16163249834248, 136.8824509819242)   # 終点
    ]
    outdir = Path(query.replace(",", "_"))
    outdir.mkdir(exist_ok=True)

    planner = RoutePlanner(query)
    planner.load_graph()
    planner.find_nearest_nodes(points)
    planner.calculate_route()
    planner.save_route_csv(outdir / "route_with_waypoints_nodes.csv")
    fmap = planner.plot_route(points)
    fmap.save(outdir / "route_with_waypoints.html")

if __name__ == "__main__":
    main()