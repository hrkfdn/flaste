import sqlite3, time, encode

class PasteDB:
	def __init__(self, filename):
		self.filename = filename

	def connect(self):
		self.db = sqlite3.connect(self.filename)
		self.db.cursor().execute("CREATE TABLE IF NOT EXISTS pastes (id INTEGER PRIMARY KEY, src text, paste text, date date, lexer text)")

	def disconnect(self):
		self.db.close()

	def getcursor(self):
		return self.db.cursor()

	def getpaste(self, id):
		id_decoded = encode.base_decode(id)

		c = self.getcursor()
		c.execute("SELECT * FROM pastes WHERE id=(?)", (id_decoded,))
		result = c.fetchone()
		if result is not None:
			return result
		else:
			return None 

	def savepaste(self, src, content, lexer):
		id = encode.crc(content)
		c = self.getcursor()
		try:
			c.execute("INSERT INTO pastes VALUES (?, ?, ?, ?, ?)", (id, src, content, time.time(), lexer))
			self.db.commit()
		except sqlite3.IntegrityError: # hash collision, most likely same paste
			pass
		return encode.base_encode(id)
