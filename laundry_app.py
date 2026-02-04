import streamlit as st
from datetime import date as dt_date, datetime
import sqlite3
import pandas as pd

# ---------------- إعداد الصفحة ----------------
st.set_page_config(
    page_title="🧼 مغسلة المتحدة للسجاد",
    layout="wide"
)

# ---------------- رقم التواصل + العنوان ----------------
CONTACT_PHONE = "01063316053"
CONTACT_ADDRESS = "الشؤون الاجتماعية"

# ---------------- إخفاء واجهة Streamlit ----------------
st.markdown("""
<style>
#MainMenu {visibility: hidden;}
header {visibility: hidden;}
footer {visibility: hidden;}
.stDeployButton {display:none;}
</style>
""", unsafe_allow_html=True)

# ---------------- ستايل الموقع + رمضان ----------------
st.markdown("""
<style>
.stApp {
    background: linear-gradient(135deg,#E3F2FD,#BBDEFB,#90CAF9,#64B5F6);
    font-family: 'Cairo', sans-serif;
}

div[data-testid="stForm"],
div[data-testid="stVerticalBlock"] > div {
    background-color: rgba(255,255,255,0.88);
    padding: 20px;
    border-radius: 18px;
    box-shadow: 0 8px 25px rgba(0,0,0,0.12);
}

h1, h2, h3 { color: #0D47A1; text-align: center; }

.stButton > button {
    background: linear-gradient(90deg,#1E88E5,#42A5F5);
    color: white;
    border-radius: 14px;
    font-size: 16px;
    padding: 10px 22px;
    border: none;
}

input, textarea {
    border-radius: 10px !important;
    border: 1px solid #90CAF9 !important;
}

.ramadan-box {
    background: linear-gradient(135deg,#1A237E,#283593);
    color: white;
    padding: 28px;
    border-radius: 22px;
    text-align: center;
    margin-bottom: 30px;
    box-shadow: 0 12px 35px rgba(0,0,0,0.3);
}

.phone-box {
    background: rgba(255,255,255,0.15);
    padding: 12px;
    border-radius: 14px;
    margin-top: 10px;
    font-size: 18px;
}

.success-card {
    background: linear-gradient(135deg,#2E7D32,#66BB6A);
    color: white;
    padding: 30px;
    border-radius: 25px;
    text-align: center;
    margin-top: 30px;
    box-shadow: 0 12px 35px rgba(0,0,0,0.3);
}
</style>
""", unsafe_allow_html=True)

# ---------------- اليوم ----------------
today = dt_date.today()
last_booking_date = dt_date(2026, 3, 10)

# ---------------- قاعدة البيانات ----------------
conn = sqlite3.connect("bookings.db", check_same_thread=False)
c = conn.cursor()

c.execute("""
CREATE TABLE IF NOT EXISTS bookings (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    address TEXT,
    phone TEXT,
    date TEXT,
    feedback TEXT,
    time_slot TEXT
)
""")
conn.commit()

# ---------------- هيدر + رمضان + رقم التليفون + العنوان ----------------
st.markdown(f"""
<div class="ramadan-box">
    <h1>🧼 مغسلة المتحدة للسجاد</h1>
    <h3>📍 العنوان: {CONTACT_ADDRESS}</h3>
    <div class="phone-box">
        📞 للتواصل والحجز: <b>{CONTACT_PHONE}</b>
    </div>
    <h2>🌙 رمضان كريم 🌙</h2>
    <p style="margin-top:10px;">🕌 ✨ 🏮 ✨ 🕌</p>
</div>
""", unsafe_allow_html=True)

# ================= الحجز =================
if "done" not in st.session_state:
    st.session_state.done = False

if not st.session_state.done:
    now = datetime.now()
    end_datetime = datetime.combine(last_booking_date, datetime.max.time())
    remaining = end_datetime - now

    if remaining.total_seconds() > 0:
        d = remaining.days
        h, r = divmod(remaining.seconds, 3600)
        m, s = divmod(r, 60)
        st.info(f"⏳ متبقي للحجز: {d} يوم {h} ساعة {m} دقيقة {s} ثانية")

        with st.form("booking"):
            name = st.text_input("الاسم")
            address = st.text_input("العنوان")
            phone = st.text_input("رقم الهاتف")
            booking_date = st.date_input("التاريخ", max_value=last_booking_date)
            time_slot = st.radio("الوقت", ["صباحًا", "مساءً"], horizontal=True)
            feedback = st.text_area("ملاحظات")
            submit = st.form_submit_button("تأكيد الحجز")

            if submit and name and address and phone:
                c.execute(
                    "SELECT 1 FROM bookings WHERE name=? AND phone=? AND date=?",
                    (name, phone, booking_date.strftime("%Y-%m-%d"))
                )
                if c.fetchone():
                    st.error("❌ لا يمكن الحجز مرتين في نفس اليوم")
                else:
                    c.execute("""
                    INSERT INTO bookings (name,address,phone,date,feedback,time_slot)
                    VALUES (?,?,?,?,?,?)
                    """, (
                        name,
                        address,
                        phone,
                        booking_date.strftime("%Y-%m-%d"),
                        feedback,
                        time_slot
                    ))
                    conn.commit()

                    st.session_state.done = True
                    st.session_state.data = {
                        "name": name,
                        "address": address,
                        "phone": phone,
                        "date": booking_date.strftime("%Y-%m-%d"),
                        "time": time_slot,
                        "feedback": feedback
                    }
                    st.experimental_rerun()
    else:
        st.error("❌ انتهت فترة الحجز")

# -------- رسالة الشكر --------
else:
    d = st.session_state.data
    st.markdown(f"""
    <div class="success-card">
        <h1>✅ تم تأكيد الحجز بنجاح</h1>
        <h3>شكرًا لاختياركم مغسلة المتحدة للسجاد 🌸</h3>
        <hr>
        <p><b>👤 الاسم:</b> {d['name']}</p>
        <p><b>📍 العنوان:</b> {d['address']}</p>
        <p><b>📞 الهاتف:</b> {d['phone']}</p>
        <p><b>📅 التاريخ:</b> {d['date']}</p>
        <p><b>⏰ الوقت:</b> {d['time']}</p>
        <p><b>📝 ملاحظات:</b> {d['feedback'] or "—"}</p>
        <br>
        <p>📞 للاستفسار: {CONTACT_PHONE}</p>
        <p>🌙 كل عام وأنتم بخير</p>
    </div>
    """, unsafe_allow_html=True)
