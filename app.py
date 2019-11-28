from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///LocalFlask.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
db = SQLAlchemy(app)


class Resources(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.Enum('VIDEO', 'IMAGE', 'MOVIE', 'APPLY', 'MUSIC', 'FICTION', 'CARTOON', 'ANIME'))
    name = db.Column(db.String(80))
    url = db.Column(db.String(120))

    def __init__(self, type, name, url):
        self.type = type
        self.name = name
        self.url = url

    def __repr__(self):
        return '<Resources %r>' % self.name


# Create all databases
# db.create_all()

@app.route('/')
def index():
    return redirect(url_for('gather', span=0))


@app.route('/resource/?<string:search>', methods=['get'])
def resource(search):
    count = Resources.query.count()
    if search == ':)':
        return render_template('resource.html', navigation='resource', search='', resources=[], count=count)
    elif search == 'all':
        resources = Resources.query.order_by('name').all()
        return render_template('resource.html', navigation='resource', search=search, resources=resources, count=count)
    else:
        resources = Resources.query.order_by('name').filter(Resources.name.like('%{0}%'.format(search))).all()
        return render_template('resource.html', navigation='resource', search=search, resources=resources, count=count)


@app.route('/resource/search', methods=['post'])
def resource_search():
    search = request.form.get('search').strip()
    if search is '':
        search = ':)'
    return redirect(url_for('resource', search=search))


@app.route('/gather/?<string:span>', methods=['get'])
def gather(span):
    return render_template('gather.html', navigation='gather', span=span)


@app.route('/gather/warehouse', methods=['post'])
def gather_warehouse():
    name = request.form.get('name').strip()
    url = request.form.get('url').strip()
    type = request.form.get('type')
    if name.isspace() or url.isspace():
        return redirect(url_for('gather', span=1))
    else:
        new_resources = Resources(type=type, name=name, url=url)
        db.session.add(new_resources)
        db.session.commit()
        if len(name) > 7:
            name = name[0:8]
        return redirect(url_for('resource', search=name))


if __name__ == '__main__':
    app.run()
