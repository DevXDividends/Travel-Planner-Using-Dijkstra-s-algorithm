<div align="center">

```
████████╗██████╗  █████╗ ██╗   ██╗███████╗██╗
╚══██╔══╝██╔══██╗██╔══██╗██║   ██║██╔════╝██║
   ██║   ██████╔╝███████║██║   ██║█████╗  ██║
   ██║   ██╔══██╗██╔══██║╚██╗ ██╔╝██╔══╝  ██║
   ██║   ██║  ██║██║  ██║ ╚████╔╝ ███████╗███████╗
   ╚═╝   ╚═╝  ╚═╝╚═╝  ╚═╝  ╚═══╝  ╚══════╝╚══════╝
                P L A N N E R  —  I N D I A
```

**Find the cheapest, fastest route between any cities in India — trains, buses & flights, all in one place.**

![Python](https://img.shields.io/badge/Python-3776AB?style=flat-square&logo=python&logoColor=white)
![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=flat-square&logo=streamlit&logoColor=white)
![Folium](https://img.shields.io/badge/Folium-77B829?style=flat-square&logo=leaflet&logoColor=white)
![Pandas](https://img.shields.io/badge/Pandas-150458?style=flat-square&logo=pandas&logoColor=white)
![Geopy](https://img.shields.io/badge/Geopy-00BFFF?style=flat-square&logo=googlemaps&logoColor=white)

</div>

---

## 🗺️ What Is This?

**Travel Planner India** is a Streamlit web app that takes the hassle out of planning multi-city trips across India. Enter your cities, and the app compares all available travel modes — 🚂 trains, 🚌 buses, and ✈️ flights — then recommends the best route based on cost or time, visualizes it on a live map, and exports a full itinerary to Excel.

---

## ✨ Features

| Feature | Details |
|---|---|
| 🗺️ **Interactive Route Map** | Folium-powered map with route visualization |
| 💰 **Cheapest Route Finder** | Multi-city support with cost comparison |
| ⏱️ **Smart Duration Calc** | Geopy-based distance & time estimation |
| 📄 **Itinerary Generator** | Detailed breakdown of each leg of the trip |
| 📊 **Excel Export** | Download full route data via OpenPyXL |
| 🚂🚌✈️ **Multi-mode Comparison** | Trains, buses, and flights side-by-side |

---

## 🖼️ Screenshots

### Route Overview
<img width="1920" alt="App Overview" src="https://github.com/user-attachments/assets/a612c6ce-388f-48ef-944d-2fb515b62dfa" />

### Interactive Map & Routes
<img width="1906" alt="Route Map" src="https://github.com/user-attachments/assets/da9a31f0-1dc4-46e9-8160-f41b342e789d" />

---

## 🧩 Tech Stack

| Layer | Technology |
|---|---|
| **UI / Frontend** | Streamlit |
| **Backend Logic** | Python |
| **Mapping** | Folium + Streamlit-Folium |
| **Data Handling** | Pandas, NumPy |
| **Geo Calculations** | Geopy |
| **Export** | OpenPyXL (Excel) |

---

## 🚦 Getting Started

### 1️⃣ Clone the repository

```bash
git clone https://github.com/<your-username>/<your-repo-name>.git
cd <your-repo-name>
```

### 2️⃣ Create & activate a virtual environment

```bash
python -m venv travelenv

# Windows
travelenv\Scripts\activate

# Mac / Linux
source travelenv/bin/activate
```

### 3️⃣ Install dependencies

```bash
pip install -r requirements.txt
```

### 4️⃣ Run the app

```bash
streamlit run app.py
```

> App opens at → `http://localhost:8501`

---
### 5️⃣ Run with Docker

Build the Docker image:

```bash
docker build -t travel-planner .
```

Run the container:

```bash
docker run -p 8501:8501 travel-planner
```

Open the application in your browser:

```text
http://localhost:8501
```

### Docker Notes

- No Python installation required on the host machine.
- No virtual environment setup required.
- All dependencies are installed inside the container.
- The application runs in an isolated and reproducible environment.


## 📍 How to Use

```
Step 1 — Enter your starting city and destination(s)
Step 2 — Choose travel mode preference (cheapest / fastest)
Step 3 — View all route options with cost & duration
Step 4 — Explore the interactive map preview
Step 5 — Download your full itinerary as Excel
```

---

## 🗂️ Project Structure

```
travel-planner/
│
├── app.py                  # Main Streamlit app entry point
├── requirements.txt        # All dependencies
│
├── utils/
│   ├── route_finder.py     # Core routing & comparison logic
│   ├── geo_utils.py        # Geopy distance & time estimation
│   └── map_builder.py      # Folium map generation
│
└── output/
    └── itinerary.xlsx      # Generated on export
```

---

## 📦 Requirements

```
streamlit
folium
streamlit-folium
pandas
numpy
geopy
openpyxl
```

> Install all at once: `pip install -r requirements.txt`

---

<div align="center">

Built with 🗺️ and ☕ for every Indian traveller on a budget.

*Drop a ⭐ if this saved you from a 14-hour bus when there was a 2-hour train.*

</div>
