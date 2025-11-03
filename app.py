
import streamlit as st
import json
import heapq
import pandas as pd
import logging
from datetime import datetime
import itertools

# Optional map support
try:
    import folium
    from streamlit_folium import folium_static
    MAP_AVAILABLE = True
except ImportError:
    MAP_AVAILABLE = False

# Setup logging
logging.basicConfig(filename="travel_planner.log", level=logging.INFO,
                    format="%(asctime)s - %(levelname)s - %(message)s")
logging.info("Travel Planner started")

# Static attractions data
ATTRACTIONS = {
    "Mumbai": [{"name": "Gateway of India", "duration": 90, "description": "Iconic monument by the sea.", "category": "Landmark", "cost": 0, "rating": 4.7}],
    "Delhi": [{"name": "India Gate", "duration": 90, "description": "Iconic war memorial.", "category": "Landmark", "cost": 0, "rating": 4.6}],
    "Ahmedabad": [{"name": "Sabarmati Ashram", "duration": 120, "description": "Historic site of Gandhi's residence.", "category": "Historical", "cost": 0, "rating": 4.6}],
}

# -----------------------------
# Load graph from JSON
# -----------------------------
@st.cache_data
def load_graph(json_file="cities.json"):
    try:
        with open(json_file, "r") as f:
            graph = json.load(f)
        # Make graph undirected
        undirected_graph = graph.copy()
        valid_modes = {"train", "bus", "plane"}
        for city1 in graph:
            for city2 in graph[city1]:
                if city2 not in ["lat", "lon"]:
                    edge_data = graph[city1][city2]
                    if not isinstance(edge_data.get("price"), dict) or not isinstance(edge_data.get("duration"), dict):
                        logging.error(f"Invalid data for {city1} to {city2}")
                        continue
                    # Ensure all modes exist
                    for mode in valid_modes:
                        edge_data["price"][mode] = edge_data["price"].get(mode, 0)
                        edge_data["duration"][mode] = edge_data["duration"].get(mode, 0)
                    if city2 not in undirected_graph:
                        undirected_graph[city2] = {}
                    if city1 not in undirected_graph[city2]:
                        undirected_graph[city2][city1] = edge_data
        return undirected_graph
    except FileNotFoundError:
        st.error("cities.json not found!")
        logging.error("cities.json not found")
        return {}
    except json.JSONDecodeError:
        st.error("Invalid JSON format in cities.json")
        logging.error("Invalid JSON format")
        return {}

graph = load_graph()
CITY_KEYS = list(graph.keys())

# -----------------------------
# Layover recommendations
# -----------------------------
def get_layover_recommendations(city, layover_duration, min_layover, max_layover, preferred_category, max_budget):
    recommendations = []
    if city in ATTRACTIONS:
        for attraction in ATTRACTIONS[city]:
            if (min_layover <= layover_duration <= max_layover and
                attraction["duration"] <= layover_duration and
                (preferred_category == "All" or attraction["category"] == preferred_category) and
                attraction["cost"] <= max_budget):
                recommendations.append({
                    "name": attraction["name"],
                    "description": f"{attraction['description']} (Est. {attraction['duration']} min, Cost: ₹{attraction['cost']}, Rating: {attraction['rating']}/5)"
                })
    if not recommendations:
        recommendations.append({"name": "None", "description": "No suitable attractions for your preferences."})
    return recommendations

# -----------------------------
# Folium map
# -----------------------------
def create_map(path):
    if not MAP_AVAILABLE:
        return None
    m = folium.Map(location=[20.5937, 78.9629], zoom_start=5, tiles="CartoDB Voyager")
    for city in path:
        if city in graph and "lat" in graph[city] and "lon" in graph[city]:
            folium.Marker([graph[city]["lat"], graph[city]["lon"]], popup=city, icon=folium.Icon(color="blue")).add_to(m)
    for i in range(len(path)-1):
        if path[i] in graph and path[i+1] in graph:
            start = (graph[path[i]]["lat"], graph[path[i]]["lon"])
            end = (graph[path[i+1]]["lat"], graph[path[i+1]]["lon"])
            folium.PolyLine([start, end], color="blue", weight=2.5, opacity=1).add_to(m)
    return m

# -----------------------------
# Modified Dijkstra
# -----------------------------
def modified_dijkstra(graph, start, end, objective, k=4, min_layover=60, max_layover=720, preferred_category="All", max_budget=1000):
    valid_modes = ["bus", "train", "plane"]
    modes = [objective.lower()] if objective.lower() in valid_modes else valid_modes
    counter = itertools.count()
    pq = [(0, next(counter), start, [start], [], 0, {start}, 0)]
    found_paths = []
    count = {city:0 for city in graph}

    while pq and len(found_paths) < k:
        priority, _, city, path, path_details, duration, visited, prev_arrival_time = heapq.heappop(pq)
        count[city] +=1
        if count[city] > k*10:
            continue
        if city == end:
            found_paths.append({
                "path": path,
                "total_cost": sum(d["cost"] for d in path_details),
                "total_duration": duration,
                "path_details": path_details
            })
            continue
        for neighbor, data in graph.get(city, {}).items():
            if neighbor in ["lat","lon"] or neighbor in visited:
                continue
            for mode in modes:
                price = data.get("price", {}).get(mode,0)
                time = data.get("duration", {}).get(mode,0)
                if price <=0 or time <=0:
                    continue
                new_duration = duration + time
                new_cost = sum(d["cost"] for d in path_details)+price if path_details else price
                layover_time = new_duration - prev_arrival_time if path_details else 0
                new_path_details = path_details + [{
                    "from": city,
                    "to": neighbor,
                    "mode": mode,
                    "cost": price,
                    "duration": time,
                    "layover_duration": layover_time,
                    "layover_recommendations": get_layover_recommendations(neighbor, layover_time, min_layover, max_layover, preferred_category, max_budget) if city != start else []
                }]
                new_priority = new_cost if objective.lower()=="cheapest" else new_duration
                heapq.heappush(pq,(new_priority,next(counter),neighbor,path+[neighbor],new_path_details,new_duration,visited|{neighbor},new_duration))
    return found_paths

