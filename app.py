from flask import Flask,render_template,request,redirect,url_for
from flask_sqlalchemy import SQLAlchemy
import webview


app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///datas.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
# db.init_app(app)

app.app_context().push()

class Todo(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    # date=db.Column(db.Integer,primary_key=True)
    card=db.Column(db.String(150),nullable=False)

class Doing(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    # date=db.Column(db.Integer,primary_key=True)
    card=db.Column(db.String(150),nullable=False)

class Done(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    # date=db.Column(db.Integer,primary_key=True)
    card=db.Column(db.String(150),nullable=False)

# with app.app_context():
#     db.create_all()

#Landing page
@app.route('/')
def index():
    return render_template("home.html")

#Boards
@app.route('/boards')
@app.route('/boards/<name>')
def boards(name=''):
    todoDetails=[]
    doneDetails=[]
    doingDetails=[]
    initialDetail={
        'cardName':"",
        'cardVisibility':"hidden",
        'editOption':"hidden",
        'modifyOption':"hidden"
    }

    todoDetails.append(initialDetail)
    doneDetails.append(initialDetail)
    doingDetails.append(initialDetail)

    todos = Todo.query.all()
    for todo in todos:
        detail={
        'cardName':todo.card,
        'cardVisibility':"",
        'modifyOption':"hidden",
        'editOption':"hidden",
        }
        
        if name == todo.card:
            detail['modifyOption']=''

        if name == 'edit'+todo.card:
            detail['modifyOption']='hidden'
            detail['cardVisibility']='hidden'
            detail['editOption']=''

        todoDetails.append(detail)

    doing = Doing.query.all()
    for doingCard in doing:
        detail={
        'cardName':doingCard.card,
        'cardVisibility':"",
        'editOption':"hidden",
        'modifyOption':"hidden",
        }
        if name == doingCard.card:
            detail['modifyOption']=''

        if name == 'edit'+doingCard.card:
            detail['modifyOption']='hidden'
            detail['cardVisibility']='hidden'
            detail['editOption']=''

        doingDetails.append(detail)

    done = Done.query.all()
    for doneCard in done:
        detail={
        'cardName':doneCard.card,
        'cardVisibility':"",
        'editOption':"hidden",
        'modifyOption':"hidden",
        }
        if name == doneCard.card:
            detail['modifyOption']=''
            
        if name == 'edit'+doneCard.card:
            detail['modifyOption']='hidden'
            detail['cardVisibility']='hidden'
            detail['editOption']=''

        doneDetails.append(detail)
    
    #REally unnecessary addition
    inputs={
    'todoAdd':'',
    'doingAdd':'',
    'doneAdd':'',
    'todoInput':'hidden',
    'doingInput':'hidden',
    'doneInput':'hidden',
    }
    if name == 'todoList':
        inputs['todoAdd']='hidden'
        inputs['todoInput']=''

    if name == 'doingList':
        inputs['doingAdd']='hidden'
        inputs['doingInput']=''

    if name == 'doneList':
        inputs['doneAdd']='hidden'
        inputs['doneInput']=''

    return render_template('boards.html',todoDetails=todoDetails,doingDetails=doingDetails,doneDetails=doneDetails,inputs=inputs)


@app.route('/addCard/<board>',methods=['POST'])
#adding datas in the todo:
def addCard(board):
    newCard=request.form.get('card')
    if newCard:
        if board == 'todo':
            newCardObject=Todo(card=newCard)
        elif board == 'doing':
            newCardObject=Doing(card=newCard)
        if board == 'done':
            newCardObject=Done(card=newCard)
        db.session.add(newCardObject)
        db.session.commit()
    return redirect(url_for('boards'))

@app.route('/edit/<name>',methods=['POST'])
#adding datas in the todo:
def editCard(name):
    newCard=request.form.get('editCard')
    if newCard:
        # newCardObject=Todo(card=newCard)
        temp = name.split(' ',1)
        board=temp[0]
        cardName=temp[1]
        if board == 'todo':
            editCard=Todo.query.filter_by(card=cardName).first()
        elif board== 'doing':
            editCard=Doing.query.filter_by(card=cardName).first()
        else:
            editCard=Done.query.filter_by(card=cardName).first()
            
        editCard.card=newCard
        db.session.add(editCard)
        db.session.commit()
    return redirect(url_for('boards'))


@app.route('/deleteCard/<name>')
#adding datas in the todo:
def deleteCard(name):
    temp=name.split(' ',1)
    board=temp[0]
    cardName=temp[1]
    
    if board == 'todo':
        card = Todo.query.filter_by(card=cardName).first()

    elif board == 'doing':
        card = Doing.query.filter_by(card=cardName).first()

    else:
        card = Done.query.filter_by(card=cardName).first()
    db.session.delete(card)
    db.session.commit()
    return redirect(url_for('boards'))


 

@app.route('/moveCard/<name>')
def moveCard(name):
    temp=name.split(' ',2)
    fromCard=temp[0]
    toCard=temp[1]
    cardName=temp[2]
    
    if fromCard == 'todo':
        card = Todo.query.filter_by(card=cardName).first()

    elif fromCard == 'doing':
        card = Doing.query.filter_by(card=cardName).first()

    else:
        card = Done.query.filter_by(card=cardName).first()
    db.session.delete(card)
    
    if toCard == 'todo':
        newCardObject=Todo(card=cardName)

    elif toCard == 'doing':
        newCardObject=Doing(card=cardName)

    else:
        newCardObject=Done(card=cardName)
    db.session.add(newCardObject)
    db.session.commit()
    return redirect(url_for('boards'))

if __name__=="__main__":
#     app.run(debug=True)
    db.create_all()
    webview.start()
