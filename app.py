from flask import Flask, render_template, request, redirect, url_for, request
from flask_mysqldb import MySQL

'''
cd /c/FlaskProjects
source VirtualFlask/Scripts/activate
export FLASK_ENV=development
export FLASK_APP=app.py
flask run

git add .
git commit -am 'NameOfCommit'
git push

Initialising the tables given below at the end
'''

# Initialising the parameters on the basis of which the data will be inserted into the PhoneDetails MySQL table
# Website used for data is gsmarena
PhoneSpecifications=['Sno','Name','Announced','Dimensions','Weight','Build','Size','Resolution','Protection','OS','Chipset','Internal','Sensors','Colors','Price']

# App configuration for MySQL and the name of the app
app = Flask(__name__)


#MySQL configuration
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'root'
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_DB'] = 'Project2020'
mysql = MySQL()
mysql.init_app(app)

# Defining the function for the home page and its route for href tags for HTML
@app.route('/', methods=['POST', 'GET'])
#This is a dummy page which is present for looks
def home():
    return render_template("home.html")

# Defining the function for the about page and its route for href tags for HTML
@app.route('/about')
#This is a dummy page which is present for looks
def about():
    return render_template("about.html")

# Defining the function for the service page and its route for href tags for HTML
@app.route('/service')
#This is a dummy page which is present for looks
def service():
    return render_template("service.html")

# Defining the function for the pricing page and its route for href tags for HTML (Now Scrapped)
@app.route('/pricing')
def pricing():
    return render_template("pricing.html")

# Defining the function for the phone overview page and its route for href tags for HTML.
@app.route('/phones', methods=['POST', 'GET']) #Defining the methods of accessing the page to differentiate when using forms
#This function is responsible for the page phone.html. It is responsible for the comparing the phones and displaying their details while also making the filters work.
def phones():
    #When a form such as the search bar is POSTED from the webpage the we have to get the form. 
    if request.method == "POST":
        try:
            #Checking if the first form is empty or not
            NameFilter = request.form.get('NameFilter')
            cur = mysql.connection.cursor()
            cur.execute(f'''SELECT Sno, Name, Company, DATE_FORMAT(Date, "%M %e %Y") as date FROM Phone WHERE upper(name) like \'%{NameFilter.upper()}%\' ;''')
            data=cur.fetchall()
            return render_template("phones.html", data=data)
        except:
            #if first form is empty and no value is returned then the second form is checked    
            try:
                BrandFilter = request.form.get('BrandFilter')
                cur = mysql.connection.cursor()
                cur.execute(f'''SELECT Sno, Name, Company, DATE_FORMAT(Date, "%M %e %Y") as date FROM Phone WHERE upper(company) like \'%{BrandFilter.upper()}%\' ;''')
                data=cur.fetchall()
                return render_template("phones.html", data=data)
            except:
                #Left empty because even if the form is empty, due to the use of %% with like in each query all of the data is rendered essentially rendering the stock page
                pass
        else:
            #checking for second form
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
        #if no form is filled (ie the page is fetched using GET) then render entire page
        cur = mysql.connection.cursor()
        cur.execute('''SELECT Sno, Name, Company, DATE_FORMAT(Date, "%M %e %Y") as Date FROM Phone order by name;''')
        data=cur.fetchall()
        return render_template("phones.html", data=data)


# Defining the function for the phone details page and its route for href tags for HTML.
#PLEASE SEE googlescrape.py TO SEE HOW THE DATA IS ENTERED INTO PhoneDetails
@app.route('/phonedetails', methods=['POST', 'GET'])
#This function is responsible for the page phonedetails.html. It is responsible for the showing the details of a single phone.
def phonedetails():
    if request.method == "POST":
        cur = mysql.connection.cursor()
        DetailsRequest=request.form.get('DetailsRequest')
        cur.execute(f'''SELECT * FROM PhoneDetails where Sno={DetailsRequest};''')
        data=cur.fetchone()
        Len=len(data)
        return render_template("phonedetails.html", data=data, PhoneSpecifications=PhoneSpecifications, Len=Len, DetailsRequest=DetailsRequest) 
    elif request.method == "GET":
        cur = mysql.connection.cursor()
        cur.execute('''SELECT Sno, Name, Company, DATE_FORMAT(Date, "%M %e %Y") as Date FROM Phone order by name;''')
        data=cur.fetchall()
        return redirect(url_for('phones'), code=307) #Code 307 refers to forcing the redirect function to consider itself as a POST request so as to take in all the parameters

