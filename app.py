from flask import Flask , render_template,request,session,redirect,url_for
import datetime
from flask_mysqldb import MySQL 
app = Flask(__name__, template_folder='template')
app.secret_key="casestudy"

app.config['MYSQL_HOST']= 'localhost'
app.config['MYSQL_USER']= 'root'
app.config['MYSQL_PASSWORD']=''
app.config['MYSQL_DB']='retailbanking'

mysql=MySQL(app)

@app.route('/', methods=['GET','POST'])
def index():
    if request.method == 'POST':
        userDetails= request.form 
        name=userDetails['uname']
        pas=userDetails['pass']
        cur = mysql.connection.cursor()
        cur.execute("select * from userstore")
        myresult=cur.fetchall()
        l=len(myresult)
        for i in range(l):
            if(myresult[i][0]==name and myresult[i][1]==pas):
                session['uname']=name
                return dashboard()
        else:
            return render_template('index.html',err="Wrong userid or password!")
        cur.close()
    return render_template('index.html')


@app.route('/dashboard', methods=['GET','POST'])
def dashboard():
    if 'uname' in session:
        uname=session['uname']
        return render_template('dashboard.html',uname=uname)

    return render_template('dashboard.html')

@app.route('/logout', methods=['GET','POST'])
def logout():
    return index()


@app.route('/createcustomer', methods=['GET','POST'])
def createcustomer():
    cur=mysql.connection.cursor()
    cur.execute("SELECT ssnid,customerid FROM customerdetails ORDER BY ssnid DESC LIMIT 1")
    values=cur.fetchall()
    new_ssnid=values[0][0]+1
    new_customerid=values[0][1]+1
    if request.method=='POST':
        name=request.form['name']
        ssn=request.form['ssn']
        custmid=request.form['custid']
        age=request.form['age']
        adr=request.form['adr']
        city=request.form['city']
        state=request.form['state']
        cur=mysql.connection.cursor()
        cur.execute("INSERT INTO customerdetails(ssnid,customername,age,address,state,city,customerid) VALUES(%s,%s,%s,%s,%s,%s,%s)",(ssn,name,age,adr,state,city,custmid))
        cur.execute("INSERT INTO customerstatus(ssnid,customerid,status,message) VALUES(%s,%s,%s,%s)",(ssn,custmid,"Active","Created Successfully"))
        mysql.connection.commit()
        cur.close()
        return render_template('createcustomer.html',mes="Successfully created")
    return render_template('createcustomer.html',new_customerid=new_customerid,new_ssnid=new_ssnid)


@app.route('/transfermoney', methods=['GET','POST'])
def transfermoney():
    return render_template('transfermoney.html')

@app.route('/home', methods=['GET','POST'])
def home():
    return dashboard()

@app.route('/updatecustomer', methods=['GET','POST'])
def updatecustomer():
    if 'custid1' in session:
        custid=session['custid1']
    if 'result1' in session:
        result=session['result1']
    if 'ssid' in session:
        ssnid=session['ssid']
    if request.method=='POST':
        name=request.form['new_name']
        age=request.form['new_age']
        adr=request.form['new_adr']
        cur=mysql.connection.cursor()
        data=(name,age,adr,custid)
        query="UPDATE customerdetails SET customername= %s,age=%s,address=%s WHERE customerid= %s"
        cur.execute(query,data)
        cur.execute("update customerstatus set status=%s, message=%s where customerid=%s",("Active","Updated Successfully",custid))
        mysql.connection.commit()
        data=custid
        cur=mysql.connection.cursor()
        cur.execute("SELECT * FROM customerdetails WHERE customerid= %s",[data])
        result=cur.fetchall()
        cur.close()
        #return "successfull"
        return render_template('updatecustomer.html',mes="Sucessfully updated!",result=result)
    return render_template('updatecustomer.html',result=result)

