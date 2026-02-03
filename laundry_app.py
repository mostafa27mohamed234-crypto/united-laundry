import streamlit as st
from datetime import datetime, date as dt_date

st.set_page_config(page_title="مغسلة المتحدة للسجاد")

# البيانات
bookings = []
ADMIN_PASSWORD = "المتحده@1996"
show_admin = False
tab = st.sidebar.selectbox("اختر الصفحة", ["الحجز", "المسؤول"])
message = ""

# HTML ثابت
header_html = """
<div style="text-align:center; padding:20px; background-color:#d4af37; color:white;">
    <h1>مغسلة المتحدة للسجاد</h1>
</div>
<div style="text-align:center; font-size:20px; font-weight:bold; color:#b85c38; margin-top:10px;">
✨ مغسلة المتحدة تهنئكم بحلول شهر رمضان الكريم ✨
</div>
<div style="text-align:center; font-size:16px; color:#4b2e83; margin-top:5px;">
إدارة الأستاذ أكرم حموده - 📞 01063316053
</div>
"""

st.markdown(header_html, unsafe_allow_html=True)

# صفحة الحجز
if tab == "الحجز":
    st.markdown("### صفحة الحجز")
    with st.form(key="booking_form"):
        name = st.text_input("الاسم")
        address = st.text_input("العنوان")
        phone = st.text_input("رقم الهاتف")
        booking_date = st.date_input("تاريخ الحجز")
        submit = st.form_submit_button("احجز")

        if submit:
            cutoff_date = dt_date(datetime.now().year, 3, 20)

            if booking_date > cutoff_date:
                message = "❌ لا يمكن الحجز بعد يوم 20/3"
            else:
                booking = {
                    "name": name,
                    "address": address,
                    "phone": phone,
                    "date": booking_date.strftime("%Y-%m-%d")
                }
                bookings.append(booking)
                message = f"✅ تم الحجز بنجاح! الاسم: {booking['name']}, التاريخ: {booking['date']}"

# صفحة المسؤول
elif tab == "المسؤول":
    st.markdown("### صفحة المسؤول")
    password = st.text_input("كلمة السر", type="password")
    check = st.button("دخول")

    if check:
        if password == ADMIN_PASSWORD:
            show_admin = True
        else:
            message = "❌ كلمة السر خاطئة"

    if show_admin:
        st.markdown("### الحجوزات")
        if bookings:
            st.table(bookings)
        else:
            st.info("لا توجد حجوزات حتى الآن.")

# رسالة
if message:
    st.markdown(
        f"<div style='text-align:center; color:#b85c38; font-weight:bold; margin-bottom:15px;'>{message}</div>",
        unsafe_allow_html=True
    )

# Footer
st.markdown(
    "<div style='text-align:center; margin-top:30px; padding:15px; font-size:14px; color:#4b2e83; font-weight:bold;'>"
    "تحت إشراف البشمهندس مصطفى الفيشاوي</div>",
    unsafe_allow_html=True
)
