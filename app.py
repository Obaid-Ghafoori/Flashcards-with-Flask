from glob import escape

from modal import db, save_db

from flask import (Flask, render_template, abort,jsonify, request, redirect, url_for)


# from modal import db, save_db



app = Flask(__name__)

# @app.route('/<name>')
# def greeting(name=None):
#     # return f"Hello, {escape(name)}!"
#     return render_template('welcome.html', name=name)

@app.route('/')
def welcome():
    return render_template('welcome.html', cards=db)


@app.route('/card/<int:index>')
def card(index):
    try:
        card = db[index]
        return render_template('card.html', card=card, index=index, max_index=len(db)-1)
    except IndexError:
        abort(404)



@app.route('/api/card/')
def api_card_list():
    try:
        return jsonify(db)
    except IndexError:
        abort(404)


@app.route('/api/card/<int:index>')
def api_card_detail(index):
    try:
        return db[index]
    except IndexError:
        abort(404)


@app.route('/add_card', methods=['GET', 'POST'])
def add_card():
    if request.method == 'POST':
        card = { "firstname" : request.form['firstname'],
                 "lastname" : request.form['lastname'],
                 "age": request.form['age']}
        db.append(card)
        return redirect(url_for('card', index=len(db)-1))
    else:
        return render_template('add_card.html')
    
  

@app.route('/remove_card/<int:index>', methods=["GET", "POST"])
def remove_card(index):
    try:
        if request.method == "POST":
            # db.pop(index)
            del db[index]
            save_db()
            return redirect(url_for('welcome'))
        else:
            return render_template("remove_card.html", card=db[index])
    except IndexError:
        abort(404)

if __name__ == '__main__':
    app.run(debug=True)
