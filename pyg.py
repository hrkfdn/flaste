import pygments
from pygments.lexers import guess_lexer, guess_lexer_for_filename, get_lexer_by_name, get_all_lexers
from pygments.formatters import HtmlFormatter

try:
	FORMATTER = HtmlFormatter(linenos=True, style="solarizedlight")
except pygments.util.ClassNotFound:
	FORMATTER = HtmlFormatter(linenos=True)

CSS = FORMATTER.get_style_defs('.highlight')

def determine_lexer(content, src):
	lexer = ""
	try:
		if src == "web" or src == "stdin":
			lexer = guess_lexer(content).aliases[0]
		else:
			lexer = guess_lexer_for_filename(src, content).aliases[0]
	except pygments.util.ClassNotFound:
		pass

	if lexer.lower() == "numpy": # this hack is needed when the lexer detection returns NumPy
		return "python"
	else:
		return lexer

def highlight(content, lexer):
	try:
		lexer = get_lexer_by_name(lexer.lower(), stripall=True)
	except pygments.util.ClassNotFound:
		lexer = get_lexer_by_name("text")
	result = pygments.highlight(content, lexer, FORMATTER)

	return result

def getcss():
	return CSS

def lexer_list():
	lexers = []
	for i in get_all_lexers():
		lexers.append((i[0], i[1][0]))
	lexers.sort()
	return lexers

LEXERS = lexer_list()

def generate_dropdown(selected=None):
	out = "<select onchange=\"this.options[this.selectedIndex].value && (window.location = this.options[this.selectedIndex].value);\">\n"
	for i in LEXERS:
		shortname = i[1]
		fullname = i[0]
		if shortname == selected:
			out += "\t<option selected value=\"" + shortname + "\">" + fullname + "</option>\n"
		else:
			out += "\t<option value=\"" + shortname + "\">" + fullname + "</option>\n"
	out += "</select>\n"
	return out
