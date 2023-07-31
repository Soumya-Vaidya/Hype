from flask import Flask, render_template, request, redirect, url_for
from models import Committee, SubEvent, MainEvent, Newsletter, Sponsors, db
from datetime import date, datetime


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///hype.sqlite3"
db.init_app(app)
app.app_context().push()


@app.route("/", methods=["GET", "POST"])
def hype():
    if request.method == "GET":
        today = date.today()
        timeline = MainEvent.query.filter(MainEvent.start_date >= today).order_by(MainEvent.start_date).limit(5).all()
        date_list = []
        day_list = []
        for t in timeline:
            datetime_object = datetime.strptime(str(t.start_date), '%Y-%m-%d').date()
            date_string = datetime_object.strftime('%B')
            day_string = datetime_object.strftime('%d')
            date_list.append(date_string)
            day_list.append(day_string)
        return render_template("index.html", events=timeline, date_list = date_list, day_list = day_list)
    elif request.method == "POST":
        email = request.form['email']
        event = Newsletter(email=email)
        db.session.add(event)
        db.session.commit()
        print('Email stored for Newsletter')
        return (redirect('/'))


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("login.html")
    elif request.method == "POST":
        message=""
        email = request.form['email']
        password = request.form['password']
        storeduser = Committee.query.filter_by(email=email).first()
        if storeduser is not None:
            users = Committee.query.all()
            flag = True
            for s in users:
                if s.email == email:
                    flag = False
                    if s.password == password:
                        sid = s.cid
                        print("Login successful redirecting to dashboard")
                        return redirect(url_for('home', cid = sid))
                    else:
                        print("Login unsuccessful - wrong password")
                        message = "Login unsuccessful!"
                        return render_template("login.html", message=message)
                        # return (redirect('/'))
            print("Login unsuccessful - invalid email")
            # return (redirect('/'))
            message = "Login unsuccessful!"
            return render_template("login.html", message=message)
        else:
            message = "Email Not Reistered!"
            print("Login unsuccessful!")
            return render_template("login.html", message=message)
            # return (redirect('/'))


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "GET":
        return render_template("register.html", message="")
    elif request.method == "POST":
        flag = False
        name = request.form['name']
        password = request.form['password']
        confirm_password = request.form['confirm_password']
        email = request.form['email']
        sc = request.form['sc']
        faculty_incharge = request.form['faculty_incharge']
        faculty_email = request.form['faculty_email']
        student_incharge = request.form['student_incharge']
        contact = request.form['contact']
        image = request.form['image']
        domain = request.form['domain']
        about = request.form['about']
        strength = request.form['strength']
        website = request.form['website']
        socials = request.form['socials']
        storedusername = Committee.query.filter_by(name=name).first()
        if storedusername is not None:
            flag = True
            message="Username unavailable!"
        storedemail = Committee.query.filter_by(email=email).first()
        if storedemail is not None:
            flag = True
            message="Email already registered!"
        if (password != confirm_password):
            flag = True
            message="Passwords do not match!"
        if flag:
            return render_template("register.html", message=message)
        else:
            committee = Committee(name = name, password = password, email = email, sc=sc, faculty_incharge = faculty_incharge, student_incharge= student_incharge,image=image, strength=strength, domain=domain, about=about, faculty_email=faculty_email,  website=website, socials=socials, contact=contact)
            db.session.add(committee)
            db.session.commit()
            cid = committee.cid
            print('User successfully registered')
            return redirect(url_for('home', cid = cid))


@app.route("/Hype/<cid>", methods=["GET", "POST"])
def home(cid):
    if request.method == "GET":
        today = date.today()
        c = Committee.query.get(cid)

        all_events = MainEvent.query.filter_by(cid = cid).all()

        events = MainEvent.query.filter_by(cid = cid).filter(MainEvent.start_date >= today).order_by(MainEvent.start_date).all()
        d = {}
        for i in range(len(events)):
            d[i] = SubEvent.query.filter_by(eid = events[i].eid).all()

        past_events = MainEvent.query.filter_by(cid = cid).filter(MainEvent.start_date < today).order_by(MainEvent.start_date).all()
        dold = {}
        for i in range(len(past_events)):
            dold[i] = SubEvent.query.filter_by(eid = past_events[i].eid).all()

        return render_template("committee_dashboard.html", committee = c, events = events, subevents = d, past_events = past_events, past_subevents = dold, all_events=all_events)


