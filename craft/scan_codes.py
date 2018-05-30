
SCAN_CODES = {}
# Special
SCAN_CODES['lctrl'] = 29
SCAN_CODES['lshift'] = 42
SCAN_CODES['lalt'] = 56
SCAN_CODES['`'] = 41
SCAN_CODES['\\'] = 43
# Numpad
SCAN_CODES['num7'] = 71
SCAN_CODES['num8'] = 72
SCAN_CODES['num9'] = 73
SCAN_CODES['num4'] = 75
SCAN_CODES['num5'] = 76
SCAN_CODES['num6'] = 77
SCAN_CODES['num1'] = 79
SCAN_CODES['num2'] = 80
SCAN_CODES['num3'] = 81
SCAN_CODES['num0'] = 82
SCAN_CODES['num.'] = 83
SCAN_CODES['num/'] = 53
SCAN_CODES['num*'] = 55
SCAN_CODES['num-'] = 74
SCAN_CODES['num+'] = 78
# Letters
SCAN_CODES['q'] = 16
SCAN_CODES['w'] = 17
SCAN_CODES['e'] = 18
SCAN_CODES['r'] = 19
# ...
SCAN_CODES['a'] = 30
SCAN_CODES['s'] = 31
SCAN_CODES['d'] = 32
SCAN_CODES['f'] = 33
# ...
SCAN_CODES['z'] = 44
SCAN_CODES['x'] = 45
SCAN_CODES['c'] = 46
SCAN_CODES['v'] = 47
# Numbers / Top Row
SCAN_CODES['1'] = 2
SCAN_CODES['2'] = 3
SCAN_CODES['3'] = 4
SCAN_CODES['4'] = 5
SCAN_CODES['5'] = 6
SCAN_CODES['6'] = 7
SCAN_CODES['7'] = 8
SCAN_CODES['8'] = 9
SCAN_CODES['9'] = 10
SCAN_CODES['0'] = 11
SCAN_CODES['-'] = 12
SCAN_CODES['='] = 13




def flip_dict(d):
   return { v:k for (k,v) in d.items() }
   
KEY_NAMES = flip_dict(SCAN_CODES)

def get_code(name):
   if name in SCAN_CODES:
      return SCAN_CODES[name]
   return -1

def get_name(code):
   if code in KEY_NAMES:
      return KEY_NAMES[code]
   return 'UnknownKey'