# Defining the function for the laptop page and its route for href tags for HTML.
@app.route('/laptops', methods=['POST', 'GET'])
def laptops():
#This function is responsible for the page laptops.html. It is responsible for the showing the table of laptops.
    #When a form such as the search bar is POSTED from the webpage the we have to get the form. 
    if request.method == "POST":
        try:
            #if first form is empty and no value is returned then the second form is checked    
            NameFilter = request.form.get('NameFilter')
            cur = mysql.connection.cursor()
            cur.execute(f'''SELECT Sno, Name, Company, DATE_FORMAT(Date, "%M %e %Y") as date FROM laptop WHERE upper(name) like \'%{NameFilter.upper()}%\' ;''')
            data=cur.fetchall()
            return render_template("laptops.html", data=data)
        except:
            try:
                #checking for second form
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
        #if no form is filled (ie the page is fetched using GET) then render entire page
        cur = mysql.connection.cursor()
        cur.execute('''SELECT Sno, Name, Company, DATE_FORMAT(Date, "%M %e %Y") as date FROM laptop order by name;''')
        data=cur.fetchall()
        return render_template("laptops.html", data=data)   
    

# Defining the function for the main add page which the consumer can also access and its route for href tags for HTML.
@app.route('/add', methods=['POST', 'GET'])
#This funtion is responsible for adding data to the temporary tables which can be accessed via the add.html page
def add():
    if request.method == "POST":
        try:
            #Getting all the details from the Add A Phone part of the page to see if the user is entering the details for a phone or not
            user_name = request.form.get('user-name')
            phone_name = request.form.get('phone-name')
            phone_manufacturer = request.form.get('phone-manufacturer')
            phone_date = request.form.get('phone-date')
            cur = mysql.connection.cursor()
            Query=f'''select max(Sno)from TempPhone;'''
            cur.execute(Query)
            C=cur.fetchone()[0]
            #Used to autoincrement the table while also being able to reset it when needed
            if C==None:
                C=0
            Q=f'''insert into TempPhone
                values({C+1},\'{phone_name}\',\'{phone_manufacturer}\',\'{phone_date}\') ;'''
            cur.execute(Q)
            mysql.connection.commit()
            return render_template("add.html", phone_name = phone_name, phone_manufacturer = phone_manufacturer, phone_date = phone_date, user_name = user_name)
        except:
            try:
                #Getting all the details from the Add A Laptop part of the page to see if the user is entering the details for a Laptop or not after checking if the phone form is empty
                user_name = request.form.get('user-name')
                laptop_name = request.form.get('laptop-name')
                laptop_manufacturer = request.form.get('laptop-manufacturer')
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
                #Getting all the details from the Add A Product part of the page to see if the user is entering the details for another product or not after checking if all the other forms are empty
                user_name = request.form.get('user-name')
                other_name = request.form.get('other-name')
                other_manufacturer = request.form.get('other-manufacturer')
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
    #if the page is just requested via a button
    elif request.method == "GET":
            return render_template("add.html")


# Defining the function for the blog page which the consumer can also access and its route for href tags for HTML.(Now scrapped)
@app.route('/blog')
def blog():
    return render_template("blog.html")

# Defining the function for the blog details page which the consumer can also access and its route for href tags for HTML.(Now scrapped)
@app.route('/blog_details')
def blog_details():
    return render_template("blog_details.html")

# Defining the function for the contact page which the consumer can also access and its route for href tags for HTML.
@app.route('/contact', methods=['POST', 'GET'])
#This page is just for display
def contact():
    if request.method == "POST":
        #requesting the data from the phone
        message_name = request.form.get('message-name')
        message_email = request.form.get('message-email')
        message = request.form.get('message')
        return render_template("contact.html", message_name = message_name, message_email=message_email, message=message)
    elif request.method == "GET":
        #rendering the page if no data is present
        return render_template("contact.html")

# Defining the function for the login page which the consumer can also access and its route for href tags for HTML.
@app.route('/login', methods=['POST', 'GET'])
#This is the login page responsible for giving access to the methods which allow editing the main tables
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

