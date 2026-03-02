import pandas as pd
import requests
import folium
from urllib.parse import quote

# ==============================
# 🔐 YOUR MAPBOX INFO (Already Added)
# ==============================

access_token = "pk.eyJ1Ijoia2F0aWVjYXZhbmFnaCIsImEiOiJjbWx0cW9qY2gwMzgwM2ZxM2hxMzA1dnQ2In0.oYohDpcqD8iM12wy2oH-IQ"
username = "katiecavanagh"
style_id = "cmm3qosk3004c01s23nsbeang"

# Mapbox custom tile URL
tiles = f"https://api.mapbox.com/styles/v1/{username}/{style_id}/tiles/256/{{z}}/{{x}}/{{y}}@2x?access_token={access_token}"

# ==============================
# 📍 READ CSV FILE
# ==============================

df = pd.read_csv("hometowns.csv")

# ==============================
# 🌎 FUNCTION TO GEOCODE ADDRESS
# ==============================

def geocode_address(address):
    encoded_address = quote(address)
    geocode_url = f"https://api.mapbox.com/search/geocode/v6/forward?q={encoded_address}&access_token={access_token}"

    response = requests.get(geocode_url)
    data = response.json()

    if data.get("features"):
        coordinates = data["features"][0]["geometry"]["coordinates"]
        return coordinates[1], coordinates[0]  # return lat, lon
    else:
        return None, None

# ==============================
# 🎨 ICON COLORS BY LOCATION TYPE
# ==============================

icon_colors = {
    "restaurant": "red",
    "park": "green",
    "school": "purple",
    "place of worship": "blue",
    "fitness center": "orange",
    "supermarket": "darkgreen",
    "coffee shop": "cadetblue",
    "country club": "darkpurple",
    "bar and grill": "darkred",
    "default": "gray"
}

# ==============================
# 🗺 CREATE BASE MAP
# ==============================

# Temporary center (Edina/Minneapolis area — change if needed)
m = folium.Map(location=[44.9, -93.3], zoom_start=11, tiles=None)

folium.TileLayer(
    tiles=tiles,
    attr="Mapbox",
    name="Katie's Custom Map"
).add_to(m)

# ==============================
# ➕ ADD MARKERS
# ==============================

for index, row in df.iterrows():
    lat, lon = geocode_address(row["address"])

    if lat and lon:
        location_type = row["type"].lower()
        color = "darkred"

        popup_html = f"""
        <h4>{row['name']}</h4>
        <p>{row['description']}</p>
        <img src="{row['image_url']}" width="200">
        """

        folium.Marker(
            location=[lat, lon],
            popup=folium.Popup(popup_html, max_width=300),
            icon=folium.Icon(color=color, icon="info-sign")
        ).add_to(m)

        print(f"✅ Added: {row['name']}")
    else:
        print(f"❌ Could not geocode: {row['name']}")

# ==============================
# 💾 SAVE MAP
# ==============================

m.save("my_hometown_map.html")

print("🎉 Map saved as my_hometown_map.html")