from flask import *
from pricedropFLIPKART import check_price

app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def basic():
    return "<h1>Welcome! This is homepage</h1>"


@app.route('/uploads', methods=['GET', 'POST'])
def uploads():
    if request.method == 'POST':
        return redirect(url_for('basic'))
    if True:
        x, y = check_price()
        return {"title": x,
                "price": y
                }

if __name__ == '__main__':
    app.run(debug=True)
