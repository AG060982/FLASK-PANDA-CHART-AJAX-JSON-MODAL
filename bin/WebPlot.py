from flask import Flask, abort, render_template, jsonify, request, redirect, url_for
from threading import Timer
import pandas as pd
import yaml

app = Flask(__name__)

def prepare_df(interval):
    global df
    Timer(interval, prepare_df, [interval]).start()
    df = pd.read_csv("<path of your CSV File>")


prepare_df(60) #update the df every 60 second

@app.route('/')
def index():
    return render_template('modal_chart.html')

@app.route('/get_detail',methods=['POST','GET'])
def get_detail():
        if request.method == "POST":
        db = request.form['db']
        server = request.form['server']
        data = df.loc[(df['server'] == server) & (df['database'] == db)] #make sure colum name matches with your CSV data
        data = data.to_json(orient='records')
        data = data.replace('[','').replace(']','') #can have many other way to convert the Data in dict format like we can do it in above step
        data = yaml.load(data) # coverted to Dict format
        print(data)
        return jsonify(data)


if __name__== "__main__":
    app.run(host='127.0.0.1', port=8080,debug=True)
