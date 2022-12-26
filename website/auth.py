from flask import Blueprint,render_template, request,flash,redirect,url_for
from .models import User
from werkzeug.security import generate_password_hash,check_password_hash
from . import db
import sqlite3
from flask_login import login_user, login_required,logout_user,current_user


auth = Blueprint('auth', __name__)

@auth.route('/login',methods=['GET', 'POST'])
def login():
    if request.method=='POST':
        email=request.form.get('email')
        password=request.form.get('password')
        connection=sqlite3.connect('database.db')
        cursor=connection.cursor()
        connection.commit()
        user=User.query.filter_by(email=email).first()
        if user:
            if check_password_hash(user.password,password):
                flash('Logged in successfully!',category='succes')
                login_user(user,remember=True)
                return redirect(url_for('views.home'))
            else:
                flash('Incorrect password!',category='error')
        else:
            flash('Email does not exist!',category='error')

    return render_template("login.html",user=current_user)

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))

@auth.route('/sign-up', methods=['GET', 'POST'])
def sign_up():
    if request.method=='POST':
        email=request.form.get('email')
        first_name=request.form.get('firstName')
        password1=request.form.get('password1')
        password2=request.form.get('password2')
        user=User.query.filter_by(email=email).first()
        
        if user:
            flash('Email already exists!',category='error')
        elif len(email) < 4:
            flash('Email must be greater than 3 characters.',category='error')
        elif len(first_name) < 2:
            flash('First name must be greater than 1 characters.',category='error')
        elif password1!=password2:
            flash('Your password dont match',category='error')
        elif len(password1) < 7:
            flash('Password must be at least 7 characters',category='error')
        else:
            new_user=User(email=email,first_name=first_name,password=generate_password_hash(password1,method='sha256'))
            db.session.add(new_user)
            db.session.commit()
            login_user(user,remember=True)
            flash('Account created!',category='succes')
            return redirect(url_for('views.home'))

    return render_template("sign_up.html",user=current_user)

@auth.route('/populare/')
def populare():
    fd=open('script_populare.sql','r')
    script_populare=fd.read()
    fd.close()
    connection=sqlite3.connect('database.db')
    cursor=connection.cursor()
    sqlCommands=script_populare.split(';')
    for command in sqlCommands:
        try:
            cursor.execute(command)
        except sqlite3.OperationalError:
            print("Eroare in scriptul de populare a tabelelor!")
    connection.commit()
    print ('I got clicked!')
    return '',204

@auth.route('/afisare/<tabel>',methods=['GET', 'POST'])
def afisare(tabel):
    connection=sqlite3.connect('database.db')
    cursor=connection.cursor()
    cursor.execute("SELECT * FROM {}".format(tabel))
    pacienti=[]
    medici=[]
    retete=[]
    departamente=[]
    internari=[]
    rows=cursor.fetchall()
    if tabel=='reteta':
        cursor.execute("SELECT diagnostic,medicamente,durata,data_intocmire,nume,prenume,telefon FROM reteta,pacient WHERE reteta.id_pacient=pacient.id")
        rows=cursor.fetchall()
        cursor.execute("SELECT * FROM pacient")
        rowsPacienti=cursor.fetchall()
        for row in rowsPacienti:
            pacienti.append(row[1])
    elif tabel=='internare':
        cursor.execute("SELECT data_intrare,data_iesire,pacient.nume,pacient.prenume,medic.nume,medic.prenume,departament.nume_departament FROM internare JOIN pacient ON (internare.id_pacient=pacient.id) JOIN medic ON (internare.id_medic=medic.id) JOIN departament ON (internare.departament=departament.nume_departament)")
        rows=cursor.fetchall()
        cursor.execute("SELECT * FROM medic")
        rowsMedici=cursor.fetchall()
        for row in rowsMedici:
            medici.append(row[1])
        cursor.execute("SELECT * FROM pacient")
        rowsPacienti=cursor.fetchall()
        for row in rowsPacienti:
            pacienti.append(row[1])
        cursor.execute("SELECT * FROM departament")
        rowsDepartament=cursor.fetchall()
        for row in rowsDepartament:
            departamente.append(row[1])
    connection.commit()
    return render_template("{}.html".format(tabel),user=current_user,rows=rows,listaPacienti=pacienti,listaMedici=medici,listaDepartamente=departamente,retete=retete, internari=internari)


