```python
# Search for Empyrean Band
TARGET_ITEM_NAME = 'Empyrean Band'
def craft():
   print('\n\nStarting crafting loop...\n\n')
   # Track empyrean band count
   count = 0
   # Loop until we're done, each iteration is one character
   done = False
   while (not done):
      # Restore character
      character = backrest.restore_recent(BACKUP_ALL_OVERWRITTEN_FILES)
      if (VERBOSE): print('Restored', character)
      # Create game
      actions.create_singleplayer_game()
      actions.open_inventory()
      # Loop through 2x arcane crystal, 1x oil of renewal
      # tile(w, h, total_w, total_h, n, x0=0, y0=0, skip_list=[])
      crystal_indices = util.tile(2, 1, 10, 5, 50, y0=3)
      oil_indices = util.tile(1, 1, 10, 5, 25, skip_list=[0, 1, 10, 11, 20])
      charm_ij = (0, 2) # x, y
      for i, zipped_indices in enumerate(zip(crystal_indices, oil_indices)):
         if done: break
         # Compute positions
         crystal_ij, oil_ij = zipped_indices
         crystal2_ij = (crystal_ij[0] + 1, crystal_ij[1])
         crystal_coords = median.get_inv_coords(crystal_ij)
         crystal2_coords = median.get_inv_coords(crystal2_ij)
         oil_coords = median.get_inv_coords(oil_ij)
         # Cube ring + 2 crystals + 1 oil
         actions.move_item_to_cube(crystal_coords)
         actions.move_item_to_cube(crystal2_coords)
         actions.move_item_to_cube(oil_coords)
         item_stats = actions.transmute_get_stats(size='large')
         # Check name
         if (item_parser.get_name(item_stats) == TARGET_ITEM_NAME):
            print(TARGET_ITEM_NAME, 'found ( i =', i, ')')
            actions.move_item_to_cube(median.get_inv_coords(charm_ij))
            lucky_stats = actions.transmute_get_stats()
            done = True
            break
         # Ensure that if the window loses focus, loop exits
         if (not util.check_active_window()):
            print('Game window lost focus, exiting crafting loop.')
            break
      # End of inventory loop
      # Exit game
      if (not done):
         actions.exit_game()
      # Ensure that if the window loses focus, loop exits
      if (not util.check_active_window()):
         print('Game window lost focus, exiting crafting loop.')
         break
   # End of while loop
   ##
   # Print out stats
   print('Best average flat damage:', best_avg_flat_dmg)
   return 'Completed crafting'
   ```
