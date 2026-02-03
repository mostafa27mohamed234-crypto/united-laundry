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

ADMIN_PASSWORD = "المتحده@1996"  # كلمة السر الجديدة
show_admin = False
tab = st.sidebar.selectbox("اختر الصفحة", ["الحجز", "المسؤول"])
message = ""

# ---------------- CSS للتجميل ----------------
st.markdown("""
<style>
body {
    background: linear-gradient(to bottom right, #fdf6e3, #e0c3fc);
    font-family: 'Arial', sans-serif;
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
header_html = """
<div style="text-align:center; padding:20px; background-color:#4b2e83; color:white; border-radius:15px;">
    <h1>مغسلة المتحدة للسجاد</h1>
</div>
<div style="text-align:center; font-size:20px; font-weight:bold; color:#b85c38; margin-top:10px;">
✨ مغسلة المتحدة تهنئكم بحلول شهر رمضان المبارك ✨
</div>
<div style="text-align:center; font-size:16px; color:#333; margin-top:5px;">
إدارة الأستاذ أكرم حموده - 📞 01063316053
</div>
"""
st.markdown(header_html, unsafe_allow_html=True)

# ---------------- صفحة الحجز ----------------
if tab == "الحجز":
    st.markdown("### صفحة الحجز")
    with st.form(key="booking_form"):
        name = st.text_input("الاسم", autocomplete="off")
        address = st.text_input("العنوان", autocomplete="off")
        phone = st.text_input("رقم الهاتف", autocomplete="off")
        booking_date = st.date_input("تاريخ الحجز")
        submit = st.form_submit_button("احجز")

        if submit:
            # التحقق من أن جميع الحقول تم إدخالها
            if not name or not address or not phone or not booking_date:
                message = "❌ يجب ملء جميع الحقول قبل الحجز"
            else:
                cutoff_date = dt_date(datetime.now().year, 3, 20)
                if booking_date > cutoff_date:
                    message = "❌ لا يمكن الحجز بعد يوم 20/3"
                else:
                    c.execute(
                        "INSERT INTO bookings (name, address, phone, date) VALUES (?, ?, ?, ?)",
                        (name, address, phone, booking_date.strftime("%Y-%m-%d"))
                    )
                    conn.commit()
                    message = f"✅ تم الحجز بنجاح! الاسم: {name}, التاريخ: {booking_date.strftime('%Y-%m-%d')}"

# ---------------- صفحة المسؤول ----------------
elif tab == "المسؤول":
    st.markdown("### صفحة المسؤول")
    password = st.text_input("كلمة السر", type="password")
    check = st.button("دخول")

    if check:
        if password == ADMIN_PASSWORD:
            show_admin = True
        else:
            message = "❌ كلمة السر خاطئة"

    if show_admin:
        st.markdown("### الحجوزات")
        c.execute("SELECT id, name, address, phone, date FROM bookings")
        rows = c.fetchall()

        if rows:
            for r in rows:
                booking_id, name, address, phone, date = r
                st.markdown(f"<div class='card'>"
                            f"<b>الاسم:</b> {name} <br>"
                            f"<b>العنوان:</b> {address} <br>"
                            f"<b>الهاتف:</b> {phone} <br>"
                            f"<b>التاريخ:</b> {date} <br>", unsafe_allow_html=True)
                
                col1, col2 = st.columns([1,1])
                with col1:
                    if st.button(f"حذف {booking_id}", key=f"del{booking_id}"):
                        c.execute("DELETE FROM bookings WHERE id = ?", (booking_id,))
                        conn.commit()
                        st.experimental_rerun()
                with col2:
                    with st.expander("تعديل"):
                        new_name = st.text_input("الاسم الجديد", value=name, key=f"name{booking_id}")
                        new_address = st.text_input("العنوان الجديد", value=address, key=f"address{booking_id}")
                        new_phone = st.text_input("الهاتف الجديد", value=phone, key=f"phone{booking_id}")
                        new_date = st.date_input("التاريخ الجديد", value=datetime.strptime(date, "%Y-%m-%d"), key=f"date{booking_id}")
                        if st.button(f"تحديث {booking_id}", key=f"update{booking_id}"):
                            c.execute(
                                "UPDATE bookings SET name=?, address=?, phone=?, date=? WHERE id=?",
                                (new_name, new_address, new_phone, new_date.strftime("%Y-%m-%d"), booking_id)
                            )
                            conn.commit()
                            st.experimental_rerun()
                st.markdown("</div>", unsafe_allow_html=True)
        else:
            st.info("لا توجد حجوزات حتى الآن.")

# ---------------- رسالة ----------------
if message:
    st.markdown(
        f"<div style='text-align:center; color:#b85c38; font-weight:bold; margin-bottom:15px;'>{message}</div>",
        unsafe_allow_html=True
    )
