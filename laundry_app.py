import streamlit as st
from datetime import date as dt_date
import sqlite3
import pandas as pd

# ---------------- إعداد الصفحة ----------------
st.set_page_config(
    page_title="المتحدة - رمضان كريم",
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

# ---------------- الستايل المطور (تصغير + تغيير ألوان) ----------------
st.markdown(f"""
<style>
/* تصغير المسافات العامة */
.block-container {{
    padding-top: 1rem !important;
    padding-bottom: 0rem !important;
}}

.stApp {{
    background-color: #080c16;
    background-image: url("https://www.transparenttextures.com/patterns/stardust.png");
    color: #ffffff;
}}

/* تعديل شكل حقول الإدخال (Inputs) */
.stTextInput input, .stNumberInput input, .stDateInput input, .stSelectbox div[data-baseweb="select"] {{
    background-color: rgba(26, 35, 58, 0.9) !important; /* لون أزرق ليلي بدلاً من الأبيض */
    color: #FFD700 !important; /* نص ذهبي */
    border: 1px solid #FFD700 !important;
    border-radius: 8px !important;
    padding: 5px 10px !important;
}}

/* تصميم الكروت (ملمومة أكثر) */
div[data-testid="stForm"], 
div[data-testid="stVerticalBlock"] > div {{
    background: rgba(255, 255, 255, 0.05) !important;
    border-radius: 15px !important;
    border: 1px solid rgba(255, 215, 0, 0.4);
    padding: 15px !important;
    margin-bottom: 10px !important;
}}

.main-header-box {{
    text-align: center;
    padding: 10px;
    background: rgba(26, 35, 58, 0.5);
    border-radius: 15px;
    border-bottom: 3px solid #FFD700;
    margin-bottom: 15px;
}}

.ramadan-greeting {{
    font-size: 24px;
    color: #FFD700 !important;
    font-weight: bold;
}}

/* الأزرار */
.stButton > button {{
    background: linear-gradient(90deg, #FFD700 0%, #FFA500 100%) !important;
    color: #080c16 !important;
    font-weight: bold !important;
    font-size: 14px !important;
    border-radius: 8px !important;
    border: none !important;
}}

/* تصغير التبويبات */
.stTabs [data-baseweb="tab"] {{
    padding: 5px 15px !important;
    font-size: 14px !important;
}}

.footer-signature {{
    text-align: center;
    padding: 10px;
    color: rgba(255, 215, 0, 0.6) !important;
    font-size: 13px;
    border-top: 1px solid rgba(255, 215, 0, 0.1);
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

# ---------------- الهيدر ----------------
st.markdown(f"""
<div class="main-header-box">
    <h2 style="margin:0; color:#FFD700;">🌟 مغسلة المتحدة 🌟</h2>
    <div class="ramadan-greeting">🌙 رمضان كريم 🕌</div>
    <p style="margin:0; font-size:14px;">📍 {CONTACT_ADDRESS} | 📞 {CONTACT_PHONE}</p>
</div>
""", unsafe_allow_html=True)

# ---------------- التبويبات ----------------
tabs = st.tabs(["📝 الحجوزات", "👷 الموظفين", "💰 الإيرادات", "🔐 الإدارة"])
footer_html = f"""<div class="footer-signature">إشراف وتطوير: البشمهندس مصطفى الفيشاوي 🚀</div>"""

# 1. تسجيل الحجوزات
with tabs[0]:
    with st.form("booking_form", clear_on_submit=True):
        c1, c2, c3 = st.columns(3)
        name = c1.text_input("الاسم")
        phone = c2.text_input("الموبايل")
        addr = c3.text_input("العنوان")
        
        c4, c5 = st.columns([2, 1])
        b_date = c4.date_input("التاريخ", dt_date.today())
        time_slot = c5.radio("الفترة", ["صباحًا", "مساءً"], horizontal=True)
        
        if st.form_submit_button("حفظ البيانات ✨"):
            if name and phone:
                c.execute("INSERT INTO bookings (name,address,phone,date,time_slot) VALUES (?,?,?,?,?)", 
                          (name, addr, phone, b_date.strftime("%Y-%m-%d"), time_slot))
                conn.commit(); st.success("تم الحفظ!")
            else: st.error("أكمل البيانات")
    st.markdown(footer_html, unsafe_allow_html=True)

# 2. حسابات الموظفين
with tabs[1]:
    pwd = st.text_input("الباسورد", type="password", key="emp_p")
    if pwd == EMP_PASSWORD:
        c.execute("SELECT id, name, daily_rate FROM employees")
        emps = c.fetchall()
        
        # الحضور في صف واحد
        st.write("📊 **تسجيل حضور اليوم**")
        cols = st.columns(len(emps))
        for i, (eid, ename, rate) in enumerate(emps):
            if cols[i].checkbox(ename, key=f"at_{eid}"):
                c.execute("SELECT 1 FROM attendance WHERE employee_id=? AND date=?", (eid, dt_date.today().strftime("%Y-%m-%d")))
                if not c.fetchone():
                    c.execute("INSERT INTO attendance (employee_id, date) VALUES (?,?)", (eid, dt_date.today().strftime("%Y-%m-%d")))
        if st.button("حفظ الحضور"): conn.commit(); st.rerun()

        st.markdown("---")
        c1, c2 = st.columns([1, 1])
        with c1:
            st.write("💸 **سلف وخصومات**")
            target = st.selectbox("الموظف", [e[1] for e in emps])
            amt = st.number_input("المبلغ", min_value=0)
            if st.button("تأكيد"):
                eid = next(e[0] for e in emps if e[1] == target)
                c.execute("INSERT INTO salary_deductions (employee_id, amount, date) VALUES (?,?,?)", (eid, amt, dt_date.today().strftime("%Y-%m-%d")))
                conn.commit(); st.success("تم"); st.rerun()
        with c2:
            st.write("🧾 **المستحقات**")
            res = []
            for eid, ename, rate in emps:
                days = c.execute("SELECT COUNT(*) FROM attendance WHERE employee_id=?", (eid,)).fetchone()[0]
                ded = c.execute("SELECT COALESCE(SUM(amount),0) FROM salary_deductions WHERE employee_id=?", (eid,)).fetchone()[0]
                res.append([ename, (days * rate) - ded])
            st.table(pd.DataFrame(res, columns=["الاسم", "المستحق"]))
    st.markdown(footer_html, unsafe_allow_html=True)

# 3. الإيرادات
with tabs[2]:
    pwd = st.text_input("الباسورد", type="password", key="ord_p")
    if pwd == ORDERS_PASSWORD:
        with st.form("ord_f", clear_on_submit=True):
            c1, c2 = st.columns([3, 1])
            o_name = c1.text_input("الوصف")
            o_price = c2.number_input("السعر", min_value=0)
            if st.form_submit_button("إضافة"):
                c.execute("INSERT INTO daily_orders (order_name,price,date) VALUES (?,?,?)", (o_name, o_price, dt_date.today().strftime("%Y-%m-%d")))
                conn.commit(); st.rerun()

        st.markdown("---")
        c.execute("SELECT order_name, price FROM daily_orders WHERE date=?", (dt_date.today().strftime("%Y-%m-%d"),))
        data = c.fetchall()
        st.dataframe(pd.DataFrame(data, columns=["الأوردر", "السعر"]), use_container_width=True)
        st.metric("دخل اليوم", f"{sum(o[1] for o in data)} ج.م")
    st.markdown(footer_html, unsafe_allow_html=True)

# 4. الإدارة
with tabs[3]:
    pwd = st.text_input("الباسورد", type="password", key="adm_p")
    if pwd == ADMIN_PASSWORD:
        st.write("📋 **سجل الحجوزات**")
        df_b = pd.read_sql("SELECT name, phone, address, date FROM bookings ORDER BY date DESC", conn)
        st.dataframe(df_b, use_container_width=True)
        if st.button("🗑️ مسح الكل"): c.execute("DELETE FROM bookings"); conn.commit(); st.rerun()
    st.markdown(footer_html, unsafe_allow_html=True)