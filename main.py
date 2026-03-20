import streamlit as st
from api import get_current_weather, get_forecast
from storage import load_history, save_to_history, clear_history
from datetime import datetime

st.set_page_config(page_title="Weather Dashboard", page_icon="🌤️", layout="centered")

st.title("🌤️ Weather Dashboard")
st.markdown("Get real-time weather and 5-day forecast for any city.")

city_input = st.text_input("Enter city name", placeholder="e.g. Mumbai, London, Tokyo")

col1, col2 = st.columns([2, 1])
with col1:
    search_btn = st.button("Get Weather", use_container_width=True)
with col2:
    unit = st.selectbox("Unit", ["°C", "°F"], label_visibility="collapsed")

if search_btn and city_input:
    with st.spinner("Fetching weather data..."):
        weather = get_current_weather(city_input)
        forecast = get_forecast(city_input)

    if weather == "connection_error":
        st.error("No internet connection. Please check your network.")
    elif weather is None:
        st.error(f"City '{city_input}' not found. Please check the spelling.")
    else:
        temp = weather["temp"]
        feels = weather["feels_like"]
        if unit == "°F":
            temp = round((temp * 9/5) + 32, 1)
            feels = round((feels * 9/5) + 32, 1)

        save_to_history(city_input, weather)

        if weather["temp"] >= 40:
            st.warning(f"🔥 Extreme heat alert! Temperature is {weather['temp']}°C")
        elif weather["temp"] <= 5:
            st.warning(f"🥶 Cold alert! Temperature is {weather['temp']}°C")
        if "rain" in weather["description"].lower():
            st.info("🌧️ Rain expected — carry an umbrella!")

        st.subheader(f"{weather['city']}, {weather['country']}")
        st.caption(f"Last updated: {datetime.now().strftime('%d %b %Y, %I:%M %p')}")

        m1, m2, m3, m4 = st.columns(4)
        m1.metric("Temperature", f"{temp}{unit}")
        m2.metric("Feels Like", f"{feels}{unit}")
        m3.metric("Humidity", f"{weather['humidity']}%")
        m4.metric("Wind Speed", f"{weather['wind_speed']} m/s")

        st.markdown(f"**Condition:** {weather['description']}")

        if forecast and forecast != "connection_error":
            st.subheader("5-Day Forecast")
            cols = st.columns(len(forecast))
            for i, day in enumerate(forecast):
                date_label = datetime.strptime(day["date"], "%Y-%m-%d").strftime("%a, %d %b")
                min_t = day["min_temp"]
                max_t = day["max_temp"]
                if unit == "°F":
                    min_t = round((min_t * 9/5) + 32, 1)
                    max_t = round((max_t * 9/5) + 32, 1)
                with cols[i]:
                    st.markdown(f"**{date_label}**")
                    st.markdown(f"↑ {max_t}{unit}")
                    st.markdown(f"↓ {min_t}{unit}")
                    st.caption(day["description"])

            st.subheader("Temperature Trend")
            import pandas as pd
            df = pd.DataFrame({
                "Date": [d["date"] for d in forecast],
                "Max Temp": [d["max_temp"] for d in forecast],
                "Min Temp": [d["min_temp"] for d in forecast],
            }).set_index("Date")
            st.line_chart(df)

st.divider()
st.subheader("Recent Searches")
history = load_history()
if history:
    for entry in reversed(history):
        st.markdown(f"🕐 **{entry['city']}** — {entry['temp']}°C, {entry['description']} *(searched {entry['timestamp']})*")
    if st.button("Clear History"):
        clear_history()
        st.rerun()
else:
    st.caption("No searches yet. Search a city above to get started.")