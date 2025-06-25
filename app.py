import streamlit as st
import pandas as pd
import altair as alt
import plotly.express as px
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from datetime import datetime
import json


def dashboard():
    st.set_page_config(page_title="Hotel Booking Dashboard", layout="wide")

    # Google Sheets Setup using Streamlit secrets
    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
    creds_dict = json.loads(st.secrets["GOOGLE_SHEETS_CREDENTIALS"])
    creds = ServiceAccountCredentials.from_json_keyfile_dict(creds_dict, scope)
    client = gspread.authorize(creds)
    sheet = client.open("hotel_bookings").sheet1

    def fetch_data():
        try:
            data = sheet.get_all_records()
            return pd.DataFrame(data)
        except Exception as e:
            st.error(f"❌ Failed to fetch data: {e}")
            return pd.DataFrame()

    def insert_data(data):
        try:
            sheet.append_row(data)
        except Exception as e:
            st.error(f"❌ Failed to insert data: {e}")

    st.markdown("""
        <style>
        .stTabs [data-baseweb="tab"] {
            font-size: 16px;
            font-weight: 600;
        }
        </style>
    """, unsafe_allow_html=True)

    st.title("🏨 Hotel Booking Analytics Dashboard")
    tab1, tab2, tab3 = st.tabs(["📝 Insert Booking", "📈 Insights", "🔍 View Data"])

    with tab1:
        st.subheader("➕ Insert New Booking Record")
        with st.form("booking_form"):
            col1, col2 = st.columns(2)
            with col1:
                booking_date = st.date_input("Booking Date")
                hotel_name = st.text_input("Hotel Name")
                room_type = st.text_input("Room Type")
                occupancy_rate = st.slider("Occupancy Rate (%)", 0.0, 100.0, 75.0)
                revenue = st.number_input("Revenue (₹)", min_value=0)
            with col2:
                guest_nationality = st.text_input("Guest Nationality")
                booking_channel = st.selectbox("Booking Channel", options=["Online", "Direct", "Travel Agent", "Corporate"])
                is_cancelled = st.radio("Is Cancelled?", options=[0, 1], format_func=lambda x: "No" if x == 0 else "Yes")

            submitted = st.form_submit_button("Submit Booking")
            if submitted:
                if not all([hotel_name.strip(), room_type.strip(), guest_nationality.strip(), booking_channel.strip()]) or occupancy_rate == 0.0 or revenue == 0:
                    st.warning("⚠️ Please fill all fields before submitting.")
                else:
                    data = [
                        booking_date.strftime("%Y-%m-%d"),
                        hotel_name,
                        room_type,
                        occupancy_rate,
                        revenue,
                        guest_nationality,
                        booking_channel,
                        is_cancelled
                    ]
                    insert_data(data)
                    st.success("✅ Booking inserted successfully!")

    with tab2:
        st.subheader("📈 Booking Trends & Insights")
        df = fetch_data()
        if df.empty:
            st.warning("No data to visualize.")
            return

        df['booking_date'] = pd.to_datetime(df['booking_date'])

        st.markdown("### 📊 Key Metrics")
        col1, col2, col3 = st.columns(3)
        col1.metric("📅 Total Bookings", f"{len(df)}")
        col2.metric("💰 Total Revenue", f"₹{df['revenue'].sum():,.0f}")
        col3.metric("❌ Cancellation Rate", f"{(df['is_cancelled'].mean()*100):.2f}%")

        st.markdown("### 🧠 Advanced Insights")
        avg_revenue = df['revenue'].mean()
        top_hotel = df['hotel_name'].value_counts().idxmax()
        peak_date = df['booking_date'].value_counts().idxmax().strftime("%Y-%m-%d")

        st.info(f"📌 **Average Revenue per Booking:** ₹{avg_revenue:,.2f}")
        st.info(f"🏨 **Most Booked Hotel:** {top_hotel}")
        st.info(f"📈 **Peak Booking Date:** {peak_date}")

        st.markdown("### 🔍 Filters")
        with st.expander("🔎 Filter Data"):
            min_date = df['booking_date'].min()
            max_date = df['booking_date'].max()
            selected_range = st.date_input("Select Date Range", [min_date, max_date])
            selected_hotel = st.multiselect("Filter by Hotel", options=df['hotel_name'].unique())

        filtered_df = df.copy()
        if len(selected_range) == 2:
            filtered_df = filtered_df[(filtered_df['booking_date'] >= pd.to_datetime(selected_range[0])) &
                                      (filtered_df['booking_date'] <= pd.to_datetime(selected_range[1]))]
        if selected_hotel:
            filtered_df = filtered_df[filtered_df['hotel_name'].isin(selected_hotel)]

        st.markdown("### 🔹 Revenue by Booking Channel")
        fig1 = px.bar(
            filtered_df.groupby("booking_channel")["revenue"].sum().reset_index(),
            x="booking_channel", y="revenue",
            color="booking_channel",
            labels={"booking_channel": "Booking Channel", "revenue": "Total Revenue"},
            template="plotly_white"
        )
        st.plotly_chart(fig1, use_container_width=True)

        st.markdown("### 🔹 Occupancy Rate Over Time")
        fig2 = px.line(
            filtered_df.groupby("booking_date")["occupancy_rate"].mean().reset_index(),
            x="booking_date", y="occupancy_rate",
            title="Average Occupancy Rate",
            template="plotly_white",
            markers=True
        )
        st.plotly_chart(fig2, use_container_width=True)

        st.markdown("### 🔹 Booking Count by Hotel")
        hotel_counts = filtered_df["hotel_name"].value_counts().reset_index()
        hotel_counts.columns = ["hotel_name", "count"]
        fig3 = px.pie(
            hotel_counts,
            names="hotel_name", values="count",
            title="Booking Distribution by Hotel",
            hole=0.4,
            color_discrete_sequence=px.colors.qualitative.Pastel
        )
        st.plotly_chart(fig3, use_container_width=True)

    with tab3:
        st.subheader("📋 All Hotel Bookings")
        df = fetch_data()
        if not df.empty:
            with st.expander("🕽 Export Options"):
                csv = df.to_csv(index=False).encode('utf-8')
                st.download_button("⬇️ Download as CSV", csv, "hotel_bookings.csv", "text/csv")
            st.dataframe(df, use_container_width=True, height=500)
        else:
            st.warning("No data available or failed to load.")


if __name__ == "__main__":
    dashboard()
