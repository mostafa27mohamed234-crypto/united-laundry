import streamlit as st
from datetime import date as dt_date
import sqlite3
import pandas as pd

# ---------------- إعداد الصفحة ----------------
st.set_page_config(
    page_title="المتحدة - الكلاسيكية",
    page_icon="👑",
    layout="wide"
)

# ---------------- توحيد كلمات السر ----------------
SHARED_PASSWORD = "المتحده@1996"
CONTACT_PHONE = "01063316053"
CONTACT_ADDRESS = "الشؤون الاجتماعية"

# ---------------- الستايل الكلاسيك (Royal Classic UI) ----------------
st.markdown(f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Amiri:wght@400;700&family=Cairo:wght@400;700&display=swap');

/* الخلفية العامة باللون الكحلي الملكي الهادئ */
.stApp {{
    background-color: #f4f7f6;
    font-family: 'Cairo', sans-serif;
}}

/* العناوين الرئيسية بلمسة ذهبية وكلاسيكية */
h1, h2, h3 {{
    font-family: 'Amiri', serif;
    color: #1a2a44 !important;
    text-align: center;
}}

/* تنسيق الكروت (البطاقات) */
div[data-testid="stForm"], 
div[data-testid="stVerticalBlock"] > div {{
    background: #ffffff !important;
    border-radius: 8px !important;
    border: 1px solid #d1d5db !important;
    box-shadow: 0 4px 6px rgba(0,0,0,0.05) !important;
    padding: 25px !important;
}}

/* الأزرار الكلاسيكية */
div[data-testid="stFormSubmitButton"] button, .stButton > button {{
    background-color: #1a2a44 !important;
    color: #d4af37 !important; /* لون ذهبي */
    border: 1px solid #d4af37 !important;
    border-radius: 4px !important;
    font-weight: bold !important;
    transition: all 0.3s ease !important;
    width: 100% !important;
}}

div[data-testid="stFormSubmitButton"] button:hover, .stButton > button:hover {{
    background-color: #d4af37 !important;
    color: #1a2a44 !important;
    border: 1px solid #1a2a44 !important;
}}

/* مدخلات البيانات */
input, select, textarea {{
    border-radius: 4px !important;
    border: 1px solid #bfc9d4 !important;
}}

/* الهيدر الكلاسيكي */
.classic-header {{
    background: #1a2a44;
    padding: 30px;
    border-radius: 10px;
    border-bottom: 5px solid #d4af37;
    margin-bottom: 30px;
    color: white;
    text-align: center;
}}

.classic-header h1 {{ color: #d4af37 !important; margin: 0; }}
.classic-header p {{ color: #ffffff !important; margin: 5px 0; opacity: 0.8; }}

/* العداد الكلاسيكي */
.classic-countdown {{
    background: #ffffff;
    border-left: 5px solid #1a2a44;
    padding: 15px;
    margin: 20px 0;
    text-align: right;
    box-shadow: 2px 2px 10px rgba(0,0,0,0.1);
}}

.footer-signature {{
    text-align: center;
    padding: 20px;
    color: #1a2a44;
    font-weight: bold;
    font-family: 'Amiri', serif;
    border-top: 1px solid #d4af37;
    margin-top: 50px;
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

# ---------------- الهيدر الكلاسيكي ----------------
st.markdown(f"""
<div class="classic-header">
    <h1>مغسلة المتحدة - United Laundry</h1>
    <p>بإدارة البشمهندس مصطفى الفيشاوي</p>
    <p style="font-size:14px;">📍 {CONTACT_ADDRESS} | 📞 {CONTACT_PHONE}</p>
</div>
""", unsafe_allow_html=True)

# ---------------- العداد ----------------
target_date = dt_date(2026, 3, 10)
days_left = (target_date - dt_date.today()).days

if days_left >= 0:
    st.markdown(f"""
    <div class="classic-countdown">
        <h4 style="margin:0; color:#1a2a44;">⏳ المتبقي على نهاية فترة الحجز</h4>
        <h2 style="margin:0; text-align:right; color:#d4af37 !important;">{days_left} يوم</h2>
    </div>
    """, unsafe_allow_html=True)

# ---------------- التبويبات ----------------
tabs = st.tabs(["📝 الحجوزات", "👷 الموظفين", "💰 الخزنة", "🔐 الإدارة"])

# 1. تسجيل الحجوزات
with tabs[0]:
    if dt_date.today() <= target_date:
        with st.form("classic_booking", clear_on_submit=True):
            st.markdown("### سجل طلب جديد")
            c1, c2 = st.columns(2)
            name = c1.text_input("اسم العميل")
            phone = c2.text_input("رقم الهاتف")
            addr = st.text_input("العنوان والتفاصيل")
            c3, c4 = st.columns(2)
            b_date = c3.date_input("التاريخ المطلوب", dt_date.today())
            time_s = c4.selectbox("الفترة", ["صباحًا", "مساءً"])
            if st.form_submit_button("إتمام الحجز 🖋️"):
                if name and phone:
                    c.execute("INSERT INTO bookings (name,address,phone,date,time_slot) VALUES (?,?,?,?,?)", (name, addr, phone, b_date.strftime("%Y-%m-%d"), time_s))
                    conn.commit(); st.success("تم الحجز بنجاح")
    else: st.error("فترة الحجز انتهت")

# 2. الموظفين
with tabs[1]:
    pwd = st.text_input("كلمة السر", type="password", key="emp_p")
    if pwd == SHARED_PASSWORD:
        with st.expander("إدارة قاعدة بيانات الموظفين"):
            c1, c2 = st.columns(2)
            with c1:
                n_emp = st.text_input("اسم الموظف")
                r_emp = st.number_input("اليومية", min_value=0)
                if st.button("إضافة"):
                    c.execute("INSERT INTO employees (name, daily_rate) VALUES (?,?)", (n_emp, r_emp))
                    conn.commit(); st.rerun()
            with c2:
                c.execute("SELECT name FROM employees")
                names = [r[0] for r in c.fetchall()]
                if names:
                    d_emp = st.selectbox("حذف موظف", names)
                    if st.button("حذف"):
                        c.execute("DELETE FROM employees WHERE name=?", (d_emp,))
                        conn.commit(); st.rerun()

        st.markdown("---")
        att_date = st.date_input("تاريخ الحضور والغياب", dt_date.today())
        d_str = att_date.strftime("%Y-%m-%d")

        c.execute("SELECT id, name, daily_rate FROM employees")
        emps = c.fetchall()
        if emps:
            st.markdown(f"**كشف حضور يوم: {d_str}**")
            c.execute("SELECT employee_id FROM attendance WHERE date=?", (d_str,))
            p_ids = [r[0] for r in c.fetchall()]
            
            with st.form("att_form"):
                cols = st.columns(len(emps))
                at_list = []
                for i, (eid, ename, rate) in enumerate(emps):
                    if cols[i].checkbox(f"{ename}", value=(eid in p_ids)): at_list.append(eid)
                if st.form_submit_button("حفظ الكشف"):
                    c.execute("DELETE FROM attendance WHERE date=?", (d_str,))
                    for eid in at_list: c.execute("INSERT INTO attendance (employee_id, date) VALUES (?,?)", (eid, d_str))
                    conn.commit(); st.rerun()

            st.markdown("---")
            c1, c2 = st.columns(2)
            with c1:
                st.markdown("### تسجيل سلفية")
                target = st.selectbox("الموظف", [e[1] for e in emps])
                amt = st.number_input("المبلغ", min_value=0)
                if st.button("تأكيد الخصم"):
                    eid = next(e[0] for e in emps if e[1] == target)
                    c.execute("INSERT INTO salary_deductions (employee_id, amount, date) VALUES (?,?,?)", (eid, amt, d_str))
                    conn.commit(); st.success("تم")
            with c2:
                st.markdown("### ملخص الحسابات")
                res = []
                for eid, ename, rate in emps:
                    days = c.execute("SELECT COUNT(*) FROM attendance WHERE employee_id=?", (eid,)).fetchone()[0]
                    ded = c.execute("SELECT COALESCE(SUM(amount),0) FROM salary_deductions WHERE employee_id=?", (eid,)).fetchone()[0]
                    res.append([ename, f"{days} أيام", f"{(days * rate) - ded} ج.م"])
                st.table(pd.DataFrame(res, columns=["الموظف", "العمل", "المستحق"]))

# 3. الخزنة
with tabs[2]:
    pwd = st.text_input("كلمة السر", type="password", key="rev_p")
    if pwd == SHARED_PASSWORD:
        with st.form("rev_f"):
            b, p = st.columns([3, 1])
            desc = b.text_input("بيان الإيراد")
            price = p.number_input("المبلغ", min_value=0)
            if st.form_submit_button("إضافة للخزينة"):
                c.execute("INSERT INTO daily_orders (order_name,price,date) VALUES (?,?,?)", (desc, price, dt_date.today().strftime("%Y-%m-%d")))
                conn.commit(); st.rerun()
        
        df_rev = pd.read_sql(f"SELECT order_name as 'البيان', price as 'المبلغ' FROM daily_orders WHERE date='{dt_date.today().strftime('%Y-%m-%d')}'", conn)
        st.dataframe(df_rev, use_container_width=True)
        st.metric("إجمالي إيراد اليوم", f"{df_rev['المبلغ'].sum()} ج.م")

# 4. الإدارة
with tabs[3]:
    pwd = st.text_input("كلمة السر", type="password", key="adm_p")
    if pwd == SHARED_PASSWORD:
        df_b = pd.read_sql("SELECT id, name, phone, address, date FROM bookings ORDER BY id DESC", conn)
        st.dataframe(df_b.drop(columns=['id']), use_container_width=True)
        if st.button("حذف كافة الحجوزات"):
            c.execute("DELETE FROM bookings"); conn.commit(); st.rerun()

st.markdown(f'<div class="footer-signature">كل عام وأنتم بخير - مغسلة المتحدة</div>', unsafe_allow_html=True)