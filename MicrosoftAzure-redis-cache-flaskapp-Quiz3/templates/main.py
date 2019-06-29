# from flask import Flask
from flask import Flask, request, render_template
app = Flask(__name__)

@app.route('/')
def my_form():
    return render_template('my-form.html')

@app.route('/', methods=['POST'])
def my_form_post():
    text = request.form['text']
    processed_text = text.upper()
    return ( 'Welcome, 😊 ' + processed_text + ' 😊 to our Cloud Computing Summar 2018 class')

def hello_world():
  return 'Hello, World!\n This looks just amazing within 5 minutes'

if __name__ == '__main__':
  app.run()
