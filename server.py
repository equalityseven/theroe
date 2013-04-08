from flask import Flask, render_template
import AWSmodule as aws

app = Flask(__name__)

@app.route('/')
def hello_world():
	try:
		instances = aws.AWSInst('sa-east-1')
	except ValueError:
		return "Unable to get instances"

	return render_template("index.html", instances=instances.all_instances())

if __name__ == '__main__':
    app.run()
