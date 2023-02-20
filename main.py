from builtins import print
from flask import Flask, request, render_template, url_for, flash, redirect
import datetime
import sqlite3
import itertools

app = Flask(__name__)

main_data = {}
app.secret_key = 'super secret key'
app.config['SESSION_TYPE'] = 'filesystem'


@app.route("/")
def home():
    con = sqlite3.connect("database.db")
    con.row_factory = sqlite3.Row
    cur = con.cursor()
    cur.execute("SELECT phonenumber, name, dress, date, deliverydate FROM shirtorders UNION SELECT phonenumber, name, dress, date, deliverydate FROM pantorders")
    data = cur.fetchall()
    length = len(data)
    print(length)
    print(data)

    cur.execute("SELECT * FROM shirtorders")
    shirt = cur.fetchall()
    shirtlen = len(shirt)

    cur.execute("SELECT * FROM pantorders")
    pant = cur.fetchall()
    pantlen = len(pant)

    con.close()

    return render_template('dashboard.html', data=data, length=length, shirtlen=shirtlen, pantlen=pantlen)



@app.route("/view_all_orders")
def view_all_orders():
    con = sqlite3.connect("database.db")
    con.row_factory = sqlite3.Row
    cur = con.cursor()
    cur.execute(
        "SELECT phonenumber, name, dress, orderid, deliverydate FROM shirtorders UNION SELECT phonenumber, name, dress, orderid, deliverydate FROM pantorders")
    data = cur.fetchall()
    print(data)
    con.close()

    return render_template('viewallorders.html', data=data)


@app.route("/completed-order")
def completed_order():
    return render_template('completedorders.html')


@app.route("/canceled-order")
def cancelled_order():
    return render_template('canceledorders.html')


@app.route("/search", methods=['GET', "POST"])
def search():
    if request.method == 'POST':
        phonenumber = request.form.get('phonenumber')
        dress = request.form.get('dress')
        if dress == 'shirt':
            connection = sqlite3.connect('database.db')
            cursor = connection.cursor()

            cursor.execute('select * from shirtorders where phonenumber=?', (phonenumber,))
            data = cursor.fetchone()
            print(data)
            columns = []
            data_dict = {}
            for item in cursor.description:
                columns.append(item[0])
            for item in columns:
                data_dict[f'{item}'] = data[columns.index(item)]

            print(data_dict)

            return render_template('search_data.html', data=data_dict)

        else:
            connection = sqlite3.connect('database.db')
            cursor = connection.cursor()
            cursor.execute('select * from pantorders where phonenumber=?', (phonenumber,))
            data = cursor.fetchone()
            print(data)
            columns = []
            data_dict = {}
            for item in cursor.description:
                columns.append(item[0])
            for item in columns:
                data_dict[f'{item}'] = data[columns.index(item)]

            print(data_dict)

            return render_template('search_data.html', data=data_dict)

    return render_template('search.html')


@app.route("/new-order", methods=["GET", "POST"])
def new_order():
    if request.method == "POST":
        data = {'name': request.form.get('name'),
                'address': request.form.get('address'),
                'phonenumber': request.form.get('phonenumber'),
                'dress': request.form.get('dress'),
                'date': datetime.date.today(),
                }
        main_data['info'] = data
        if data['dress'] == "shirt":
            print("selected Shirt\nRedirecting to Shirt section:")
            print(main_data)
            return render_template('newordershirt.html', data=data)
        elif data['dress'] == 'pant':
            print("selected Pant\nRedirecting to Pant section:")
            print(main_data)
            return render_template('neworderpant.html', data=data)
    return render_template("neworder.html")


