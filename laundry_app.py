import streamlit as st
from datetime import date as dt_date, datetime, timedelta
import sqlite3
import pandas as pd

# ---------------- إعداد الصفحة ----------------
st.set_page_config(
    page_title="🧼 مغسلة المتحدة - نسخة رمضان",
    layout="wide"
)

# ---------------- كلمات السر + بيانات الهيدر ----------------
ADMIN_PASSWORD = "المتحده@1996"
EMP_PASSWORD = "mostafa23"
ORDERS_PASSWORD = "اكرم1996"
CONTACT_ADDRESS = "الشؤون الاجتماعية"

# ---------------- إخفاء واجهة Streamlit الافتراضية ----------------
st.markdown("""
<style>
#MainMenu {visibility: hidden;}
header {visibility: hidden;}
footer {visibility: hidden;}
.stDeployButton {display:none;}
</style>
""", unsafe_allow_html=True)

# ---------------- ستايل رمضان الخرافي ----------------
st.markdown("""
<style>
/* خلفية ليلية رمضانية متحركة */
.stApp {
    background: linear-gradient(to bottom, #050510 0%, #101030 50%, #1a1a40 100%);
    background-attachment: fixed;
    color: #f0f0f0;
}

/* إضافة نجوم في الخلفية */
.stApp::before {
    content: " ";
    position: fixed;
    top: 0; left: 0; width: 100%; height: 100%;
    background: url('https://www.transparenttextures.com/patterns/stardust.png');
    opacity: 0.3;
}

/* تصميم البطاقات الزجاجي (Glassmorphism) */
div[data-testid="stForm"], 
div[data-testid="stVerticalBlock"] > div {
    background: rgba(255, 255, 255, 0.07) !important;
    backdrop-filter: blur(15px);
    border-radius: 25px !important;
    border: 1px solid rgba(255, 215, 0, 0.2);
    box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.8);
    padding: 25px !important;
}

/* عناوين رمضانية ذهبية */
h1, h2, h3 { 
    color: #FFD700 !important; 
    text-align: center; 
    text-shadow: 0 0 15px rgba(255, 215, 0, 0.5);
    font-family: 'Cairo', sans-serif;
}

/* هيدر رمضان */
.ramadan-header {
    background: rgba(0, 0, 0, 0.4);
    border: 2px solid #FFD700;
    padding: 30px;
    border-radius: 30px;
    text-align: center;
    margin-bottom: 40px;
    box-shadow: 0 0 25px rgba(255, 215, 0, 0.2);
}

/* ستايل الأزرار */
.stButton > button {
    background: linear-gradient(90deg, #FFD700 0%, #FFA500 100%) !important;
    color: #050510 !important;
    font-weight: bold !important;
    border-radius: 15px !important;
    border: none !important;
    transition: 0.3s !important;
}
.stButton > button:hover {
    transform: scale(1.05);
    box-shadow: 0 0 20px #FFD700;
}

/* الجداول */
.stTable {
    background: rgba(0, 0, 0, 0.2) !important;
    border-radius: 15px;
}

/* التبويبات */
.stTabs [data-baseweb="tab-list"] {
    gap: 10px;
    background-color: transparent;
}
.stTabs [data-baseweb="tab"] {
    background-color: rgba(255, 215, 0, 0.1);
    border-radius: 10px 10px 0 0;
    color: #FFD700;
}
</style>
""", unsafe_allow_html=True)

# ---------------- اليوم ----------------
today = dt_date.today()
last_booking_date = dt_date(2026, 3, 10)

# ---------------- قاعدة البيانات ----------------
conn = sqlite3.connect("bookings.db", check_same_thread=False)
c = conn.cursor()

c.execute("CREATE TABLE IF NOT EXISTS bookings (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT, address TEXT, phone TEXT, date TEXT, feedback TEXT, time_slot TEXT)")
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

# ---------------- هيدر رمضان ----------------
st.markdown(f"""
<div class="ramadan-header">
    <h1>🌙 مغسلة المتحدة للسجاد 🌙</h1>
    <h3 style="color: #f0f0f0 !important;">📍 {CONTACT_ADDRESS}</h3>
    <h2 style="letter-spacing: 2px;">رمضان كريم</h2>
    <p style="color: #FFD700;">وكل عام وأنتم بخير بمناسبة الشهر الفضيل</p>
</div>
""", unsafe_allow_html=True)

tabs = st.tabs(["✨ الحجز", "🔐 المسؤول", "👷 الموظفين", "📦 أوردرات اليوم"])

# ================= صفحة الحجز =================
with tabs[0]:
    with st.form("booking"):
        name = st.text_input("اسم العميل")
        address = st.text_input("العنوان بالتفصيل")
        phone = st.text_input("رقم التليفون")
        booking_date = st.date_input("تاريخ الحجز", max_value=last_booking_date)
        time_slot = st.radio("موعد العمل", ["صباحًا", "مساءً"], horizontal=True)
        submit = st.form_submit_button("تأكيد حجز الأوردر 🌙")
        if submit and name and phone:
            c.execute("INSERT INTO bookings (name,address,phone,date,time_slot) VALUES (?,?,?,?,?)", 
                      (name, address, phone, booking_date.strftime("%Y-%m-%d"), time_slot))
            conn.commit()
            st.success("✨ تم تسجيل الحجز بنجاح.. رمضان مبارك!")

