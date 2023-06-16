from flask import Flask, render_template, request

app = Flask(__name__)


@app.route('/')
def hello():
	return render_template('index.jinja2')


@app.route('/hi', methods=['GET'])
def hi():
	name = request.args.get('name')
	return render_template('hi.jinja2', name=name)


if __name__ == '__main__':
	app.debug = True
	app.run()
