from PIL import ImageGrab
import numpy as np
import time
import keyboard
import clipboard

import scan_codes

# SINGLEPLAYER_POS =  {true: (958, 540), false: (397, 309)} # key = windowed_flag
# CUBE_POS =  {true: (1006, 474), false: (448, 242)} # key = windowed_flag
# TRANSMUTE_POS = {true: (800, 569), false: (240, 338)} # key = windowed_flag
# TRADERCHEST_POS =  {true: (931, 524), false: (371, 293)} # key = windowed_flag
# EXIT_POS =  {true: (959, 491), false: (396, 260)} # key = windowed_flag
# GOLD_POS = {true: (1058, 694), false: (495, 465)} # key = windowed_flag

WINDOWED_COORDS = {}
WINDOWED_COORDS['singleplayer'] = 958, 540
WINDOWED_COORDS['exit'] = 959, 491
WINDOWED_COORDS['cube'] = 1006, 476
WINDOWED_COORDS['transmute'] = 801, 570
WINDOWED_COORDS['cubetopleft'] = 670, 320
WINDOWED_COORDS['cubebotright'] = 931, 524
WINDOWED_COORDS['cubecenter'] = 801, 425

INV_ACTION_DELAY = .6 # seconds

def get_coords(key):
   return WINDOWED_COORDS[key]

def get_pixels_bbox(minX, minY, maxX, maxY):
   return np.asarray(ImageGrab.grab(bbox=(minX, minY, maxX, maxY)))
   
# center is an int pair   
def get_pixels_around(center, apothem):
   minX = center[0] - apothem
   maxX = center[0] + apothem
   minY = center[1] - apothem
   maxY = center[1] + apothem
   return np.asarray(ImageGrab.grab(bbox=(minX, minY, maxX, maxY)))
   
def wait_enter_game():
   # print('Waiting for game to be entered...')
   center = (1130, 384)
   apothem = 2
   entered_threshold = 30
   entered = False
   time.sleep(.5)
   while (not entered):
      avg_val = np.mean(get_pixels_around(center, apothem))
      entered = (avg_val > entered_threshold)
   # print('Entered game')

def wait_exit_game():
   # print('Waiting for game to be exited...')
   centers = [(960, 433), (880, 484), (1038, 483)]
   # intensities = [199.3, 198.8, 201.2] # for 3D Glide settings
   intensities = [155.5, 151.9, 162.1] # for 2D Low graphics settings
   apothem = 2
   max_total_delta = 10
   entered = False
   time.sleep(.1)
   while (not entered):
      total_delta = 0
      for center, target_intensity in zip(centers, intensities):
         intensity = np.mean(get_pixels_around(center, apothem))
         total_delta += abs(intensity - target_intensity)
         # print('Center: ', center, '    Intensity: ', intensity)
      entered = (total_delta <= max_total_delta)
   # print('Exited game')
   
   
def lerp(x0, x1, y0, y1, x):
   r = (x - x0) / (x1 - x0)
   return y0 + (y1 - y0)*r
   
# convert square indices to pixel coordinates
def get_inv_coords(indices):
   x, y = indices
   W = 10
   H = 8
   XMIN, YMIN = 993, 458 # top left corner of inventory
   XMAX, YMAX = 1253, 663 # bot right corner of inventory
   xcoord = lerp(0, W-1, XMIN, XMAX, x)
   ycoord = lerp(0, H-1, YMIN, YMAX, y)
   return xcoord, ycoord
   
   

# Iterates through the inventory, jumping by xstep and ystep
# Currently coordinates are based on windowed mode only
def inv_iter(xstep, ystep):
   W = 10
   H = 8
   for y in range(0, H, ystep):
      for x in range(0, W, xstep):
         yield get_inv_coords(x, y)
         
# Uses the D2Stats feature of reading an item's text into the clipboard
# Current D2Stats hotkey: Insert = 82
def get_item_text():
   read_hotkey = 82 
   keyboard.send(read_hotkey)
   return clipboard.paste().replace('\r', '')