@app.route('/deletecustomer', methods=['GET','POST'])
def deletecustomer():
    if request.method =='POST':
        del_ssnid=request.form["ssnid"]
        del_custid=request.form["custid"]
        del_name=request.form["customername"]
        del_age=request.form["age"]
        cur=mysql.connection.cursor()
        query='SELECT COUNT(1) FROM customerdetails WHERE ssnid=%s and customerid=%s and customername=%s and age=%s'
        data=(del_ssnid,del_custid,del_name,del_age)
        cur.execute(query,data)
        if cur.fetchone()[0]:
            cur.execute( "delete  FROM customerdetails WHERE ssnid=%s", [del_ssnid] )
            cur.execute("update customerstatus set status=%s, message=%s where customerid=%s",("Not Active(deleted)","Account deleted",del_custid))
            mysql.connection.commit()
            cur.close()
            return render_template("deletecustomer.html",mes="Succefully deleted",flag=1)
        else:
            cur.close() 
            return render_template("deletecustomer.html",mes="no such customer exist",flag=0)
    return render_template("deletecustomer.html")


@app.route('/customerstatus', methods=['GET','POST'])
def customerstatus():
    cur=mysql.connection.cursor()
    resultval=cur.execute('SELECT * FROM customerstatus')
    if resultval>0:
        userdetails=cur.fetchall()
        return render_template('customerstatus.html',userdetails=userdetails)
    return render_template('customerstatus.html',mes="Not able to display!!")

@app.route('/createaccount', methods=['GET','POST'])
def createaccount():
    cur=mysql.connection.cursor()
    cur.execute("SELECT accountid FROM accounts ORDER BY accountid DESC LIMIT 1")
    values=cur.fetchall()
    new_actid=values[0][0]+1
    if request.method=='POST':
        ac_custid=request.form['custid']
        actid=request.form['actid']
        acctype=request.form['acctype']
        tr_amt=request.form['tr_amt']
        cur=mysql.connection.cursor()
        cur.execute('insert into accounts(customerid,accountid,accounttype,amt) values(%s,%s, %s, %s)', (ac_custid,actid,acctype,tr_amt))
        cur.execute('insert into accountstatus(customerid,accountid,accounttype,status,message) values(%s,%s, %s, %s,%s)', (ac_custid,actid,acctype,"Active","created successfully"))
        mysql.connection.commit()
        cur.close()
        return render_template('createaccount.html',mes="success!")
    return render_template('createaccount.html',new_actid=new_actid)


@app.route('/deleteaccount', methods=['GET','POST'])
def deleteaccount():
    if request.method=='POST':
        accid=request.form['accid']
        acctype=request.form['acctype']
        query='DELETE FROM accounts WHERE accountid=%s and accounttype= %s'
        data=(accid,acctype)
        cur=mysql.connection.cursor()
        cur.execute(query,data)
        cur.execute('update accountstatus set status=%s,message=%s where accountid=%s', ("Not Active","account deleted",accid))
        mysql.connection.commit()
        cur.close()
        return render_template('deleteaccount.html',mes="Successfully deleted!!")
    return render_template('deleteaccount.html')


@app.route('/accountstatus', methods=['GET','POST'])
def accountstatus():
    cur=mysql.connection.cursor()
    resultval=cur.execute('SELECT * FROM accountstatus')
    if resultval>0:
        userdetails=cur.fetchall()
        return render_template('accountstatus.html',userdetails=userdetails)
    return render_template('accountstatus.html',mes="Not able to display!!")


@app.route('/depositmoney', methods=['GET','POST'])
def depositmoney():
    return render_template('depositmoney.html')

@app.route('/withdrawmoney', methods=['GET','POST'])
def withdrawmoney():
    return render_template('withdrawmoney.html')


@app.route('/customer_search',methods=['GET','POST'])
def search():
    if request.method=="POST":
        ssnid=request.form['ssnid']
        custid=request.form['custid']
        session['custid1']=custid
        session['ssid']=ssnid
        data=custid
        cur=mysql.connection.cursor()
        cur.execute("SELECT * FROM customerdetails WHERE customerid= %s",[data])
        result=cur.fetchall()
        session['result1']=result
        return redirect(url_for('updatecustomer'))
    return render_template('/customer_search.html')

app.run()
