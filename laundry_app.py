import streamlit as st
from datetime import date as dt_date, timedelta
import sqlite3
import pandas as pd

st.set_page_config(page_title="مغسلة المتحدة للسجاد", layout="wide")

# ---------------- اليوم ----------------
today = dt_date.today()

# ---------------- قاعدة البيانات ----------------
conn = sqlite3.connect("bookings.db", check_same_thread=False)
c = conn.cursor()

# ---------------- الجداول ----------------
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
        c.execute(
            "INSERT INTO employees (name,daily_rate) VALUES (?,?)",
            (name, rate)
        )
conn.commit()

EMP_PASSWORD = "mostafa23"

# ---------------- Sidebar ----------------
tab = st.sidebar.selectbox(
    "اختر الصفحة",
    ["الموظفين"]
)

# ================= صفحة الموظفين =================
if tab == "الموظفين":
    st.subheader("🔐 تسجيل وحساب حضور الموظفين")

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

        # اختيار اليوم للحضور
        first_day = dt_date(today.year, today.month, 1)
        days_list = [first_day + timedelta(days=i) for i in range((today - first_day).days + 1)]
        selected_day = st.selectbox(
            "اختر اليوم لتسجيل الحضور",
            [d.strftime("%Y-%m-%d") for d in days_list]
        )

        # Checkbox لكل موظف
        attendance_state = {}
        for emp_id, emp_name, _ in emps:
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

        col1, col2 = st.columns(2)
        if col1.button("💾 حفظ الحضور"):
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
            st.success("✅ تم حفظ الحضور")

        if col2.button("🗑 مسح حضور اليوم"):
            c.execute("DELETE FROM attendance WHERE date=?", (selected_day,))
            conn.commit()
            st.warning("🗑 تم مسح حضور هذا اليوم")
            st.experimental_rerun()

        # ---------------- جدول الحضور الشهري ----------------
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
            row.append(count * rate)
            data.append(row)

        df = pd.DataFrame(data, columns=col_names)
        st.dataframe(df.style.set_properties(**{'text-align': 'center'}))
