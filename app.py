from flask import Flask, render_template, request, redirect, url_for, request
from flask_mysqldb import MySQL


PhoneSpecifications=['Sno','Name','Announced','Dimensions','Weight','Build','Size','Resolution','Protection','OS','Chipset','Internal','Sensors','Colors','Price']
app = Flask(__name__)

#MySQL configuration
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'root'
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_DB'] = 'Project2020'
'''app.config[]'''
mysql = MySQL()
mysql.init_app(app)

@app.route('/')
def home():
	return render_template("home.html")

@app.route('/about')
def about():
	return render_template("about.html")

@app.route('/service')
def service():
	return render_template("service.html")

@app.route('/pricing')
def pricing():
	return render_template("pricing.html")

@app.route('/phones', methods=['POST', 'GET'])
def phones():
	if request.method == "POST":
		try:
			NameFilter = request.form.get('NameFilter')
			cur = mysql.connection.cursor()
			cur.execute(f'''SELECT Sno, Name, Company, DATE_FORMAT(Date, "%M %e %Y") as date FROM Phone WHERE upper(name) like \'%{NameFilter.upper()}%\' ;''')
			data=cur.fetchall()
			return render_template("phones.html", data=data)
		except:
			pass	
			try:
				BrandFilter = request.form.get('BrandFilter')
				cur = mysql.connection.cursor()
				cur.execute(f'''SELECT Sno, Name, Company, DATE_FORMAT(Date, "%M %e %Y") as date FROM Phone WHERE upper(company) like \'%{BrandFilter.upper()}%\' ;''')
				data=cur.fetchall()
				return render_template("phones.html", data=data)
			except:
				pass
		else:
			try:
				BrandFilter = request.form.get('BrandFilter')
				cur = mysql.connection.cursor()
				cur.execute(f'''SELECT Sno, Name, Company, DATE_FORMAT(Date, "%M %e %Y") as date FROM Phone WHERE upper(company) like \'%{BrandFilter.upper()}%\' ;''')
				data=cur.fetchall()
				return render_template("phones.html", data=data)
			except:
				return render_template("phones.html", data=data)
			else:
				BrandFilter = request.form.get('BrandFilter')
				cur = mysql.connection.cursor()
				cur.execute(f'''SELECT Sno, Name, Company, DATE_FORMAT(Date, "%M %e %Y") as date FROM Phone WHERE upper(name) like \'%{BrandFilter.upper()}%\' and  upper(company) like \'%{BrandFilter.upper()}%\' ;''')
				data=cur.fetchall()
				return render_template("phones.html", data=data)
	else:
		cur = mysql.connection.cursor()
		#cur.execute('''Create table example (id Integer, name Varchar(20))''')
		cur.execute('''SELECT Sno, Name, Company, DATE_FORMAT(Date, "%M %e %Y") as Date FROM Phone order by name;''')
		data=cur.fetchall()
		return render_template("phones.html", data=data)	


@app.route('/phonedetails', methods=['POST', 'GET'])
def phonedetails():
	if request.method == "POST":
		cur = mysql.connection.cursor()
		DetailsRequest=request.form.get('DetailsRequest')
		cur.execute(f'''SELECT * FROM PhoneDetails where Sno={DetailsRequest};''')
		data=cur.fetchone()
		Len=len(data)
		return render_template("phonedetails.html", data=data,PhoneSpecifications=PhoneSpecifications, Len=Len,DetailsRequest=DetailsRequest) 
	elif request.method == "GET":
		cur = mysql.connection.cursor()
		cur.execute('''SELECT Sno, Name, Company, DATE_FORMAT(Date, "%M %e %Y") as Date FROM Phone order by name;''')
		data=cur.fetchall()
		return redirect(url_for('phones'), code=307)

