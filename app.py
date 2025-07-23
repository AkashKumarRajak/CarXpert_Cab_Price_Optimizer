import streamlit as st
from fetch_data import fetch_data
from analytics import analyze_data
import pandas as pd
import altair as alt

st.set_page_config(page_title="CarXpert - Cab Price Optimizer", layout="wide")
st.title("CarXpert - Cab Price Optimizer Dashboard")

# Input: city name
city = st.text_input("Enter city name (e.g. Delhi, Mumbai, Bangalore, Chennai, Kolkata):")

# Availability filter
availability_filter = st.selectbox(
    "Filter by availability",
    options=["All", "Available", "Unavailable"],
    index=0
)

if city:
    data = fetch_data()

    # Filter for the selected city
    city_data = [d for d in data if d['city'].lower() == city.lower()]

    if not city_data:
        st.warning(f"No cab data available for city: {city}")
    else:
        # Apply availability filter
        if availability_filter != "All":
            city_data = [d for d in city_data if d['availability'].lower() == availability_filter.lower()]

        if not city_data:
            st.info(f"No cabs found with availability '{availability_filter}' in {city}")
        else:
            df = pd.DataFrame(city_data)
            st.subheader(f"Cab Options in {city} (Availability: {availability_filter})")
            st.dataframe(df)

            col1, col2 = st.columns(2)

            # Bar Chart: Fare Comparison
            with col1:
                st.markdown("### Fare Comparison")
                fare_chart = alt.Chart(df).mark_bar().encode(
                    x=alt.X('service:N', title='Cab Service'),
                    y=alt.Y('fare:Q', title='Fare (₹)'),
                    color='service:N',
                    tooltip=['service', 'fare', 'estimated_time_min', 'availability']
                ).properties(height=400)
                st.altair_chart(fare_chart, use_container_width=True)

            # Bar Chart: ETA Comparison
            with col2:
                st.markdown("### ETA Comparison")
                eta_chart = alt.Chart(df).mark_bar().encode(
                    x=alt.X('service:N', title='Cab Service'),
                    y=alt.Y('estimated_time_min:Q', title='ETA (minutes)'),
                    color='service:N',
                    tooltip=['service', 'fare', 'estimated_time_min', 'availability']
                ).properties(height=400)
                st.altair_chart(eta_chart, use_container_width=True)

            # Pie Chart: Availability Overview
            st.markdown("### Cab Availability")
            pie_df = df['availability'].value_counts().reset_index()
            pie_df.columns = ['availability', 'count']
            pie_chart = alt.Chart(pie_df).mark_arc(innerRadius=50).encode(
                theta=alt.Theta(field="count", type="quantitative"),
                color=alt.Color(field="availability", type="nominal"),
                tooltip=['availability', 'count']
            ).properties(height=400)
            st.altair_chart(pie_chart, use_container_width=True)

            # Best Overall Fare Option
            analysis = analyze_data(data, city=city)

            best = analysis.get('best_fare_option')
            best_car_cab = analysis.get("best_car_cab_fare_option")
            best_bike_cab = analysis.get("best_bike_cab_fare_option")
            best_auto_cab = analysis.get("best_auto_fare_option")

            if best:
                st.markdown("### Best Overall Fare Option")
                st.success(f"""
                - **Service:** {best['service']}
                - **Fare:** ₹{best['fare']}
                - **ETA:** {best['estimated_time_min']} min
                - **Availability:** {best['availability']}
                """)

            # Best Car Cab Fare
            if best_car_cab:
                st.markdown("### Best Car Cab Fare")
                st.info(f"{best_car_cab['service']} - ₹{best_car_cab['fare']} | ETA: {best_car_cab['estimated_time_min']} min")
                
            # Best Auto Cab Fare
            if best_auto_cab:
                st.markdown("### Best Auto Cab Fare")
                st.info(f"{best_auto_cab['service']} - ₹{best_auto_cab['fare']} | ETA: {best_auto_cab['estimated_time_min']} min")
                
            # Best Bike Cab Fare
            if best_bike_cab:
                st.markdown("### Best Bike Cab Fare")
                st.info(f"{best_bike_cab['service']} - ₹{best_bike_cab['fare']} | ETA: {best_bike_cab['estimated_time_min']} min")
            
            # Divider line
            st.markdown(
    """
    <style>
    /* Add bottom padding so page content doesn't hide behind footer */
    .appview-container {
        padding-bottom: 60px;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

st.markdown(
    """
    <style>
    .footer {
        position: fixed;
        left: 0;
        bottom: 0;
        width: 100%;
        background-color: transparent;
        color: grey;
        text-align: center;
        font-size: 14px;
        padding: 10px 0;
        z-index: 1000;
    }
    </style>
    <div class="footer">
        <hr style="margin-bottom: 8px; border-color: #ddd;" />
        © 2025 Akash Kumar Rajak. All Rights Reserved. Created by Akash Kumar Rajak
    </div>
    """,
    unsafe_allow_html=True,
)


