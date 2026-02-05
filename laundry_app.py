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

# ---------------- ستايل الموقع + رمضان ----------------
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

.stButton > button {
    background: linear-gradient(90deg,#1E88E5,#42A5F5);
    color: white;
    border-radius: 14px;
    font-size: 16px;
    padding: 10px 22px;
    border: none;
}

input, textarea {
    border-radius: 10px !important;
    border: 1px solid #90CAF9 !important;
}

.ramadan-box {
    background: linear-gradient(135deg,#1A237E,#283593);
    color: white;
    padding: 28px;
    border-radius: 22px;
    text-align: center;
    margin-bottom: 30px;
    box-shadow: 0 12px 35px rgba(0,0,0,0.3);
}

.phone-box {
    background: rgba(255,255,255,0.15);
    padding: 12px;
    border-radius: 14px;
    margin-top: 10px;
    font-size: 18px;
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

# ---------------- الموظفين ----------------
employees_list = [
    ("مصطفى الفيشاوى", 100),
    ("وليد المالكي", 150),
    ("ابراهيم بكير", 150)
]
for name, rate in employees_list:
    c.execute("SELECT id FROM employees WHERE name=?", (name,))
    if not c.fetchone():
        c.execute("INSERT INTO employees (name,daily_rate) VALUES (?,?)", (name, rate))
conn.commit()

# ---------------- هيدر ----------------
st.markdown(f"""
<div class="ramadan-box">
    <h1>🧼 مغسلة المتحدة للسجاد</h1>
    <h3>📍 العنوان: {CONTACT_ADDRESS}</h3>
    <div class="phone-box">
        📞 للتواصل والحجز: <b>{CONTACT_PHONE}</b>
    </div>
    <h2>🌙 رمضان كريم 🌙</h2>
</div>
""", unsafe_allow_html=True)

tabs = st.tabs(["📝 الحجز", "🔐 المسؤول", "👷 الموظفين", "📦 أوردرات اليوم"])

# ================= صفحة الحجز =================
with tabs[0]:
    now = datetime.now()
    end_datetime = datetime.combine(last_booking_date, datetime.max.time())
    remaining = end_datetime - now

    if remaining.total_seconds() > 0:
        d = remaining.days
        h, r = divmod(remaining.seconds, 3600)
        m, s = divmod(r, 60)
        st.info(f"⏳ متبقي للحجز: {d} يوم {h} ساعة {m} دقيقة {s} ثانية")

        with st.form("booking"):
            name = st.text_input("الاسم")
            address = st.text_input("العنوان")
            phone = st.text_input("رقم الهاتف")
            booking_date = st.date_input("التاريخ", max_value=last_booking_date)
            time_slot = st.radio("الوقت", ["صباحًا", "مساءً"], horizontal=True)
            feedback = st.text_area("ملاحظات")
            submit = st.form_submit_button("تأكيد الحجز")

            if submit and name and address and phone:
                c.execute("SELECT 1 FROM bookings WHERE name=? AND phone=? AND date=?", (name, phone, booking_date.strftime("%Y-%m-%d")))
                if c.fetchone():
                    st.error("❌ لا يمكن الحجز مرتين في نفس اليوم")
                else:
                    c.execute("INSERT INTO bookings (name,address,phone,date,feedback,time_slot) VALUES (?,?,?,?,?,?)", (name, address, phone, booking_date.strftime("%Y-%m-%d"), feedback, time_slot))
                    conn.commit()
                    st.success("✅ تم تأكيد الحجز بنجاح")
    else:
        st.error("❌ انتهت فترة الحجز")

# ================= صفحة المسؤول =================
with tabs[1]:
    password = st.text_input("كلمة سر المسؤول", type="password")
    if password == ADMIN_PASSWORD:
        df = pd.read_sql("SELECT name,address,phone,date,time_slot,feedback FROM bookings", conn)
        st.dataframe(df if not df.empty else pd.DataFrame(), use_container_width=True)

# ================= صفحة الموظفين =================
with tabs[2]:
    password = st.text_input("كلمة سر الموظفين", type="password", key="emp_pass")
    if password == EMP_PASSWORD:
        st.markdown("### 📋 سجل رواتب الموظفين")
        
        c.execute("SELECT id, name, daily_rate FROM employees")
        emps = c.fetchall()

        # عرض الجدول الرئيسي للرواتب
        rows = []
        for emp_id, emp_name, rate in emps:
            days = c.execute("SELECT COUNT(*) FROM attendance WHERE employee_id=?", (emp_id,)).fetchone()[0]
            deductions = c.execute("SELECT COALESCE(SUM(amount),0) FROM salary_deductions WHERE employee_id=?", (emp_id,)).fetchone()[0]
            salary = (days * rate) - deductions
            rows.append([emp_name, days, rate, deductions, salary])

        df_salaries = pd.DataFrame(
            rows, columns=["اسم الموظف", "أيام الحضور", "اليومية", "إجمالي الخصم", "المرتب المستحق"]
        )
        st.table(df_salaries)

        st.markdown("---")
        
        # قسم إضافة خصم جديد
        st.markdown("### 💸 إضافة خصم / سلفة")
        with st.form("deduction_form"):
            emp_to_deduct = st.selectbox("اختر الموظف", [e[1] for e in emps])
            amount = st.number_input("المبلغ (جنيه)", min_value=0)
            reason = st.text_input("السبب (سلفة، تأخير، الخ)")
            submit_deduction = st.form_submit_button("إضافة الخصم")
            
            if submit_deduction and amount > 0:
                # الحصول على ID الموظف من اسمه
                e_id = next(e[0] for e in emps if e[1] == emp_to_deduct)
                c.execute("INSERT INTO salary_deductions (employee_id, amount, reason, date) VALUES (?, ?, ?, ?)",
                          (e_id, amount, reason, today.strftime("%Y-%m-%d")))
                conn.commit()
                st.success(f"✅ تم تسجيل خصم مبلغ {amount} للموظف {emp_to_deduct}")
                st.rerun()

# ================= صفحة أوردرات اليوم =================
with tabs[3]:
    password = st.text_input("كلمة سر الأوردرات", type="password", key="order_pass")
    if password == ORDERS_PASSWORD:
        with st.form("order_form"):
            order_name = st.text_input("اسم الأوردر")
            price = st.number_input("السعر", min_value=0)
            add = st.form_submit_button("إضافة")
            if add and order_name and price > 0:
                c.execute("INSERT INTO daily_orders (order_name,price,date) VALUES (?,?,?)", (order_name, price, today.strftime("%Y-%m-%d")))
                conn.commit()
                st.success("✅ تم إضافة الأوردر")

        c.execute("SELECT id, order_name, price FROM daily_orders WHERE date=?", (today.strftime("%Y-%m-%d"),))
        orders = c.fetchall()
        
        total = 0
        for oid, n, p in orders:
            total += p
            col1, col2, col3 = st.columns([4,2,1])
            col1.markdown(f"**{n}**")
            col2.markdown(f"💰 {p} جنيه")
            if col3.button("❌", key=f"del_{oid}"):
                c.execute("DELETE FROM daily_orders WHERE id=?", (oid,))
                conn.commit()
                st.rerun()

        st.markdown("---")
        st.markdown(f"## 💰 إجمالي اليوم: **{total} جنيه**")