@auth.route('/cautare/<tabel>',methods=["GET","POST"])
def cautarePacient(tabel):
    if request.method == 'POST':
        connection=sqlite3.connect('database.db')
        numeCautare=request.form['nume_pacient']
        if verificareNumePrenume(numeCautare)==1:
            cursor=connection.cursor()
            if tabel=='pacient':
                cursor.execute("SELECT * FROM pacient WHERE nume=?",(numeCautare,))
            elif tabel=='reteta':
                cursor.execute("SELECT diagnostic,medicamente,durata,data_intocmire,nume,prenume,telefon FROM reteta JOIN pacient ON (reteta.id_pacient=pacient.id) WHERE pacient.nume=?",(numeCautare,))
            elif tabel=='internare':
                cursor.execute("SELECT data_intrare,data_iesire,pacient.nume,pacient.prenume,medic.nume,medic.prenume,departament.nume_departament FROM internare JOIN pacient ON (internare.id_pacient=pacient.id) JOIN medic ON (internare.id_medic=medic.id) JOIN departament ON (internare.departament=departament.nume_departament) WHERE pacient.nume=?",(numeCautare,))
            elif tabel=='medic':
                cursor.execute("SELECT * FROM medic WHERE nume=?",(numeCautare,))
            elif tabel=='departament':
                cursor.execute("SELECT * FROM departament WHERE nume_departament=?",(numeCautare,))
            rows=cursor.fetchall()
            for row in rows:
                print(row)
        else:
            rows=[]
            flash("Numele de cautare contine caractere nepermise sau cifre",category="error")

    return render_template("{}.html".format(tabel),user=current_user,rows=rows)

@auth.route('/stergere/<tabel>/<element>')
def stergereInTabel(tabel,element):
    connection=sqlite3.connect('database.db')
    cursor=connection.cursor()
    if tabel=='pacient':
        print("DELETE FROM {} WHERE id = {x}".format(tabel,x=element))
        cursor.execute("DELETE FROM {} WHERE id = {x}".format(tabel,x=int(element)))
    connection.commit()
    return render_template("{}.html".format(tabel),user=current_user)

