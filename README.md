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

## 🚀 Running Locally (With Google Sheets)

```bash
git clone https://github.com/GTHUSER843/analytics-dashboard.git
cd analytics-dashboard
pip install -r requirements.txt

# Add your service account credentials file locally
# Ensure the file is named: credentials.json
streamlit run app.py
```

---

## 🌐 Deployment on Streamlit Cloud

1. **Push** code to GitHub (exclude `credentials.json` from repo)
2. Go to [share.streamlit.io](https://share.streamlit.io)
3. In **Settings > Secrets**, paste:
   ```toml
   GOOGLE_SHEETS_CREDENTIALS = """{ ...full JSON key here... }"""
   ```
4. Deploy the app! Live insert + dashboard features will work seamlessly

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

## 📸 Preview (Add your screenshots here)

---

## 👤 Author

Developed by **Sahil Tambe**  
📫 [LinkedIn](https://www.linkedin.com/in/yourprofile)  
📧 sahiltambe@example.com
