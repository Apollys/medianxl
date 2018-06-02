import keyboard
import mouse
import median
from util import sleep_ms

# Starts a single player game with the character in the first slot
def create_singleplayer_game():
   mouse.move(*median.get_coords('singleplayer'))
   mouse.click()
   keyboard.send('enter')
   median.wait_enter_game()
   
def open_inventory(inventory_hotkey='i'):
   keyboard.send(inventory_hotkey)
   sleep_ms(100)
   
def open_cube():
   mouse.move(*median.get_coords('cube'))
   sleep_ms(50)
   mouse.right_click()
   sleep_ms(50)
   
def move_item_to_cube(coords):
   # Grab item
   mouse.move(*coords)
   mouse.click()
   sleep_ms(50)
   # Place in cube
   mouse.move(*median.get_coords('cube'))
   sleep_ms(50)
   mouse.click()
   sleep_ms(50)
   
# Returns stats of transmuted item
# size parameter must be either 'big' or 'small'
def transmute_get_stats(size=''):
   # Initialize post-transmute item location
   item_coords = (0, 0)
   if (size == 'large'):
      item_coords = median.get_coords('cubetopleft')
   elif (size == 'small'):
      item_coords = median.get_coords('cubebotright')
   else:
      raise ValueError("Please give a size parameter, either 'large' or 'small'")
   # Transmute
   mouse.move(*median.get_coords('transmute'))
   sleep_ms(10)
   mouse.click()
   sleep_ms(10)
   # Mouseover item
   mouse.move(*item_coords)
   sleep_ms(100)
   # Get text
   return median.get_item_text()
   
# Close inventory, or close inventory + cube
def close_inventory():
   keyboard.send('esc')
   sleep_ms(150)
   
def exit_game():
   keyboard.send('esc')
   mouse.move(*median.get_coords('exit'))
   mouse.click()
   sleep_ms(100)
   median.wait_exit_game()
