import streamlit as st
from datetime import date as dt_date, timedelta
import sqlite3
import pandas as pd

# ---------------- إعداد الصفحة ----------------
st.set_page_config(
    page_title="🧼 مغسلة المتحدة للسجاد",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ---------------- CSS للتنسيق والألوان ----------------
st.markdown("""
<style>
body {
    background-color: #fff8f0;
    color: #333333;
}
h1 {
    color: #e07b39;
}
h2, h3 {
    color: #d65a31;
}
.stButton>button {
    background-color: #e07b39;
    color: white;
}
.stTextInput>div>div>input {
    border-radius: 8px;
}
</style>
""", unsafe_allow_html=True)

# ---------------- اليوم ----------------
today = dt_date.today()

# ---------------- قاعدة البيانات ----------------
conn = sqlite3.connect("bookings.db", check_same_thread=False)
c = conn.cursor()

# ---------------- إنشاء الجداول ----------------
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

# ---------------- بيانات الموظفين ----------------
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

# ---------------- المتغيرات ----------------
ADMIN_PASSWORD = "المتحده@1996"
EMP_PASSWORD = "mostafa23"
ORDERS_PASSWORD = "اكرم1996"
OWNER_NAME = "الأستاذ أكرم حموده"
message = ""

# ---------------- Sidebar ----------------
tab = st.sidebar.selectbox(
    "اختر الصفحة",
    ["🏠 الرئيسية", "الحجز", "المسؤول", "الموظفين", "أوردارات اليوم"]
)

# ---------------- Header ----------------
st.markdown(f"""
<div style="background-color:#ffe5d4;padding:15px;border-radius:10px;">
<h1 style="text-align:center;">🧼 مغسلة المتحدة للسجاد</h1>
<h3 style="text-align:center;">👤 المسؤول: {OWNER_NAME} | 📞 01063316053</h3>
<h2 style="text-align:center;color:#d65a31;">🌙 رمضان كريم وكل عام وأنتم بخير!</h2>
</div>
""", unsafe_allow_html=True)

# ---------------- Home Page ----------------
if tab == "🏠 الرئيسية":
    st.markdown("### أهلاً بك في نظام مغسلة المتحدة للسجاد")
    st.markdown("يمكنك استخدام الشريط الجانبي للتنقل بين الصفحات: الحجز، المسؤول، الموظفين، وأوردارات اليوم.")
    st.image("https://images.unsplash.com/photo-1581092334170-1f0e5ffce7f0?ixlib=rb-4.0.3&auto=format&fit=crop&w=1050&q=80",
             caption="مرحبًا بك في مغسلة المتحدة للسجاد", use_column_width=True)

# ================= صفحة الحجز =================
elif tab == "الحجز":
    st.markdown("## 📝 حجز خدمة")
    with st.container():
        with st.form("booking_form"):
            col1, col2 = st.columns(2)
            with col1:
                name = st.text_input("الاسم")
                address = st.text_input("العنوان")
            with col2:
                phone = st.text_input("رقم الهاتف")
                booking_date = st.date_input("التاريخ", value=today)
            time_slot = st.radio("الوقت", ["صباحًا", "مساءً"], horizontal=True)
            feedback = st.text_area("ملاحظات")
            submit = st.form_submit_button("تأكيد الحجز")

            if submit:
                if not name or not address or not phone:
                    message = "❌ برجاء استكمال البيانات"
                else:
                    c.execute("""INSERT INTO bookings (name,address,phone,date,feedback,time_slot)
                                 VALUES (?,?,?,?,?,?)""",
                              (name,address,phone,booking_date.strftime("%Y-%m-%d"),feedback,time_slot))
                    conn.commit()
                    message = "✅ تم الحجز بنجاح"

# ================= صفحة المسؤول =================
elif tab == "المسؤول":
    st.markdown("## 🔐 لوحة المسؤول")
    if "admin" not in st.session_state:
        st.session_state.admin = False

    password = st.text_input("كلمة السر", type="password")
    if st.button("دخول"):
        if password == ADMIN_PASSWORD:
            st.session_state.admin = True
        else:
            st.error("❌ كلمة السر غير صحيحة")

    if st.session_state.admin:
        st.markdown("### 📋 الحجوزات الحالية")
        df_bookings = pd.read_sql("SELECT name,address,phone,date,time_slot,feedback FROM bookings", conn)
        st.dataframe(df_bookings, use_container_width=True)

# ================= صفحة الموظفين =================
elif tab == "الموظفين":
    st.markdown("## 👥 تسجيل وحساب حضور الموظفين")
    if "emp" not in st.session_state:
        st.session_state.emp = False

    emp_pass = st.text_input("كلمة السر", type="password")
    if st.button("دخول الموظفين"):
        if emp_pass == EMP_PASSWORD:
            st.session_state.emp = True
        else:
            st.error("❌ كلمة السر غير صحيحة")

    if st.session_state.emp:
        c.execute("SELECT id,name,daily_rate FROM employees")
        emps = c.fetchall()

        first_day = dt_date(today.year, today.month, 1)
        days_list = [first_day + timedelta(days=i) for i in range((today - first_day).days + 1)]
        selected_day = st.selectbox("اختر اليوم لتسجيل الحضور",
                                    [d.strftime("%Y-%m-%d") for d in days_list])

        attendance_state = {}
        for emp_id, emp_name, _ in emps:
            c.execute("SELECT 1 FROM attendance WHERE employee_id=? AND date=?",
                      (emp_id, selected_day))
            already = bool(c.fetchone())
            attendance_state[emp_id] = st.checkbox(emp_name, value=already, key=f"{emp_id}_{selected_day}")

        col1, col2 = st.columns(2)
        if col1.button("💾 حفظ الحضور"):
            for emp_id, present in attendance_state.items():
                if present:
                    c.execute("SELECT 1 FROM attendance WHERE employee_id=? AND date=?",
                              (emp_id, selected_day))
                    if not c.fetchone():
                        c.execute("INSERT INTO attendance (employee_id,date) VALUES (?,?)",
                                  (emp_id, selected_day))
            conn.commit()
            st.success("✅ تم حفظ الحضور")

        if col2.button("🗑 مسح حضور اليوم"):
            c.execute("DELETE FROM attendance WHERE date=?", (selected_day,))
            conn.commit()
            st.warning("🗑 تم مسح حضور هذا اليوم")
            st.experimental_rerun()

        # ---------------- جدول الحضور ----------------
        st.markdown("### 📊 جدول الحضور الشهري")
        col_names = ['الموظف'] + [d.strftime('%d') for d in days_list] + ['أيام الحضور', 'الراتب']
        data = []

        for emp_id, emp_name, rate in emps:
            row = [emp_name]
            count = 0
            for d in days_list:
                d_str = d.strftime('%Y-%m-%d')
                c.execute("SELECT 1 FROM attendance WHERE employee_id=? AND date=?", (emp_id, d_str))
                present = c.fetchone()
                if present:
                    row.append('✓')
                    count += 1
                else:
                    row.append('')
            row.append(count)
            row.append(count*rate)
            data.append(row)

        df = pd.DataFrame(data, columns=col_names)
        st.dataframe(df.style.set_properties(**{'text-align': 'center'}))

# ================= أوردرات اليوم =================
elif tab == "أوردارات اليوم":
    st.markdown("## 🛒 أوردرات اليوم")
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
                c.execute("INSERT INTO daily_orders (order_name,price,date) VALUES (?,?,?)",
                          (name, price, today.strftime("%Y-%m-%d")))
                conn.commit()
                st.success("✅ تم إضافة الأوردر")

        c.execute("SELECT id,order_name,price FROM daily_orders WHERE date=?", (today.strftime("%Y-%m-%d"),))
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

# ---------------- رسالة ----------------
if message:
    st.warning(message)

# ---------------- Footer ----------------
st.markdown("""
<hr>
<center>🤲 اللهم بارك لنا في عملنا</center>
""", unsafe_allow_html=True)