@app.route('/laptops', methods=['POST', 'GET'])
def laptops():
	if request.method == "POST":
		try:
			NameFilter = request.form.get('NameFilter')
			cur = mysql.connection.cursor()
			cur.execute(f'''SELECT Sno, Name, Company, DATE_FORMAT(Date, "%M %e %Y") as date FROM laptop WHERE upper(name) like \'%{NameFilter.upper()}%\' ;''')
			data=cur.fetchall()
			return render_template("laptops.html", data=data)
		except:
			try:
				BrandFilter = request.form.get('BrandFilter')
				cur = mysql.connection.cursor()
				cur.execute(f'''SELECT Sno, Name, Company, DATE_FORMAT(Date, "%M %e %Y") as date FROM laptop WHERE upper(company) like \'%{BrandFilter.upper()}%\' ;''')
				data=cur.fetchall()
				return render_template("laptops.html", data=data)
			except:
				return render_template("laptops.html", data=data)
		else:
			try:
				BrandFilter = request.form.get('BrandFilter')
				cur = mysql.connection.cursor()
				cur.execute(f'''SELECT Sno, Name, Company, DATE_FORMAT(Date, "%M %e %Y") as date FROM laptop WHERE upper(company) like \'%{BrandFilter.upper()}%\' ;''')
				data=cur.fetchall()
				return render_template("laptops.html", data=data)
			except:
				return render_template("laptops.html", data=data)
			else:
				BrandFilter = request.form.get('BrandFilter')
				cur = mysql.connection.cursor()
				cur.execute(f'''SELECT Sno, Name, Company, DATE_FORMAT(Date, "%M %e %Y") as date FROM laptop WHERE upper(name) like \'%{BrandFilter.upper()}%\' and  upper(company) like \'%{BrandFilter.upper()}%\' ;''')
				data=cur.fetchall()
				return render_template("laptops.html", data=data)
	else:
		cur = mysql.connection.cursor()
		cur.execute('''SELECT Sno, Name, Company, DATE_FORMAT(Date, "%M %e %Y") as date FROM laptop order by name;''')
		data=cur.fetchall()
		return render_template("laptops.html", data=data)	
	
@app.route('/add', methods=['POST', 'GET'])
def add():
	if request.method == "POST":
		try:
			user_name = request.form.get('user-name')
			phone_name = request.form.get('phone-name')
			phone_manufacturer  = request.form.get('phone-manufacturer')
			phone_date = request.form.get('phone-date')
			cur = mysql.connection.cursor()
			Query=f'''select max(Sno)from TempPhone;'''
			cur.execute(Query)
			C=cur.fetchone()[0]
			if C==None:
				C=0
			Q=f'''insert into TempPhone
				values({C+1},\'{phone_name}\',\'{phone_manufacturer}\',\'{phone_date}\') ;'''
			cur.execute(Q)
			mysql.connection.commit()
			return render_template("add.html", phone_name = phone_name, phone_manufacturer = phone_manufacturer, phone_date = phone_date, user_name = user_name)
		except:
			try:
				user_name = request.form.get('user-name')
				laptop_name = request.form.get('laptop-name')
				laptop_manufacturer  = request.form.get('laptop-manufacturer')
				laptop_date = request.form.get('laptop-date')
				cur = mysql.connection.cursor()
				Query=f'''select max(Sno)from TempLaptop;'''
				cur.execute(Query)
				C=cur.fetchone()[0]
				if C==None:
					C=0
				Q=f'''insert into TempLaptop
					values({C+1},\'{laptop_name}\',\'{laptop_manufacturer}\',\'{laptop_date}\') ;'''
				cur.execute(Q)
				mysql.connection.commit()
				return render_template("add.html", laptop_name = laptop_name, laptop_manufacturer = laptop_manufacturer, laptop_date = laptop_date, user_name = user_name)
			except:
				user_name = request.form.get('user-name')
				other_name = request.form.get('other-name')
				other_manufacturer  = request.form.get('other-manufacturer')
				other_date = request.form.get('other-date')
				cur = mysql.connection.cursor()
				Query=f'''select max(Sno)from Tempother;'''
				cur.execute(Query)
				C=cur.fetchone()[0]
				if C==None:
					C=0
				Q=f'''insert into Tempother
					values({C+1},\'{other_name}\',\'{other_manufacturer}\',\'{other_date}\') ;'''
				cur.execute(Q)
				mysql.connection.commit()
				return render_template("add.html", other_name = other_name, other_manufacturer = other_manufacturer, other_date = other_date, user_name = user_name)

	elif request.method == "GET":
			return render_template("add.html")

