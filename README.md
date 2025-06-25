# 🏨 Hotel Booking Analytics Dashboard
A Streamlit-powered dashboard for analyzing hotel booking trends using **Google Sheets** as a live backend. This app enables teams to track and update booking insights in real-time without hosting a database.
---

## 📊 Features

- Add and store hotel booking records directly into Google Sheets
- Key KPIs: Total bookings, Total revenue, Cancellation rate
- Live metrics and trends from synced spreadsheet
- Filters: date range and hotel-specific filtering
- Charts:
  - 📊 Revenue by booking channel (bar)
  - 📉 Occupancy rate trends over time (line)
  - 🥧 Hotel-wise booking count (donut chart)
- Export current dataset as CSV

---

## 🛠️ Tech Stack

- **Frontend**: Streamlit
- **Backend/Storage**: Google Sheets via Service Account
- **Libraries**: pandas, plotly, altair, gspread, oauth2client

---

## 🗃️ Sample Dataset (Optional for Testing)

If you're not using Google Sheets, test locally with the CSV:

🔗 [Download sample_data.csv](./sample_data.csv)

| booking_date | hotel_name      | room_type | occupancy_rate | revenue | guest_nationality | booking_channel | is_cancelled |
|--------------|------------------|-----------|----------------|---------|-------------------|------------------|--------------|
| 2024-05-01   | Hotel Taj        | Deluxe    | 90.0           | 12000   | India             | Online           | 0            |
| 2024-05-02   | Sea Breeze Inn   | Standard  | 75.0           | 8000    | UK                | Direct           | 0            |

---
## 📦 Requirements

```txt
streamlit
pandas
gspread
oauth2client
plotly
altair
```

---

## 🎯 Use Cases

- Hotel and resort analytics
- Educational projects on live dashboards
- NoSQL backend dashboards using Google Sheets

---

## 👤 Author

Developed by **Sahil Tambe**  
📧 sahiltambe340@gmail.com
