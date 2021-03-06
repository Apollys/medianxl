import time # time.sleep()
import datetime # for timestamping messages
import win32gui # get current active window
import os # os._exit(code)

import keyboard

GAME_WINDOW_TITLE = 'Diablo II'

# Get current time as a string
def current_time_string():
   full_string = str(datetime.datetime.now())
   return full_string.split('.')[0]
   
def prepend_timestamp(s):
   return '[' + current_time_string() + ']   ' + str(s)

# Get title of currently active window
def active_window_title():
   return win32gui.GetWindowText(win32gui.GetForegroundWindow())
   
# Check if the game is the currently active window
def check_active_window():
   return active_window_title() == GAME_WINDOW_TITLE

# Callback function should return a string,
# which will be the message displayed on the gui
def add_guarded_hotkey(hotkey, callback, suppress=False):
   def full_callback():
      if (check_active_window()):
         res_str = callback()
         message = prepend_timestamp(res_str)
         print(message)
         log(message)
      else:
         if suppress:
            keyboard.send(hotkey)
   keyboard.add_hotkey(hotkey, full_callback, suppress=suppress)
   
# Log a message to a log file
def log(s, filename='log.txt'):
   with open(filename, 'a') as f:
       f.write(s + '\n')

# Sleeps for the given number of milliseconds
def sleep_ms(ms):
   time.sleep(ms/1000.0)
   
# Exit app function
def exit_app():
   print('Exiting app.')
   os._exit(0)
   

def tile(w, h, total_w, total_h, n=-1, x0=0, y0=0, skip_list=[]):
   # Ensure the boundaries are "tight"
   dim_x = total_w // w
   dim_y = total_h // h
   total_w = dim_x * w
   total_h = dim_y * h
   # Compute n if not given
   if (n == -1):
      n = dim_x * dim_y
   n = min(dim_x * dim_y, n) # ensure n isn't too large
   xs = []
   ys = []
   i = 0
   while (i < n):
      if (i in skip_list):
         skip_list.remove(i)
         if (n < dim_x * dim_y):
            n += 1
      else:
         x_counter = i*w + x0
         xs.append((i*w) % total_w + x0)
         ys.append(((i*w) // total_w) * h + y0)
      i += 1
   return list(zip(xs, ys))
   
   
   
   