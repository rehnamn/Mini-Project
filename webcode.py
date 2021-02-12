from flask import *

from src.dbop import select, selectall, iud

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('login.html')


@app.route('/main')
def main():
    return render_template('login.html')


@app.route('/login', methods=['POST'])
def login():
    uname = request.form['un']
    password = request.form['pwd']

    qry = "select * from Login where username='" + uname + "' and password='" + password + "'"
    res = select(qry)

    if res is None:
        return ''' <script> alert('Invalid Username or Pssword');window.location='/'</script>'''
    else:
        if res[3] == 'admin':
            return render_template('adminhome.html')
        else:
            return ''' <script> alert('Invalid Username or Pssword');window.location='/'</script>'''


@app.route('/admin_view_user')
def admin_view_user():
    qry = "SELECT `user_reg`.*,`login`.`type`  FROM `login` JOIN `user_reg` ON `login`.`id` =`user_reg`.`lid`"
    res = selectall(qry)
    print(res)
    return render_template('adminviewuser.html', val=res)


@app.route('/blockuser')
def blockuser():
    lid = request.args.get('lid')
    qry = "update login set type='block' where id=" + str(lid) + ""
    iud(qry)
    return ''' <script> alert('blocked');window.location='/admin_view_user'</script>'''


@app.route('/unblockuser')
def unblockuser():
    lid = request.args.get('lid')
    qry = "update login set type='user' where id=" + str(lid) + ""
    iud(qry)
    return ''' <script> alert('unblock');window.location='/admin_view_user'</script>'''


@app.route('/view_traffic_police')
def view_traffic_police():
    qry = "SELECT * FROM traffic_police_reg"
    res = selectall(qry)
    print(res)
    return render_template('viewtrafficpolice.html', val=res)


@app.route('/deletepolice')
def deletepolice():
    police_id = request.args.get('id')
    qry = "delete from  traffic_police_reg where tp_id=" + str(police_id) + ""
    iud(qry)
    return ''' <script> alert('deleted');window.location='/view_traffic_police'</script>'''


@app.route('/traffic_police_reg', methods=['POST'])
def traffic_police_reg():
    return render_template('trafficpolicereg.html')


@app.route('/addpolice', methods=['POST'])
def addpolice():
    first_name = request.form['fname']
    mid_name = request.form['mname']
    last_name = request.form['lname']
    phone = request.form['ph']
    email = request.form['email']
    uname = request.form['un']
    password = request.form['pwd']
    qry = "insert into login values(null,'" + uname + "','" + password + "','police')"
    print(qry)
    lid = iud(qry)
    qry = "insert into traffic_police_reg values(null,'" + str(lid) + "','" + first_name + "','" + mid_name + "','" + last_name + "' ," + phone + ",'" + email + "')"
    print(qry)
    iud(qry)
    return ''' <script> alert('successful');window.location='/view_traffic_police'</script>'''


@app.route('/view_traffic_signal')
def view_traffic_signal():
    qry = "SELECT * FROM trafficsignal_reg"
    res = selectall(qry)
    print(res)
    return render_template('viewtrafficsignal.html', val=res)


@app.route('/deletesignal',methods=['get','post'])
def deletesignal():
    signal_id = request.args.get('id')
    qry = "delete from  trafficsignal_reg where ts_id=" + str(signal_id) + ""
    iud(qry)
    return ''' <script> alert('deleted');window.location='/view_traffic_signal'</script>'''


@app.route('/trafficsignal_reg', methods=['POST'])
def trafficsignal_reg():
    return render_template('trafficsignalreg.html')


@app.route('/addsignal', methods=['POST'])
def addsignal():
    name = request.form['name']
    latitude = request.form['latitude']
    longitude = request.form['longitude']
    qry = "insert into trafficsignal_reg values(null,'" + name + "','" +latitude+ "','" +longitude+ "')"
    print(qry)
    iud(qry)
    return ''' <script> alert('successful');window.location='/view_traffic_signal'</script>'''


@app.route('/view_important_place')
def view_important_place():
    qry = "SELECT * FROM imp_place_reg"
    res = selectall(qry)
    print(res)
    return render_template('viewimportentplace.html', val=res)


@app.route('/deleteplace',methods=['post','get'])
def deleteplace():
    place_id = request.args.get('id')
    qry = "delete from  imp_place_reg where ip_id='" + str(place_id) + "'"
    iud(qry)
    return ''' <script> alert('deleted');window.location='/view_important_place'</script>'''


@app.route('/importent_place_reg', methods=['POST'])
def important_place_reg():
    return render_template('importentplacereg.html')


@app.route('/addimp_place', methods=['POST','get'])
def addimp_place():
    name = request.form['name']
    description = request.form['description']
    latitude = request.form['latitude']
    longitude = request.form['longitude']
    qry = "insert into imp_place_reg values (null,'" + name + "','" + description + "','" + latitude + "','" + longitude + "')"
    iud(qry)
    return ''' <script> alert('successful');window.location='/view_important_place'</script>'''


@app.route('/view_spot_complaint')
def view_spot_complaint():
    qry = "SELECT `spotcomplaint`.*,`user_reg`.`fname`,`user_reg`.`mname`,`user_reg`.`lname`,`user_reg`.`phone` FROM `user_reg` JOIN `spotcomplaint` ON `spotcomplaint`.`uid`=`user_reg`.`lid`"
    res = selectall(qry)
    print(res)
    return render_template('viewspotcomplaint.html', val=res)


# @app.route('/deletespotcomplaint')
# def deletespotcomplaint():
#     spot_cmp_id = request.args.get('sc_id')
#     qry = "delete from spotcomplaint where sc_id=" + str(spot_cmp_id) + ""
#     iud(qry)
#     return ''' <script> alert('deleted');window.location='/view_spot_complaint'</script>'''


app.run(debug=True)

