import streamlit as st
from datetime import date as dt_date, datetime, timedelta
import sqlite3
import pandas as pd

# ---------------- إعداد الصفحة ----------------
st.set_page_config(
    page_title="🧼 مغسلة المتحدة - Ramadan Edition",
    layout="wide"
)

# ---------------- كلمات السر + البيانات ----------------
ADMIN_PASSWORD = "المتحده@1996"
EMP_PASSWORD = "mostafa23"
ORDERS_PASSWORD = "اكرم1996"
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

# ---------------- الستايل الرمضاني الخرافي ----------------
st.markdown(f"""
<style>
/* خلفية الفضاء الرمضاني المتحرك */
.stApp {{
    background: linear-gradient(-45deg, #050510, #101030, #1a1a40, #000000);
    background-size: 400% 400%;
    animation: gradient 15s ease infinite;
    color: #ffffff;
}}

@keyframes gradient {{
    0% {{ background-position: 0% 50%; }}
    50% {{ background-position: 100% 50%; }}
    100% {{ background-position: 0% 50%; }}
}}

/* تأثير النجوم المتلألئة */
.stApp::before {{
    content: "";
    position: fixed;
    top: 0; left: 0; width: 100%; height: 100%;
    background: url('https://www.transparenttextures.com/patterns/stardust.png');
    opacity: 0.4;
    pointer-events: none;
}}

/* كروت شفافة (Glassmorphism) */
div[data-testid="stForm"], 
div[data-testid="stVerticalBlock"] > div {{
    background: rgba(255, 255, 255, 0.05) !important;
    backdrop-filter: blur(15px);
    border-radius: 25px !important;
    border: 1px solid rgba(255, 215, 0, 0.3);
    box-shadow: 0 10px 40px rgba(0, 0, 0, 0.5);
    padding: 30px !important;
    margin-bottom: 20px !important;
}}

/* الهيدر العلوي المطور */
.header-container {{
    text-align: center;
    padding: 40px;
    background: rgba(0, 0, 0, 0.5);
    border-radius: 30px;
    border-bottom: 3px solid #FFD700;
    margin-bottom: 40px;
    box-shadow: 0 0 30px rgba(255, 215, 0, 0.2);
}}

.phone-badge {{
    display: inline-block;
    background: linear-gradient(90deg, #FFD700, #FFA500);
    color: #000 !important;
    padding: 10px 25px;
    border-radius: 50px;
    font-weight: bold;
    font-size: 20px;
    margin-top: 15px;
    box-shadow: 0 0 20px rgba(255, 215, 0, 0.4);
}}

/* ستايل الأزرار النيون */
.stButton > button {{
    background: transparent !important;
    color: #FFD700 !important;
    border: 2px solid #FFD700 !important;
    border-radius: 15px !important;
    font-weight: bold !important;
    padding: 10px 30px !important;
    transition: all 0.4s ease-in-out !important;
}}

.stButton > button:hover {{
    background: #FFD700 !important;
    color: #000 !important;
    box-shadow: 0 0 25px #FFD700;
    transform: translateY(-3px);
}}

/* الجداول */
.stTable {{
    background: rgba(255, 255, 255, 0.02) !important;
    border-radius: 20px;
}}
</style>
""", unsafe_allow_html=True)

# ---------------- قاعدة البيانات ----------------
conn = sqlite3.connect("bookings.db", check_same_thread=False)
c = conn.cursor()
c.execute("CREATE TABLE IF NOT EXISTS bookings (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT, address TEXT, phone TEXT, date TEXT, time_slot TEXT)")
c.execute("CREATE TABLE IF NOT EXISTS employees (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT, daily_rate INTEGER)")
c.execute("CREATE TABLE IF NOT EXISTS attendance (id INTEGER PRIMARY KEY AUTOINCREMENT, employee_id INTEGER, date TEXT)")
c.execute("CREATE TABLE IF NOT EXISTS salary_deductions (id INTEGER PRIMARY KEY AUTOINCREMENT, employee_id INTEGER, amount INTEGER, reason TEXT, date TEXT)")
c.execute("CREATE TABLE IF NOT EXISTS daily_orders (id INTEGER PRIMARY KEY AUTOINCREMENT, order_name TEXT, price INTEGER, date TEXT)")
conn.commit()

# الموظفين
employees_data = [("مصطفى الفيشاوى", 100), ("وليد المالكي", 150), ("ابراهيم بكير", 150)]
for name, rate in employees_data:
    c.execute("SELECT id FROM employees WHERE name=?", (name,))
    if not c.fetchone():
        c.execute("INSERT INTO employees (name,daily_rate) VALUES (?,?)", (name, rate))
conn.commit()

# ---------------- الهيدر الاحترافي الجديد ----------------
st.markdown(f"""
<div class="header-container">
    <h1 style="font-size: 55px; margin-bottom: 10px;">✨ مغسلة المتحدة ✨</h1>
    <h3 style="color: #f0f0f0;">📍 العنوان: {CONTACT_ADDRESS}</h3>
    <div class="phone-badge">📞 للتواصل والحجز: {CONTACT_PHONE}</div>
    <h2 style="margin-top: 25px; color: #FFD700; font-family: 'Cairo';">🌙 رمضان كريم وكل عام وأنتم بخير 🌙</h2>
</div>
""", unsafe_allow_html=True)

