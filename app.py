from flask import Flask, render_template

from headscale import get_all

app = Flask(__name__)


@app.route('/metrics')
def metrics():
    try:
        return render_template('metrics.html', meta=get_all())
    except Exception as e:
        return f"Error: {e} with dict: {get_all()}"


if __name__ == '__main__':
    app.run(debug=True)
