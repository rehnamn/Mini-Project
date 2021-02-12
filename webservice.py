import os

from flask import *
import pymysql
from werkzeug.utils import secure_filename
from datetime import datetime
from src.classify import predictfn
con = pymysql.connect(host='localhost', port=3306, user='root', passwd='', db='roadsens')
cmd = con.cursor()
app = Flask(__name__)


@app.route('/userreg', methods=['get', 'post'])
def userreg():
    fname = request.form['fname']
    mname = request.form['mname']
    lname = request.form['lname']

    ph = request.form['ph']
    email = request.form['email']
    username = request.form['un']
    pwd = request.form['pwd']
    cmd.execute("select * from login where username='" + username + "'  and type='user'")
    s = cmd.fetchone()
    if s is not None:
        return jsonify({'task': "invalid"})

    else:
        cmd.execute("INSERT INTO`login` values(null,'" + username + "','" + pwd + "','user')")
        id = con.insert_id()
        cmd.execute("insert into user_reg values(null,'" + str(id) + "','" + fname + "','" + mname + "','" + lname + "','" + ph + "','" + email + "')")
        con.commit()
        return jsonify({'task': "success"})


@app.route('/login', methods=['POST'])
def login():
    try:
        username = request.form['un']
        pwd = request.form['pwd']
        try:
            cmd.execute(
                "select * from login where username='" + username + "' and password='" + pwd + "'")
            s = cmd.fetchone()
            print(s)
            if s is not None:
                id = s[0]

                print(id)
                return jsonify({'task': str(id), 'type': s[3]})
            else:
                return jsonify({'task': "invalid"})
        except Exception as e:
            print(str(e))
            return jsonify({'task': "invalid"})
    except Exception as e:
        print(e)
        return jsonify({'task': "success"})





@app.route('/send_emg_alert', methods=['get', 'post'])
def send_emg_alert():
    latitude = request.form['latitude']
    longitude = request.form['longitude']
    description = request.form['description']
    uid = request.form['uid']
    cmd.execute(
        "insert into emergency_alert values(null,'" + uid + "','" + latitude + "','" + longitude + "','" + description + "')")
    con.commit()
    return jsonify({'task': "success"})


@app.route('/view_signal', methods=['POST', 'GET'])
def view_signal():
    latitude = request.form['latitude']
    longitude = request.form['longitude']

    cmd.execute("select * ,(3959 * ACOS ( COS ( RADIANS('" + str(
        latitude) + "') ) * COS( RADIANS(`latitude`) ) * COS( RADIANS(`longitude`) - RADIANS('" + str(
        longitude) + "') ) + SIN ( RADIANS('" + str(
        latitude) + "') ) * SIN( RADIANS(`latitude`) ))) AS user_distance from trafficsignal_reg  HAVING user_distance  < 6.2137")

    print("select * ,(3959 * ACOS ( COS ( RADIANS('" + str(
        latitude) + "') ) * COS( RADIANS(`latitude`) ) * COS( RADIANS(`longitude`) - RADIANS('" + str(
        longitude) + "') ) + SIN ( RADIANS('" + str(
        latitude) + "') ) * SIN( RADIANS(`latitude`) ))) AS user_distance from trafficsignal_reg  HAVING user_distance  < 6.2137")
    s = cmd.fetchall();
    print(s)
    row_headers = [x[0] for x in cmd.description]
    json_data = []
    for result in s:
        json_data.append(dict(zip(row_headers, result)))
    print(json_data)
    return jsonify(json_data)


@app.route('/view_important_place', methods=['POST', 'GET'])
def view_important_place():
    latitude = request.form['latitude']
    longitude = request.form['longitude']
    cmd.execute("select *  ,(3959 * ACOS ( COS ( RADIANS('" + str(latitude) + "') ) * COS( RADIANS(`latitude`) ) * COS( RADIANS(`longitude`) - RADIANS('" + str(
        longitude) + "') ) + SIN ( RADIANS('" + str(latitude) + "') ) * SIN( RADIANS(`latitude`) ))) AS user_distance from imp_place_reg HAVING user_distance  < 6.2137")
    s = cmd.fetchall();
    print(s)
    row_headers = [x[0] for x in cmd.description]
    json_data = []
    for result in s:
        json_data.append(dict(zip(row_headers, result)))
    print(json_data)
    return jsonify(json_data)


@app.route('/view_complaint', methods=['POST', 'GET'])
def view_complaint():

    cmd.execute(" SELECT `spotcomplaint`.* ,`user_reg`.`fname`,`mname`,`lname`,`phone` FROM `user_reg` JOIN `spotcomplaint` ON `spotcomplaint`.`uid`=`user_reg`.lid  where status='pending'")
    s = cmd.fetchall();
    print(s)
    row_headers = [x[0] for x in cmd.description]
    json_data = []
    for result in s:
        json_data.append(dict(zip(row_headers, result)))
    print(json_data)
    return jsonify(json_data)


@app.route('/view_status', methods=['POST', 'GET'])
def view_status():
    uid = request.form['uid']
    cmd.execute( " SELECT`spotcomplaint`.complaint,status,`traffic_police_reg`.`fname`,`mname`,`lname`,`phone` FROM `traffic_police_reg` JOIN `spotcomplaint` ON `spotcomplaint`.`policid`=`traffic_police_reg`.lid WHERE uid='" + uid + "'")
    s = cmd.fetchall();
    print(s)
    row_headers = [x[0] for x in cmd.description]
    json_data = []
    for result in s:
        json_data.append(dict(zip(row_headers, result)))
    print(json_data)
    return jsonify(json_data)