# ---------------- التبويبات ----------------
tabs = st.tabs(["📋 حجز أوردر", "👷 الموظفين", "📦 أوردرات اليوم", "🔐 الإدارة"])

# 1. الحجز
with tabs[0]:
    with st.form("booking_form"):
        st.markdown("### 📝 بيانات الحجز الجديد")
        c1, c2 = st.columns(2)
        name = c1.text_input("اسم العميل")
        phone = c2.text_input("رقم الهاتف")
        addr = st.text_input("العنوان")
        b_date = st.date_input("تاريخ اليوم")
        slot = st.radio("موعد العمل", ["صباحًا", "مساءً"], horizontal=True)
        if st.form_submit_button("تأكيد الحجز 🌙"):
            if name and phone:
                c.execute("INSERT INTO bookings (name,address,phone,date,time_slot) VALUES (?,?,?,?,?)", (name, addr, phone, b_date.strftime("%Y-%m-%d"), slot))
                conn.commit()
                st.success("تم الحجز بنجاح يا بطل! رمضان مبارك")

# 2. الموظفين
with tabs[1]:
    if st.text_input("كلمة سر الموظفين", type="password", key="emp_p") == EMP_PASSWORD:
        c.execute("SELECT id, name, daily_rate FROM employees")
        emps = c.fetchall()
        
        st.markdown("### ✅ تسجيل حضور الموظفين")
        selected_ids = []
        cols = st.columns(3)
        for i, (eid, ename, rate) in enumerate(emps):
            if cols[i % 3].checkbox(ename, key=f"att_{eid}"):
                selected_ids.append(eid)
        
        if st.button("حفظ الحضور"):
            for eid in selected_ids:
                c.execute("INSERT INTO attendance (employee_id, date) VALUES (?,?)", (eid, dt_date.today().strftime("%Y-%m-%d")))
            conn.commit(); st.success("تم الحفظ"); st.rerun()

        st.divider()
        st.markdown("### 📊 جدول الرواتب والخصومات")
        rows = []
        for eid, ename, rate in emps:
            days = c.execute("SELECT COUNT(*) FROM attendance WHERE employee_id=?", (eid,)).fetchone()[0]
            deducts = c.execute("SELECT COALESCE(SUM(amount),0) FROM salary_deductions WHERE employee_id=?", (eid,)).fetchone()[0]
            rows.append([ename, days, rate, deducts, (days*rate)-deducts])
        st.table(pd.DataFrame(rows, columns=["الاسم", "الحضور", "اليومية", "الخصومات", "الصافي"]))
        
        with st.expander("💸 إضافة خصم جديد"):
            target = st.selectbox("الموظف", [e[1] for e in emps])
            amt = st.number_input("المبلغ", min_value=0)
            if st.button("تأكيد الخصم"):
                eid = next(e[0] for e in emps if e[1] == target)
                c.execute("INSERT INTO salary_deductions (employee_id, amount, date) VALUES (?,?,?)", (eid, amt, dt_date.today().strftime("%Y-%m-%d")))
                conn.commit(); st.rerun()

# 3. أوردرات اليوم
with tabs[2]:
    if st.text_input("كلمة سر الأوردرات", type="password", key="ord_p") == ORDERS_PASSWORD:
        with st.form("orders"):
            item = st.text_input("نوع الأوردر")
            price = st.number_input("السعر", min_value=0)
            if st.form_submit_button("إضافة"):
                c.execute("INSERT INTO daily_orders (order_name, price, date) VALUES (?,?,?)", (item, price, dt_date.today().strftime("%Y-%m-%d")))
                conn.commit(); st.rerun()
        
        res = c.execute("SELECT id, order_name, price FROM daily_orders WHERE date=?", (dt_date.today().strftime("%Y-%m-%d"),)).fetchall()
        total = sum(r[2] for r in res)
        for rid, n, p in res:
            col1, col2, col3 = st.columns([4,2,1])
            col1.write(n); col2.write(f"{p} ج")
            if col3.button("❌", key=f"del_{rid}"):
                c.execute("DELETE FROM daily_orders WHERE id=?", (rid,)); conn.commit(); st.rerun()
        st.markdown(f"## 💰 الإجمالي: `{total}` جنيه")

# 4. الإدارة
with tabs[3]:
    if st.text_input("كلمة سر الإدارة", type="password", key="adm_p") == ADMIN_PASSWORD:
        st.dataframe(pd.read_sql("SELECT * FROM bookings", conn), use_container_width=True)
        if st.button("⚠️ تصفير حسابات الموظفين"):
            c.execute("DELETE FROM attendance"); c.execute("DELETE FROM salary_deductions"); conn.commit(); st.rerun()