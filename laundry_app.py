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
/* خلفية رمضان الفخمة */
.stApp {{
    background-color: #0d1222; /* أزرق داكن جداً */
    background-image: url("https://www.transparenttextures.com/patterns/stardust.png"); /* نجوم خفيفة */
    background-size: cover;
    background-attachment: fixed;
    color: #ffffff;
}}

/* تصميم الكروت الشفافة */
div[data-testid="stForm"], 
div[data-testid="stVerticalBlock"] > div {{
    background: rgba(255, 255, 255, 0.08) !important;
    border-radius: 25px !important;
    border: 2px solid #FFD700; /* إطار ذهبي */
    padding: 30px !important;
    box-shadow: 0 6px 20px rgba(0,0,0,0.4);
    margin-bottom: 25px !important; /* مسافة أفضل بين الكروت */
}}

/* تقوية الخطوط */
h1, h2, h3, label, p, span, .stMarkdown, .stTable .header {{
    color: #ffffff !important;
    font-weight: bold !important;
    font-family: 'Cairo', sans-serif;
}}

/* هيدر الصفحة الرئيسي */
.main-header-box {{
    text-align: center;
    padding: 35px;
    background: #1a233a; /* خلفية أغمق للهيدر */
    border-radius: 30px;
    border-bottom: 6px solid #FFD700;
    margin-bottom: 40px;
    box-shadow: 0 0 30px rgba(255,215,0,0.3);
}}

/* تصميم "رمضان كريم" المزينة */
.ramadan-greeting {{
    font-size: 38px;
    color: #FFD700 !important; /* ذهبي متوهج */
    font-weight: 900 !important;
    text-shadow: 0 0 15px rgba(255,215,0,0.8);
    margin-top: 20px;
    margin-bottom: 10px;
    letter-spacing: 2px;
}}

.ramadan-icons {{
    font-size: 45px;
    color: #FFD700;
    vertical-align: middle;
    margin: 0 10px;
}}