@app.route('/view_emergency_alert', methods=['POST', 'GET'])
def view_emergency_alert():
    cmd.execute("SELECT `emergency_alert`.`descripion` ,`user_reg`.`fname`,`mname`,`lname`,`phone` FROM `user_reg` JOIN `emergency_alert` ON `emergency_alert`.`uid`=`user_reg`.lid ")
    s = cmd.fetchall();
    print(s)
    row_headers = [x[0] for x in cmd.description]
    json_data = []
    for result in s:
        json_data.append(dict(zip(row_headers, result)))
    print(json_data)
    return jsonify(json_data)


@app.route('/update_status', methods=['POST', 'GET'])
def update_status():
    sc_id = request.form['cid']
    reply=request.form['reply']
    pid=request.form['pid']

    cmd.execute( "UPDATE `spotcomplaint` SET `spotcomplaint`.`status`='"+reply+"',policid='"+pid+"' WHERE `spotcomplaint`.`sc_id`='"+str(sc_id)+"'")
    con.commit()
    return jsonify({'task': "success"})



@app.route('/emergency', methods=['get', 'post'])
def emergency():
    con = pymysql.connect(host='localhost', port=3306, user='root', passwd='', db='roadsens')
    cmd = con.cursor()
    latitude = request.form['latitude']
    longitude = request.form['longitude']
    speed = request.form['speed']

    cmd.execute("insert into distruption  values(null,'" + latitude + "','" + longitude + "','" +speed + "',now())")
    con.commit()
    return jsonify({'task': "success"})

@app.route('/service',methods=['POST'])
def service():
    con = pymysql.connect(host='localhost', port=3306, user='root', passwd='', db='roadsens')
    cmd = con.cursor()
    latitude=request.form['lati']
    longitude=request.form['longi']
    cmd.execute("select *  ,(3959 * ACOS ( COS ( RADIANS("+latitude+") ) * COS( RADIANS(`latitude`) ) * COS( RADIANS(`longitude`) - RADIANS("+longitude+") ) + SIN ( RADIANS("+latitude+") ) * SIN( RADIANS(`latitude`) ))) AS user_distance from distruption where strength<4440 and strength>1000 and date>=DATE_ADD(curdate(),interval -10 day)  HAVING user_distance  < 2 ")
    s=cmd.fetchall()

    cmd.execute(
        "select *  ,(3959 * ACOS ( COS ( RADIANS(" + latitude + ") ) * COS( RADIANS(`latitude`) ) * COS( RADIANS(`longitude`) - RADIANS(" + longitude + ") ) + SIN ( RADIANS(" + latitude + ") ) * SIN( RADIANS(`latitude`) ))) AS user_distance from distruption where strength<4440 and strength>1000 and date<DATE_ADD(curdate(),interval -10 day)and date>DATE_ADD(curdate(),interval -20 day)  HAVING user_distance  < 2 ")
    s1 = cmd.fetchall()
    print(len(s1))

    print(len(s))
    if len(s1)<len(s):
        if len(s)>5:
            return jsonify({"task":"yes"})
        else:
            return jsonify({"task": "no"})
    else:
        if len(s1)>5:
            p=(len(s)/len(s1))*100
            if p>50.0:
                return jsonify({"task": "yes"})
            else:
                return jsonify({"task": "no"})
        else:
            return jsonify({"task": "no"})


@app.route("/capture",methods=['post'])
def capture():
    img=request.files["files"]
    lt=request.form['latitude']
    lon=request.form['longitude']

    file = datetime.now().strftime("%Y%m%d%H%M%S")+".jpg"
    img.save(os.path.join("static/camimg", file))
    re=predictfn(os.path.join("static/camimg", file))
    if re!='normal':
        cmd.execute("insert into distruption  values(null,'" + lt + "','" + lon + "','4000',now())")
        con.commit()
    return jsonify({'task': "success"})

@app.route('/marker', methods=['POST', 'GET'])
def marker():
    cmd.execute("select * from distruption where date>=DATE_ADD(curdate(),interval -10 day)")
    s = cmd.fetchall();
    print(s)
    row_headers = [x[0] for x in cmd.description]
    json_data = []
    for result in s:
        json_data.append(dict(zip(row_headers, result)))
    print(json_data)
    return jsonify(json_data)



@app.route('/send_spot_complaint', methods=['get', 'post'])
def send_spot_complaint():
    latitude = request.form['latitude']
    print(latitude)
    longitude = request.form['longitude']
    complaint = request.form['complaint']
    print(complaint)
    uid = request.form['uid']
    image=request.files['files']
    file=secure_filename(image.filename)
    image.save(os.path.join("static/image",file))
    cmd.execute(
        "insert into spotcomplaint values(null,'" + uid + "','" + latitude + "','" + longitude + "','" + complaint + "','pending',null,'"+str(file)+"')")
    con.commit()
    return jsonify({'task': "success"})
if (__name__ == "__main__"):
    app.run(host='0.0.0.0', port=5000)
