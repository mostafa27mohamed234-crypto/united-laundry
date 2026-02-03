import streamlit as st
from datetime import datetime, date as dt_date
import sqlite3

st.set_page_config(page_title="مغسلة المتحدة للسجاد", layout="wide")

# ---------------- قاعدة البيانات ----------------
conn = sqlite3.connect("bookings.db", check_same_thread=False)
c = conn.cursor()

# إنشاء الجدول الأساسي
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

# التأكد من وجود عمود feedback (حل المشكلة)
c.execute("PRAGMA table_info(bookings)")
columns = [col[1] for col in c.fetchall()]

if "feedback" not in columns:
    c.execute("ALTER TABLE bookings ADD COLUMN feedback TEXT")
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
h1, h2, h3 {
    color: #4b2e83;
}
.card {
    background-color: #fff9f0;
    padding: 15px;
    margin: 10px 0;
    border-radius: 15px;
    box-shadow: 0 4px 10px rgba(0,0,0,0.1);
}
button {
    background-color: #d4af37 !important;
    color: white !important;
    font-weight: bold;
}
</style>
""", unsafe_allow_html=True)

# ---------------- Header ----------------
st.markdown("""
<div style="text-align:center; padding:20px; background-color:#4b2e83; color:white; border-radius:15px;">
    <h1>مغسلة المتحدة للسجاد</h1>
</div>
<div style="text-align:center; font-size:20px; font-weight:bold; color:#b85c38; margin-top:10px;">
✨ مغسلة المتحدة تهنئكم بحلول شهر رمضان المبارك ✨
</div>
<div style="text-align:center; font-size:16px; color:#333; margin-top:5px;">
إدارة الأستاذ أكرم حموده - 📞 01063316053
</div>
""", unsafe_allow_html=True)

# ---------------- صفحة الحجز ----------------
if tab == "الحجز":
    st.markdown("### صفحة الحجز")

    with st.form("booking_form"):
        name = st.text_input("الاسم", autocomplete="off")
        address = st.text_input("العنوان", autocomplete="off")
        phone = st.text_input("رقم الهاتف", autocomplete="off")
        booking_date = st.date_input("تاريخ الحجز")
        feedback = st.text_area("رأيك يهمنا (اختياري)")
        submit = st.form_submit_button("احجز")

        if submit:
            if not name or not address or not phone:
                message = "❌ يجب ملء البيانات الأساسية"
            else:
                cutoff_date = dt_date(2026, 3, 10)
                if booking_date > cutoff_date:
                    message = "❌ الحجز متاح حتى 10 / 3 / 2026 فقط"
                else:
                    c.execute(
                        "INSERT INTO bookings (name, address, phone, date, feedback) VALUES (?, ?, ?, ?, ?)",
                        (name, address, phone, booking_date.strftime("%Y-%m-%d"), feedback)
                    )
                    conn.commit()
                    message = "✅ تم الحجز بنجاح"

# ---------------- صفحة المسؤول ----------------
elif tab == "المسؤول":
    st.markdown("### صفحة المسؤول")
    password = st.text_input("كلمة السر", type="password")

    if st.button("دخول"):
        if password == ADMIN_PASSWORD:
            show_admin = True
        else:
            message = "❌ كلمة السر غير صحيحة"

    if show_admin:
        c.execute("SELECT * FROM bookings")
        rows = c.fetchall()

        if rows:
            for r in rows:
                id, name, address, phone, date, feedback = r
                st.markdown(f"""
                <div class='card'>
                <b>الاسم:</b> {name}<br>
                <b>العنوان:</b> {address}<br>
                <b>الهاتف:</b> {phone}<br>
                <b>التاريخ:</b> {date}<br>
                <b>رأي العميل:</b> {feedback if feedback else "—"}
                </div>
                """, unsafe_allow_html=True)
        else:
            st.info("لا توجد حجوزات حالياً.")

# ---------------- رسالة ----------------
if message:
    st.markdown(
        f"<div style='text-align:center; color:#b85c38; font-weight:bold;'>{message}</div>",
        unsafe_allow_html=True
    )
