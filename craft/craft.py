import keyboard
import mouse
import time

import backup_restore as backrest
import median
import scan_codes
import util
import item_parser

from util import sleep_ms

VERBOSE = True
# Set to false for tasks with huge amounts of new games
# True is fine most of the time
BACKUP_ALL_OVERWRITTEN_FILES = False

def mouse_coord_callback():
   coord_string = 'Mouse coordinates: ' + str(mouse.get_position())
   util.log(coord_string)
   return coord_string
   
def craft():
   FLAT_DMG_THRESH = 175
   ENH_DMG_THRESH = 120
   print('\n\nStarting crafting loop...\n\n')
   # Loop until we're done, each iteration is one character
   done = False
   while (not done):
      # Track best average damage per character
      best_avg_flat_dmg = 0
      corr_enh_dmg = 0
      # Restore character
      character = backrest.restore_recent(BACKUP_ALL_OVERWRITTEN_FILES)
      if (VERBOSE): print('Restored', character)
      # Create singleplayer game
      mouse.move(*median.get_coords('singleplayer'))
      mouse.click()
      keyboard.send('enter')
      if (VERBOSE): print('Entering new game...')
      median.wait_enter_game()
      if (VERBOSE): print('Entered game')
      # Open inventory
      keyboard.send('i')
      time.sleep(.1)
      # Loop through each shrine
      shrine_size = 1, 2 # width, height
      for i, coords in enumerate(median.inv_iter(*shrine_size)):
         if done: break
         # Skip first two "shrines", these are where the cube is
         if (i < 2): continue
         # Place shrine into cube
         #   1) Grab shrine
         mouse.move(*coords)
         mouse.click()
         sleep_ms(50)
         #   2) Place in cube
         mouse.move(*median.get_coords('cube'))
         sleep_ms(50)
         mouse.click()
         sleep_ms(50)
         #   3) Open cube only if first shrine
         if (i == 2):
            mouse.right_click()
            sleep_ms(50)
         # Loop through a shrine's 10 charges
         for charge in range(10):
            # Ensure that if the window loses focus, loop exits
            if (not util.check_active_window()):
               print('Game window lost focus, exiting crafting loop.')
               done = True
               break
            # Transmute
            mouse.move(*median.get_coords('transmute'))
            sleep_ms(10)
            mouse.click()
            sleep_ms(10)
            # Mouseover item
            mouse.move(*median.get_coords('cubetopleft'))
            sleep_ms(100)
            # Get text
            item_stats = median.get_item_text()
            enh_dmg = item_parser.get_enhanced_damage(item_stats)
            avg_flat_dmg = item_parser.get_flat_damage(item_stats)
            if (avg_flat_dmg > best_avg_flat_dmg):
               best_avg_flat_dmg = avg_flat_dmg
               corr_enh_dmg = enh_dmg
            # log_string = '=========================\n\n' + item_stats + '\n'
            # util.log(log_string, 'item_log.txt')
            sleep_ms(100)
            # Check if we are done
            if ( (enh_dmg >= ENH_DMG_THRESH) and (avg_flat_dmg >= FLAT_DMG_THRESH) ):
               done = True
               break
         # End of shrine charges loop
         # For testing, break early
         # if (i == 3): break
      # End of shrines loop
      # Print out best average damage for this character
      print('Finished this character')
      print('   best average flat damage: ', best_avg_flat_dmg, sep='')
      print('   corresponding enh damage: ', corr_enh_dmg, '%', sep='')
      print()
      # Exit game
      if (not done):
         keyboard.send('esc')
         sleep_ms(150)
         keyboard.send('esc')
         mouse.move(*median.get_coords('exit'))
         if (VERBOSE): print('Exiting game...')
         mouse.click()
         sleep_ms(100)
         median.wait_exit_game()
         if (VERBOSE): print('Exited game...')
         sleep_ms(100)
      # Ensure that if the window loses focus, loop exits
      if (not util.check_active_window()):
         print('Game window lost focus, exiting crafting loop.')
         break
   # End of while loop
   ##
   # Print out stats
   print('Best average flat damage:', best_avg_flat_dmg)
   return 'Completed crafting'
      
   
def main():
   # Add hotkeys
   util.add_guarded_hotkey('\\', mouse_coord_callback, suppress=False)
   util.add_guarded_hotkey('a', craft, suppress=False)
   
   print('Awaiting user input...')
   
   # Press q at any time to quit
   keyboard.wait('q')




if __name__ == '__main__':
   main()