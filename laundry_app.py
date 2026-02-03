import streamlit as st
from datetime import date as dt_date, timedelta
import sqlite3
import pandas as pd

st.set_page_config(page_title="مغسلة المتحدة للسجاد", layout="wide")

# ---------------- اليوم الحالي ----------------
today = dt_date.today()

# ---------------- قاعدة البيانات ----------------
conn = sqlite3.connect("bookings.db", check_same_thread=False)
c = conn.cursor()

# جدول الحجز
c.execute("""
CREATE TABLE IF NOT EXISTS bookings (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    address TEXT,
    phone TEXT,
    date TEXT,
    feedback TEXT,
    rating INTEGER,
    time_slot TEXT
)
""")

# جدول الموظفين
c.execute("""
CREATE TABLE IF NOT EXISTS employees (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    daily_rate INTEGER
)
""")

# جدول الحضور
c.execute("""
CREATE TABLE IF NOT EXISTS attendance (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    employee_id INTEGER,
    date TEXT,
    note TEXT
)
""")

# جدول أوردرات اليوم
c.execute("""
CREATE TABLE IF NOT EXISTS daily_orders (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    order_name TEXT,
    price INTEGER,
    date TEXT
)
""")
conn.commit()

# ---------------- بيانات الموظفين ----------------
employees = [
    ("مصطفى الفيشاوى", 100),
    ("وليد المالكي", 150),
    ("ابراهيم بكير", 150)
]

for name, rate in employees:
    c.execute("SELECT id FROM employees WHERE name=?", (name,))
    if not c.fetchone():
        c.execute("INSERT INTO employees (name, daily_rate) VALUES (?,?)", (name, rate))
conn.commit()

# ---------------- متغيرات ----------------
ADMIN_PASSWORD = "المتحده@1996"
EMP_PASSWORD = "mostafa23"
ORDERS_PASSWORD = "اكرم1996"
OWNER_NAME = "الأستاذ أكرم حموده"
message = ""

# ---------------- Sidebar ----------------
tab = st.sidebar.selectbox(
    "اختر الصفحة",
    ["الحجز", "المسؤول", "الموظفين", "أوردارات اليوم"]
)

# ---------------- Header ----------------
st.markdown(f"""
<h1 style="text-align:center;">🧼 مغسلة المتحدة للسجاد</h1>
<p style="text-align:center;">👤 المسؤول: {OWNER_NAME} | 📞 01063316053</p>
<hr>
""", unsafe_allow_html=True)

# ================= صفحة الحجز =================
if tab == "الحجز":
    st.subheader("📝 احجز خدمتك")
    with st.form("booking"):
        name = st.text_input("الاسم")
        address = st.text_input("العنوان")
        phone = st.text_input("رقم الهاتف")
        booking_date = st.date_input("التاريخ")
        time_slot = st.radio("الوقت", ["صباحًا", "مساءً"], horizontal=True)
        feedback = st.text_area("ملاحظات")
        submit = st.form_submit_button("تأكيد الحجز")

        if submit:
            if not name or not address or not phone:
                message = "❌ برجاء استكمال البيانات"
            else:
                c.execute("""
                INSERT INTO bookings (name, address, phone, date, feedback, time_slot)
                VALUES (?,?,?,?,?,?)
                """, (name, address, phone, booking_date.strftime("%Y-%m-%d"), feedback, time_slot))
                conn.commit()
                message = "✅ تم الحجز بنجاح"

# ================= صفحة المسؤول =================
elif tab == "المسؤول":
    st.subheader("🔐 لوحة المسؤول")
    password = st.text_input("كلمة السر", type="password")

    if st.button("دخول"):
        if password == ADMIN_PASSWORD:
            st.session_state.admin = True
        else:
            message = "❌ كلمة السر غير صحيحة"

    if st.session_state.get("admin"):
        c.execute("SELECT name,address,phone,date,time_slot FROM bookings")
        for r in c.fetchall():
            st.info(f"""
👤 {r[0]}
📍 {r[1]}
📞 {r[2]}
📅 {r[3]}
⏰ {r[4]}
""")

# ================= صفحة الموظفين =================
elif tab == "الموظفين":
    st.subheader("🔐 حضور الموظفين")
    emp_pass = st.text_input("كلمة السر", type="password")

    if st.button("دخول الموظفين"):
        if emp_pass == EMP_PASSWORD:
            st.session_state.emp = True
        else:
            message = "❌ كلمة السر غير صحيحة"

    if st.session_state.get("emp"):
        c.execute("SELECT id,name,daily_rate FROM employees")
        emps = c.fetchall()

        first_day = dt_date(today.year, today.month, 1)
        days = [first_day + timedelta(days=i) for i in range((today - first_day).days + 1)]
        day = st.selectbox("اختر اليوم", [d.strftime("%Y-%m-%d") for d in days])

        for emp_id, emp_name, _ in emps:
            present = st.checkbox(emp_name, key=f"{emp_id}{day}")
            if present:
                c.execute("SELECT 1 FROM attendance WHERE employee_id=? AND date=?", (emp_id, day))
                if not c.fetchone():
                    c.execute("INSERT INTO attendance (employee_id,date) VALUES (?,?)", (emp_id, day))
        if st.button("حفظ"):
            conn.commit()
            st.success("تم حفظ الحضور")

# ================= أوردرات اليوم =================
elif tab == "أوردارات اليوم":
    st.subheader("🔐 أوردرات اليوم")
    order_pass = st.text_input("كلمة السر", type="password")

    if st.button("دخول"):
        if order_pass == ORDERS_PASSWORD:
            st.session_state.orders = True
        else:
            message = "❌ كلمة السر غير صحيحة"

    if st.session_state.get("orders"):
        with st.form("order"):
            order_name = st.text_input("اسم الأوردر")
            price = st.number_input("السعر", min_value=0)
            add = st.form_submit_button("إضافة")

            if add and order_name and price > 0:
                c.execute("""
                INSERT INTO daily_orders (order_name,price,date)
                VALUES (?,?,?)
                """, (order_name, price, today.strftime("%Y-%m-%d")))
                conn.commit()
                st.success("تم إضافة الأوردر")

        st.markdown("### 📋 أوردرات اليوم")
        c.execute("SELECT id,order_name,price FROM daily_orders WHERE date=?", (today.strftime("%Y-%m-%d"),))
        orders = c.fetchall()

        total = 0
        for oid, name, price in orders:
            total += price
            col1, col2, col3 = st.columns([4,2,1])
            col1.write(name)
            col2.write(f"{price} جنيه")
            if col3.button("❌", key=oid):
                c.execute("DELETE FROM daily_orders WHERE id=?", (oid,))
                conn.commit()
                st.experimental_rerun()

        st.markdown(f"## 💰 إجمالي اليوم: **{total} جنيه**")

# ---------------- رسالة ----------------
if message:
    st.warning(message)

# ---------------- Footer ----------------
st.markdown("<hr><center>🤲 اللهم بارك لنا في عملنا</center>", unsafe_allow_html=True)
