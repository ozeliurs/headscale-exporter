from flask import Flask, render_template

from headscale import get_all

app = Flask(__name__)


@app.route('/metrics')
def metrics():
    return render_template('metrics.html', meta=get_all())


if __name__ == '__main__':
    app.run(debug=True)
