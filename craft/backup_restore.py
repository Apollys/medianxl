import os
import shutil

WORKING_PATH = 'D:\\Games\\Diablo II\\Save'
BACKUP_PATH = 'D:\\Games\\Diablo II\\Save\\_MuleBackup'
OVERWRITTEN_PATH = 'D:\\Games\\Diablo II\\Save\\XOverwritten'
EXTENSION = 'd2s' # file extension that we care about, do not include the period

DEBUG_FLAG = True

def printd(s):
   if DEBUG_FLAG: print(s)

# Returns a list of all files in path having the given extension
def listfiles(path, ext):
   all_filenames = os.listdir(path)
   return [x for x in all_filenames if '.' in x and x.split('.')[-1] == ext]

# If the source does not exist, does nothing
# If the destination directory does not exist, it is created
# Returns true iff the file was copied
def adv_copy(src, dest):
   if os.path.exists(src):
      dest_path = '\\'.join(dest.split('\\')[:-1])
      if not os.path.exists(dest_path):
         os.makedirs(dest_path)
      shutil.copyfile(src, dest)
      return True
   else:
      return False
   
# Returns a unique name for the file to be saved in OVERWRITTEN_PATH
# Example: name = hello.txt --> hello.1.txt, hello.2.txt, ...
def next_over_name(name):
   prefix = '.'.join(name.split('.')[:-1])
   suffix = '.' + name.split('.')[-1]
   i = 1
   while True:
      next_name = prefix + str(i) + suffix
      if not os.path.exists(os.path.join(OVERWRITTEN_PATH, next_name)):
         return next_name
      else:
         i += 1
#

# Returns the filename (not full path) of the most recently
# modified file in the specified path
def get_recent(path):
   filenames = listfiles(path, EXTENSION)
   mod_times = [os.path.getmtime(os.path.join(path, name)) for name in filenames]
   maxi = mod_times.index(max(mod_times))
   if filenames[maxi]=='Host.d2s':
      del filenames[maxi]
      del mod_times[maxi]
      maxi = mod_times.index(max(mod_times))
   return filenames[maxi]

# Copies the most recently modified file (with correct extension)
# in the working path to the overwritten path 
# Returns the name of the backed up file
def backup_recent(save_overwritten=True):
   name = get_recent(WORKING_PATH)
   src_name = os.path.join(WORKING_PATH, name)
   dest_name = os.path.join(BACKUP_PATH, name)
   over_name = os.path.join(OVERWRITTEN_PATH, next_over_name(name))
   if save_overwritten: adv_copy(dest_name, over_name)
   adv_copy(src_name, dest_name)
   return name
   
# Copies the most recently modified file (with correct extension)
# in the backup path to the overwritten path 
# Returns the name of the restored file
def restore_recent(save_overwritten=True):
   name = get_recent(WORKING_PATH)
   dest_name = os.path.join(WORKING_PATH, name)
   src_name = os.path.join(BACKUP_PATH, name)
   over_name = os.path.join(OVERWRITTEN_PATH, next_over_name(name))
   if save_overwritten: adv_copy(dest_name, over_name)
   adv_copy(src_name, dest_name)
   return name