@app.route('/blog')
def blog():
	return render_template("blog.html")

@app.route('/blog_details')
def blog_details():
	return render_template("blog_details.html")

@app.route('/contact', methods=['POST', 'GET'])
def contact():
	if request.method == "POST":
		message_name = request.form.get('message-name')
		message_email  = request.form.get('message-email')
		message = request.form.get('message')
		return render_template("contact.html", message_name = message_name, message_email=message_email, message=message )
	elif request.method == "GET":
		return render_template("contact.html")

@app.route('/login', methods=['POST', 'GET'])
def login():
	Boolean= False
	error=None
	if request.method == "POST":
		if request.form['username'] != 'admin' or request.form['password'] != 'admin':
			error = 'Invalid Credentials. Please try again.'
		else:
			Boolean= True
			return redirect(url_for('menu'), code=307)
	return render_template('login.html', error=error, Boolean=Boolean)


@app.route('/menu', methods=['POST', 'GET'])
def menu():
	if request.method == "POST":
		try:
			choice=request.form['1.']
			pass
		except:
			try:
				choice=request.form['2.']
			except:
				try:
					choice=request.form['3.']
				except:
					try:
						choice=request.form['4.']
					except:
						#add another try block for 5.
						return render_template("menu.html")
					else:
						return render_template("laptops.html")
				else:
					return render_template("addlaptop.html")
			else:
				return render_template("addother.html")
		else:
			return render_template("addphone.html")				
	elif request.method == "GET":
		return redirect(url_for('login'))

@app.route('/addphone', methods=['POST', 'GET'] )
def addphone():
	cur = mysql.connection.cursor()
	cur.execute('''select*from TempPhone''')
	data=cur.fetchall()
	if request.method == "POST":
		try:
			if request.form['ListOfSno'] != '':
				pass
		except:
			return render_template("addphone.html", data=data)
		else:
			try:
				ListOfSno=request.form.get('ListOfSno')
				ListOfSno=ListOfSno.split(',')
				for i in ListOfSno:	

					Q=f'''insert into Phone(Name,Company,Date)
							select Name, Company, Date from TempPhone where Sno={i};'''
					cur.execute(Q)
					mysql.connection.commit()
					Q1=f'''delete from TempPhone where Sno={i};'''
					cur.execute(Q1)
					mysql.connection.commit()
					return render_template("addphone.html",ListOfSno=ListOfSno, data=data)


					
			except:
				return render_template("addphone.html",ListOfSno='Error', data=data)					
	elif request.method == "GET":
		return redirect(url_for('login'))

@app.route('/addlaptop', methods=['POST', 'GET'] )
def addlaptop():
	cur = mysql.connection.cursor()
	cur.execute('''select*from TempLaptop''')
	data=cur.fetchall()
	if request.method == "POST":
		try:
			if request.form['ListOfSno'] != '':
				pass
		except:
			return render_template("addlaptop.html", data=data)
		else:
			ListOfSno=request.form.get('ListOfSno')
			ListOfSno=ListOfSno.split(',')
			for i in ListOfSno:	
				Q=f'''insert into Laptop(Name,Company,Date)
						select Name, Company, Date from TempLaptop where Sno={i};'''
				cur.execute(Q)
				mysql.connection.commit()
				Q1=f'''delete from TempLaptop where Sno={i};'''
				cur.execute(Q1)

				mysql.connection.commit()
			return render_template("addlaptop.html",ListOfSno=ListOfSno, data=data)			
	elif request.method == "GET":
		return redirect(url_for('login'))


