import streamlit as st
from datetime import date as dt_date, timedelta
import sqlite3

st.set_page_config(page_title="مغسلة المتحدة للسجاد", layout="wide")

# ---------------- اليوم ----------------
today = dt_date.today()

# ---------------- قاعدة البيانات ----------------
conn = sqlite3.connect("bookings.db", check_same_thread=False)
c = conn.cursor()

# ---------------- الجداول ----------------
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

c.execute("""
CREATE TABLE IF NOT EXISTS employees (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    daily_rate INTEGER
)
""")

c.execute("""
CREATE TABLE IF NOT EXISTS attendance (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    employee_id INTEGER,
    date TEXT
)
""")

c.execute("""
CREATE TABLE IF NOT EXISTS daily_orders (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    order_name TEXT,
    price INTEGER,
    date TEXT
)
""")
conn.commit()

# ---------------- الموظفين ----------------
employees = [
    ("مصطفى الفيشاوى", 100),
    ("وليد المالكي", 150),
    ("ابراهيم بكير", 150)
]

for name, rate in employees:
    c.execute("SELECT id FROM employees WHERE name=?", (name,))
    if not c.fetchone():
        c.execute("INSERT INTO employees (name,daily_rate) VALUES (?,?)", (name, rate))
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
<p style="text-align:center;">👤 المسؤول: {OWNER_NAME}</p>
<hr>
""", unsafe_allow_html=True)

# ================= صفحة الموظفين =================
if tab == "الموظفين":
    st.subheader("🔐 تسجيل حضور الموظفين")

    if "emp" not in st.session_state:
        st.session_state.emp = False

    emp_pass = st.text_input("كلمة السر", type="password")

    if st.button("دخول الموظفين"):
        if emp_pass == EMP_PASSWORD:
            st.session_state.emp = True
        else:
            st.error("❌ كلمة السر غير صحيحة")

    if st.session_state.emp:
        c.execute("SELECT id,name FROM employees")
        emps = c.fetchall()

        first_day = dt_date(today.year, today.month, 1)
        days = [first_day + timedelta(days=i) for i in range((today - first_day).days + 1)]
        selected_day = st.selectbox(
            "اختر اليوم",
            [d.strftime("%Y-%m-%d") for d in days]
        )

        attendance_state = {}

        for emp_id, emp_name in emps:
            c.execute(
                "SELECT 1 FROM attendance WHERE employee_id=? AND date=?",
                (emp_id, selected_day)
            )
            already = bool(c.fetchone())

            attendance_state[emp_id] = st.checkbox(
                emp_name,
                value=already,
                key=f"{emp_id}_{selected_day}"
            )

        if st.button("💾 حفظ الحضور"):
            for emp_id, present in attendance_state.items():
                if present:
                    c.execute(
                        "SELECT 1 FROM attendance WHERE employee_id=? AND date=?",
                        (emp_id, selected_day)
                    )
                    if not c.fetchone():
                        c.execute(
                            "INSERT INTO attendance (employee_id,date) VALUES (?,?)",
                            (emp_id, selected_day)
                        )
            conn.commit()
            st.success("✅ تم حفظ الحضور بنجاح")

# ================= أوردرات اليوم =================
elif tab == "أوردارات اليوم":
    st.subheader("🔐 أوردرات اليوم")

    if "orders" not in st.session_state:
        st.session_state.orders = False

    order_pass = st.text_input("كلمة السر", type="password")

    if st.button("دخول أوردرات اليوم"):
        if order_pass == ORDERS_PASSWORD:
            st.session_state.orders = True
        else:
            st.error("❌ كلمة السر غير صحيحة")

    if st.session_state.orders:
        with st.form("order_form"):
            name = st.text_input("اسم الأوردر")
            price = st.number_input("السعر", min_value=0)
            add = st.form_submit_button("إضافة")

            if add and name and price > 0:
                c.execute(
                    "INSERT INTO daily_orders (order_name,price,date) VALUES (?,?,?)",
                    (name, price, today.strftime("%Y-%m-%d"))
                )
                conn.commit()
                st.success("✅ تم إضافة الأوردر")

        c.execute(
            "SELECT id,order_name,price FROM daily_orders WHERE date=?",
            (today.strftime("%Y-%m-%d"),)
        )
        total = 0
        for oid, n, p in c.fetchall():
            total += p
            col1, col2, col3 = st.columns([4,2,1])
            col1.write(n)
            col2.write(f"{p} جنيه")
            if col3.button("❌", key=oid):
                c.execute("DELETE FROM daily_orders WHERE id=?", (oid,))
                conn.commit()
                st.experimental_rerun()

        st.markdown(f"## 💰 إجمالي اليوم: **{total} جنيه**")

# ---------------- Footer ----------------
st.markdown("<hr><center>🤲 اللهم بارك لنا في عملنا</center>", unsafe_allow_html=True)