@app.route("/Hype/<cid>/edit", methods=["GET", "POST"])
def edit_committee(cid):
    if request.method =="GET":
        committee = Committee.query.get(cid)
        return render_template("edit_committee.html", cid = cid, committee = committee)
    elif request.method == "POST":
        email = request.form['email']
        sc = request.form['sc']
        faculty_incharge = request.form['faculty_incharge']
        faculty_email = request.form['faculty_email']
        student_incharge = request.form['student_incharge']
        contact = request.form['contact']
        domain = request.form['domain']
        about = request.form['about']
        strength = request.form['strength']
        website = request.form['website']
        socials = request.form['socials']
        try:
            committee = db.session.query(Committee).get(cid)
            committee.email = email
            committee.sc = sc
            committee.faculty_incharge = faculty_incharge
            committee.faculty_email = faculty_email
            committee.student_incharge = student_incharge
            committee.contact = contact
            committee.domain = domain
            committee.about = about
            committee.strength = strength
            committee.website = website
            committee.socials = socials
        except:
            db.session.rollback()
            print(2)
        else:
            db.session.commit()
            print("Committee edited - getting commited")
            return redirect(url_for('home', cid = cid))
    else:
        print("F - problem in edit event")

    
@app.route("/Hype/<cid>/event/add", methods=["GET", "POST"])
def add_event(cid):
    if request.method =="GET":
        return render_template("add_event.html", cid = cid)
    elif request.method == "POST":
        name = request.form["name"]
        about = request.form["about"]
        start_date = request.form["start_date"]
        end_date = request.form["end_date"]
        event_website = request.form["event_website"]
        event_socials = request.form["event_socials"]
        image = request.form["image"]
        event = MainEvent(cid = cid, name = name, about=about, start_date=start_date, end_date=end_date, event_website=event_website, event_socials=event_socials, image=image)
        db.session.add(event)
        db.session.commit()
        print('Event added!')
        return redirect(url_for('home', cid = cid))


@app.route("/Hype/<cid>/event/<eid>/edit", methods=["GET", "POST"])
def edit_event(cid,eid):
    if request.method =="GET":
        event = MainEvent.query.get(eid)
        return render_template("edit_event.html", cid = cid, event=event)
    elif request.method == "POST":
        name = request.form["name"]
        about = request.form["about"]
        start_date = request.form["start_date"]
        end_date = request.form["end_date"]
        event_website = request.form["event_website"]
        event_socials = request.form["event_socials"]
        try:
            event = db.session.query(MainEvent).get(eid)
            event.name = name
            event.about = about
            event.start_date = start_date
            event.end_date = end_date
            event.event_website = event_website
            event.event_socials = event_socials
        except:
            db.session.rollback()
        else:
            db.session.commit()
            print("Event edited - getting commited")
            return redirect(url_for('home', cid = cid))
    else:
        print("F - problem in edit event")


@app.route('/Hype/<cid>/event/<eid>/delete', methods=["GET", "POST"])
def delete_event(cid, eid):
    event = MainEvent.query.get(eid)
    subevents = SubEvent.query.filter_by(eid=eid).all()

    for subevent in subevents:
        db.session.delete(subevent)

    db.session.delete(event)
    db.session.commit()
    return redirect(url_for('home', cid = cid))


@app.route("/Hype/<cid>/event/<eid>/subevent/add", methods=["GET", "POST"])
def add_subevent(cid, eid):
    if request.method =="GET":
        return render_template("add_subevent.html", cid = cid, eid = eid)
    elif request.method == "POST":
        name = request.form["name"]
        about = request.form["about"]
        start_date = request.form["start_date"]
        end_date = request.form["end_date"]
        start_time = request.form["start_date"]
        end_time = request.form["end_date"]
        image = request.form["image"]
        event = SubEvent(eid = eid, name = name, about=about, start_date=start_date, end_date=end_date, start_time=start_time, end_time=end_time, image=image)
        db.session.add(event)
        db.session.commit()
        print('Subevent added!')
        return redirect(url_for('home', cid = cid))


