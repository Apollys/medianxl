import re

NUMERIC_CHARS = '0123456789'

# return a list of integers containing the numbers in the string
def parse_ints(s):
   int_list = []
   curr_num = ''
   in_num = False
   for c in s:
      if c in NUMERIC_CHARS:
         curr_num += c
         in_num = True
      else:
         if in_num:
            int_list.append(int(curr_num))
            curr_num = ''
            in_num = False
   if in_num:
      int_list.append(int(curr_num))
   return int_list

def get_1h_damage(item_stats, ret_type='avg'):
   line_prefix = 'One-Hand Damage'
   lines = item_stats.split('\n')
   damage_range = (0, 0)
   for line in lines:
      if line.startswith(line_prefix):
         damage_range = tuple(parse_ints(line))
         break
   if (ret_type == 'avg'):
      return 0.5*sum(damage_range)
   else:
      return damage_range
      
def get_flat_damage(item_stats):
   avg_flat_dmg = 0
   # Note: The compiled versions of the most recent patterns passed to re.match(),
   # re.search() or re.compile() are cached, so programs that use only a few
   # regular expressions at a time needn’t worry about compiling regular
   # expressions.  [From the official documentation]
   pattern = 'Adds [0-9]*-[0-9]* Damage'
   m = re.search(pattern, item_stats)
   if m:
      avg_flat_dmg = 0.5*sum(parse_ints(m.group()))
   return avg_flat_dmg
   
def get_enhanced_damage(item_stats):
   enh_dmg = 0
   pattern = '\+[0-9]*% Enhanced Damage'
   m = re.search(pattern, item_stats)
   if m:
      enh_dmg = parse_ints(m.group())[0]
   return enh_dmg
   
def get_enhanced_defense(item_stats):
   enhanced_defense = 0
   pattern = '\+[0-9]*% Enhanced Defense'
   m = re.search(pattern, item_stats)
   if m:
      enhanced_defense = parse_ints(m.group())[0]
   return enhanced_defense
   
def get_all_skills(item_stats):
   all_skills = 0
   pattern = '\+[0-9]* to All Skills'
   m = re.search(pattern, item_stats)
   if m:
      all_skills = parse_ints(m.group())[0]
   return all_skills
   
def get_pierce_all_res(item_stats):
   pierce_all_res = 0
   pattern = '\-[0-9]*% to All Enemy Resistances'
   m = re.search(pattern, item_stats)
   if m:
      pierce_all_res = parse_ints(m.group())[0]
   return pierce_all_res
   
def get_all_max_res(item_stats):
   all_max_res = 0
   pattern = '\+[0-9]*% to All Maximum Resistances'
   m = re.search(pattern, item_stats)
   if m:
      all_max_res = parse_ints(m.group())[0]
   return all_max_res
   
def get_damage_reduced_percent(item_stats):
   damage_reduced_percent = 0
   pattern = 'Damage Reduced by [0-9]*%'
   m = re.search(pattern, item_stats)
   if m:
      damage_reduced_percent = parse_ints(m.group())[0]
   return damage_reduced_percent