A Python + Streamlit-based Travel Planner that helps users find the cheapest and fastest travel routes between multiple cities across India.
The app intelligently compares trains, buses, and flights, visualizes routes on an interactive map, and generates a detailed itinerary with cost and duration insights.

🚀 Features
🗺️ Interactive Route Map using Folium
💰 Cheapest Route Finder (multi-city support)
⏱️ Smart Duration Calculation
📄 Detailed Itinerary Generation
📊 Excel Export for Routes
⚙️ Geopy-based distance and time estimation
🧩 Tech Stack

Frontend/UI: Streamlit
Backend Logic: Python
Mapping: Folium + Streamlit-Folium
Data Handling: Pandas, NumPy
Geo Calculations: Geopy
Output: Excel via OpenPyXL

🛠️ Setup Instructions
1️⃣ Clone this repository
git clone https://github.com/<your-username>/<your-repo-name>.git
cd <your-repo-name>

2️⃣ Create and activate a virtual environment
python -m venv travelenv
travelenv\Scripts\activate   # (Windows)
# or
source travelenv/bin/activate  # (Mac/Linux)

3️⃣ Install dependencies
pip install -r requirements.txt

4️⃣ Run the app
streamlit run app.py

📍 Example Usage

Enter your starting city, destination, and choose to explore multiple possible routes.

Calculates the best paths
Shows you total cost & time
Displays a beautiful map preview
Generates a structured travel itinerary

## 🖼️ App Screenshots

The system automatically:<img width="1920" height="927" alt="Screenshot 2025-11-03 125428" src="https://github.com/user-attachments/assets/a612c6ce-388f-48ef-944d-2fb515b62dfa" />

📍 Routes

<img width="1906" height="920" alt="new" src="https://github.com/user-attachments/assets/da9a31f0-1dc4-46e9-8160-f41b342e789d" />
