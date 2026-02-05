import streamlit as st
from datetime import date as dt_date, datetime, timedelta
import sqlite3
import pandas as pd

# ---------------- إعداد الصفحة ----------------
st.set_page_config(
    page_title="🧼 مغسلة المتحدة للسجاد",
    layout="wide"
)

# ---------------- كلمات السر + بيانات الهيدر ----------------
ADMIN_PASSWORD = "المتحده@1996"
EMP_PASSWORD = "mostafa23"
ORDERS_PASSWORD = "اكرم1996"
OWNER_NAME = "الأستاذ أكرم حموده"
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

# ---------------- ستايل الموقع ----------------
st.markdown("""
<style>
.stApp {
    background: linear-gradient(135deg,#E3F2FD,#BBDEFB,#90CAF9,#64B5F6);
    font-family: 'Cairo', sans-serif;
}
div[data-testid="stForm"],
div[data-testid="stVerticalBlock"] > div {
    background-color: rgba(255,255,255,0.88);
    padding: 20px;
    border-radius: 18px;
    box-shadow: 0 8px 25px rgba(0,0,0,0.12);
}
h1, h2, h3 { color: #0D47A1; text-align: center; }
.ramadan-box {
    background: linear-gradient(135deg,#1A237E,#283593);
    color: white;
    padding: 28px;
    border-radius: 22px;
    text-align: center;
    margin-bottom: 30px;
}
</style>
""", unsafe_allow_html=True)

# ---------------- اليوم ----------------
today = dt_date.today()
last_booking_date = dt_date(2026, 3, 10)

# ---------------- قاعدة البيانات ----------------
conn = sqlite3.connect("bookings.db", check_same_thread=False)
c = conn.cursor()

# ---------------- إنشاء الجداول ----------------
c.execute("CREATE TABLE IF NOT EXISTS bookings (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT, address TEXT, phone TEXT, date TEXT, feedback TEXT, time_slot TEXT)")
c.execute("CREATE TABLE IF NOT EXISTS employees (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT, daily_rate INTEGER)")
c.execute("CREATE TABLE IF NOT EXISTS attendance (id INTEGER PRIMARY KEY AUTOINCREMENT, employee_id INTEGER, date TEXT)")
c.execute("CREATE TABLE IF NOT EXISTS salary_deductions (id INTEGER PRIMARY KEY AUTOINCREMENT, employee_id INTEGER, amount INTEGER, reason TEXT, date TEXT)")
c.execute("CREATE TABLE IF NOT EXISTS daily_orders (id INTEGER PRIMARY KEY AUTOINCREMENT, order_name TEXT, price INTEGER, date TEXT)")
conn.commit()

# ---------------- الموظفين الثابتين ----------------
employees_data = [
    ("مصطفى الفيشاوى", 100),
    ("وليد المالكي", 150),
    ("ابراهيم بكير", 150)
]
for name, rate in employees_data:
    c.execute("SELECT id FROM employees WHERE name=?", (name,))
    if not c.fetchone():
        c.execute("INSERT INTO employees (name,daily_rate) VALUES (?,?)", (name, rate))
conn.commit()

# ---------------- هيدر ----------------
st.markdown(f"""
<div class="ramadan-box">
    <h1>🧼 مغسلة المتحدة للسجاد</h1>
    <h3>📍 العنوان: {CONTACT_ADDRESS}</h3>
    <h2>🌙 رمضان كريم 🌙</h2>
</div>
""", unsafe_allow_html=True)

tabs = st.tabs(["📝 الحجز", "🔐 المسؤول", "👷 الموظفين", "📦 أوردرات اليوم"])

# ================= صفحة الحجز =================
with tabs[0]:
    with st.form("booking"):
        name = st.text_input("الاسم")
        address = st.text_input("العنوان")
        phone = st.text_input("رقم الهاتف")
        booking_date = st.date_input("التاريخ", max_value=last_booking_date)
        time_slot = st.radio("الوقت", ["صباحًا", "مساءً"], horizontal=True)
        submit = st.form_submit_button("تأكيد الحجز")
        if submit and name and phone:
            c.execute("INSERT INTO bookings (name,address,phone,date,time_slot) VALUES (?,?,?,?,?)", 
                      (name, address, phone, booking_date.strftime("%Y-%m-%d"), time_slot))
            conn.commit()
            st.success("✅ تم تأكيد الحجز")

# ================= صفحة المسؤول =================
with tabs[1]:
    password = st.text_input("كلمة سر المسؤول", type="password", key="admin_pwd")
    if password == ADMIN_PASSWORD:
        df = pd.read_sql("SELECT name,address,phone,date,time_slot FROM bookings", conn)
        st.dataframe(df, use_container_width=True)

