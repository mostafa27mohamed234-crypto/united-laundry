from flask import Flask, request
from datetime import datetime

app = Flask(__name__)

bookings = []
ADMIN_PASSWORD = "المتحده@1996"  # كلمة السر الجديدة

@app.route("/", methods=["GET", "POST"])
def main():
    tab = request.args.get("tab", "booking")
    message = ""
    show_admin = False

    # حجز العميل
    if request.method == "POST" and request.form.get("action") == "book":
        date_str = request.form["date"]
        booking_date = datetime.strptime(date_str, "%Y-%m-%d")
        cutoff_date = datetime(datetime.now().year, 3, 20)

        if booking_date > cutoff_date:
            message = "❌ لا يمكن الحجز بعد يوم 20/3"
        else:
            booking = {
                "name": request.form["name"],
                "address": request.form["address"],
                "phone": request.form["phone"],
                "date": date_str
            }
            bookings.append(booking)
            message = f"✅ تم الحجز بنجاح! الاسم: {booking['name']}, التاريخ: {booking['date']}"

    # دخول المسؤول
    if request.method == "POST" and request.form.get("action") == "admin":
        if request.form.get("password") == ADMIN_PASSWORD:
            show_admin = True
        else:
            message = "❌ كلمة السر خاطئة"

    html = f"""
    <html>
    <head>
        <meta charset="utf-8">
        <title>مغسلة المتحدة للسجاد</title>
        <style>
            body {{ font-family: Arial; background: linear-gradient(to bottom, #fff9e6, #ffeedd); margin:0; padding:0; }}
            .header {{ text-align:center; padding:20px; background-color:#d4af37; color:white; }}
            .ramadan-msg {{ text-align:center; font-size:20px; font-weight:bold; color:#b85c38; margin-top:10px; }}
            .admin-info {{ text-align:center; font-size:16px; color:#4b2e83; margin-top:5px; }}
            .tabs {{ display:flex; justify-content:center; margin:20px; }}
            .tab {{ padding: 10px 25px; margin:0 10px; border-radius:10px; background-color:#b8860b; color:white; cursor:pointer; text-decoration:none; }}
            .tab:hover {{ background-color:#d4af37; }}
            .content {{ max-width:600px; margin:auto; padding:20px; background:white; border-radius:15px; border:2px solid #d4af37; }}
            input, button {{ width:90%; padding:10px; margin:8px 0; font-size:15px; }}
            button {{ background:#d4af37; color:white; border:none; font-weight:bold; cursor:pointer; }}
            button:hover {{ background-color:#b8860b; }}
            .message {{ text-align:center; color:#b85c38; font-weight:bold; margin-bottom:15px; }}
            table {{ width:100%; border-collapse:collapse; margin-top:10px; }}
            th, td {{ border:1px solid #d4af37; padding:8px; text-align:center; }}
            th {{ background-color:#d4af37; color:white; }}
            tr:nth-child(even) {{ background-color:#ffeedd; }}
            .footer {{
                text-align:center;
                margin-top:30px;
                padding:15px;
                font-size:14px;
                color:#4b2e83;
                font-weight:bold;
            }}
        </style>
    </head>
    <body>
        <div class="header">
            <h1>مغسلة المتحدة للسجاد</h1>
        </div>
        <div class="ramadan-msg">✨ مغسلة المتحدة تهنئكم بحلول شهر رمضان الكريم ✨</div>
        <div class="admin-info">إدارة الأستاذ أكرم حموده - 📞 01063316053</div>

        <div class="tabs">
            <a class="tab" href="/?tab=booking">الحجز</a>
            <a class="tab" href="/?tab=admin">المسؤول</a>
        </div>

        <div class="content">
            <div class="message">{message}</div>
    """

    if tab == "booking":
        html += """
            <h2>صفحة الحجز</h2>
            <form method='post' autocomplete="off">
                <input name='name' placeholder='الاسم' required>
                <input name='address' placeholder='العنوان' required>
                <input name='phone' placeholder='رقم الهاتف' required>
                <input type='date' name='date' required>
                <button type='submit' name='action' value='book'>احجز</button>
            </form>
        """

    if tab == "admin":
        if not show_admin:
            html += """
                <h2>صفحة المسؤول</h2>
                <form method='post'>
                    <input type='password' name='password' placeholder='كلمة السر' required>
                    <button type='submit' name='action' value='admin'>دخول</button>
                </form>
            """
        else:
            html += """
                <h2>الحجوزات</h2>
                <table>
                    <tr><th>الاسم</th><th>العنوان</th><th>الهاتف</th><th>تاريخ الحجز</th></tr>
            """
            for b in bookings:
                html += f"<tr><td>{b['name']}</td><td>{b['address']}</td><td>{b['phone']}</td><td>{b['date']}</td></tr>"
            html += "</table>"

    html += """
        </div>
        <div class="footer">
            تحت إشراف البشمهندس مصطفى الفيشاوي
        </div>
    </body>
    </html>
    """

    return html


if __name__ == "__main__":
    print("🌟 السيرفر شغال على http://127.0.0.1:5000")
    app.run(host="0.0.0.0", port=5000, debug=True)