@auth.route('/adaugare/<tabel>',methods=["GET","POST"])
def adaugareInTabel(tabel):
    if request.method == 'POST':
        connection=sqlite3.connect('database.db')
        cursor=connection.cursor()
        cursor.execute("SELECT * FROM {}".format(tabel))
        rows=cursor.fetchall()
        id_pk=len(rows)+1
        for i in range(1,len(rows)+1):
            ok=0
            for row in rows:
                if row[0] == i:
                    ok=1
            if ok==0:
                id_pk=i
                break
        print(id_pk)
        if tabel == 'pacient':
            numeAdaugare=request.form['nume_pacient']
            prenumeAdaugare=request.form['prenume_pacient']
            varstaAdaugare=request.form['varsta_pacient']
            localitateAdaugare=request.form['localitate_pacient']
            emailAdaugare=request.form['email_pacient']
            telefonAdaugare=request.form['telefon_pacient']
            if verificareNumePrenume(numeAdaugare) == 0:
                flash('Nume invalid',category='error')
                return '',204
            if verificareNumePrenume(prenumeAdaugare)==0:
                flash('Prenume invalid',category='error')
                return '',204
            if verificareNumePrenume(localitateAdaugare)==0:
                flash('Localitate invalid',category='error')
                return '',204
            if verificareTelefon(telefonAdaugare)==0:
                flash('Telefon invalid',category='error')
                return '',204
            try:
                varstaAdaugare=int(varstaAdaugare)
            except:
                flash('Varsta invalida',category='error')
                return '',204
            cursor.execute("INSERT INTO pacient VALUES (?,?,?,?,?,?,?)",(id_pk,numeAdaugare,prenumeAdaugare,varstaAdaugare,telefonAdaugare,localitateAdaugare,emailAdaugare,))
       
        elif tabel=='reteta':
            numePacient=request.form['pacienti']
            diagnostic=request.form['diagnostic']
            durataTimp=request.form['durata_timp']
            data=request.form['data']
            medicamente=request.form['medicamente']
            if verificareNumePrenume(diagnostic) == 0:
                flash('Diagnostic invalid',category='error')
                return '',204
            cursor.execute("SELECT * FROM pacient")
            rows=cursor.fetchall()
            c=1
            for row in rows:
                if row[1]==numePacient:
                    break
                c=c+1
            cursor.execute("INSERT INTO reteta VALUES (?,?,?,?,?,?)",(id_pk,c,medicamente,diagnostic,durataTimp,data))
        
        elif tabel=='internare':
            numePacient=request.form['pacienti']
            numeMedic=request.form['medici']
            numeDepartament=request.form['departamente']
            dateIn=request.form['datein']
            dateOut=request.form['dateout']
            if dateOut:
                inProgress=0
            else:
                inProgress=1
            cursor.execute("SELECT * FROM pacient")
            idP=idM=idD=1
            rows=cursor.fetchall()
            for row in rows:
                if row[1]==numePacient:
                    break
                idP=idP+1
            cursor.execute("SELECT * FROM medic")
            rows=cursor.fetchall()
            for row in rows:
                if row[1]==numeMedic:
                    break
                idM=idM+1
            cursor.execute("INSERT INTO internare VALUES (?,?,?,?,?,?,?)",(id_pk,idP,idM,dateIn,dateOut,inProgress,numeDepartament))
        
        elif tabel == 'medic':
            numeAdaugare=request.form['nume_medic']
            prenumeAdaugare=request.form['prenume_medic']
            varstaAdaugare=request.form['varsta_medic']
            emailAdaugare=request.form['email_medic']
            telefonAdaugare=request.form['telefon_medic']
            if verificareNumePrenume(numeAdaugare) == 0:
                flash('Nume invalid',category='error')
                return '',204
            if verificareNumePrenume(prenumeAdaugare)==0:
                flash('Prenume invalid',category='error')
                return '',204
            if verificareTelefon(telefonAdaugare)==0:
                flash('Telefon invalid',category='error')
                return '',204
            try:
                varstaAdaugare=int(varstaAdaugare)
            except:
                flash('Varsta invalida',category='error')
                return '',204
            cursor.execute("INSERT INTO medic VALUES (?,?,?,?,?,?,?)",(id_pk,numeAdaugare,prenumeAdaugare,varstaAdaugare,telefonAdaugare,emailAdaugare,))
       
        elif tabel=='departament':
            numeAdaugare=request.form['nume_departament']
            corpDepartament=request.form['corp_departament']
            numarSaloane=request.form['numar_saloane']
            if verificareNumePrenume(numeAdaugare) == 0:
                flash('Nume departament invalid',category='error')
                return '',204
            cursor.execute("INSERT INTO departament VALUES (?,?,?,?)",(id_pk,numeAdaugare,corpDepartament,numarSaloane))
        connection.commit()
        connection=sqlite3.connect('database.db')
        cursor=connection.cursor()
        cursor.execute("SELECT * FROM {}".format(tabel))
        rows=cursor.fetchall()
        connection.commit()
        return render_template("home.html",user=current_user,rows=rows)
    return '',204

def verificareNumePrenume(nume):
    ok=0
    for letter in nume:
        if (letter>='a' and letter <='z') or (letter>='A' and letter<='Z'):
            ok=1
        else:
            return 0
    if ok == 0:
        return 0
    return 1

def verificareTelefon(telefon):
    if len(telefon) != 10:
        return 0
    ok=1
    for cif in telefon:
        if cif >='0' and cif <='9':
            ok=1
        else:
            return 0
    return 1