from flask import Flask, render_template, request
from pymysql import connections
import os
import boto3
from config import *

app = Flask(__name__)

bucket = custombucket
region = customregion

db_conn = connections.Connection(
    host=customhost,
    port=3306,
    user=customuser,
    password=custompass,
    db=customdb

)
output = {}
table = 'staff'
bucket_location = boto3.client('s3').get_bucket_location(Bucket=custombucket)
s3_location = (bucket_location['LocationConstraint'])

@app.route("/staff", methods=['GET', 'POST'])
def home():
    cursor = db_conn.cursor()
    cursor.execute("SELECT * FROM staff")
    data = cursor.fetchall()
    cursor.close()
    return render_template('Staff.html', staff=data,custombucket=bucket,s3_location=s3_location)


@app.route("/about", methods=['POST'])
def about():
    return render_template('AboutUs.html')


@app.route("/addstaff", methods=['POST'])
def AddStaff():
    name = request.form['Name']
    email = request.form['Email']
    phone = request.form['Phone']
    role = request.form['Role']
    department = request.form['Department']
    salary = request.form['Salary']
    image_file = request.files['image']

    if image_file.filename == "":
        return "Please select a file"

    try:
        
        # Uplaod image file in S3 #
        image_file_name = "staff-id-" + str(name) + "_image_file"
        s3 = boto3.resource('s3')

        insert_sql = "INSERT INTO staff(Name,Email, Phone, Role, Department, Salary, Status) VALUES (%s,%s, %s, %s, %s, %s, 'Active',%s)"
        cursor = db_conn.cursor()
        cursor.execute(insert_sql, (name,email, phone, role, department, salary))
        db_conn.commit()

        try:
            print("Data inserted in MySQL RDS... uploading image to S3...")
            s3.Bucket(custombucket).put_object(Key=image_file_name, Body=image_file)
            bucket_location = boto3.client('s3').get_bucket_location(Bucket=custombucket)
            s3_location = (bucket_location['LocationConstraint'])

            if s3_location is None:
                s3_location = ''
            else:
                s3_location = '-' + s3_location

            object_url = "https://s3{0}.amazonaws.com/{1}/{2}".format(
                s3_location,
                custombucket,
                image_file_name)

        except Exception as e:
            return str(e)

    finally:
        cursor.close()

    print("all modification done...")
    title = "Data Added"
    return render_template('StaffOutput.html',title=title)

@app.route("/editstaff", methods=['POST'])
def EditStaff():
    staffID= request.form['getStaffID']
    name = request.form['getName']
    email = request.form['getEmail']
    phone = request.form['getPhone']
    role = request.form['getRole']
    department = request.form['getDepartment']
    salary = request.form['getSalary']
    status = request.form['getStatus']
    image_file = request.files['edtimage']

    if image.filename == "":
        return "Please select a file"

    try:
        
        # Upload image file in S3 #
        image_file_name = "staff-id-" + str(name) + "_image_file"
        s3 = boto3.resource('s3')

        insert_sql = """
               UPDATE staff
               SET Name=%s, Email=%s, Phone=%s,Role=%s,Department=%s,Salary=%s,Status=%s 
               WHERE StaffID=%s
            """
        cursor = db_conn.cursor()
        cursor.execute(insert_sql, (name, email, phone, role,department,salary,status,staffID))
        db_conn.commit()

        try:
            print("Data inserted in MySQL RDS... uploading image to S3...")
            s3.Bucket(custombucket).put_object(Key=image_file_name, Body=image_file)
            bucket_location = boto3.client('s3').get_bucket_location(Bucket=custombucket)
            s3_location = (bucket_location['LocationConstraint'])

            if s3_location is None:
                s3_location = ''
            else:
                s3_location = '-' + s3_location

            object_url = "https://s3{0}.amazonaws.com/{1}/{2}".format(
                s3_location,
                custombucket,
                image_file_name)

        except Exception as e:
            return str(e)

    finally:
        cursor.close()

    print("all modification done...")
    title = "Data Updated"
    return render_template('StaffOutput.html',title=title)


@app.route('/delete/<string:staffID>',methods=['POST','GET'])
def delete():
    s3_client = boto3.client("s3")
    #response = s3_client.delete_object(Bucket=custombucket, Key=image_file_name)
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM staff WHERE StaffID=%s", (staffID,))
    mysql.connection.commit()
    title = "Data deleted"
    return render_template('StaffOutput.html',title=title)

""" #Backup
@app.route('/update',methods=['POST','GET'])
def update():
    if request.method == 'POST':
        staffID = request.form['getStaffID']
        name = request.form['Name']
        email = request.form['Email']
        phone = request.form['Phone']
        role = request.form['Role']
        department = request.form['Department']
        salary = request.form['Salary']
        image = request.files['image']
        cursor = db_conn.cursor()
        cursor.execute(, (name, email, phone, role,department,salary,staffID))
        flash("Data Updated Successfully")
        db_conn.commit()
        return redirect(url_for('home'))
"""

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80, debug=True)