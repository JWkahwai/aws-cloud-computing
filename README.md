# CCAssignment

## PRE-STEP RDS
RDS setup follow config.py
customuser = "aws_user"
custompass = "Bait3273"
customdb = "staff" (dont change)
RDS create database -> mysql -> Free tier> database name 'staff' -> user = "aws_user" 
-> pass = "Bait3273" -> Public access :YES -> Security group : web-access -> AZ : 1b
-> initial db name : staff (not that important) ->disable automated backup -> CREATE

## PRE-STEP S3
custombucket = "kongkahwai-bucket" (changable config.py)
location : us-east-1
turn off the Block all public access


put this stuff into bucket policy

{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Sid": "AllowPublicRead",
            "Effect": "Allow",
            "Principal": {
                "AWS": "*"
            },
            "Action": "s3:GetObject",
            "Resource": "arn:aws:s3:::kongkahwai-bucket/*"
        }
    ]
}

##Create EC2 as usual

##Step 1 - config.py
Change line 1,5 to own RDS endpoint and S3 bucket Name

##Step 2 - connect rds with Heidisql [endpoint,user,pass]

##Step 3 - click left side first item on the Heidisql and click on a blue |> button Query at right hand side
Find staff.sql in this file and copy whole thing into the field (SPEED UP UR default data import)

##Step 4 - connect EC2 with ur git bash
EC2 -> Connect -> ssh blabla

after connect EC2,
type sudo su  [press enter]
then 
*COPY below*
#!/bin/bash
yum update -y
yum install git -y
git clone https://github.com/JWkahwai/CCAssignment.git
cd CCAssignment
pip3 install flask
pip3 install pymysql
pip3 install boto3
python3 StaffApp.py
---------------
*till above*
and click enter

Back to ur EC2,  
(IF U GOOD LUCK, find Public IPv4 address and click open address
ELSE find Public IPv4 DNS and click open address)

***NOTES***
1. All staff data have to insert one by one [due to the store file in cloud might cost]
2. All data will be inserted into RDS exclude the image will store into S3 bucket. [although it can be store RDS :D]
3. All data can be delete including the image inside the S3 bucket.
4. The about us page only display the data for the HR department. [Data have to inserted first to have better view on the about us page]
5. Might have minor change.

Special Acknowledge
1. Bootstrap css framework
2. DataTable
3. SweetAlert.js
4. AWS
5. bloody flask
