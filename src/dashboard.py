import streamlit as st
import pandas as pd
import pickle
import matplotlib.pyplot as plt
from pathlib import Path

st.set_page_config(
    page_title="HeatWave Intelligence",
    page_icon="🌡️",
    layout="wide"
)

# Load data and model
df = pd.read_csv("data/processed/weather_clean.csv")
df["timestamp"] = pd.to_datetime(df["timestamp"])

with open("models/heatwave_model.pkl", "rb") as f:
    model = pickle.load(f)

with open("models/features.pkl", "rb") as f:
    features = pickle.load(f)

stations = sorted(df["station"].unique())
seasons = sorted(df["season"].unique())

station_codes = {
    name: i for i, name in enumerate(stations)
}

season_codes = {
    name: i for i, name in enumerate(seasons)
}

locations = (
    df.groupby("station")[["latitude", "longitude"]]
    .first().to_dict("index")
)

labels = {
    0: "NORMAL",
    1: "HEAT ALERT",
    2: "SEVERE HEAT ALERT"
}

# Header
st.title("🌡️ HeatWave Intelligence")
st.subheader("AI-Powered Heatwave Monitoring and Prediction System")

st.info(
    "Academic demonstration using synthetic weather data. "
    "Predictions are not real-world forecasts."
)

# Sidebar
st.sidebar.title("Navigation")

page = st.sidebar.radio(
    "Select Module",
    [
        "Dashboard Overview",
        "Heatwave Prediction",
        "Weather Analytics",
        "Dataset Explorer",
        "Contextual Assistant"
]
)

# Dashboard overview
if page == "Dashboard Overview":

    st.header("System Overview")

    c1, c2, c3 = st.columns(3)

    c1.metric("Total Observations", f"{len(df):,}")
    c2.metric("Weather Stations", df["station"].nunique())
    c3.metric(
        "Average Temperature",
        f"{df['maximum_temperature'].mean():.2f} °C"
    )

    st.divider()

    st.subheader("City-wise Temperature")

    city_avg = df.groupby("station")[
        "maximum_temperature"
    ].mean()

    st.bar_chart(city_avg)

    st.subheader("Monthly Temperature Trend")

    monthly = df.groupby(
        df["timestamp"].dt.month
    )["maximum_temperature"].mean()

    st.line_chart(monthly)

    st.subheader("Heatwave Category Distribution")

    category = df["maximum_temperature"].apply(
        lambda x: (
            "Severe Heat Alert" if x >= 40
            else "Heat Alert" if x >= 35
            else "Normal"
        )
    )

    st.bar_chart(category.value_counts())

# Prediction
elif page == "Heatwave Prediction":

    st.header("AI Heatwave Prediction")

    col1, col2 = st.columns(2)

    with col1:
        city = st.selectbox("Select City", stations)

        temperature = st.number_input(
            "Maximum Temperature (°C)",
            min_value=-20.0,
            max_value=60.0,
            value=38.0
        )

    with col2:
        humidity = st.slider(
            "Humidity (%)",
            0, 100, 50
        )

        season = st.selectbox("Select Season", seasons)

    if st.button("Predict Heatwave Risk", type="primary"):

        location = locations[city]

        input_data = pd.DataFrame([{
            "maximum_temperature": temperature,
            "humidity": humidity,
            "latitude": location["latitude"],
            "longitude": location["longitude"],
            "station_code": station_codes[city],
            "season_code": season_codes[season]
        }])[features]

        prediction = model.predict(input_data)[0]

        probabilities = model.predict_proba(input_data)[0]

        st.divider()

        st.subheader("Prediction Result")

        st.metric(
            "Predicted Status",
            labels[prediction]
        )

        st.metric(
            "Model Confidence",
            f"{max(probabilities)*100:.2f}%"
        )

        st.subheader("Class Probabilities")

        probability_df = pd.DataFrame({
            "Category": [labels[i] for i in range(3)],
            "Probability": probabilities
        }).set_index("Category")

        st.bar_chart(probability_df)

# Weather analytics
elif page == "Weather Analytics":

    st.header("Weather Analytics")

    st.subheader("City-wise Average Temperature")

    city_avg = df.groupby("station")[
        "maximum_temperature"
    ].mean()

    st.bar_chart(city_avg)

    st.subheader("Monthly Temperature Trend")

    monthly = df.groupby(
        df["timestamp"].dt.month
    )["maximum_temperature"].mean()

    st.line_chart(monthly)

    st.subheader("Temperature vs Humidity")

    st.scatter_chart(
        df,
        x="humidity",
        y="maximum_temperature"
    )

    st.subheader("Seasonal Temperature")

    seasonal = df.groupby("season")[
        "maximum_temperature"
    ].mean()

    st.bar_chart(seasonal)