.phone-badge-style {{
    background: linear-gradient(90deg, #FFD700, #FFA500);
    color: #000000 !important;
    padding: 10px 25px;
    border-radius: 30px;
    font-size: 20px;
    font-weight: bold;
    display: inline-block;
    margin-top: 15px;
    box-shadow: 0 0 15px rgba(255,215,0,0.5);
}}

/* الأزرار العصرية */
.stButton > button {{
    background: linear-gradient(90deg, #FFD700 0%, #FFA500 100%) !important;
    color: #1a233a !important; /* لون غامق للنص على الذهبي */
    font-weight: bold !important;
    border-radius: 12px !important;
    padding: 10px 20px !important;
    transition: all 0.3s ease !important;
    border: none !important;
    box-shadow: 0 4px 10px rgba(0,0,0,0.3);
}}
.stButton > button:hover {{
    transform: translateY(-2px);
    box-shadow: 0 6px 15px rgba(255,215,0,0.6);
}}

/* التوقيع السفلي */
.footer-signature {{
    text-align: center;
    padding: 25px;
    margin-top: 60px; /* مسافة أكبر */
    border-top: 1px solid rgba(255,215,0,0.2);
    color: #FFD700 !important;
    font-size: 17px;
    font-weight: bold;
}}

/* تعديل شكل التبويبات */
.stTabs [data-baseweb="tab-list"] {{
    gap: 15px; /* مسافة أكبر بين التبويبات */
    background: rgba(255, 255, 255, 0.05);
    border-radius: 15px;
    padding: 5px;
}}
.stTabs [data-baseweb="tab"] {{
    background-color: rgba(255, 215, 0, 0.15) !important;
    border-radius: 12px !important;
    color: #FFD700 !important;
    font-weight: bold !important;
    padding: 10px 25px;
}}
.stTabs [data-baseweb="tab"]:hover {{
    background-color: rgba(255, 215, 0, 0.3) !important;
}}
.stTabs [aria-selected="true"] {{
    background-color: #FFD700 !important; /* لون التبويب النشط */
    color: #1a233a !important; /* نص غامق على التبويب النشط */
    box-shadow: 0 0 10px rgba(255,215,0,0.5);
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

# الموظفين الافتراضيين
employees_data = [("مصطفى الفيشاوى", 100), ("وليد المالكي", 150), ("ابراهيم بكير", 150)]
for name, rate in employees_data:
    c.execute("SELECT id FROM employees WHERE name=?", (name,))
    if not c.fetchone():
        c.execute("INSERT INTO employees (name,daily_rate) VALUES (?,?)", (name, rate))
conn.commit()

# ---------------- الهيدر الرئيسي مع "رمضان كريم" المزينة ----------------
st.markdown(f"""
<div class="main-header-box">
    <h1 style="font-size: 55px;">🌟 مغسلة المتحدة 🌟</h1>
    <p style="font-size: 22px; margin-top: -10px;">📍 {CONTACT_ADDRESS}</p>
    <div class="phone-badge-style">📞 للتواصل والحجز: {CONTACT_PHONE}</div>
    <div class="ramadan-greeting">
        <span class="ramadan-icons">🌙</span> رمضان كريم <span class="ramadan-icons">🕌</span>
    </div>
</div>
""", unsafe_allow_html=True)

# ---------------- التبويبات ----------------
tabs = st.tabs(["📝 تسجيل حجز", "👷 حسابات الموظفين", "📦 أوردرات اليوم", "🔐 لوحة الإدارة"])

# توقيع البشمهندس مصطفى الفيشاوي (سيظهر في كل صفحة بالأسفل)
footer_html = f"""<div class="footer-signature">🚀 إشراف وتطوير: البشمهندس مصطفى الفيشاوي 🚀</div>"""

# 1. تسجيل حجز
with tabs[0]:
    with st.form("booking_form"):
        st.subheader("إضافة أوردر حجز جديد")
        col1, col2 = st.columns(2)
        name = col1.text_input("اسم العميل")
        phone = col2.text_input("رقم الهاتف")
        addr = st.text_input("عنوان العميل بالتفصيل")
        b_date = st.date_input("تاريخ الحجز", dt_date.today())
        time_slot = st.radio("الفترة الزمنية", ["صباحًا", "مساءً"], horizontal=True)
        if st.form_submit_button("تأكيد وحفظ الحجز ✨"):
            if name and phone:
                c.execute("INSERT INTO bookings (name,address,phone,date,time_slot) VALUES (?,?,?,?,?)", 
                          (name, addr, phone, b_date.strftime("%Y-%m-%d"), time_slot))
                conn.commit(); st.success("✅ تم حفظ طلب الحجز بنجاح!")
            else:
                st.error("الرجاء إدخال الاسم ورقم الهاتف على الأقل.")
    st.markdown(footer_html, unsafe_allow_html=True)

# 2. حسابات الموظفين
with tabs[1]:
    password = st.text_input("كلمة سر الموظفين", type="password", key="emp_password_key")
    if password == EMP_PASSWORD:
        c.execute("SELECT id, name, daily_rate FROM employees")
        emps = c.fetchall()
        
        st.subheader("✅ تسجيل حضور اليوم")
        selected_ids = []
        cols = st.columns(3)
        for i, (eid, ename, rate) in enumerate(emps):
            if cols[i % 3].checkbox(f"حضر: **{ename}**", key=f"att_emp_{eid}"):
                selected_ids.append(eid)
        
        if st.button("حفظ سجل الحضور 📝"):
            for eid in selected_ids:
                c.execute("SELECT 1 FROM attendance WHERE employee_id=? AND date=?", (eid, dt_date.today().strftime("%Y-%m-%d")))
                if not c.fetchone():
                    c.execute("INSERT INTO attendance (employee_id, date) VALUES (?,?)", (eid, dt_date.today().strftime("%Y-%m-%d")))
            conn.commit(); st.success("الحضور تم تسجيله!")
            st.rerun()

        st.markdown("---")
        st.subheader("💸 الخصومات والسلف")
        with st.expander("➕ إضافة خصم / سلفة لموظف"):
            target_emp = st.selectbox("اختر الموظف", [e[1] for e in emps])
            deduct_amt = st.number_input("المبلغ المطلوب خصمه (جنيه)", min_value=0)
            deduct_reason = st.text_input("سبب الخصم (اختياري)")
            if st.button("تأكيد الخصم"):
                if deduct_amt > 0:
                    emp_id_to_deduct = next(e[0] for e in emps if e[1] == target_emp)
                    c.execute("INSERT INTO salary_deductions (employee_id, amount, reason, date) VALUES (?,?,?,?)",
                              (emp_id_to_deduct, deduct_amt, deduct_reason, dt_date.today().strftime("%Y-%m-%d")))
                    conn.commit(); st.success(f"تم خصم {deduct_amt} جنيه من {target_emp}")
                    st.rerun()

        st.markdown("---")
        st.subheader("📊 كشف حساب الرواتب النهائي")
        rows = []
        for emp_id, emp_name, rate in emps:
            days = c.execute("SELECT COUNT(*) FROM attendance WHERE employee_id=?", (emp_id,)).fetchone()[0]
            total_deduct = c.execute("SELECT COALESCE(SUM(amount),0) FROM salary_deductions WHERE employee_id=?", (emp_id,)).fetchone()[0]
            final_salary = (days * rate) - total_deduct
            rows.append([emp_name, days, rate, total_deduct, final_salary])
        
        df_salaries = pd.DataFrame(rows, columns=["اسم الموظف", "أيام الحضور", "اليومية", "إجمالي الخصم", "المرتب المستحق"])
        st.dataframe(df_salaries, use_container_width=True)
    st.markdown(footer_html, unsafe_allow_html=True)

# 3. أوردرات اليوم
with tabs[2]:
    password = st.text_input("كلمة سر الأوردرات", type="password", key="orders_password_key")
    if password == ORDERS_PASSWORD:
        st.subheader("➕ إضافة أوردر إيراد جديد")
        with st.form("order_form"):
            order_name = st.text_input("وصف الأوردر")
            price = st.number_input("السعر المستلم (جنيه)", min_value=0)
            if st.form_submit_button("حفظ الأوردر 💰"):
                if order_name and price > 0:
                    c.execute("INSERT INTO daily_orders (order_name,price,date) VALUES (?,?,?)", (order_name, price, dt_date.today().strftime("%Y-%m-%d")))
                    conn.commit(); st.success("✅ تم إضافة الأوردر")
                    st.rerun()
                else:
                    st.error("الرجاء إدخال وصف وسعر صحيح للأوردر.")

        st.markdown("---")
        st.subheader("📋 كشف أوردرات اليوم")
        c.execute("SELECT id, order_name, price FROM daily_orders WHERE date=?", (dt_date.today().strftime("%Y-%m-%d"),))
        day_orders = c.fetchall()
        total_day = sum(o[2] for o in day_orders)
        
        for oid, n, p in day_orders:
            col1, col2, col3 = st.columns([4,2,1])
            col1.write(f"🏷️ **{n}**")
            col2.write(f"💰 **{p} جنيه**")
            if col3.button("❌", key=f"del_ord_{oid}"):
                c.execute("DELETE FROM daily_orders WHERE id=?", (oid,))
                conn.commit(); st.rerun()
        st.markdown(f"## 💵 إجمالي دخل اليوم: `{total_day}` جنيه")
    st.markdown(footer_html, unsafe_allow_html=True)

# 4. لوحة الإدارة (المسؤول)
with tabs[3]:
    password = st.text_input("كلمة سر لوحة الإدارة", type="password", key="admin_password_key")
    if password == ADMIN_PASSWORD:
        st.subheader("📊 جميع حجوزات العملاء")
        df_bookings = pd.read_sql("SELECT name as 'اسم العميل', address as 'العنوان', phone as 'رقم الهاتف', date as 'تاريخ الحجز', time_slot as 'الفترة' FROM bookings ORDER BY date DESC", conn)
        st.dataframe(df_bookings, use_container_width=True)

        st.markdown("---")
        st.subheader("🧹 أدوات الصيانة والمسح")
        col_clear1, col_clear2 = st.columns(2)
        with col_clear1:
            if st.button("⚠️ تصفير سجلات الموظفين (لشهر جديد)"):
                c.execute("DELETE FROM attendance"); c.execute("DELETE FROM salary_deductions")
                conn.commit(); st.warning("تم مسح حضور وخصومات الموظفين!")
                st.rerun()
        with col_clear2:
            if st.button("🗑️ مسح جميع بيانات الحجوزات"):
                c.execute("DELETE FROM bookings")
                conn.commit(); st.warning("تم مسح جميع الحجوزات!")
                st.rerun()
    st.markdown(footer_html, unsafe_allow_html=True)