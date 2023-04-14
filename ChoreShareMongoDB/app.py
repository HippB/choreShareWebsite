from flask import Flask, render_template, request, url_for, redirect
from flask_pymongo import PyMongo
from bson.objectid import ObjectId

app = Flask(__name__)

app.config['MONGO_URI'] = 'mongodb+srv://ttman224:WeHateTheMets@cluster0.qjytdnl.mongodb.net/choreshare-db?retryWrites=true&w=majority'
mongo = PyMongo(app)

chores = mongo.db.chores
groups = mongo.db.groups

@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template('index.html')

@app.route('/joingroup', methods=['GET', 'POST'])
def join_group():
    if request.method == 'POST':
        groupID = request.form['group_id']
        password = request.form['password']
        group = groups.find_one({'group_id': groupID, 'password': password})
        if group:
            saved_chores = chores.find()
            return render_template('groupview.html', groupid = groupID, chores = saved_chores)
    return render_template('joingroup.html')

@app.route('/creategroup', methods=['GET', 'POST'])
def create_group():
    if request.method == 'POST':
        groupID = request.form['group_id']
        password = request.form['password']
        group = groups.find_one({'group_id': groupID})
        if group:
            return render_template('creategroup.html')
        else:
            groups.insert_one({'group_id': groupID, 'password': password})
            saved_chores = chores.find()
            return render_template('groupview.html', groupid = groupID, chores = saved_chores)
    return render_template('creategroup.html')
        
@app.route('/group', methods=['GET', 'POST'])
def group_view():
    if request.method == 'POST':
        title = request.form['title']
        desc = request.form['description']
        assignee = request.form['assignee']
        groupID = request.form['groupid']
        chores.insert_one({'title': title, 'description': desc, 'assignee': assignee, 'chore-group-id': groupID})

        saved_chores = chores.find()
        return render_template('groupview.html', groupid = groupID, chores=saved_chores)

if(__name__ == '__main__'):
    app.run(debug=True)