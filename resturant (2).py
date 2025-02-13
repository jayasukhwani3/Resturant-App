from flask import Flask, request, render_template
import mysql.connector as x
import matplotlib.pyplot as p
from datetime import date

time = date.today()

# Database connection
con = x.connect(host='localhost', user='root', password='XYZ123', database='resturant')
y = con.cursor()

totalbill = []

# Flask app initialization
app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/order', methods=['POST'])
def order():
    category = request.form['category']
    dish = int(request.form['dish'])
    qty = int(request.form['qty'])

    if category == 'north':
        north1 = {1: "Dal Chawal", 2: "Chhole Bhature", 3: "Pav Bhaji"}
        north2 = {1: 120, 2: 110, 3: 100}
        pname = north1[dish]
        price = north2[dish]
    elif category == 'south':
        south1 = {1: "Idli Sambhar", 2: "Masala Dosa", 3: "Paper Dosa"}
        south2 = {1: 150, 2: 130, 3: 110}
        pname = south1[dish]
        price = south2[dish]
    elif category == 'chinese':
        chinese1 = {1: "Noodles", 2: "Manchurian", 3: "Chinese Bhel"}
        chinese2 = {1: 120, 2: 160, 3: 100}
        pname = chinese1[dish]
        price = chinese2[dish]
    else:
        return "Invalid category"

    bill = qty * price
    totalbill.append(bill)
    data = (pname, qty, price, bill, time)
    y.execute("Insert into transaction(product_name, price, qty, bill, orderdatetime) values ('%s', %s, %s, %s, '%s')" % data)
    con.commit()

    return f"Order placed for {qty} x {pname}. Total: {bill}"

@app.route('/admin', methods=['POST'])
def admin():
    return render_template('admin.html')

@app.route('/sales/overall', methods=['GET'])
def overall():
    y.execute("Select * from transaction")
    transactions = y.fetchall()

    y.execute("Select product_name, sum(qty) from transaction group by product_name")
    d = y.fetchall()
    proname = []
    proqty = []

    for i in d:
        proname.append(i[0])
        proqty.append(i[1])

    p.bar(proname, proqty)
    p.show()

    return render_template('overall.html', transactions=transactions)

@app.route('/sales/datewise', methods=['POST'])
def datewise():
    ds = request.form['date']
    proname = []
    proqty = []

    y.execute("Select product_name, sum(qty) from transaction where orderdatetime='%s' group by product_name" % ds)
    hey = y.fetchall()
    for k in hey:
        proname.append(k[0])
        proqty.append(k[1])

    p.bar(proname, proqty)
    p.show()

    return "Sales chart for the date displayed."

@app.route('/exit', methods=['GET'])
def exit():
    tt = sum(totalbill)
    return f"Your total bill is {tt}. Date: {time}"

if __name__ == '__main__':
    app.run(debug=True)
