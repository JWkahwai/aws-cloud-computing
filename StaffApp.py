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

@app.route("/", methods=['GET', 'POST'])
def home():
    #Staff list
    cursor = db_conn.cursor()
    cursor.execute("SELECT staff.StaffID,staff.Name,staff.Email,staff.Phone,role.RoleName,department.DepartmentName,staff.Salary,staff.Status,staff.ImageURL,staff.RoleID,staff.DepartmentID FROM staff LEFT JOIN role ON staff.RoleID=role.RoleID LEFT JOIN department ON staff.DepartmentID=department.DepartmentID")
    staffdata = cursor.fetchall()
    cursor.close()

    #Dropdown list
    cursor1 = db_conn.cursor()
    cursor1.execute("SELECT * FROM department")
    departdata = cursor1.fetchall()
    cursor1.close()

    #Dropdown list
    cursor2 = db_conn.cursor()
    cursor2.execute("SELECT * FROM role")
    roledata = cursor2.fetchall()
    cursor2.close()
    return render_template('Staff.html',depart=departdata,role=roledata,staff=staffdata)


@app.route("/about", methods=['GET', 'POST'])
def about():
    cursor = db_conn.cursor()
    cursor.execute("SELECT staff.Name,staff.Email,staff.Phone,role.RoleName,department.DepartmentName,staff.ImageURL FROM staff LEFT JOIN role ON staff.RoleID=role.RoleID LEFT JOIN department ON staff.DepartmentID=department.DepartmentID WHERE staff.DepartmentID=1 AND staff.Status='Active' ORDER BY RoleID ASC")
    staffdata = cursor.fetchall()
    cursor.close()
    return render_template('AboutUs.html',staff=staffdata)


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
        insert_sql = "INSERT INTO staff(Name,Email, Phone, RoleID, DepartmentID, Salary, Status) VALUES (%s,%s, %s, %s, %s, %s, 'Active')"
        cursor = db_conn.cursor()
        cursor.execute(insert_sql, (name,email, phone, role, department, salary))
        getID= cursor.lastrowid
        print("get cursor"+str(getID))
        print("get db:"+str(db_conn.insert_id()))
        db_conn.commit()
        # Uplaod image file in S3 #
        image_file_name = "staff-id-" + str(getID) + "_image_file"
        s3 = boto3.resource('s3')

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
            
            UpdateImage_sql = "UPDATE staff SET ImageURL=%s WHERE StaffID=%s"
            cursor = db_conn.cursor()
            cursor.execute(UpdateImage_sql, (object_url,getID))
            db_conn.commit()


        except Exception as e:
            return str(e)

    finally:
        cursor.close()

    titleData = "Data Added"
    return render_template('StaffOutput.html',title=titleData)

@app.route("/update", methods=['POST'])
def EditStaff():
    staffID= request.form['getStaffID']
    name = request.form['getName']
    email = request.form['getEmail']
    phone = request.form['getPhone']
    role = request.form['getRole']
    department = request.form['getDepartment']
    salary = request.form['getSalary']
    status = request.form['getStatus']
    edit_image = request.files['edtimage']

    #if no image uploaded
    if edit_image.filename == "":
        try:
            insert_sql = "UPDATE staff SET Name=%s, Email=%s, Phone=%s,RoleID=%s,DepartmentID=%s,Salary=%s,Status=%s WHERE StaffID=%s"
            cursor = db_conn.cursor()
            cursor.execute(insert_sql, (name, email, phone, role,department,salary,status,staffID))
            db_conn.commit()

        except Exception as e:
            return str(e)
            
        finally:
            cursor.close()

    #else got image upload, run image file query
    else:
        try:
            
            # Upload image file in S3 #
            image_file_name = "staff-id-" + str(staffID) + "_image_file"
            s3 = boto3.resource('s3')

            insert_sql = "UPDATE staff SET Name=%s, Email=%s, Phone=%s,RoleID=%s,DepartmentID=%s,Salary=%s,Status=%s WHERE StaffID=%s"
            cursor = db_conn.cursor()
            cursor.execute(insert_sql, (name, email, phone, role,department,salary,status,staffID))
            db_conn.commit()
            
            print("Data inserted in MySQL RDS... uploading image to S3...")
            s3.Bucket(custombucket).put_object(Key=image_file_name, Body=edit_image)
            bucket_location = boto3.client('s3').get_bucket_location(Bucket=custombucket)
            s3_location = (bucket_location['LocationConstraint'])
            
            if s3_location is None:
                s3_location = ''
            else:
                s3_location = '-' + s3_location
                object_url = "https://s3{0}.amazonaws.com/{1}/{2}".format(s3_location,custombucket,image_file_name)
        except Exception as e:
            return str(e)
        
        finally:
            cursor.close()
            
    titleData = "Data Updated"
    return render_template('StaffOutput.html',title=titleData)


@app.route('/delete/<string:ID>',methods=['POST','GET'])
def delete(ID):
    s3_client = boto3.client("s3")
    image_file_name = "staff-id-" + str(ID) + "_image_file"
    response = s3_client.delete_object(Bucket=custombucket, Key=image_file_name)
    delete_sql = "DELETE FROM staff WHERE StaffID=%s"
    cursor = db_conn.cursor()
    cursor.execute(delete_sql, (ID))
    db_conn.commit()
    titleData = "Data deleted"
    return render_template('StaffOutput.html',title=titleData)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80, debug=True)
