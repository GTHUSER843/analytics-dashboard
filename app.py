import streamlit as st
import mysql.connector
import pandas as pd
import altair as alt
from mysql.connector import Error


def dashboard():
    st.set_page_config(page_title="Hotel Booking Dashboard", layout="wide")

    def get_connection():
        try:
            return mysql.connector.connect(
                host="localhost",
                user="root",
                password="root",
                database="dash",
                port=3306
            )
        except Error as e:
            st.error(f"Database connection failed: {e}")
            return None

    def fetch_data():
        conn = get_connection()
        if conn is None:
            return pd.DataFrame()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM hotel_bookings")
        rows = cursor.fetchall()
        columns = [desc[0] for desc in cursor.description]
        df = pd.DataFrame(rows, columns=columns)
        cursor.close()
        conn.close()
        return df

    def insert_data(data):
        conn = get_connection()
        if conn is None:
            return
        cursor = conn.cursor()
        insert_query = """
        INSERT INTO hotel_bookings 
        (booking_date, hotel_name, room_type, occupancy_rate, revenue, 
         guest_nationality, booking_channel, is_cancelled)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """
        try:
            cursor.execute(insert_query, data)
            conn.commit()
        except Error as e:
            st.error(f"Failed to insert data: {e}")
        finally:
            cursor.close()
            conn.close()

    st.title("📊 Hotel Booking Analytics Dashboard")
    tab1, tab2, tab3 = st.tabs(["📝 Insert Booking", "📈 Insights", "🔍 View Data"])

    with tab1:
        st.subheader("Insert New Booking Record")
        with st.form("booking_form"):
            col1, col2 = st.columns(2)
            with col1:
                booking_date = st.date_input("Booking Date")
                hotel_name = st.text_input("Hotel Name")
                room_type = st.text_input("Room Type")
                occupancy_rate = st.number_input("Occupancy Rate (%)", min_value=0.0, max_value=100.0, step=0.1)
                revenue = st.number_input("Revenue", min_value=0)
            with col2:
                guest_nationality = st.text_input("Guest Nationality")
                booking_channel = st.selectbox("Booking Channel", options=["Online", "Direct", "Travel Agent", "Corporate"])
                is_cancelled = st.radio("Is Cancelled?", options=[0, 1], format_func=lambda x: "No" if x == 0 else "Yes")
                submitted = st.form_submit_button("Submit Booking")
                if submitted:
                    if (
                        hotel_name.strip() == "" or
                        room_type.strip() == "" or
                        guest_nationality.strip() == "" or
                        booking_channel.strip() == "" or
                        occupancy_rate == 0.0 or
                        revenue == 0
                    ):
                        st.warning("⚠️ Please fill all fields before submitting.")
                    else:
                        data = (
                            booking_date.strftime("%Y-%m-%d"),
                            hotel_name,
                            room_type,
                            occupancy_rate,
                            revenue,
                            guest_nationality,
                            booking_channel,
                            is_cancelled
                        )
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
        chart1 = alt.Chart(filtered_df).mark_bar().encode(
            x=alt.X('booking_channel:N', title='Booking Channel'),
            y=alt.Y('sum(revenue):Q', title='Total Revenue'),
            color='booking_channel:N',
            tooltip=['booking_channel:N', 'sum(revenue):Q']
        ).properties(width=600, height=400)
        st.altair_chart(chart1, use_container_width=True)

        st.markdown("### 🔹 Occupancy Rate Over Time")
        chart2 = alt.Chart(filtered_df).mark_line(point=True).encode(
            x=alt.X('booking_date:T', title='Date'),
            y=alt.Y('mean(occupancy_rate):Q', title='Avg. Occupancy Rate'),
            color=alt.value("#1f77b4"),
            tooltip=['booking_date:T', 'mean(occupancy_rate):Q']
        ).properties(width=600, height=400)
        st.altair_chart(chart2, use_container_width=True)

        st.markdown("### 🔹 Booking Count by Hotel")
        hotel_counts = filtered_df['hotel_name'].value_counts().reset_index()
        hotel_counts.columns = ['Hotel Name', 'Booking Count']
        chart3 = alt.Chart(hotel_counts).mark_bar().encode(
            x=alt.X('Hotel Name:N', sort='-y'),
            y='Booking Count:Q',
            color='Hotel Name:N',
            tooltip=['Hotel Name', 'Booking Count']
        ).properties(width=800, height=400)
        st.altair_chart(chart3, use_container_width=True)

    with tab3:
        st.subheader("All Hotel Bookings")
        df = fetch_data()
        if not df.empty:
            with st.expander("🔽 Export Options"):
                csv = df.to_csv(index=False).encode('utf-8')
                st.download_button("Download as CSV", csv, "hotel_bookings.csv", "text/csv")
            st.dataframe(df, use_container_width=True)
        else:
            st.warning("No data available or failed to load.")

if __name__ == "__main__":
    dashboard()
