import streamlit as st
from datetime import date as dt_date
import sqlite3
import pandas as pd

# ---------------- إعداد الصفحة ----------------
st.set_page_config(
    page_title="المتحدة - رمضان كريم",
    page_icon="🌙",
    layout="wide"
)

# ---------------- توحيد كلمات السر ----------------
SHARED_PASSWORD = "المتحده@1996"
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

# ---------------- الستايل المطور الأصلي ----------------
st.markdown(f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Cairo:wght@600;800&display=swap');

.stApp {{
    background-color: #080c16;
    background-image: url("https://www.transparenttextures.com/patterns/stardust.png");
    font-family: 'Cairo', sans-serif;
}}

h1, h2, h3, label, p {{
    color: #FFFFFF !important;
    font-weight: 800 !important;
}}

.stTextInput input, .stNumberInput input, .stDateInput input, .stSelectbox div[data-baseweb="select"] {{
    background-color: rgba(30, 45, 80, 0.9) !important;
    color: #FFFFFF !important;
    border: 1px solid #FFD700 !important;
}}

div[data-testid="stForm"], 
div[data-testid="stVerticalBlock"] > div {{
    background: rgba(255, 255, 255, 0.1) !important;
    border-radius: 15px !important;
    border: 1px solid #FFD700 !important;
    padding: 15px !important;
}}

div[data-testid="stFormSubmitButton"] button {{
    background: linear-gradient(90deg, #39FF14 0%, #00FF7F 100%) !important;
    color: #000000 !important;
    font-size: 22px !important;
    font-weight: 900 !important;
    border-radius: 50px !important;
    border: none !important;
    height: 60px !important;
    width: 100% !important;
    box-shadow: 0 0 20px rgba(57, 255, 20, 0.4) !important;
    transition: all 0.4s ease-in-out !important;
}}

.stButton > button {{
    background: #FFD700 !important;
    color: #000000 !important;
    font-weight: bold !important;
    border-radius: 10px !important;
}}

.footer-signature {{
    text-align: center;
    padding: 15px;
    color: #FFD700 !important;
    font-weight: bold;
    border-top: 1px solid rgba(255, 215, 0, 0.1);
}}

.countdown-container {{
    background: linear-gradient(90deg, #1e2d50 0%, #080c16 100%); 
    padding: 20px; 
    border-radius: 15px; 
    border: 2px solid #39FF14; 
    text-align: center; 
    margin-bottom: 25px; 
    box-shadow: 0 0 15px rgba(57, 255, 20, 0.3);
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
<div style="text-align: center; border-bottom: 3px solid #FFD700; margin-bottom: 20px;">
    <h1 style="color:#FFD700 !important; font-size: 45px; margin:0;">🌟 مغسلة المتحدة 🌟</h1>
    <h2 style="margin:0;">🌙 رمضان كريم 🕌</h2>
    <p style="font-size:16px;">📍 {CONTACT_ADDRESS} | 📞 {CONTACT_PHONE}</p>
</div>
""", unsafe_allow_html=True)

# ---------------- عداد الأيام ----------------
target_date = dt_date(2026, 3, 10)
days_left = (target_date - dt_date.today()).days

if days_left >= 0:
    st.markdown(f"""
    <div class="countdown-container">
        <h3 style="margin:0; color:#39FF14 !important;">⏳ متبقي على غلق باب الحجوزات</h3>
        <h1 style="margin:0; font-size: 55px; color:#FFFFFF !important;">{days_left} يوم</h1>
        <p style="margin:0; color:#FFD700 !important;">آخر موعد متاح للحجز هو 10 مارس 2026</p>
    </div>
    """, unsafe_allow_html=True)
else:
    st.markdown("""<div style="background: rgba(255, 0, 0, 0.2); padding: 20px; border-radius: 15px; border: 2px solid #FF0000; text-align: center; margin-bottom: 25px;"><h2 style="margin:0; color:#FF0000 !important;">🚫 نعتذر، تم غلق باب الحجوزات</h2></div>""", unsafe_allow_html=True)

# ---------------- التبويبات ----------------
tabs = st.tabs(["📝 تسجيل الحجوزات", "👷 الموظفين", "💰 الإيرادات", "🔐 الإدارة"])
footer_html = f"""<div class="footer-signature">🚀 تطوير: البشمهندس مصطفى الفيشاوي 🚀</div>"""

# 1. تسجيل الحجوزات
with tabs[0]:
    if dt_date.today() <= target_date:
        with st.form("booking_form", clear_on_submit=True):
            st.markdown("<h3 style='color:#FFD700;'>إضافة بيانات الطلب</h3>", unsafe_allow_html=True)
            c1, c2, c3 = st.columns(3)
            name, phone, addr = c1.text_input("اسم العميل"), c2.text_input("رقم الموبايل"), c3.text_input("العنوان / التفاصيل")
            c4, c5 = st.columns([2, 1])
            b_date = c4.date_input("تاريخ الحجز", dt_date.today(), max_value=target_date)
            time_slot = c5.radio("وقت الحضور", ["صباحًا", "مساءً"], horizontal=True)
            if st.form_submit_button("تأكيد وحفظ الأوردر الآن ✅"):
                if name and phone:
                    c.execute("INSERT INTO bookings (name,address,phone,date,time_slot) VALUES (?,?,?,?,?)", (name, addr, phone, b_date.strftime("%Y-%m-%d"), time_slot))
                    conn.commit(); st.success("🎉 تم تسجيل الأوردر بنجاح!")
    st.markdown(footer_html, unsafe_allow_html=True)

# 2. الموظفين
with tabs[1]:
    pwd = st.text_input("كلمة السر", type="password", key="emp_p")
    if pwd == SHARED_PASSWORD:
        with st.expander("➕ إدارة الموظفين"):
            c_a, c_d = st.columns(2)
            new_n = c_a.text_input("اسم الموظف")
            new_r = c_a.number_input("اليومية", min_value=0)
            if c_a.button("حفظ الموظف"):
                c.execute("INSERT INTO employees (name, daily_rate) VALUES (?,?)", (new_n, new_r))
                conn.commit(); st.rerun()
        
        st.markdown("---")
        # التعديل المطلوب: اختيار اليوم
        att_day = st.date_input("📅 اختر يوم الحضور", dt_date.today())
        day_str = att_day.strftime("%Y-%m-%d")

        c.execute("SELECT id, name, daily_rate FROM employees")
        emps = c.fetchall()
        if emps:
            st.write(f"📊 **دفتر الحضور لـ {day_str}**")
            c.execute("SELECT employee_id FROM attendance WHERE date=?", (day_str,))
            p_ids = [r[0] for r in c.fetchall()]
            
            with st.form("att_form"):
                cols = st.columns(len(emps))
                at_list = []
                for i, (eid, ename, rate) in enumerate(emps):
                    if cols[i].checkbox(f"{ename}", value=(eid in p_ids), key=f"at_{eid}"): at_list.append(eid)
                if st.form_submit_button("حفظ الحضور"):
                    c.execute("DELETE FROM attendance WHERE date=?", (day_str,))
                    for eid in at_list: c.execute("INSERT INTO attendance (employee_id, date) VALUES (?,?)", (eid, day_str))
                    conn.commit(); st.success("تم الحفظ")

            st.markdown("---")
            c1, c2 = st.columns(2)
            with c1:
                st.write("💸 **سلفيات**")
                target = st.selectbox("الموظف", [e[1] for e in emps])
                amt = st.number_input("المبلغ", min_value=0)
                reason = st.text_input("السبب")
                if st.button("خصم المبلغ"):
                    eid = next(e[0] for e in emps if e[1] == target)
                    c.execute("INSERT INTO salary_deductions (employee_id, amount, reason, date) VALUES (?,?,?,?)", (eid, amt, reason, day_str))
                    conn.commit(); st.rerun()
            with c2:
                st.write("🧾 **الحسابات**")
                res = []
                for eid, ename, rate in emps:
                    days = c.execute("SELECT COUNT(*) FROM attendance WHERE employee_id=?", (eid,)).fetchone()[0]
                    ded = c.execute("SELECT COALESCE(SUM(amount),0) FROM salary_deductions WHERE employee_id=?", (eid,)).fetchone()[0]
                    res.append([ename, f"{days} يوم", f"{(days * rate) - ded} ج.م", day_str])
                st.table(pd.DataFrame(res, columns=["الاسم", "الأيام", "باقي له", "التاريخ"]))
    st.markdown(footer_html, unsafe_allow_html=True)

# 3. الإيرادات
with tabs[2]:
    pwd = st.text_input("الباسورد", type="password", key="ord_p")
    if pwd == SHARED_PASSWORD:
        with st.form("ord_f"):
            c1, c2 = st.columns([3, 1])
            o_name, o_price = c1.text_input("بيان الأوردر"), c2.number_input("المبلغ", min_value=0)
            if st.form_submit_button("إضافة للإيراد 💰"):
                c.execute("INSERT INTO daily_orders (order_name,price,date) VALUES (?,?,?)", (o_name, o_price, dt_date.today().strftime("%Y-%m-%d")))
                conn.commit(); st.rerun()
        c.execute("SELECT order_name, price FROM daily_orders WHERE date=?", (dt_date.today().strftime("%Y-%m-%d"),))
        data = c.fetchall()
        st.dataframe(pd.DataFrame(data, columns=["البيان", "السعر"]), use_container_width=True)
        st.metric("إجمالي الخزنة اليوم", f"{sum(o[1] for o in data)} ج.م")
    st.markdown(footer_html, unsafe_allow_html=True)

# 4. الإدارة
with tabs[3]:
    pwd = st.text_input("الباسورد", type="password", key="adm_p")
    if pwd == SHARED_PASSWORD:
        st.subheader("📋 سجل الحجوزات")
        df_b = pd.read_sql("SELECT id, name, phone, address, date FROM bookings ORDER BY id DESC", conn)
        st.dataframe(df_b.drop(columns=['id']), use_container_width=True)
        st.markdown("---")
        st.subheader("🗑️ إدارة المسح")
        c_del1, c_del2 = st.columns(2)
        with c_del1:
            c.execute("SELECT id, name FROM bookings")
            all_b = c.fetchall()
            if all_b:
                opt = {f"{r[1]} (ID: {r[0]})": r[0] for r in all_b}
                sel = st.selectbox("حذف عميل", list(opt.keys()))
                if st.button("حذف العميل"):
                    c.execute("DELETE FROM bookings WHERE id=?", (opt[sel],))
                    conn.commit(); st.rerun()
        with c_del2:
            if st.button("مسح السجل بالكامل"):
                c.execute("DELETE FROM bookings"); conn.commit(); st.rerun()
    st.markdown(footer_html, unsafe_allow_html=True)