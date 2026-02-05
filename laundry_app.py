import streamlit as st
from datetime import date as dt_date
import sqlite3
import pandas as pd

# ---------------- إعداد الصفحة ----------------
st.set_page_config(
    page_title="🌙 مغسلة المتحدة - رمضان كريم 🌙",
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

# ---------------- الستايل الرمضاني المروّق ----------------
st.markdown(f"""
<style>
.stApp {{
    background-color: #0d1222;
    background-image: url("https://www.transparenttextures.com/patterns/stardust.png");
    background-size: cover;
    background-attachment: fixed;
    color: #ffffff;
}}

/* تصميم الكروت بالعرض */
div[data-testid="stForm"], 
div[data-testid="stVerticalBlock"] > div {{
    background: rgba(255, 255, 255, 0.08) !important;
    border-radius: 20px !important;
    border: 1px solid #FFD700;
    padding: 25px !important;
    box-shadow: 0 4px 15px rgba(0,0,0,0.3);
}}

h1, h2, h3, label, p, span {{
    color: #ffffff !important;
    font-family: 'Cairo', sans-serif;
}}

.main-header-box {{
    text-align: center;
    padding: 20px;
    background: #1a233a;
    border-radius: 20px;
    border-bottom: 5px solid #FFD700;
    margin-bottom: 20px;
}}

.ramadan-greeting {{
    font-size: 32px;
    color: #FFD700 !important;
    font-weight: bold;
    text-shadow: 0 0 10px rgba(255,215,0,0.5);
}}

.stButton > button {{
    background: linear-gradient(90deg, #FFD700 0%, #FFA500 100%) !important;
    color: #1a233a !important;
    font-weight: bold !important;
    border-radius: 10px !important;
    width: 100%;
}}

.footer-signature {{
    text-align: center;
    padding: 15px;
    color: #FFD700 !important;
    font-weight: bold;
    border-top: 1px solid rgba(255,215,0,0.2);
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

# ---------------- الهيدر ----------------
st.markdown(f"""
<div class="main-header-box">
    <h1 style="margin:0;">🌟 مغسلة المتحدة 🌟</h1>
    <div class="ramadan-greeting">🌙 رمضان كريم 🕌</div>
    <p style="margin:5px 0;">📍 {CONTACT_ADDRESS} | 📞 {CONTACT_PHONE}</p>
</div>
""", unsafe_allow_html=True)

# ---------------- التبويبات ----------------
tabs = st.tabs(["📝 تسجيل طلبات", "👷 الموظفين", "📦 الإيرادات", "🔐 الإدارة"])
footer_html = f"""<div class="footer-signature">🚀 إشراف وتطوير: البشمهندس مصطفى الفيشاوي 🚀</div>"""

# 1. تسجيل طلبات (تم التوزيع بالعرض)
with tabs[0]:
    with st.form("booking_form"):
        st.subheader("إضافة بيانات العميل")
        c1, c2, c3 = st.columns(3)
        name = c1.text_input("اسم العميل")
        phone = c2.text_input("رقم الهاتف")
        addr = c3.text_input("العنوان")
        
        c4, c5 = st.columns([2, 1])
        b_date = c4.date_input("تاريخ الحجز", dt_date.today())
        time_slot = c5.radio("الفترة", ["صباحًا", "مساءً"], horizontal=True)
        
        if st.form_submit_button("حفظ البيانات الآن ✨"):
            if name and phone:
                c.execute("INSERT INTO bookings (name,address,phone,date,time_slot) VALUES (?,?,?,?,?)", 
                          (name, addr, phone, b_date.strftime("%Y-%m-%d"), time_slot))
                conn.commit(); st.success("✅ تم الحفظ!")
            else: st.error("أكمل الاسم والهاتف")
    st.markdown(footer_html, unsafe_allow_html=True)

# 2. حسابات الموظفين
with tabs[1]:
    password = st.text_input("كلمة السر", type="password", key="emp_p")
    if password == EMP_PASSWORD:
        c.execute("SELECT id, name, daily_rate FROM employees")
        emps = c.fetchall()
        
        # توزيع الحضور بالعرض
        st.subheader("تسجيل حضور اليوم")
        cols = st.columns(len(emps))
        selected_ids = []
        for i, (eid, ename, rate) in enumerate(emps):
            if cols[i].checkbox(ename, key=f"at_{eid}"):
                selected_ids.append(eid)
        if st.button("تأكيد الحضور"):
            for eid in selected_ids:
                c.execute("SELECT 1 FROM attendance WHERE employee_id=? AND date=?", (eid, dt_date.today().strftime("%Y-%m-%d")))
                if not c.fetchone():
                    c.execute("INSERT INTO attendance (employee_id, date) VALUES (?,?)", (eid, dt_date.today().strftime("%Y-%m-%d")))
            conn.commit(); st.success("تم!"); st.rerun()

        st.markdown("---")
        # سلفيات بالعرض
        c1, c2 = st.columns([2, 1])
        with c1:
            st.subheader("سلف وخصومات")
            target_emp = st.selectbox("الموظف", [e[1] for e in emps])
            amt = st.number_input("المبلغ", min_value=0)
            if st.button("تأكيد الخصم"):
                eid = next(e[0] for e in emps if e[1] == target_emp)
                c.execute("INSERT INTO salary_deductions (employee_id, amount, date) VALUES (?,?,?)", (eid, amt, dt_date.today().strftime("%Y-%m-%d")))
                conn.commit(); st.success("تم الخصم"); st.rerun()
        with c2:
            st.subheader("الرواتب")
            rows = []
            for eid, ename, rate in emps:
                days = c.execute("SELECT COUNT(*) FROM attendance WHERE employee_id=?", (eid,)).fetchone()[0]
                ded = c.execute("SELECT COALESCE(SUM(amount),0) FROM salary_deductions WHERE employee_id=?", (eid,)).fetchone()[0]
                rows.append([ename, (days * rate) - ded])
            st.table(pd.DataFrame(rows, columns=["الاسم", "المستحق"]))
    st.markdown(footer_html, unsafe_allow_html=True)

# 3. أوردرات اليوم (بالعرض)
with tabs[2]:
    password = st.text_input("كلمة السر", type="password", key="ord_p")
    if password == ORDERS_PASSWORD:
        with st.form("order_form"):
            c1, c2 = st.columns([3, 1])
            order_name = c1.text_input("وصف الأوردر")
            price = c2.number_input("السعر", min_value=0)
            if st.form_submit_button("إضافة"):
                c.execute("INSERT INTO daily_orders (order_name,price,date) VALUES (?,?,?)", (order_name, price, dt_date.today().strftime("%Y-%m-%d")))
                conn.commit(); st.rerun()

        st.markdown("---")
        c.execute("SELECT id, order_name, price FROM daily_orders WHERE date=?", (dt_date.today().strftime("%Y-%m-%d"),))
        data = c.fetchall()
        df_ord = pd.DataFrame(data, columns=["ID", "الأوردر", "السعر"])
        st.dataframe(df_ord[["الأوردر", "السعر"]], use_container_width=True)
        st.metric("إجمالي الدخل اليومي", f"{sum(o[2] for o in data)} جنيه")
    st.markdown(footer_html, unsafe_allow_html=True)

# 4. لوحة الإدارة
with tabs[3]:
    password = st.text_input("كلمة السر", type="password", key="adm_p")
    if password == ADMIN_PASSWORD:
        st.subheader("سجل الحجوزات الكامل")
        df_b = pd.read_sql("SELECT name, phone, address, date FROM bookings ORDER BY date DESC", conn)
        st.dataframe(df_b, use_container_width=True)
        
        if st.button("⚠️ مسح السجلات القديمة"):
            c.execute("DELETE FROM bookings"); conn.commit(); st.rerun()
    st.markdown(footer_html, unsafe_allow_html=True)