@app.route("/Hype/<cid>/event/<eid>/subevent/<seid>/edit", methods=["GET", "POST"])
def edit_subevent(cid,eid,seid):
    if request.method =="GET":
        subevent = SubEvent.query.get(seid)
        return render_template("edit_subevent.html", cid = cid, eid = eid, seid = seid, subevent = subevent)
    elif request.method == "POST":
        about = request.form["about"]
        start_date = request.form["start_date"]
        end_date = request.form["end_date"]
        start_time = request.form["start_time"]
        end_time = request.form["end_time"]
        image = request.form["image"]
        try:
            subevent = db.session.query(SubEvent).get(seid)
            subevent.about = about
            subevent.start_date = start_date
            subevent.end_date = end_date
            subevent.start_time = start_time
            subevent.end_time = end_time
            subevent.image = image
        except:
            db.session.rollback()
        else:
            db.session.commit()
            print("Subevent editted - getting commited")
            return redirect(url_for('home', cid = cid))
    else:
        print("F")


@app.route('/Hype/<cid>/event/<eid>/subevent/<seid>/delete', methods=["GET", "POST"])
def delete_subevent(cid, eid, seid):
    subevent = SubEvent.query.get(seid)

    db.session.delete(subevent)
    db.session.commit()
    return redirect(url_for('home', cid = cid))

@app.route("/Hype/event/<eid>", methods=["GET","POST"])
def event(eid):
    event = MainEvent.query.get(eid)
    subevents = SubEvent.query.filter_by(eid=eid).all()
    committee = Committee.query.filter_by(cid=event.cid).one()
    datetime_object = datetime.strptime(str(event.start_date), '%Y-%m-%d').date()
    date_string = datetime_object.strftime('%B %d, %Y 00:00:00 PDT')
    today = date.today()
    today1 = str(today)
    return render_template("event.html", event = event, subevents = subevents, committee = committee, start_date = date_string, today=today1)

@app.route("/Hype/committees", methods=["GET","POST"])
def committee():
    if request.method == "GET":
        c = Committee.query.all()
        # return jsonpickle.encode(c)
        return render_template("view_committees.html")
    

@app.route("/Hype/committees/sc", methods=["GET","POST"])
def sc():
    if request.method == "GET":
        c = Committee.query.filter_by(sc=1).all()
        return render_template("view_committees.html", committees = c)
    

@app.route("/Hype/committees/others", methods=["GET","POST"])
def other():
    if request.method == "GET":
        c = Committee.query.filter_by(sc=0).all()
        return render_template("view_committees.html", committees = c)
    
@app.route("/Hype/committees/all", methods=["GET","POST"])
def all():
    if request.method == "GET":
        c = Committee.query.all()
        return render_template("view_committees.html", committees = c)
    

@app.route('/Hype/committees/<cid>')
def individual(cid):
    if request.method == 'GET':
        today = date.today()
        c = Committee.query.get(cid)
        
        all_events = MainEvent.query.filter_by(cid = cid).all()

        events = MainEvent.query.filter_by(cid = cid).filter(MainEvent.start_date >= today).order_by(MainEvent.start_date).all()
        d = {}
        for i in range(len(events)):
            d[i] = SubEvent.query.filter_by(eid = events[i].eid).all()

        past_events = MainEvent.query.filter_by(cid = cid).filter(MainEvent.start_date < today).order_by(MainEvent.start_date).all()
        dold = {}
        for i in range(len(past_events)):
            dold[i] = SubEvent.query.filter_by(eid = past_events[i].eid).all()

        return render_template("committee.html", committee = c, events = events, subevents = d, past_events = past_events, past_subevents = dold, all_events=all_events)


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug= True, port= 8000 )
