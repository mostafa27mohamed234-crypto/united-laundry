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

# ---------------- الستايل المطور (ألوان فاتحة وواضحة) ----------------
st.markdown(f"""
<style>
/* تفتيح الخطوط الأساسية */
@import url('https://fonts.googleapis.com/css2?family=Cairo:wght@600;800&display=swap');

.stApp {{
    background-color: #080c16;
    background-image: url("https://www.transparenttextures.com/patterns/stardust.png");
    font-family: 'Cairo', sans-serif;
}}

/* الأسماء والعناوين باللون الأبيض الساطع */
h1, h2, h3, h4, h5, h6, .stMarkdown p, label {{
    color: #FFFFFF !important;
    text-shadow: 1px 1px 2px rgba(0,0,0,0.5);
    font-weight: 800 !important;
}}

/* لون الذهب الساطع للأسماء الهامة */
.highlight-text {{
    color: #FFD700 !important;
    font-weight: bold;
}}

/* تعديل شكل حقول الإدخال لتكون فاتحة النصوص */
.stTextInput input, .stNumberInput input, .stDateInput input, .stSelectbox div[data-baseweb="select"] {{
    background-color: rgba(30, 45, 80, 0.9) !important;
    color: #FFFFFF !important; /* نص أبيض ساطع داخل الحقل */
    border: 1px solid #FFD700 !important;
    font-weight: bold !important;
}}

/* تعديل شكل الراديو (الفترة صباحاً ومساءً) */
div[data-testid="stMarkdownContainer"] p {{
    color: #FFFFFF !important;
    font-size: 16px !important;
}}

/* الكروت */
div[data-testid="stForm"], 
div[data-testid="stVerticalBlock"] > div {{
    background: rgba(255, 255, 255, 0.1) !important;
    border-radius: 15px !important;
    border: 1px solid #FFD700 !important;
    padding: 15px !important;
}}

/* الأزرار بذهبي ساطع */
.stButton > button {{
    background: linear-gradient(90deg, #FFE44D 0%, #FFB900 100%) !important;
    color: #000000 !important;
    font-weight: 900 !important;
    border-radius: 10px !important;
    border: none !important;
    box-shadow: 0 4px 15px rgba(255, 215, 0, 0.3);
}}

/* نصوص الجداول باللون الأبيض */
.stTable td, .stTable th, div[data-testid="stDataFrame"] td {{
    color: #FFFFFF !important;
    font-weight: bold !important;
}}

.footer-signature {{
    text-align: center;
    padding: 15px;
    color: #FFD700 !important;
    font-size: 15px;
    font-weight: bold;
    background: rgba(0,0,0,0.3);
    border-radius: 10px;
}}
</style>
""", unsafe_allow_html=True)

# ---------------- الهيدر ----------------
st.markdown(f"""
<div style="text-align: center; background: rgba(255,255,255,0.05); padding: 15px; border-radius: 20px; border-bottom: 4px solid #FFD700; margin-bottom: 20px;">
    <h1 style="margin:0; color:#FFD700 !important; font-size: 40px;">🌟 مغسلة المتحدة 🌟</h1>
    <h2 style="margin:0; color:#FFFFFF !important;">🌙 رمضان كريم 🕌</h2>
    <p style="margin:5px 0; color:#E0E0E0 !important; font-size:16px;">📍 {CONTACT_ADDRESS} | 📞 {CONTACT_PHONE}</p>
</div>
""", unsafe_allow_html=True)

# ---------------- التبويبات ----------------
tabs = st.tabs(["📝 تسجيل الحجوزات", "👷 حسابات الموظفين", "💰 إيرادات اليوم", "🔐 لوحة الإدارة"])
footer_html = f"""<div class="footer-signature">🚀 تم التطوير بواسطة: البشمهندس مصطفى الفيشاوي 🚀</div>"""

# 1. تسجيل الحجوزات
with tabs[0]:
    with st.form("booking_form", clear_on_submit=True):
        st.markdown("<h3 style='color:#FFD700;'>بيانات العميل</h3>", unsafe_allow_html=True)
        c1, c2, c3 = st.columns(3)
        name = c1.text_input("اسم العميل")
        phone = c2.text_input("رقم الموبايل")
        addr = c3.text_input("العنوان")
        
        c4, c5 = st.columns([2, 1])
        b_date = c4.date_input("تاريخ الحجز", dt_date.today())
        time_slot = c5.radio("الفترة الزمنية", ["صباحًا", "مساءً"], horizontal=True)
        
        if st.form_submit_button("تأكيد وحفظ الحجز ✨"):
            if name and phone:
                c.execute("INSERT INTO bookings (name,address,phone,date,time_slot) VALUES (?,?,?,?,?)", 
                          (name, addr, phone, b_date.strftime("%Y-%m-%d"), time_slot))
                conn.commit(); st.success("✅ تم حفظ البيانات بنجاح!")
            else: st.error("الرجاء إكمال الاسم ورقم الهاتف")
    st.markdown(footer_html, unsafe_allow_html=True)

