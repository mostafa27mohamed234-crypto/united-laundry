import streamlit as st
from datetime import date as dt_date, datetime, timedelta
import sqlite3
import pandas as pd

# ---------------- إعداد الصفحة ----------------
st.set_page_config(
    page_title="🧼 مغسلة المتحدة للسجاد",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ---------------- اليوم ----------------
today = dt_date.today()
last_booking_date = dt_date(2026, 3, 10)  # آخر يوم مسموح للحجز

# ---------------- قاعدة البيانات ----------------
conn = sqlite3.connect("bookings.db", check_same_thread=False)
c = conn.cursor()

# ---------------- الجداول ----------------
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

# ---------------- المتغيرات ----------------
ADMIN_PASSWORD = "المتحده@1996"
EMP_PASSWORD = "mostafa23"
ORDERS_PASSWORD = "اكرم1996"
OWNER_NAME = "الأستاذ أكرم حموده"
message = ""

# ---------------- Sidebar ----------------
tab = st.sidebar.selectbox(
    "📌 اختر الصفحة",
    ["الحجز", "المسؤول", "الموظفين", "أوردارات اليوم"]
)

# ---------------- Header ----------------
st.markdown(f"""
<div style="text-align:center; background-color:#FFF3E0; padding:20px; border-radius:15px;">
    <h1 style="color:#FF6F00;">🧼 مغسلة المتحدة للسجاد</h1>
    <h3 style="color:#E65100;">👤 المسؤول: {OWNER_NAME} | 📞 01063316053</h3>
    <h2 style="color:#D32F2F; margin-top:10px;">🌙 رمضان كريم! كل عام وأنتم بخير 🌙</h2>
</div>
""", unsafe_allow_html=True)

# ================= صفحة الحجز =================
if tab == "الحجز":
    st.markdown("## 📝 حجز خدمة", unsafe_allow_html=True)

    # --------- زر مسح الحجوزات (مرة واحدة) ---------
    if st.button("🗑 مسح كل الحجوزات القديمة"):
        c.execute("DELETE FROM bookings")
        conn.commit()
        st.success("✅ تم مسح كل الحجوزات القديمة")
        st.experimental_rerun()

    # --------- العد التنازلي ---------
    countdown_placeholder = st.empty()
    now = datetime.now()
    end_datetime = datetime.combine(last_booking_date, datetime.max.time())
    remaining = end_datetime - now

    if remaining.total_seconds() > 0:
        days = remaining.days
        hours, remainder = divmod(remaining.seconds, 3600)
        minutes, seconds = divmod(remainder, 60)
        countdown_placeholder.info(
            f"⏳ الوقت المتبقي للحجز: {days} يوم {hours} ساعة {minutes} دقيقة {seconds} ثانية"
        )

        # --------- نموذج الحجز ---------
        with st.form("booking_form"):
            name = st.text_input("الاسم")
            address = st.text_input("العنوان")
            phone = st.text_input("رقم الهاتف")
            booking_date = st.date_input("التاريخ", min_value=dt_date.today(), max_value=last_booking_date)
            time_slot = st.radio("الوقت", ["صباحًا", "مساءً"], horizontal=True)
            feedback = st.text_area("ملاحظات")
            submit = st.form_submit_button("تأكيد الحجز", use_container_width=True)

            if submit:
                if not name or not address or not phone:
                    message = "❌ برجاء استكمال البيانات"
                else:
                    # --------- تحقق من الحجز اليومي ---------
                    c.execute("""
                        SELECT 1 FROM bookings
                        WHERE name=? AND phone=? AND date=?
                    """, (name, phone, booking_date.strftime("%Y-%m-%d")))
                    if c.fetchone():
                        message = "❌ لا يمكنك الحجز أكثر من مرة في اليوم نفسه"
                    else:
                        c.execute("""INSERT INTO bookings (name,address,phone,date,feedback,time_slot)
                                     VALUES (?,?,?,?,?,?)""",
                                  (name,address,phone,booking_date.strftime("%Y-%m-%d"),feedback,time_slot))
                        conn.commit()
                        message = "✅ تم الحجز بنجاح"
    else:
        countdown_placeholder.warning("❌ انتهت فترة الحجز المتاحة حتى 10/03/2026")
        st.info("الحجز مغلق الآن")

# ================= صفحة المسؤول =================
elif tab == "المسؤول":
    st.markdown("## 🔐 لوحة المسؤول", unsafe_allow_html=True)
    if "admin" not in st.session_state:
        st.session_state.admin = False

    password = st.text_input("كلمة السر", type="password")
    if st.button("دخول"):
        if password == ADMIN_PASSWORD:
            st.session_state.admin = True
        else:
            st.error("❌ كلمة السر غير صحيحة")

    if st.session_state.admin:
        st.markdown("### 📋 الحجوزات المسجلة")
        c.execute("SELECT name,address,phone,date,time_slot,feedback FROM bookings")
        bookings = c.fetchall()
        if bookings:
            df = pd.DataFrame(bookings, columns=['الاسم','العنوان','رقم الهاتف','التاريخ','الوقت','ملاحظات'])
            st.dataframe(df.style.set_properties(**{
                'text-align': 'center', 'background-color':'#FFFDE7', 'color':'#3E2723'
            }))
        else:
            st.info("لا توجد حجوزات بعد")

# ================= صفحة الموظفين =================
elif tab == "الموظفين":
    st.markdown("## 🔐 تسجيل وحساب حضور الموظفين")
    if "emp" not in st.session_state:
        st.session_state.emp = False

    emp_pass = st.text_input("كلمة السر", type="password")
    if st.button("دخول الموظفين"):
        if emp_pass == EMP_PASSWORD:
            st.session_state.emp = True
        else:
            st.error("❌ كلمة السر غير صحيحة")

    if st.session_state.emp:
        c.execute("SELECT id,name,daily_rate FROM employees")
        emps = c.fetchall()

        first_day = dt_date(today.year, today.month, 1)
        days_list = [first_day + timedelta(days=i) for i in range((today - first_day).days + 1)]
        selected_day = st.selectbox("اختر اليوم لتسجيل الحضور",
                                    [d.strftime("%Y-%m-%d") for d in days_list])

        attendance_state = {}
        for emp_id, emp_name, _ in emps:
            c.execute("SELECT 1 FROM attendance WHERE employee_id=? AND date=?", (emp_id, selected_day))
            already = bool(c.fetchone())
            attendance_state[emp_id] = st.checkbox(emp_name, value=already, key=f"{emp_id}_{selected_day}")

        col1, col2 = st.columns(2)
        if col1.button("💾 حفظ الحضور"):
            for emp_id, present in attendance_state.items():
                if present:
                    c.execute("SELECT 1 FROM attendance WHERE employee_id=? AND date=?", (emp_id, selected_day))
                    if not c.fetchone():
                        c.execute("INSERT INTO attendance (employee_id,date) VALUES (?,?)", (emp_id, selected_day))
            conn.commit()
            st.success("✅ تم حفظ الحضور")

        if col2.button("🗑 مسح حضور اليوم"):
            c.execute("DELETE FROM attendance WHERE date=?", (selected_day,))
            conn.commit()
            st.warning("🗑 تم مسح حضور هذا اليوم")
            st.experimental_rerun()

        # ---------------- جدول الحضور ----------------
        st.markdown("### 📊 جدول الحضور الشهري")
        col_names = ['الموظف'] + [d.strftime('%d') for d in days_list] + ['أيام الحضور', 'الراتب']
        data = []
        for emp_id, emp_name, rate in emps:
            row = [emp_name]
            count = 0
            for d in days_list:
                d_str = d.strftime('%Y-%m-%d')
                c.execute("SELECT 1 FROM attendance WHERE employee_id=? AND date=?", (emp_id, d_str))
                present = c.fetchone()
                if present:
                    row.append('✓')
                    count += 1
                else:
                    row.append('')
            row.append(count)
            row.append(count*rate)
            data.append(row)
        df = pd.DataFrame(data, columns=col_names)
        st.dataframe(df.style.set_properties(**{'text-align': 'center', 'background-color':'#E0F7FA','color':'#006064'}))

# ================= أوردرات اليوم =================
elif tab == "أوردارات اليوم":
    st.markdown("## 🔐 أوردرات اليوم")
    if "orders" not in st.session_state:
        st.session_state.orders = False

    order_pass = st.text_input("كلمة السر", type="password")
    if st.button("دخول أوردرات اليوم"):
        if order_pass == ORDERS_PASSWORD:
            st.session_state.orders = True
        else:
            st.error("❌ كلمة السر غير صحيحة")

    if st.session_state.orders:
        with st.form("order_form"):
            name = st.text_input("اسم الأوردر")
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

# ---------------- رسالة ----------------
if message:
    st.warning(message)

# ---------------- Footer ----------------
st.markdown("""
<hr>
<center style="color:#4E342E;">🤲 اللهم بارك لنا في عملنا</center>
""", unsafe_allow_html=True)
