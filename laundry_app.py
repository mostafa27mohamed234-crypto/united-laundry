import streamlit as st
from datetime import datetime, date as dt_date
import sqlite3

st.set_page_config(page_title="مغسلة المتحدة للسجاد", layout="wide")

# ---------------- قاعدة البيانات ----------------
conn = sqlite3.connect("bookings.db", check_same_thread=False)
c = conn.cursor()

c.execute("""
CREATE TABLE IF NOT EXISTS bookings (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    address TEXT,
    phone TEXT,
    date TEXT
)
""")
conn.commit()

# التأكد من الأعمدة
c.execute("PRAGMA table_info(bookings)")
columns = [col[1] for col in c.fetchall()]

if "feedback" not in columns:
    c.execute("ALTER TABLE bookings ADD COLUMN feedback TEXT")

if "rating" not in columns:
    c.execute("ALTER TABLE bookings ADD COLUMN rating INTEGER")

if "time_slot" not in columns:
    c.execute("ALTER TABLE bookings ADD COLUMN time_slot TEXT")

conn.commit()

ADMIN_PASSWORD = "المتحده@1996"
show_admin = False
tab = st.sidebar.selectbox("اختر الصفحة", ["الحجز", "المسؤول"])
message = ""

# ---------------- CSS ----------------
st.markdown("""
<style>
body {
    background: linear-gradient(to bottom right, #fdf6e3, #e0c3fc);
    font-family: Arial, sans-serif;
}
.hero {
    background: linear-gradient(to left, #4b2e83, #6a4fb3);
    color: white;
    padding: 25px;
    border-radius: 20px;
    text-align: center;
    margin-bottom: 20px;
}
.countdown {
    background-color: #fff3cd;
    color: #856404;
    padding: 12px;
    border-radius: 12px;
    font-weight: bold;
    text-align: center;
    margin-bottom: 15px;
}
.call-btn a {
    display: inline-block;
    background-color: #28a745;
    color: white;
    padding: 12px 25px;
    border-radius: 12px;
    font-weight: bold;
    text-decoration: none;
}
.card {
    background-color: #fff9f0;
    padding: 18px;
    margin: 12px 0;
    border-radius: 18px;
    box-shadow: 0 6px 15px rgba(0,0,0,0.12);
}
</style>
""", unsafe_allow_html=True)

# ---------------- Header ----------------
st.markdown("""
<div class="hero">
    <h1>🧼 مغسلة المتحدة للسجاد</h1>
    <p>نظافة • أمان • التزام في الميعاد</p>
    <p>📞 01063316053</p>
</div>
""", unsafe_allow_html=True)

# ---------------- عد تنازلي ----------------
cutoff_date = dt_date(2026, 3, 10)
today = dt_date.today()
days_left = (cutoff_date - today).days

if days_left >= 0:
    st.markdown(
        f"<div class='countdown'>⏳ متبقي {days_left} يوم على غلق الحجز</div>",
        unsafe_allow_html=True
    )
else:
    st.markdown(
        "<div class='countdown'>❌ تم غلق باب الحجز</div>",
        unsafe_allow_html=True
    )

# ---------------- زر الاتصال ----------------
st.markdown("""
<div class="call-btn" style="text-align:center; margin-bottom:20px;">
    <a href="tel:01063316053">📞 اتصل بنا الآن</a>
</div>
""", unsafe_allow_html=True)

# ---------------- صفحة الحجز ----------------
if tab == "الحجز":
    st.markdown("### 📝 احجز خدمتك الآن")

    with st.form("booking_form"):
        name = st.text_input("👤 الاسم")
        address = st.text_input("📍 العنوان")
        phone = st.text_input("📞 رقم الهاتف")
        booking_date = st.date_input("📅 تاريخ الحجز")
        time_slot = st.radio("⏰ اختر الوقت المناسب", ["صباحًا", "مساءً"], horizontal=True)
        feedback = st.text_area("💬 رأيك يهمنا (اختياري)")
        submit = st.form_submit_button("✅ تأكيد الحجز")

        if submit:
            if not name or not address or not phone:
                message = "❌ برجاء استكمال البيانات الأساسية"
            elif booking_date > cutoff_date:
                message = "❌ الحجز متاح حتى 10 / 3 / 2026 فقط"
            else:
                c.execute(
                    "INSERT INTO bookings (name, address, phone, date, feedback, time_slot) VALUES (?, ?, ?, ?, ?, ?)",
                    (name, address, phone, booking_date.strftime("%Y-%m-%d"), feedback, time_slot)
                )
                conn.commit()
                message = "✅ تم الحجز بنجاح، سيتم التواصل معكم قريبًا"

# ---------------- صفحة المسؤول ----------------
elif tab == "المسؤول":
    st.markdown("### 🔐 لوحة التحكم")
    password = st.text_input("كلمة السر", type="password")

    if st.button("دخول"):
        if password == ADMIN_PASSWORD:
            show_admin = True
        else:
            message = "❌ كلمة السر غير صحيحة"

    if show_admin:
        c.execute("SELECT name, address, phone, date, time_slot, feedback FROM bookings")
        rows = c.fetchall()

        if rows:
            for r in rows:
                name, address, phone, date, time_slot, feedback = r
                st.markdown(f"""
                <div class='card'>
                <b>👤 الاسم:</b> {name}<br>
                <b>📍 العنوان:</b> {address}<br>
                <b>📞 الهاتف:</b> {phone}<br>
                <b>📅 التاريخ:</b> {date}<br>
                <b>⏰ الوقت:</b> {time_slot}<br>
                <b>💬 الرأي:</b> {feedback if feedback else "—"}
                </div>
                """, unsafe_allow_html=True)
        else:
            st.info("لا توجد حجوزات حالياً.")

# ---------------- رسالة ----------------
if message:
    st.markdown(
        f"<div style='text-align:center; font-weight:bold; font-size:18px; color:#4b2e83;'>{message}</div>",
        unsafe_allow_html=True
    )

# ---------------- Footer ----------------
st.markdown("""
<div style="text-align:center; margin-top:35px; font-weight:bold; color:#4b2e83;">
🤲 اللهم بارك لنا في عملنا وارزقنا رضا عملائنا 🤍
</div>
""", unsafe_allow_html=True)
