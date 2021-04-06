from datetime import datetime
from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database/metrics.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
db = SQLAlchemy(app)


'''
Se crea la tabla que va a guardar los datos
'''
class Metrics(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    metric = db.Column(db.String(200))
    value = db.Column(db.String(10))
    created_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)


'''
home
'''
@app.route('/')
def home():
    metrics = Metrics.query.order_by(Metrics.id.desc()).all()
    return render_template('index.html', metrics = metrics)


'''
endpoint para borrar una metrica
'''
@app.route('/delete/<id>')
def delete(id):
    Metrics.query.filter_by(id=int(id)).delete()
    db.session.commit()
    return redirect(url_for('home'))


'''
<URL>/data: espera los datos por POST para el guardado en la db
'''
@app.route('/data', methods=['GET','POST'])
def data():
    if request.method == 'POST':
        data = request.json
        metric = data['metric']
        value = data['value']
        new_metric = Metrics(metric=metric, value=value)

        db.session.add(new_metric)
        db.session.commit()
        return "ok"
    
    else:
        return "este es el sitio del admin"
        

if __name__ == '__main__':
    app.run(debug=True)