# ================= صفحة الموظفين =================
with tabs[2]:
    password = st.text_input("كلمة سر الموظفين", type="password", key="emp_pwd")
    if password == EMP_PASSWORD:
        c.execute("SELECT id, name, daily_rate FROM employees")
        emps = c.fetchall()

        # --- 1. قسم تسجيل الحضور اليومي ---
        st.markdown("### 📝 تسجيل حضور اليوم")
        att_date = st.date_input("تاريخ اليوم", today)
        
        col_att1, col_att2 = st.columns([2, 1])
        with col_att1:
            selected_ids = []
            for eid, ename, _ in emps:
                if st.checkbox(f"حضر: {ename}", key=f"check_{eid}"):
                    selected_ids.append(eid)
        
        with col_att2:
            if st.button("حفظ سجل الحضور"):
                for e_id in selected_ids:
                    c.execute("SELECT 1 FROM attendance WHERE employee_id=? AND date=?", (e_id, att_date.strftime("%Y-%m-%d")))
                    if not c.fetchone():
                        c.execute("INSERT INTO attendance (employee_id, date) VALUES (?,?)", (e_id, att_date.strftime("%Y-%m-%d")))
                conn.commit()
                st.success("تم الحفظ!")
                st.rerun()

        st.markdown("---")

        # --- 2. قسم إضافة خصم (الجديد) ---
        st.markdown("### 💸 إضافة خصم / سلفة")
        with st.form("deduction_form"):
            col_d1, col_d2, col_d3 = st.columns(3)
            with col_d1:
                target_emp = st.selectbox("الموظف", [e[1] for e in emps])
            with col_d2:
                deduct_amt = st.number_input("المبلغ (جنيه)", min_value=0)
            with col_d3:
                deduct_reason = st.text_input("السبب")
            
            if st.form_submit_button("إضافة الخصم"):
                if deduct_amt > 0:
                    emp_id_to_deduct = next(e[0] for e in emps if e[1] == target_emp)
                    c.execute("INSERT INTO salary_deductions (employee_id, amount, reason, date) VALUES (?,?,?,?)",
                              (emp_id_to_deduct, deduct_amt, deduct_reason, today.strftime("%Y-%m-%d")))
                    conn.commit()
                    st.success(f"تم خصم {deduct_amt} من {target_emp}")
                    st.rerun()

        st.markdown("---")

        # --- 3. جدول عرض الرواتب والحسابات ---
        st.markdown("### 📊 جدول الحسابات النهائية")
        rows = []
        for emp_id, emp_name, rate in emps:
            # حساب الأيام
            days = c.execute("SELECT COUNT(*) FROM attendance WHERE employee_id=?", (emp_id,)).fetchone()[0]
            # حساب الخصومات
            total_deduct = c.execute("SELECT COALESCE(SUM(amount),0) FROM salary_deductions WHERE employee_id=?", (emp_id,)).fetchone()[0]
            # الصافي
            final_salary = (days * rate) - total_deduct
            rows.append([emp_name, days, rate, total_deduct, final_salary])

        df_salaries = pd.DataFrame(rows, columns=["اسم الموظف", "أيام الحضور", "اليومية", "إجمالي الخصم", "المرتب المستحق"])
        st.table(df_salaries)

        # --- 4. زر التصفير النهائي ---
        if st.button("⚠️ تصفير كافة السجلات (ابدأ شهر جديد)"):
            c.execute("DELETE FROM attendance")
            c.execute("DELETE FROM salary_deductions")
            conn.commit()
            st.warning("تم تصفير كافة الحسابات بنجاح!")
            st.rerun()

# ================= صفحة أوردرات اليوم =================
with tabs[3]:
    password = st.text_input("كلمة سر الأوردرات", type="password", key="ord_pwd")
    if password == ORDERS_PASSWORD:
        with st.form("order_form"):
            order_name = st.text_input("اسم الأوردر")
            price = st.number_input("السعر", min_value=0)
            if st.form_submit_button("إضافة أوردر"):
                c.execute("INSERT INTO daily_orders (order_name,price,date) VALUES (?,?,?)", (order_name, price, today.strftime("%Y-%m-%d")))
                conn.commit()
                st.rerun()

        c.execute("SELECT id, order_name, price FROM daily_orders WHERE date=?", (today.strftime("%Y-%m-%d"),))
        day_orders = c.fetchall()
        total_day = sum(o[2] for o in day_orders)
        
        for oid, n, p in day_orders:
            col1, col2, col3 = st.columns([4,2,1])
            col1.text(n)
            col2.text(f"{p} جنيه")
            if col3.button("❌", key=f"del_ord_{oid}"):
                c.execute("DELETE FROM daily_orders WHERE id=?", (oid,))
                conn.commit()
                st.rerun()
        st.markdown(f"### 💰 إجمالي اليوم: {total_day} جنيه")