# 2. حسابات الموظفين
with tabs[1]:
    pwd = st.text_input("كلمة السر الخاصة بالموظفين", type="password", key="emp_p")
    if pwd == EMP_PASSWORD:
        c.execute("SELECT id, name, daily_rate FROM employees")
        emps = c.fetchall()
        
        st.markdown("<h3 style='color:#FFD700;'>تسجيل الحضور اليومي</h3>", unsafe_allow_html=True)
        cols = st.columns(len(emps))
        for i, (eid, ename, rate) in enumerate(emps):
            if cols[i].checkbox(f"**{ename}**", key=f"at_{eid}"):
                c.execute("SELECT 1 FROM attendance WHERE employee_id=? AND date=?", (eid, dt_date.today().strftime("%Y-%m-%d")))
                if not c.fetchone():
                    c.execute("INSERT INTO attendance (employee_id, date) VALUES (?,?)", (eid, dt_date.today().strftime("%Y-%m-%d")))
        if st.button("تأكيد سجل الحضور"): conn.commit(); st.success("تم تسجيل الحضور")

        st.markdown("---")
        c1, c2 = st.columns([1, 1])
        with c1:
            st.markdown("<h3 style='color:#FFD700;'>💸 سلف وخصومات</h3>", unsafe_allow_html=True)
            target = st.selectbox("اختر الموظف", [e[1] for e in emps])
            amt = st.number_input("المبلغ (ج.م)", min_value=0)
            if st.button("تأكيد الخصم"):
                eid = next(e[0] for e in emps if e[1] == target)
                c.execute("INSERT INTO salary_deductions (employee_id, amount, date) VALUES (?,?,?)", (eid, amt, dt_date.today().strftime("%Y-%m-%d")))
                conn.commit(); st.success(f"تم خصم {amt} من {target}"); st.rerun()
        with c2:
            st.markdown("<h3 style='color:#FFD700;'>🧾 صافي المستحقات</h3>", unsafe_allow_html=True)
            res = []
            for eid, ename, rate in emps:
                days = c.execute("SELECT COUNT(*) FROM attendance WHERE employee_id=?", (eid,)).fetchone()[0]
                ded = c.execute("SELECT COALESCE(SUM(amount),0) FROM salary_deductions WHERE employee_id=?", (eid,)).fetchone()[0]
                res.append([ename, f"{days} أيام", f"{(days * rate) - ded} ج.م"])
            st.table(pd.DataFrame(res, columns=["اسم الموظف", "الحضور", "المبلغ المتبقي"]))
    st.markdown(footer_html, unsafe_allow_html=True)

# 3. إيرادات اليوم
with tabs[2]:
    pwd = st.text_input("كلمة سر الإيرادات", type="password", key="ord_p")
    if pwd == ORDERS_PASSWORD:
        with st.form("ord_f", clear_on_submit=True):
            st.markdown("<h3 style='color:#FFD700;'>إضافة إيراد جديد</h3>", unsafe_allow_html=True)
            c1, c2 = st.columns([3, 1])
            o_name = c1.text_input("وصف الأوردر (مثال: غسيل سجاد فلان)")
            o_price = c2.number_input("المبلغ المستلم", min_value=0)
            if st.form_submit_button("حفظ الإيراد 💰"):
                c.execute("INSERT INTO daily_orders (order_name,price,date) VALUES (?,?,?)", (o_name, o_price, dt_date.today().strftime("%Y-%m-%d")))
                conn.commit(); st.success("تم الحفظ"); st.rerun()

        st.markdown("---")
        c.execute("SELECT order_name, price FROM daily_orders WHERE date=?", (dt_date.today().strftime("%Y-%m-%d"),))
        data = c.fetchall()
        st.markdown("<h3 style='color:#FFD700;'>كشف إيرادات اليوم</h3>", unsafe_allow_html=True)
        st.dataframe(pd.DataFrame(data, columns=["الوصف", "السعر"]), use_container_width=True)
        st.metric("إجمالي دخل اليوم", f"{sum(o[1] for o in data)} ج.م")
    st.markdown(footer_html, unsafe_allow_html=True)

# 4. لوحة الإدارة
with tabs[3]:
    pwd = st.text_input("كلمة سر المسؤول", type="password", key="adm_p")
    if pwd == ADMIN_PASSWORD:
        st.markdown("<h3 style='color:#FFD700;'>سجل جميع الحجوزات</h3>", unsafe_allow_html=True)
        df_b = pd.read_sql("SELECT name as 'الاسم', phone as 'الموبايل', address as 'العنوان', date as 'التاريخ' FROM bookings ORDER BY date DESC", conn)
        st.dataframe(df_b, use_container_width=True)
        
        if st.button("🗑️ مسح جميع الحجوزات (تفريغ السجل)"):
            c.execute("DELETE FROM bookings"); conn.commit(); st.warning("تم مسح السجل بالكامل"); st.rerun()
    st.markdown(footer_html, unsafe_allow_html=True)