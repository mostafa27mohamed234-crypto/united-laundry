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

.success-card {
    background: linear-gradient(135deg,#2E7D32,#66BB6A);
    color: white;
    padding: 30px;
    border-radius: 25px;
    text-align: center;
    margin-top: 30px;
    box-shadow: 0 12px 35px rgba(0,0,0,0.3);
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
c.execute("""
CREATE TABLE IF NOT EXISTS bookings (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    address TEXT,
    phone TEXT,
    date TEXT,
    feedback TEXT,
    time_slot TEXT
)
""")

c.execute("""
CREATE TABLE IF NOT EXISTS employees (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    daily_rate INTEGER
)
""")

c.execute("""
CREATE TABLE IF NOT EXISTS attendance (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    employee_id INTEGER,
    date TEXT
)
""")

c.execute("""
CREATE TABLE IF NOT EXISTS salary_deductions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    employee_id INTEGER,
    amount INTEGER,
    reason TEXT,
    date TEXT
)
""")

c.execute("""
CREATE TABLE IF NOT EXISTS daily_orders (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    order_name TEXT,
    price INTEGER,
    date TEXT
)
""")
conn.commit()

# ---------------- الموظفين ----------------
employees = [
    ("مصطفى الفيشاوى", 100),
    ("وليد المالكي", 150),
    ("ابراهيم بكير", 150)
]
for name, rate in employees:
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
    <p style="margin-top:10px;">🕌 ✨ 🏮 ✨ 🕌</p>
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
                c.execute(
                    "SELECT 1 FROM bookings WHERE name=? AND phone=? AND date=?",
                    (name, phone, booking_date.strftime("%Y-%m-%d"))
                )
                if c.fetchone():
                    st.error("❌ لا يمكن الحجز مرتين في نفس اليوم")
                else:
                    c.execute("""
                    INSERT INTO bookings (name,address,phone,date,feedback,time_slot)
                    VALUES (?,?,?,?,?,?)
                    """, (
                        name, address, phone,
                        booking_date.strftime("%Y-%m-%d"),
                        feedback, time_slot
                    ))
                    conn.commit()

                    # ---------------- عرض رسالة الشكر بدون rerun ----------------
                    st.markdown(f"""
                    <div class="success-card">
                        <h1>✅ تم تأكيد الحجز بنجاح</h1>
                        <h3>شكرًا لاختياركم مغسلة المتحدة للسجاد 🌸</h3>
                        <hr>
                        <p><b>👤 الاسم:</b> {name}</p>
                        <p><b>📍 العنوان:</b> {address}</p>
                        <p><b>📞 الهاتف:</b> {phone}</p>
                        <p><b>📅 التاريخ:</b> {booking_date.strftime("%Y-%m-%d")}</p>
                        <p><b>⏰ الوقت:</b> {time_slot}</p>
                        <p><b>📝 ملاحظات:</b> {feedback or "—"}</p>
                        <br>
                        <p>📞 للاستفسار: {CONTACT_PHONE}</p>
                        <p>🌙 كل عام وأنتم بخير</p>
                    </div>
                    """, unsafe_allow_html=True)
    else:
        st.error("❌ انتهت فترة الحجز")

# ================= صفحة المسؤول =================
with tabs[1]:
    password = st.text_input("كلمة سر المسؤول", type="password")
    if password == ADMIN_PASSWORD:
        st.markdown("### 📋 الحجوزات المسجلة")
        df = pd.read_sql("SELECT name,address,phone,date,time_slot,feedback FROM bookings", conn)
        if not df.empty:
            st.dataframe(df)
        else:
            st.info("لا توجد حجوزات بعد")

# ================= صفحة الموظفين =================
with tabs[2]:
    password = st.text_input("كلمة سر الموظفين", type="password")
    if password == EMP_PASSWORD:
        c.execute("SELECT id,name,daily_rate FROM employees")
        emps = c.fetchall()

        st.markdown("### تسجيل الحضور")
        day = st.date_input("اليوم")

        for emp_id, emp_name, _ in emps:
            if st.checkbox(emp_name, key=f"a{emp_id}"):
                c.execute(
                    "INSERT OR IGNORE INTO attendance (employee_id,date) VALUES (?,?)",
                    (emp_id, day.strftime("%Y-%m-%d"))
                )
        conn.commit()

        st.markdown("### خصم من المرتب")
        emp_map = {name: emp_id for emp_id, name, _ in emps}
        emp = st.selectbox("الموظف", emp_map.keys())
        amount = st.number_input("قيمة الخصم", min_value=0)
        reason = st.text_input("سبب الخصم")

        if st.button("تنفيذ الخصم"):
            c.execute("""
            INSERT INTO salary_deductions (employee_id,amount,reason,date)
            VALUES (?,?,?,?)
            """, (emp_map[emp], amount, reason, today.strftime("%Y-%m-%d")))
            conn.commit()
            st.success("✅ تم الخصم")

        rows = []
        for emp_id, emp_name, rate in emps:
            days = c.execute(
                "SELECT COUNT(*) FROM attendance WHERE employee_id=?",
                (emp_id,)
            ).fetchone()[0]
            deductions = c.execute(
                "SELECT COALESCE(SUM(amount),0) FROM salary_deductions WHERE employee_id=?",
                (emp_id,)
            ).fetchone()[0]
            salary = days * rate - deductions
            rows.append([emp_name, days, deductions, salary])

        st.dataframe(pd.DataFrame(
            rows, columns=["الموظف", "أيام الحضور", "إجمالي الخصم", "المرتب النهائي"]
        ))

# ================= صفحة أوردرات اليوم =================
with tabs[3]:
    password = st.text_input("كلمة سر الأوردرات", type="password")
    if password == ORDERS_PASSWORD:
        with st.form("order_form"):
            name = st.text_input("اسم الأوردر", key="order_name", placeholder="")
            price = st.number_input("السعر", min_value=0)
            add = st.form_submit_button("إضافة")
            if add and name and price > 0:
                c.execute("INSERT INTO daily_orders (order_name,price,date) VALUES (?,?,?)",
                          (name, price, today.strftime("%Y-%m-%d")))
                conn.commit()
                st.success("✅ تم إضافة الأوردر")

        c.execute("SELECT id,order_name,price FROM daily_orders WHERE date=?", (today.strftime("%Y-%m-%d"),))
        total = 0
        for oid, n, p in c.fetchall():
            total += p
            col1, col2, col3 = st.columns([4,2,1])
            col1.markdown(f"**{n}**")
            col2.markdown(f"💰 {p} جنيه")
            if col3.button("❌", key=oid):
                c.execute("DELETE FROM daily_orders WHERE id=?", (oid,))
                conn.commit()
                st.experimental_rerun()
        st.markdown(f"## 💰 إجمالي اليوم: **{total} جنيه**")
