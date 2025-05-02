import streamlit as st
import pandas as pd
import pydeck as pdk
import matplotlib.pyplot as plt

st.set_page_config(layout="wide")
st.title("NYC Traffic Collision Heatmap with Analysis")

@st.cache_data
def load_data():
    df = pd.read_csv("cleaned_crash_data.csv")
    df.columns = df.columns.str.strip()
    df = df.dropna(subset=["LATITUDE", "LONGITUDE"])
    return df

df = load_data()

boroughs = ["All"] + sorted(df['BOROUGH'].dropna().unique().tolist())
selected = st.selectbox("Select a Borough to Analyze:", boroughs)
filtered = df if selected == "All" else df[df['BOROUGH'] == selected]

hex_layer = pdk.Layer(
    "HexagonLayer",
    data=filtered,
    get_position='[LONGITUDE, LATITUDE]',
    auto_highlight=True,
    pickable=True,
    radius=300,
    coverage=1,
)

view = pdk.ViewState(
    latitude=40.7128,
    longitude=-74.0060,
    zoom=10.5,
    pitch=0,
)

deck = pdk.Deck(
    layers=[hex_layer],
    initial_view_state=view,
    map_style="mapbox://styles/mapbox/light-v10",
    tooltip={"html": "<b>Collisions:</b> {elevationValue}"}
)

st.pydeck_chart(deck, use_container_width=True, height=600)

st.subheader(f"Accident Cause Analysis in {selected}")
cause_counts = filtered['CATEGORY_CAUSE'].value_counts()
top = cause_counts.nlargest(5)
rest = cause_counts.iloc[5:].sum()
if rest > 0:
    top["Other"] = rest

col1, col2 = st.columns(2)

with col1:
    st.markdown("### Cause Proportion")
    fig1, ax1 = plt.subplots()
    wedges, texts, autotexts = ax1.pie(
        top,
        labels=None,  
        autopct=lambda pct: f'{pct:.1f}%' if pct > 3 else '',
        startangle=90
    )
    ax1.axis('equal')
    ax1.legend(wedges, top.index, title="Accident Cause", loc="center left", bbox_to_anchor=(1, 0.5))
    st.pyplot(fig1)

with col2:
    st.markdown("### Cause Counts")
    fig2, ax2 = plt.subplots()
    bars = ax2.bar(cause_counts.index, cause_counts.values)
    plt.xticks(rotation=45, ha="right")
    for bar in bars:
        h = bar.get_height()
        ax2.annotate(f'{h}', xy=(bar.get_x() + bar.get_width() / 2, h),
                     xytext=(0, 3), textcoords="offset points",
                     ha='center', va='bottom', fontsize=8)
    st.pyplot(fig2)

st.markdown(f"### Fatality Summary in {selected}")

pedestrian_killed = filtered['NUMBER OF PEDESTRIANS KILLED'].sum()
cyclist_killed = filtered['NUMBER OF CYCLIST KILLED'].sum()
motorist_killed = filtered['NUMBER OF MOTORIST KILLED'].sum()

death_df = pd.DataFrame({
    'Type': ['Pedestrians', 'Cyclists', 'Motorists'],
    'Count': [pedestrian_killed, cyclist_killed, motorist_killed]
})


pedestrian_killed = filtered['NUMBER OF PEDESTRIANS KILLED'].sum()
cyclist_killed = filtered['NUMBER OF CYCLIST KILLED'].sum()
motorist_killed = filtered['NUMBER OF MOTORIST KILLED'].sum()

death_counts = pd.Series({
    'Pedestrians': pedestrian_killed,
    'Cyclists': cyclist_killed,
    'Motorists': motorist_killed
})

col3, col4 = st.columns(2)

with col3:
    st.markdown("### Death Proportion")
    fig3, ax3 = plt.subplots()
    wedges, texts, autotexts = ax3.pie(
        death_counts,
        labels=death_counts.index,
        autopct='%1.1f%%',
        startangle=90
    )
    ax3.axis('equal')
    ax3.legend(wedges, death_counts.index, title="Victim Type", loc="center left", bbox_to_anchor=(1, 0.5))
    st.pyplot(fig3)

with col4:
    st.markdown("### Death Counts")
    fig4, ax4 = plt.subplots()
    bars = ax4.bar(death_counts.index, death_counts.values)
    plt.xticks(rotation=0)
    for bar in bars:
        h = bar.get_height()
        ax4.annotate(f'{int(h)}', xy=(bar.get_x() + bar.get_width() / 2, h),
                     xytext=(0, 3), textcoords="offset points",
                     ha='center', va='bottom', fontsize=8)
    st.pyplot(fig4)
