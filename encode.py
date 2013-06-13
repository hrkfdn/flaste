import string, zlib
BASE_LIST = string.digits + string.letters + '-_'
BASE_DICT = dict((c, i) for i, c in enumerate(BASE_LIST))

def base_decode(string, reverse_base=BASE_DICT):
	length = len(reverse_base)
	ret = 0
	for i, c in enumerate(string[::-1]):
		try:
			ret += (length ** i) * reverse_base[c]
		except KeyError:
			return None

	return ret

def base_encode(integer, base=BASE_LIST):
	length = len(base)
	ret = ''
	while integer != 0:
		ret = base[integer % length] + ret
		integer /= length

	return ret

def crc(string):
	return zlib.crc32(string) & 0xFFFFFFFF