# ================= صفحة المسؤول =================
with tabs[1]:
    password = st.text_input("كلمة سر الإدارة", type="password", key="admin_pwd")
    if password == ADMIN_PASSWORD:
        st.markdown("### 📋 كشف الحجوزات")
        df = pd.read_sql("SELECT name as 'الاسم', address as 'العنوان', phone as 'التليفون', date as 'التاريخ', time_slot as 'الفترة' FROM bookings", conn)
        st.dataframe(df, use_container_width=True)

# ================= صفحة الموظفين =================
with tabs[2]:
    password = st.text_input("كلمة سر شؤون الموظفين", type="password", key="emp_pwd")
    if password == EMP_PASSWORD:
        c.execute("SELECT id, name, daily_rate FROM employees")
        emps = c.fetchall()

        st.markdown("### 📝 تحضير الموظفين")
        att_date = st.date_input("تاريخ اليوم", today)
        col_att1, col_att2 = st.columns([2, 1])
        with col_att1:
            selected_ids = []
            for eid, ename, _ in emps:
                if st.checkbox(f"حضر: {ename}", key=f"check_{eid}"):
                    selected_ids.append(eid)
        with col_att2:
            if st.button("حفظ حضور اليوم ✨"):
                for e_id in selected_ids:
                    c.execute("SELECT 1 FROM attendance WHERE employee_id=? AND date=?", (e_id, att_date.strftime("%Y-%m-%d")))
                    if not c.fetchone():
                        c.execute("INSERT INTO attendance (employee_id, date) VALUES (?,?)", (e_id, att_date.strftime("%Y-%m-%d")))
                conn.commit()
                st.success("تم الحفظ بنجاح")
                st.rerun()

        st.markdown("---")
        st.markdown("### 💸 تسجيل الخصومات / السلف")
        with st.form("deduction_form"):
            col_d1, col_d2, col_d3 = st.columns(3)
            with col_d1: target_emp = st.selectbox("الموظف", [e[1] for e in emps])
            with col_d2: deduct_amt = st.number_input("المبلغ", min_value=0)
            with col_d3: deduct_reason = st.text_input("السبب")
            if st.form_submit_button("إضافة الخصم"):
                if deduct_amt > 0:
                    emp_id_to_deduct = next(e[0] for e in emps if e[1] == target_emp)
                    c.execute("INSERT INTO salary_deductions (employee_id, amount, reason, date) VALUES (?,?,?,?)",
                              (emp_id_to_deduct, deduct_amt, deduct_reason, today.strftime("%Y-%m-%d")))
                    conn.commit()
                    st.rerun()

        st.markdown("---")
        st.markdown("### 📊 كشف حساب الرواتب")
        rows = []
        for emp_id, emp_name, rate in emps:
            days = c.execute("SELECT COUNT(*) FROM attendance WHERE employee_id=?", (emp_id,)).fetchone()[0]
            total_deduct = c.execute("SELECT COALESCE(SUM(amount),0) FROM salary_deductions WHERE employee_id=?", (emp_id,)).fetchone()[0]
            final_salary = (days * rate) - total_deduct
            rows.append([emp_name, days, rate, total_deduct, final_salary])
        st.table(pd.DataFrame(rows, columns=["الموظف", "أيام الحضور", "اليومية", "الخصم", "المرتب المستحق"]))

        if st.button("🗑️ تصفية السجلات (شهر جديد)"):
            c.execute("DELETE FROM attendance"); c.execute("DELETE FROM salary_deductions"); conn.commit()
            st.warning("تم تصفير الحسابات")
            st.rerun()

# ================= صفحة أوردرات اليوم =================
with tabs[3]:
    password = st.text_input("كلمة سر الأوردرات", type="password", key="ord_pwd")
    if password == ORDERS_PASSWORD:
        with st.form("order_form"):
            order_name = st.text_input("نوع الأوردر")
            price = st.number_input("المبلغ", min_value=0)
            if st.form_submit_button("إضافة"):
                c.execute("INSERT INTO daily_orders (order_name,price,date) VALUES (?,?,?)", (order_name, price, today.strftime("%Y-%m-%d")))
                conn.commit()
                st.rerun()

        st.markdown("---")
        c.execute("SELECT id, order_name, price FROM daily_orders WHERE date=?", (today.strftime("%Y-%m-%d"),))
        day_orders = c.fetchall()
        total_day = sum(o[2] for o in day_orders)
        
        for oid, n, p in day_orders:
            col1, col2, col3 = st.columns([4,2,1])
            col1.write(f"🏷️ {n}")
            col2.write(f"💰 {p} جنيه")
            if col3.button("❌", key=f"del_{oid}"):
                c.execute("DELETE FROM daily_orders WHERE id=?", (oid,))
                conn.commit()
                st.rerun()
        st.markdown(f"## 💰 إجمالي دخل اليوم: `{total_day}` جنيه")