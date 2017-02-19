from flask import Flask
from flask import render_template


app = Flask(__name__)
app.debug = True


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/review')
def review():
    reviews = [("this thing sucks", 10), ("I am too tired for this shit", 100000)]

    return render_template('review.html', item_name="The unstoppable passage of time #entropyalwaysincreases", overall="Not Good :(", reviews=reviews)



if __name__ == '__main__':
    app.run()
