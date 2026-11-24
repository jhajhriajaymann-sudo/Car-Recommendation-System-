import streamlit as st
import pandas as pd
from sklearn.preprocessing import MinMaxScaler
from sklearn.metrics.pairwise import cosine_similarity

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="AI Car Recommendation System",
    page_icon="🚗",
    layout="wide"
)

# ---------------- CUSTOM CSS ----------------
st.markdown("""
<style>
.main {
    background: linear-gradient(135deg, #0f172a, #111827);
    color: white;
}
.stApp {
    background: linear-gradient(135deg, #0f172a, #111827);
}
h1, h2, h3 {
    color: #00ff99;
}
.card {
    background: #1e293b;
    padding: 20px;
    border-radius: 18px;
    margin-bottom: 18px;
    box-shadow: 0px 0px 12px rgba(0,255,153,0.4);
    transition: transform 0.2s ease-in-out;
}
.card:hover {
    transform: translateY(-5px);
    box-shadow: 0px 5px 15px rgba(0,255,153,0.6);
}
.small-text {
    color: #d1d5db;
    font-size: 15px;
}
.score-badge {
    background-color: #00ff99;
    color: #0f172a;
    padding: 4px 8px;
    border-radius: 12px;
    font-weight: bold;
    font-size: 12px;
    float: right;
}
</style>
""", unsafe_allow_html=True)

# ---------------- LOAD DATA & MODEL PIPELINE ----------------
@st.cache_data
def load_data():
    try:
        df = pd.read_csv("cars.csv")
    except FileNotFoundError:
        st.error("Error: cars.csv not found. Please ensure the file is in the same directory.")
        return pd.DataFrame()
    return df

@st.cache_data
def prepare_model_features(df):
    if df.empty:
        return df, None
    
    # Feature Engineering for Content-Based Filtering
    # One-hot encode categorical features
    df_encoded = pd.get_dummies(df, columns=["type", "fuel", "transmission"])
    
    # Normalize numerical features
    scaler = MinMaxScaler()
    num_cols = ["price", "mileage", "seats"]
    if all(col in df_encoded.columns for col in num_cols):
        df_encoded[num_cols] = scaler.fit_transform(df_encoded[num_cols])
        
    return df_encoded

df = load_data()
if not df.empty:
    df_features = prepare_model_features(df)

# ---------------- HEADER ----------------
st.markdown("<h1 style='text-align:center;'>🚗 AI Car Recommendation System</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align:center;' class='small-text'>Smart AI recommendations powered by Content-Based Filtering</p>", unsafe_allow_html=True)
st.write("")

if not df.empty:
    # ---------------- SIDEBAR FILTERS ----------------
    st.sidebar.header("🔍 Select Preferences")

    budget = st.sidebar.slider(
        "Maximum Budget (₹)",
        min_value=int(df["price"].min()),
        max_value=int(df["price"].max()),
        value=1500000,
        step=50000
    )

    car_type = st.sidebar.selectbox(
        "Car Type",
        ["All"] + list(df["type"].dropna().unique())
    )

    fuel = st.sidebar.selectbox(
        "Fuel Type",
        ["All"] + list(df["fuel"].dropna().unique())
    )

    transmission = st.sidebar.selectbox(
        "Transmission",
        ["All"] + list(df["transmission"].dropna().unique())
    )

    min_mileage = st.sidebar.slider(
        "Minimum Mileage (kmpl)",
        int(df["mileage"].min()), int(df["mileage"].max()), 15
    )
    
    st.sidebar.markdown("---")
    st.sidebar.header("🤖 AI Recommendation Model")
    reference_car = st.sidebar.selectbox(
        "Find similar cars to (Optional):",
        ["None"] + list(df["name"].unique()),
        help="Select a reference car to activate AI-based similarity matching (Cosine Similarity)."
    )

    # ---------------- FILTER LOGIC ----------------
    filtered = df.copy()

    # Apply Hard Filters
    filtered = filtered[filtered["price"] <= budget]

    if car_type != "All":
        filtered = filtered[filtered["type"] == car_type]

    if fuel != "All":
        filtered = filtered[filtered["fuel"] == fuel]

    if transmission != "All":
        filtered = filtered[filtered["transmission"] == transmission]

    filtered = filtered[filtered["mileage"] >= min_mileage]

    # ---------------- AI SCORING LOGIC ----------------
    if not filtered.empty:
        if reference_car != "None":
            # Item-based collaborative filtering (Content-Based) using Cosine Similarity
            target_idx = df.index[df['name'] == reference_car].tolist()[0]
            target_features = df_features.iloc[target_idx].drop('name').values.reshape(1, -1)
            
            filtered_indices = filtered.index
            filtered_features = df_features.iloc[filtered_indices].drop('name').values
            
            # Calculate Similarity
            similarities = cosine_similarity(target_features, filtered_features)[0]
            filtered['similarity_score'] = similarities
            filtered = filtered.sort_values(by='similarity_score', ascending=False)
            scoring_method = "Similarity Score"
        else:
            # Simple Utility Scoring (Value for money & mileage efficiency)
            # Higher mileage and lower price (relative to budget) gives a better score
            price_score = 1 - (filtered['price'] / budget)
            mileage_score = filtered['mileage'] / df['mileage'].max()
            filtered['utility_score'] = (price_score * 0.5) + (mileage_score * 0.5)
            filtered['utility_score'] = filtered['utility_score'].apply(lambda x: min(x, 1.0)) # cap at 1.0
            filtered = filtered.sort_values(by='utility_score', ascending=False)
            scoring_method = "Match Score"

    # ---------------- OUTPUT ----------------
    if reference_car != "None":
        st.subheader(f"🚘 Recommended Cars (Similar to {reference_car})")
    else:
        st.subheader("🚘 Recommended Cars (Best Match)")

    if filtered.empty:
        st.warning("No matching cars found. Try expanding your budget or changing filters.")
    else:
        col1, col2 = st.columns(2)

        # To keep track of column placement
        for i, (idx, row) in enumerate(filtered.iterrows()):
            
            if reference_car != "None":
                score = f"{row['similarity_score'] * 100:.1f}% Match"
            else:
                score = f"{row['utility_score'] * 100:.1f}% Match"

            card_html = f"""
            <div class='card'>
                <span class='score-badge'>{score}</span>
                <h3>{row['name']}</h3>
                <p class='small-text'>
                💰 Price: ₹{row['price']:,.0f}<br>
                ⛽ Fuel: {row['fuel']}<br>
                ⚙️ Transmission: {row['transmission']}<br>
                🛣 Mileage: {row['mileage']} kmpl<br>
                🚗 Type: {row['type']}<br>
                👨‍👩‍👧 Seats: {row['seats']}
                </p>
            </div>
            """

            if i % 2 == 0:
                col1.markdown(card_html, unsafe_allow_html=True)
            else:
                col2.markdown(card_html, unsafe_allow_html=True)

# ---------------- FOOTER ----------------
st.write("")
st.markdown("<br><p style='text-align:center;' class='small-text'>Developed by Jaymann Jhajhria | Minor Project 2026<br>Uses Content-Based Recommendation AI Pipeline</p>", unsafe_allow_html=True)