@app.route("/shirt", methods=["POST"])
def shirt_data():
    if request.method == "POST":
        shirt_size_data = {
            'shirt_chest': request.form.get("shirt_chest"),
            'shirt_seat': request.form.get('shirt_seat'),
            'shirt_arm': request.form.get('shirt_arm'),
            'shirt_length': request.form.get('shirt_length'),
            'shirt_shoulder': request.form.get('shirt_shoulder'),
            'shirt_cuff': request.form.get('shirt_cuff'),
            'shirt_collar': request.form.get('shirt_collar'),
            'shirt_sleeve': request.form.get('shirt_sleeve'),
            'shirt_waist': request.form.get('shirt_waist'),
        }
        main_data['shirt_data'] = shirt_size_data
        print(main_data)
        return render_template('finalizeorder.html', main_data=main_data)
    return render_template('newordershirt.html')


@app.route("/pant", methods=["POST"])
def pant_data():
    if request.method == "POST":
        pant_size_data = {
            'waist': request.form.get("waist"),
            'abdomen': request.form.get('abdomen'),
            'hips': request.form.get('hips'),
            'thigh': request.form.get('thigh'),
            'knee': request.form.get('knee'),
            'calf': request.form.get('calf'),
            'instep': request.form.get('instep'),
            'side_length_to_knee': request.form.get('side_length_to_knee'),
            'side_length': request.form.get('side_length'),
            'crotch_length': request.form.get('crotch_length'),
            'crotch_depth': request.form.get('crotch_depth'),
        }
        main_data['pant_data'] = pant_size_data
        print(main_data)
        print(request.form)
        return render_template('finalizeorderp.html', main_data=main_data)
    return render_template('newordershirt.html')


@app.route('/finalize-order', methods=['GET', "POST"])
def finalize_order():
    if request.method == 'POST':
        if main_data['info']['dress'] == 'shirt':
            main_data['info']['delivery_date'] = request.form.get('delivery_date')
            main_data['info']['amount'] = request.form.get('amount')
            print(main_data)

            connection = sqlite3.connect('database.db')
            cursor = connection.cursor()

            cursor.execute("insert into shirtorders values (null, ?, ?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)",
                           (
                               main_data['info']['name'],
                               main_data['info']['phonenumber'],
                               main_data['info']['address'],
                               main_data['info']['dress'],
                               main_data['info']['date'],
                               main_data['info']['delivery_date'],
                               main_data['info']['amount'],
                               main_data['shirt_data']['shirt_chest'],
                               main_data['shirt_data']['shirt_seat'],
                               main_data['shirt_data']['shirt_arm'],
                               main_data['shirt_data']['shirt_length'],
                               main_data['shirt_data']['shirt_shoulder'],
                               main_data['shirt_data']['shirt_cuff'],
                               main_data['shirt_data']['shirt_collar'],
                               main_data['shirt_data']['shirt_sleeve'],
                               main_data['shirt_data']['shirt_waist'],
                           ))
            connection.commit()
            connection.close()

        elif main_data['info']['dress'] == 'pant':
            main_data['info']['delivery_date'] = request.form.get('delivery_date')
            main_data['info']['amount'] = request.form.get('amount')
            print(main_data)

            connection = sqlite3.connect('database.db')
            cursor = connection.cursor()

            cursor.execute("insert into pantorders values (null, ?, ?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)",
                           (
                               main_data['info']['name'],
                               main_data['info']['phonenumber'],
                               main_data['info']['address'],
                               main_data['info']['dress'],
                               main_data['info']['date'],
                               main_data['info']['delivery_date'],
                               main_data['info']['amount'],
                               main_data['pant_data']['waist'],
                               main_data['pant_data']['abdomen'],
                               main_data['pant_data']['hips'],
                               main_data['pant_data']['thigh'],
                               main_data['pant_data']['knee'],
                               main_data['pant_data']['calf'],
                               main_data['pant_data']['instep'],
                               main_data['pant_data']['side_length_to_knee'],
                               main_data['pant_data']['side_length'],
                               main_data['pant_data']['crotch_length'],
                               main_data['pant_data']['crotch_depth']
                           ))
            connection.commit()
            connection.close()

    return render_template("vieworders.html", main_data=main_data)


