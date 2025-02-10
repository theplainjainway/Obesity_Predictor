from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        user_data = {
            'gender': request.form['gender'],
            'age': request.form['age'],
            'height': request.form['height'],
            'weight': request.form['weight'],
            'family_history': request.form['family_history'],
            'favc': request.form['favc'],
            'fcvc': request.form['fcvc'],
            'ncp': request.form['ncp'],
            'caec': request.form['caec'],
            'smoke': request.form['smoke'],
            'ch2o': request.form['ch2o'],
            'scc': request.form['scc'],
            'faf': request.form['faf'],
            'tue': request.form['tue'],
            'calc': request.form['calc'],
            'mtrans': request.form['mtrans'],
        }
        return render_template('result.html', data=user_data)
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        user_data = {
            'gender': request.form['gender'],
            'age': request.form['age'],
            'height': request.form['height'],
            'weight': request.form['weight'],
            'family_history': request.form['family_history'],
            'favc': request.form['favc'],
            'fcvc': request.form['fcvc'],
            'ncp': request.form['ncp'],
            'caec': request.form['caec'],
            'smoke': request.form['smoke'],
            'ch2o': request.form['ch2o'],
            'scc': request.form['scc'],
            'faf': request.form['faf'],
            'tue': request.form['tue'],
            'calc': request.form['calc'],
            'mtrans': request.form['mtrans'],
        }
        return render_template('result.html', data=user_data)
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