@app.route('/compare', methods=['POST', 'GET'] )
def compare():
	if request.method == "POST":
		try:
			Choice1 = request.form.get('Choice1')
			Choice2  = request.form.get('Choice2')
		except:
			return redirect(url_for('login'))
		else:
			cur = mysql.connection.cursor()
			cur.execute(f'''SELECT * FROM PhoneDetails where Sno={Choice1};''')
			data=cur.fetchone()
			cur.execute(f'''SELECT * FROM PhoneDetails where Sno={Choice2};''')
			data1=cur.fetchone()
			Len=len(data)
			return render_template("compare.html", data=data,data1=data1,PhoneSpecifications=PhoneSpecifications, Len=Len) 
			''', Len=Len'''
	elif request.method == "GET":

		return redirect(url_for('phones'), code=307) 	

@app.route('/others', methods=['POST', 'GET'])
def others():
	if request.method == "POST":
		try:
			NameFilter = request.form.get('NameFilter')
			cur = mysql.connection.cursor()
			cur.execute(f'''SELECT Sno, Name, Company, DATE_FORMAT(Date, "%M %e %Y") as date FROM other WHERE upper(name) like \'%{NameFilter.upper()}%\' ;''')
			data=cur.fetchall()
			return render_template("others.html", data=data)
		except:
			try:
				BrandFilter = request.form.get('BrandFilter')
				cur = mysql.connection.cursor()
				cur.execute(f'''SELECT Sno, Name, Company, DATE_FORMAT(Date, "%M %e %Y") as date FROM other WHERE upper(company) like \'%{BrandFilter.upper()}%\' ;''')
				data=cur.fetchall()
				return render_template("others.html", data=data)
			except:
				return render_template("others.html", data=data)
		else:
			try:
				BrandFilter = request.form.get('BrandFilter')
				cur = mysql.connection.cursor()
				cur.execute(f'''SELECT Sno, Name, Company, DATE_FORMAT(Date, "%M %e %Y") as date FROM other WHERE upper(company) like \'%{BrandFilter.upper()}%\' ;''')
				data=cur.fetchall()
				return render_template("others.html", data=data)
			except:
				return render_template("others.html", data=data)
			else:
				BrandFilter = request.form.get('BrandFilter')
				cur = mysql.connection.cursor()
				cur.execute(f'''SELECT Sno, Name, Company, DATE_FORMAT(Date, "%M %e %Y") as date FROM other WHERE upper(name) like \'%{BrandFilter.upper()}%\' and  upper(company) like \'%{BrandFilter.upper()}%\' ;''')
				data=cur.fetchall()
				return render_template("others.html", data=data)
	else:
		cur = mysql.connection.cursor()
		cur.execute('''SELECT Sno, Name, Company, DATE_FORMAT(Date, "%M %e %Y") as date FROM other order by name;''')
		data=cur.fetchall()
		return render_template("others.html", data=data)	

@app.route('/addother', methods=['POST', 'GET'] )
def addother():
	cur = mysql.connection.cursor()
	cur.execute('''select*from Tempother''')
	data=cur.fetchall()
	if request.method == "POST":
		try:
			if request.form['ListOfSno'] != '':
				pass
		except:
			return render_template("addother.html", data=data)
		else:
			ListOfSno=request.form.get('ListOfSno')
			ListOfSno=ListOfSno.split(',')
			for i in ListOfSno:	
				Q=f'''insert into other(Name,Company,Date)
						select Name, Company, Date from Tempother where Sno={i};'''
				cur.execute(Q)
				mysql.connection.commit()
				Q1=f'''delete from Tempother where Sno={i};'''
				cur.execute(Q1)

				mysql.connection.commit()
			return render_template("addother.html",ListOfSno=ListOfSno, data=data)			
	elif request.method == "GET":
		return redirect(url_for('login')) 	 	