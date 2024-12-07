from flask import Flask, render_template, request, url_for

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('UI.htm')


@app.route('/AboutUS')
def aboutUS():
    return render_template('AboutUs.htm')


if __name__ == '__main__':
    app.run()