# Dataset explorer
elif page == "Dataset Explorer":

    st.header("Weather Dataset Explorer")

    selected_city = st.selectbox(
        "Filter by City",
        ["All Cities"] + stations
    )

    filtered = df.copy()

    if selected_city != "All Cities":
        filtered = filtered[
            filtered["station"] == selected_city
        ]

    st.write("Total records:", len(filtered))

    st.dataframe(
        filtered,
        use_container_width=True
    )

    st.download_button(
        "Download Dataset CSV",
        filtered.to_csv(index=False),
        "weather_data.csv",
        "text/csv"
    )
    # Contextual Assistant
elif page == "Contextual Assistant":

    import sys
    sys.path.insert(0, "src")

    from contextual_os import ContextualOS

    st.header("Contextual Climate Assistant")
    st.write(
        "An intelligent weather assistant powered by "
        "Context Management, Machine Learning and a local SLM."
    )

    # Create persistent OS instance
    if "contextual_os" not in st.session_state:
        st.session_state.contextual_os = ContextualOS()

    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []

    st.subheader("1. Configure Weather Context")

    col1, col2 = st.columns(2)

    with col1:
        assistant_city = st.selectbox(
            "Select City",
            stations,
            key="assistant_city"
        )

        assistant_temperature = st.number_input(
            "Maximum Temperature (°C)",
            min_value=-20.0,
            max_value=60.0,
            value=38.0,
            key="assistant_temperature"
        )

        assistant_role = st.selectbox(
            "Select User Role",
            [
                "Citizen",
                "Farmer",
                "Outdoor Worker",
                "Health Worker",
                "Local Authority"
            ],
            key="assistant_role"
        )

    with col2:
        assistant_humidity = st.slider(
            "Humidity (%)",
            0, 100, 65,
            key="assistant_humidity"
        )

        assistant_season = st.selectbox(
            "Select Season",
            seasons,
            key="assistant_season"
        )

    # Generate ML prediction
    location = locations[assistant_city]

    assistant_input = pd.DataFrame([{
        "maximum_temperature": assistant_temperature,
        "humidity": assistant_humidity,
        "latitude": location["latitude"],
        "longitude": location["longitude"],
        "station_code": station_codes[assistant_city],
        "season_code": season_codes[assistant_season]
    }])[features]

    assistant_prediction = model.predict(assistant_input)[0]
    assistant_probabilities = model.predict_proba(assistant_input)[0]

    prediction_label = labels[assistant_prediction]

    st.divider()

    st.subheader("2. Current Context")

    c1, c2, c3 = st.columns(3)

    c1.metric("City", assistant_city)
    c2.metric("Temperature", f"{assistant_temperature} °C")
    c3.metric("Humidity", f"{assistant_humidity}%")

    st.metric("Random Forest Prediction", prediction_label)

    st.caption(
        f"Model confidence: "
        f"{max(assistant_probabilities) * 100:.2f}%"
    )

    # Update contextual OS
    os_system = st.session_state.contextual_os

    os_system.set_context(
        city=assistant_city,
        temperature=assistant_temperature,
        humidity=assistant_humidity,
        prediction=prediction_label,
        role=assistant_role
    )

    st.divider()

    st.subheader("3. Ask the Contextual Assistant")

    st.caption(
        f"Active user role: {assistant_role} | "
        f"Active city: {assistant_city}"
    )

    # Display previous conversation
    for message in st.session_state.chat_history:

        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Chat input
    user_question = st.chat_input(
        "Ask about the current heat conditions..."
    )

    if user_question:

        st.session_state.chat_history.append({
            "role": "user",
            "content": user_question
        })

        with st.chat_message("user"):
            st.markdown(user_question)

        with st.chat_message("assistant"):

            with st.spinner("Contextual OS is processing your request..."):

                result = os_system.ask(user_question)

                answer = result["answer"]

                st.markdown(answer)

                st.caption(
                    f"Detected intent: {result['intent']}"
                )

        st.session_state.chat_history.append({
            "role": "assistant",
            "content": answer
        })

    if st.button("Clear Conversation"):
        st.session_state.chat_history = []
        st.rerun()
st.sidebar.divider()

st.sidebar.caption(
    "HeatWave Intelligence | OS Mini Project"
)

st.sidebar.caption(
    "Synthetic demonstration data | 2023–2025"
)
