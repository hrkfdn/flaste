#!/usr/bin/python

# CONFIGURATION
url = "http://p.diff.cc"
# END OF CONFIGURATION

import sys
import urllib.request
import urllib.parse

if len(sys.argv) > 1:
	try:
		source = open(sys.argv[1], "r")
		filename = sys.argv[1]
	except IOError as e:
		print("I can not open the source file (" + sys.argv[1] + "). Reason: " + e.strerror)
		sys.exit()
else:
	source = sys.stdin
	filename = "stdin"

content = source.read()

postdata = { "source" : filename, "content" : content }
urlencoded = urllib.parse.urlencode(postdata)
req = urllib.request.Request(url + "/submit/", urlencoded.encode("utf-8"))
req.add_header("Content-Type", "application/x-www-form-urlencoded")

try:
	print("Pasting to " + url + " ..")
	response = urllib.request.urlopen(req)
except urllib.error.URLError as e:
	print("I could not submit the data. Reason: " + e.strerror)
	sys.exit()

print("Link: " + response.geturl())