# Defining the function for the menu page which the consumer can't access and its route for href tags for HTML.
@app.route('/menu', methods=['POST', 'GET'])
def menu():
#This is the menu which can be accessed via the login page which branches off to the addlaptop addphone andaddther page
    if request.method == "POST":
        try:
            #Checking if the first button is clicked or not. If not then we check for the second button 
            choice=request.form['1.']
            pass
        except:
            try:
                #Checking if the second button is clicked or not. If not then we check for the third button 
                choice=request.form['2.']
            except:
                try:
                    #Checking if the third button is clicked or not. If not then we check for the fourth button 
                    choice=request.form['3.']
                except:
                    try:
                        #Checking if the fourth button is clicked or not. If not then we re render the page
                        choice=request.form['4.']
                    except:
                        #If no button is clicked the menu page is loaded
                        return render_template("menu.html")
                    else:
                        #if the 4th button is clicked (Now Scraped) we render the laptops page
                        return render_template("laptops.html")
                else:
                    #if the 3rd button is clicked we render the addlaptops page which shows the user input and allows the employee to add it to the main page
                    return render_template("addlaptop.html")
            else:
                #if the 2nd button is clicked, we render the addother page which shows the user input and allows the employee to add it to the main page
                return render_template("addother.html")
        else:
            #if the 1st button is clicked, we render the addphones page which shows the user input and allows the employee to add it to the main page. after this they are prompted to use the other program to add details
            return render_template("addphone.html")             
    elif request.method == "GET":
        #if the user tries to access menu without going through login then the login page is rendered
        return redirect(url_for('login'))

# Defining the function for adding the phone to the main overview page which the consumer can also access and its route for href tags for HTML.
@app.route('/addphone', methods=['POST', 'GET'] )
def addphone():
    #This method is resposible for adding phones from the temp table to the main table via the login page 
    cur = mysql.connection.cursor()
    #fetching data from user inputs
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
                    #adding to the main table
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


# Defining the function for adding the phone to the main overview page which the consumer can also access and its route for href tags for HTML.
@app.route('/addlaptop', methods=['POST', 'GET'] )
#This method is resposible for adding laptops from the temp table to the main table via the login page 
def addlaptop():
    cur = mysql.connection.cursor()
    cur.execute('''select*from TempLaptop''')
    data=cur.fetchall()
    #fetching data from user inputs
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
                #adding to the main table
                Q=f'''insert into Laptop(Name,Company,Date)
                        select Name, Company, Date from TempLaptop where Sno={i};'''
                cur.execute(Q)
                mysql.connection.commit()
                Q1=f'''delete from TempLaptop where Sno={i};'''
                cur.execute(Q1)
                mysql.connection.commit()
            return render_template("addlaptop.html", ListOfSno=ListOfSno, data=data)            
    elif request.method == "GET":
        return redirect(url_for('login'))


# Defining the function for comparing two phone details on a page which the consumer can also access and its route for href tags for HTML.
@app.route('/compare', methods=['POST', 'GET'] )
#This method is responsible to show the comparison to the phone details of two phones that can be accessed via the phone page at the bottom
def compare():
    if request.method == "POST":
        try:
            Choice1 = request.form.get('Choice1')
            Choice2 = request.form.get('Choice2')
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
    elif request.method == "GET":
        #if the compare page is requested without any arguments then phones is loaded
        return redirect(url_for('phones'), code=307)    


# Defining the function for comparing two phone details on a page which the consumer can also access and its route for href tags for HTML.
@app.route('/others', methods=['POST', 'GET'])
#This method is responsible for displaying the list of all the other products list
def others():
    if request.method == "POST":
        try:
            #same filters as phones
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
#This method is responsible for the page to add data from the temp other table to the table to the main table that is available to the users. This can only be accessed via the login page.
    #adding another product via the menu
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
            return render_template("addother.html", ListOfSno=ListOfSno, data=data)         
    elif request.method == "GET":
        return redirect(url_for('login')) 


'''
create table Phone
(
Sno         Int(3)      Primary Key Auto_increment,
Name        Varchar(30),
Company     Varchar(50),
Date        Date);

create table TempPhone
(
Sno         Int(3),
Name        Varchar(30),
Company     Varchar(50),
Date        Date);


create table TempOther like TempPhone;

create table TempLaptop like TempPhone;

Create table Laptop like Phone;

Create table Other like Phone;

Create table PhoneDetails
(
Sno         Int(3)      Primary Key Auto_increment,
Name        Varchar(100),
Announced   Varchar(500),
Dimensions      Varchar(500),
Weight          Varchar(500),
Build           Varchar(500),
Size            Varchar(500),
Resolution      Varchar(500),
Protection      Varchar(500),
OS              Varchar(500),
Chipset         Varchar(500),
Internal        Varchar(500),
Sensors         Varchar(500),
Colors          Varchar(500),
Price           Varchar(500)
);

'''