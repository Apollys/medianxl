import mouse # https://github.com/boppreh/mouse
import keyboard # https://github.com/boppreh/keyboard

import util
from scan_codes import get_code

true = True
false = False


## Constants ##

INVENTORY_HOTKEY = 'i'
TRANSMUTE_POS = {true: (799, 566), false: (240, 338)} # key = windowed_flag
GOLD_POS = {true: (1058, 694), false: (495, 465)} # key = windowed_flag

## Global variables ##

windowed_flag = false
ac_state = {'left': 0, 'right': 0}



## Helper functions ##
   
# Adds a hotkey that only activates when Diablo II is the active window   
def add_d2_hotkey(hotkey, callback, message):
   def guarded_callback():
      if is_d2_active():
         callback()
   #
   keyboard.add_hotkey(hotkey, guarded_callback)

# Clicks at the given coordinates, then returns the mouse to current position
# pos = (x, y)       
def click_and_return(pos):
   original_pos = mouse.get_position()
   mouse.move(*pos)
   mouse.click()
   mouse.move(*original_pos)

def update_windowed_flag(flag):
   global windowed_flag
   windowed_flag = flag
   
   
## Callback definitions ##
## Each must take no arguments and return a string message describing the action ##   

def exit_app_callback():
   util.exit_app()
   return 'Application closed'

def fullscreen_callback():
   update_windowed_flag(false)
   return 'App synced to fullscreen mode'

def windowed_callback():
   update_windowed_flag(true)
   return 'App synced to windowed mode'
   
def mouse_coord_callback():
   coord_string = 'Mouse coordinates: ' + str(mouse.get_position())
   util.log(coord_string)
   return coord_string

def transmute_callback():
   click_and_return(TRANSMUTE_POS[windowed_flag])
   return 'Transmuted'
   
def drop_gold_callback():
   # Get the position before opening inventory, to ensure mouse returns correctly
   original_pos = mouse.get_position()
   keyboard.send(INVENTORY_HOTKEY)
   util.sleep_ms(1)
   click_and_return(GOLD_POS[windowed_flag])
   keyboard.send('9, 9, 9, 9, 9, 9, 9, enter')
   keyboard.send(INVENTORY_HOTKEY)
   mouse.move(*original_pos)
   return 'Dropped gold'
   

# TODO: autoclicker
# button: 'left' or 'right'
# action: 'on', 'off', 'toggle'
def autoclicker(button='left', action='toggle'):
   pass


# The result of this module is the creation of this hotkey_list
# The hotkey list contains elements of (scan_code, function) pairs
# Scan codes are either a single integer or a tuple of integers
# Each function takes no arguments and retuns a string message
def get_hotkey_list():
   hotkey_list = []
   hotkey_list.append((get_code('num-'), exit_app_callback))
   hotkey_list.append((get_code('num*'), fullscreen_callback))
   hotkey_list.append((get_code('num/'), windowed_callback))
   hotkey_list.append((get_code('num9'), mouse_coord_callback))
   hotkey_list.append((get_code('\\'), transmute_callback))
   hotkey_list.append((get_code('`'), drop_gold_callback))
   return hotkey_list
