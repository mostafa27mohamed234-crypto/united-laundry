import streamlit as st
from datetime import datetime, date as dt_date, timedelta
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

# جدول حضور الموظفين
c.execute("""
CREATE TABLE IF NOT EXISTS attendance (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    employee_id INTEGER,
    date TEXT,
    note TEXT,
    FOREIGN KEY(employee_id) REFERENCES employees(id)
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
    c.execute("SELECT id FROM employees WHERE name = ?", (name,))
    if not c.fetchone():
        c.execute("INSERT INTO employees (name, daily_rate) VALUES (?,?)", (name, rate))
conn.commit()

# ---------------- المتغيرات العامة ----------------
ADMIN_PASSWORD = "المتحده@1996"
EMP_PASSWORD = "mostafa23"
OWNER_NAME = "الأستاذ أكرم حموده"
message = ""

# ---------------- Sidebar ----------------
tab = st.sidebar.selectbox("اختر الصفحة", ["الحجز", "المسؤول", "الموظفين"])

# ---------------- CSS ----------------
st.markdown("""
<style>
body { background: linear-gradient(to bottom right, #fdf6e3, #e0c3fc); font-family: Arial, sans-serif;}
.hero { background: linear-gradient(to left, #4b2e83, #6a4fb3); color: white; padding: 25px; border-radius: 20px; text-align: center; margin-bottom: 20px;}
.countdown { background-color: #fff3cd; color: #856404; padding: 12px; border-radius: 12px; font-weight: bold; text-align: center; margin-bottom: 15px;}
.call-btn a { display: inline-block; background-color: #28a745; color: white; padding: 12px 25px; border-radius: 12px; font-weight: bold; text-decoration: none;}
.card { background-color: #fff9f0; padding: 18px; margin: 12px 0; border-radius: 18px; box-shadow: 0 6px 15px rgba(0,0,0,0.12);}
.owner { font-size: 16px; color: #ffd700; font-weight: bold;}
.table-container { overflow-x:auto;}
</style>
""", unsafe_allow_html=True)

# ---------------- Header ----------------
st.markdown(f"""
<div class="hero">
    <h1>🧼 مغسلة المتحدة للسجاد</h1>
    <p>نظافة • أمان • التزام في الميعاد</p>
    <p class="owner">👤 المسؤول: {OWNER_NAME}</p>
    <p>📞 01063316053</p>
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
            else:
                c.execute("INSERT INTO bookings (name, address, phone, date, feedback, time_slot) VALUES (?, ?, ?, ?, ?, ?)",
                          (name, address, phone, booking_date.strftime("%Y-%m-%d"), feedback, time_slot))
                conn.commit()
                message = "✅ تم الحجز بنجاح، سيتم التواصل معكم قريبًا"

# ---------------- صفحة المسؤول ----------------
elif tab == "المسؤول":
    st.markdown(f"### 🔐 لوحة التحكم — المسؤول: {OWNER_NAME}")
    password = st.text_input("كلمة السر", type="password")

    if st.button("دخول"):
        if password == ADMIN_PASSWORD:
            st.session_state.show_admin = True
        else:
            message = "❌ كلمة السر غير صحيحة"

    if st.session_state.get('show_admin', False):
        c.execute("SELECT name, address, phone, date, time_slot, feedback FROM bookings")
        rows = c.fetchall()
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

# ---------------- صفحة الموظفين ----------------
elif tab == "الموظفين":
    st.markdown("### 🔐 لوحة الموظفين — تسجيل الحضور")
    emp_pass = st.text_input("كلمة السر", type="password")

    if 'show_emp' not in st.session_state:
        st.session_state.show_emp = False

    if st.button("دخول الموظفين"):
        if emp_pass == EMP_PASSWORD:
            st.session_state.show_emp = True
        else:
            message = "❌ كلمة السر غير صحيحة للموظفين"

    if st.session_state.show_emp:
        st.markdown("### تسجيل الحضور")
        c.execute("SELECT id, name, daily_rate FROM employees")
        emps = c.fetchall()

        first_day = dt_date(today.year, today.month, 1)
        days_list = [first_day + timedelta(days=i) for i in range((today - first_day).days + 1)]
        att_date = st.selectbox("اختر تاريخ الحضور", days_list, format_func=lambda x: x.strftime('%Y-%m-%d'))

        attendance_data = {}
        for emp_id, emp_name, _ in emps:
            col1, col2 = st.columns([2,3])
            with col1:
                present = st.checkbox(f"{emp_name}", key=f"att_{emp_id}_{att_date}")
            with col2:
                note = st.text_input(f"ملاحظات {emp_name}", key=f"note_{emp_id}_{att_date}")
            attendance_data[emp_id] = (present, note)

        if st.button("حفظ جميع الحضور"):
            for emp_id, (present, note) in attendance_data.items():
                if present:
                    c.execute("INSERT INTO attendance (employee_id, date, note) VALUES (?,?,?)", (emp_id, att_date.strftime("%Y-%m-%d"), note))
            conn.commit()
            st.success(f"تم حفظ الحضور لجميع الموظفين بتاريخ {att_date}")

        st.markdown("### جدول الحضور الشهري")
        col_names = ['الموظف'] + [d.strftime('%d') for d in days_list] + ['أيام الحضور', 'الراتب']
        data = []
        for emp_id, emp_name, rate in emps:
            row = [emp_name]
            count = 0
            for d in days_list:
                c.execute("SELECT 1 FROM attendance WHERE employee_id=? AND date=?", (emp_id, d.strftime('%Y-%m-%d')))
                present = c.fetchone()
                if present:
                    row.append('✓')
                    count += 1
                else:
                    row.append('')
            row.append(count)
            row.append(count * rate)
            data.append(row)

        df = pd.DataFrame(data, columns=col_names)
        st.dataframe(df.style.set_properties(**{'text-align': 'center'}))

# ---------------- رسالة ----------------
if message:
    st.markdown(f"<div style='text-align:center; font-weight:bold; font-size:18px; color:#4b2e83;'>{message}</div>", unsafe_allow_html=True)

# ---------------- Footer ----------------
st.markdown("""
<div style="text-align:center; margin-top:35px; font-weight:bold; color:#4b2e83;">
🤲 اللهم بارك لنا في عملنا وارزقنا رضا عملائنا 🤍
</div>
""", unsafe_allow_html=True)