# -----------------------------
# Export itinerary text
# -----------------------------
def export_to_text(result, idx, destination):
    content = [
        f"Travel Planner Itinerary",
        f"Generated on {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
        f"Route {idx+1}: {' → '.join(result['path'])}",
        f"Total Cost: ₹{result['total_cost']}",
        f"Total Duration: {result['total_duration']//60}h {result['total_duration']%60}m",
        "Leg Details:"
    ]
    for detail in result["path_details"]:
        content.append(f"{detail['from']} → {detail['to']} ({detail['mode'].title()}): ₹{detail['cost']}, {detail['duration']//60}h {detail['duration']%60}m")
        if detail.get("layover_recommendations") and detail["layover_recommendations"][0]["name"]!="None":
            content.append(f"Layover in {detail['to']} ({detail['layover_duration']//60}h {detail['layover_duration']%60}m):")
            for rec in detail["layover_recommendations"]:
                content.append(f"  - {rec['name']}: {rec['description']}")
    if destination in ATTRACTIONS:
        content.append("Destination Attractions:")
        for attraction in ATTRACTIONS[destination]:
            content.append(f"  - {attraction['name']}: {attraction['description']} (Cost: ₹{attraction['cost']}, Rating: {attraction['rating']}/5)")
    return "\n".join(content)

# -----------------------------
# Streamlit UI
# -----------------------------
st.set_page_config(page_title="Travel Planner", layout="wide")
st.title("🗺️ Travel Planner")
st.markdown("Plan your journey with interactive maps and tailored recommendations! 🚌✈️🚂")

# -----------------------------
# Sidebar Inputs
# -----------------------------
with st.sidebar:
    st.header("Plan Your Trip")
    source = st.selectbox("Starting City 🌍", CITY_KEYS, index=0)
    destination = st.selectbox("Destination City 🏁", CITY_KEYS, index=1 if len(CITY_KEYS)>1 else 0)
    min_layover = st.slider("Minimum Layover (minutes)",30,360,60)
    max_layover = st.slider("Maximum Layover (minutes)",60,1440,720)
    preferred_category = st.selectbox("Preferred Attraction Category", ["All","Landmark","Historical","Cultural"],index=0)
    max_budget = st.number_input("Max Budget per Attraction (₹) 💰", min_value=0, value=1000)
    route_type = st.radio("Route Preference 🚍✈️🚆", ["Bus 🚌", "Plane ✈️", "Train 🚂", "Cheapest 💸", "Fastest ⏩"], index=3)
    num_routes = st.selectbox("Number of Routes 🔢", [1,2,3,4], index=0)

    if st.button("Find Routes 🚀"):
        if source==destination:
            st.warning("Source and Destination cannot be the same! ⚠️")
        else:
            route_type_key = route_type.split()[0].lower()
            all_results = modified_dijkstra(graph, source, destination, route_type_key, k=num_routes,
                                            min_layover=min_layover, max_layover=max_layover,
                                            preferred_category=preferred_category, max_budget=max_budget)
            st.session_state['all_results'] = all_results
            st.session_state['show_results'] = True
            st.session_state['route_type'] = route_type_key

# -----------------------------
# Display Routes
# -----------------------------
if st.session_state.get('show_results', False):
    all_results = st.session_state['all_results']
    route_type = st.session_state['route_type']
    if all_results:
        st.success(f"Found {len(all_results)} {route_type} routes! 🎉")
        for idx,result in enumerate(all_results):
            with st.expander(f"Route {idx+1}: {' → '.join(result['path'])}", expanded=(idx==0)):
                legs = []
                for detail in result["path_details"]:
                    mode_icon = {"bus":"🚌","plane":"✈️","train":"🚂"}.get(detail["mode"].lower(),"")
                    legs.append({
                        "From": detail["from"],
                        "To": detail["to"],
                        "Mode": f"{detail['mode'].title()} {mode_icon}",
                        "Cost (₹)": detail["cost"],
                        "Duration": f"{detail['duration']//60}h {detail['duration']%60}m"
                    })
                    if detail.get("layover_recommendations") and detail["layover_recommendations"][0]["name"]!="None":
                        st.markdown(f"**Layover in {detail['to']} ({detail['layover_duration']//60}h {detail['layover_duration']%60}m):**")
                        for rec in detail["layover_recommendations"]:
                            st.markdown(f"📍 {rec['name']}: {rec['description']}")
                df = pd.DataFrame(legs)
                st.dataframe(df,use_container_width=True)
                if MAP_AVAILABLE:
                    m = create_map(result["path"])
                    if m:
                        st.markdown("**Route Map:** 🗺️")
                        folium_static(m, width=700, height=400)
                text_content = export_to_text(result, idx, destination)
                st.download_button("Download Itinerary 📝", data=text_content,
                                   file_name=f"route_{idx+1}.txt", mime="text/plain")
                st.text_area(f"Itinerary Preview (Route {idx+1})", text_content, height=200)
    else:
        st.error(f"No {route_type} routes found! 😞")
