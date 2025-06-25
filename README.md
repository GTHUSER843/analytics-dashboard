# 🏨 analytics-dashboard

A Streamlit dashboard for hotel KPI analytics built using **Python**, **Pandas**, **Altair**, and **MySQL**. The dashboard helps visualize key performance indicators like revenue, occupancy rate, and cancellations.

---

## 📊 Features

- Insert and manage hotel booking records
- Visualize key metrics (total bookings, revenue, cancellation rate)
- Interactive filters by date and hotel
- Charts: revenue by channel, occupancy trends, and hotel-wise bookings
- Export full data as CSV

---

## 🛠️ Tech Stack

- **Frontend:** Streamlit
- **Backend:** Python, MySQL
- **Data Processing:** Pandas
- **Visualization:** Altair

---

## 🗃️ Sample Dataset

You can use the sample CSV below if not connected to a database:

🔗 [Download sample_data.csv](./sample_data.csv)

| booking_date | hotel_name      | room_type | occupancy_rate | revenue | guest_nationality | booking_channel | is_cancelled |
|--------------|------------------|-----------|----------------|---------|-------------------|------------------|--------------|
| 2024-05-01   | Hotel Taj        | Deluxe    | 90.0           | 12000   | India             | Online           | 0            |
| 2024-05-02   | Sea Breeze Inn   | Standard  | 75.0           | 8000    | UK                | Direct           | 0            |

---

## 🚀 Run the App Locally

```bash
git clone https://github.com/GTHUSER843/analytics-dashboard.git
cd analytics-dashboard
pip install -r requirements.txt
streamlit run app.py
