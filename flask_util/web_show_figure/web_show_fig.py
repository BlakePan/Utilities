# -*- coding: utf-8 -*-
import sys
sys.path.append(".")
from flask import Flask, request, render_template
from flask_bootstrap import Bootstrap

app = Flask(__name__, static_folder="./demo_figure")
app.secret_key = 'development key'
Bootstrap(app)


@app.route('/demo_fig', methods=['GET'])
def train_info():
    if request.method == 'GET':
        return render_template('demo_fig.html', plot_fname='./demo_figure/img.jpg')

    else:
        return "bad request"


if __name__ == '__main__':
    print('Starting service')
    app.run(debug=True, port=5010, host='0.0.0.0', threaded=True)
