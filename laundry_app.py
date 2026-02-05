import streamlit as st
from datetime import date as dt_date
import sqlite3
import pandas as pd

# ---------------- إعداد الصفحة ----------------
st.set_page_config(
    page_title="🧼 مغسلة المتحدة - نسخة البشمهندس مصطفى",
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

# ---------------- الستايل المريح والواضح ----------------
st.markdown(f"""
<style>
/* خلفية مريحة وفخمة */
.stApp {{
    background-color: #0b1120; /* أزرق داكن جداً مريح للعين */
    color: #ffffff;
}}

/* تعديل وضوح النصوص في الكروت */
div[data-testid="stForm"], 
div[data-testid="stVerticalBlock"] > div {{
    background: rgba(255, 255, 255, 0.1) !important;
    border-radius: 20px !important;
    border: 2px solid #FFD700; /* إطار ذهبي واضح */
    padding: 30px !important;
    box-shadow: 0 4px 15px rgba(0,0,0,0.5);
}}

/* تقوية الخطوط وجعلها واضحة */
h1, h2, h3, label, p, span, .stMarkdown {{
    color: #ffffff !important;
    font-weight: 900 !important; /* خط سميك جداً */
    font-family: 'Cairo', sans-serif;
}}

/* الهيدر العلوي */
.header-box {{
    text-align: center;
    padding: 30px;
    background: #1a2234;
    border-radius: 25px;
    border-bottom: 5px solid #FFD700;
    margin-bottom: 30px;
}}

.phone-style {{
    background: #FFD700;
    color: #000000 !important;
    padding: 8px 20px;
    border-radius: 10px;
    font-size: 22px;
    display: inline-block;
    margin-top: 10px;
}}

/* التوقيع السفلي */
.footer-signature {{
    text-align: center;
    padding: 20px;
    margin-top: 50px;
    border-top: 1px solid rgba(255,215,0,0.3);
    color: #FFD700 !important;
    font-size: 18px;
    font-weight: bold;
}}

/* الأزرار */
.stButton > button {{
    background-color: #FFD700 !important;
    color: #000000 !important;
    font-weight: bold !important;
    border-radius: 12px !important;
    width: 100%;
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
<div class="header-box">
    <h1 style="font-size: 45px;">🌙 مغسلة المتحدة للسجاد 🌙</h1>
    <h3 style="color: #FFD700 !important;">📍 {CONTACT_ADDRESS}</h3>
    <div class="phone-style">📞 الحجز والاستعلام: {CONTACT_PHONE}</div>
</div>
""", unsafe_allow_html=True)

# ---------------- التبويبات ----------------
tabs = st.tabs(["📝 تسجيل حجز", "👷 حسابات الموظفين", "📦 أوردرات اليوم", "🔐 لوحة الإدارة"])

# توقيع البشمهندس مصطفى الفيشاوي (سيظهر في كل صفحة بالأسفل)
footer_html = f"""<div class="footer-signature">🚀 إشراف وتطوير: البشمهندس مصطفى الفيشاوى 🚀</div>"""

# 1. تسجيل حجز
with tabs[0]:
    with st.form("booking"):
        st.subheader("إضافة أوردر جديد")
        name = st.text_input("اسم العميل (واضح)")
        phone = st.text_input("رقم الهاتف")
        addr = st.text_input("عنوان العميل")
        b_date = st.date_input("تاريخ الحجز")
        slot = st.radio("الفترة", ["صباحًا", "مساءً"], horizontal=True)
        if st.form_submit_button("حفظ البيانات ✅"):
            if name and phone:
                c.execute("INSERT INTO bookings (name,address,phone,date,time_slot) VALUES (?,?,?,?,?)", (name, addr, phone, b_date.strftime("%Y-%m-%d"), slot))
                conn.commit(); st.success("تم الحفظ بنجاح")
    st.markdown(footer_html, unsafe_allow_html=True)

# 2. حسابات الموظفين
with tabs[1]:
    if st.text_input("باسورد الموظفين", type="password", key="p1") == EMP_PASSWORD:
        c.execute("SELECT id, name, daily_rate FROM employees")
        emps = c.fetchall()
        st.subheader("✅ تحضير اليوم")
        sel_ids = []
        cols = st.columns(3)
        for i, (eid, ename, rate) in enumerate(emps):
            if cols[i%3].checkbox(f"حضر: {ename}", key=f"e_{eid}"): sel_ids.append(eid)
        
        if st.button("تأكيد الحضور"):
            for eid in sel_ids:
                c.execute("INSERT INTO attendance (employee_id, date) VALUES (?,?)", (eid, dt_date.today().strftime("%Y-%m-%d")))
            conn.commit(); st.rerun()

        st.divider()
        st.subheader("📊 الرواتب والخصومات")
        rows = []
        for eid, ename, rate in emps:
            days = c.execute("SELECT COUNT(*) FROM attendance WHERE employee_id=?", (eid,)).fetchone()[0]
            deds = c.execute("SELECT COALESCE(SUM(amount),0) FROM salary_deductions WHERE employee_id=?", (eid,)).fetchone()[0]
            rows.append([ename, days, rate, deds, (days*rate)-deds])
        st.table(pd.DataFrame(rows, columns=["الموظف", "أيام الحضور", "اليومية", "الخصومات", "الصافي"]))
        
        with st.expander("➕ إضافة خصم"):
            t = st.selectbox("الموظف", [e[1] for e in emps])
            a = st.number_input("المبلغ", min_value=0)
            if st.button("حفظ الخصم"):
                eid = next(e[0] for e in emps if e[1] == t)
                c.execute("INSERT INTO salary_deductions (employee_id, amount, date) VALUES (?,?,?)", (eid, a, dt_date.today().strftime("%Y-%m-%d")))
                conn.commit(); st.rerun()
    st.markdown(footer_html, unsafe_allow_html=True)

# 3. أوردرات اليوم
with tabs[2]:
    if st.text_input("باسورد الأوردرات", type="password", key="p2") == ORDERS_PASSWORD:
        with st.form("ords"):
            n = st.text_input("نوع الأوردر")
            p = st.number_input("السعر", min_value=0)
            if st.form_submit_button("إضافة"):
                c.execute("INSERT INTO daily_orders (order_name, price, date) VALUES (?,?,?)", (n, p, dt_date.today().strftime("%Y-%m-%d")))
                conn.commit(); st.rerun()
        
        data = c.execute("SELECT id, order_name, price FROM daily_orders WHERE date=?", (dt_date.today().strftime("%Y-%m-%d"),)).fetchall()
        for rid, name, price in data:
            col1, col2, col3 = st.columns([4,2,1])
            col1.write(f"**{name}**"); col2.write(f"**{price} ج**")
            if col3.button("❌", key=f"r_{rid}"):
                c.execute("DELETE FROM daily_orders WHERE id=?", (rid,)); conn.commit(); st.rerun()
        st.subheader(f"💰 إجمالي اليوم: {sum(r[2] for r in data)} جنيه")
    st.markdown(footer_html, unsafe_allow_html=True)

# 4. لوحة الإدارة
with tabs[3]:
    if st.text_input("باسورد المسؤول", type="password", key="p3") == ADMIN_PASSWORD:
        st.subheader("📋 كشف الحجوزات")
        st.dataframe(pd.read_sql("SELECT * FROM bookings", conn), use_container_width=True)
        if st.button("⚠️ تصفير الحضور والخصومات"):
            c.execute("DELETE FROM attendance"); c.execute("DELETE FROM salary_deductions"); conn.commit(); st.rerun()
    st.markdown(footer_html, unsafe_allow_html=True)