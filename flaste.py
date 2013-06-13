import pyg, time, encode
from pastedb import PasteDB
from flask import Flask, request, render_template, redirect, url_for, Markup, Response
app = Flask(__name__)
db = PasteDB("pastedb.sqlite")

@app.route("/")
def index():
	return render_template("index.html")

@app.route("/<id>")
@app.route("/<id>/")
@app.route("/<id>/<lexer>")
def showpaste(id, lexer=None):
	paste = db.getpaste(id)
	if paste is not None:
		if lexer is None:
			lexer = paste[4]
		if lexer == "plain":
			return Response(paste[2], mimetype="text/plain")
		else:
			highlighted = Markup(pyg.highlight(paste[2], lexer))
			return render_template("paste.html", source=paste[1], content=highlighted, date=time.ctime(paste[3]), dropdown=Markup(pyg.generate_dropdown(lexer)))
	else:
		return "Invalid ID"

@app.route("/submit/", methods=['GET', 'POST'])
def paste():
	if request.method == 'POST':	# send a paste
		lexer = pyg.determine_lexer(request.form['content'], request.form['source'])
		id_ret = db.savepaste(request.form['source'], request.form['content'], lexer)
		return redirect(url_for('showpaste', id=id_ret))
	else:
		return "" # This shouldn't happen

@app.route("/static/css/pygments.css")
def returncss():
	pygcss = pyg.getcss()
	pygcss += "table.highlighttable { border-width: 1px; border-style: dashed; }";
	pygcss += "td.linenos { background-color: #EEEEEE; }"
	return pygcss 

@app.route("/favicon.ico/")
def favicon():
	return ""

@app.before_request
def before_request():
	db.connect()

@app.teardown_request
def teardown_request(exception):
	db.disconnect()

if __name__ == "__main__":
	app.run(debug=True, host='0.0.0.0')