@app.route("/update_record/<string:ph>/<string:dr>", methods=["POST", "GET"])
def update_record(ph, dr):
    if dr == 'pant':
        connection = sqlite3.connect("database.db")
        connection.row_factory = sqlite3.Row
        cursor = connection.cursor()
        cursor.execute('select * from pantorders where phonenumber=?', (ph,))
        data = cursor.fetchone()
        connection.close()
        if request.method == 'POST':
            name = request.form['name']
            phonenumber = request.form['phonenumber']
            address = request.form['address']
            waist = request.form['waist']
            abdomen = request.form['abdomen']
            hips = request.form['hips']
            thigh = request.form['thigh']
            knee = request.form['knee']
            calf = request.form['calf']
            instep = request.form['instep']
            side_length_to_knee = request.form['side_length_to_knee']
            side_length = request.form['side_length']
            crotch_length = request.form['crotch_length']
            crotch_depth = request.form['crotch_depth']
            connection = sqlite3.connect("database.db")
            cursor = connection.cursor()
            cursor.execute(
                "UPDATE pantorders SET name=?, address=?, waist=?, abdomen=?, hips=?, thigh=?, knee=?, calf=?, instep=?, side_length_to_knee=?, side_length=?, crotch_length=?, crotch_depth=? where phonenumber=?",
                (name, address, waist, abdomen, hips, thigh, knee, calf, instep, side_length_to_knee, side_length,
                 crotch_length, crotch_depth, ph,))
            connection.commit()
            flash("Updated successfully", "success")
            return redirect(url_for("view_all_orders"))
            connection.close()
        return render_template('update_record_pant.html', data=data)
    elif dr == 'shirt':
        connection = sqlite3.connect("database.db")
        connection.row_factory = sqlite3.Row
        cursor = connection.cursor()
        cursor.execute('select * from shirtorders where phonenumber=?', (ph,))
        data = cursor.fetchone()
        connection.close()
        if request.method == 'POST':
            name = request.form['name']
            phonenumber = request.form['phonenumber']
            address = request.form['address']
            shirt_chest = request.form['shirt_chest']
            shirt_seat = request.form['shirt_seat']
            shirt_arm = request.form['shirt_arm']
            shirt_length = request.form['shirt_length']
            shirt_shoulder = request.form['shirt_shoulder']
            shirt_cuff = request.form['shirt_cuff']
            shirt_collar = request.form['shirt_collar']
            shirt_sleeve = request.form['shirt_sleeve']
            shirt_waist = request.form['shirt_waist']
            connection = sqlite3.connect("database.db")
            cursor = connection.cursor()
            cursor.execute(
                "update shirtorders set name=?, address=?, shirt_chest=?, shirt_seat=?, shirt_arm=?, shirt_length=?, shirt_shoulder=?, shirt_cuff=?, shirt_collar=?, shirt_sleeve=?, shirt_waist=? where phonenumber=?",
                (name, address, shirt_chest, shirt_seat, shirt_arm, shirt_length, shirt_shoulder, shirt_cuff,
                 shirt_collar, shirt_sleeve, shirt_waist, ph))
            connection.commit()
            flash("Updated successfully", "success")
            return redirect(url_for("view_all_orders"))
            connection.close()

        return render_template('update_record_shirt.html', data=data)

@app.route("/delete_record/<string:ph>/<string:dr>")
def delete_record(ph, dr):
    if dr == 'pant':
        connection = sqlite3.connect("database.db")
        cursor = connection.cursor()
        cursor.execute('delete from pantorders where phonenumber=?', (ph,))
        connection.commit()
        return redirect(url_for("view_all_orders"))
        connection.close()

    elif dr == 'shirt':
        connection = sqlite3.connect("database.db")
        cursor = connection.cursor()
        cursor.execute('delete from shirtorders where phonenumber=?', (ph,))
        connection.commit()
        return redirect(url_for("view_all_orders"))
        connection.close()


if __name__ == "__main__":
    app.run(debug=True)
