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
   min_dmg = 0
   max_dmg = 0
   avg_flat_dmg = 0
   # Note: The compiled versions of the most recent patterns passed to re.match(),
   # re.search() or re.compile() are cached, so programs that use only a few
   # regular expressions at a time needn’t worry about compiling regular
   # expressions.  [From the official documentation]
   patternmin = '\+[0-9]* to Minimum Damage'
   mi = re.search(patternmin, item_stats)
   patternmax = '\+[0-9]* to Maximum Damage'
   ma = re.search(patternmax, item_stats)
   pattern = 'Adds [0-9]*-[0-9]* Damage'
   m = re.search(pattern, item_stats)
   if m:
      avg_flat_dmg = 0.5*sum(parse_ints(m.group()))
   if mi:
      avg_flat_dmg += 0.5*parse_ints(mi.group())[0]
   if ma:
      avg_flat_dmg += 0.5*parse_ints(ma.group())[0]
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
   
def get_zon_skills(item_stats):
   zon_skills = 0
   pattern = '\+[0-9]* to Amazon Skill Levels'
   m = re.search(pattern, item_stats)
   if m:
      zon_skills = parse_ints(m.group())[0]
   return zon_skills
   
def get_pierce_all_res(item_stats):
   pierce_all_res = 0
   pattern = '\-[0-9]*% to All Enemy Resistances'
   m = re.search(pattern, item_stats)
   if m:
      pierce_all_res = parse_ints(m.group())[0]
   return pierce_all_res

def get_pierce_spec_res(item_stats, res):
   pierce_spec_res = 0
   pattern = '\-[0-9]*% to Enemy '+res+' Resistance'
   m = re.search(pattern, item_stats)
   if m:
      pierce_spec_res = parse_ints(m.group())[0]
   return pierce_spec_res
   
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
   
def get_attr(item_stats, attr = ''):
   att_value = 0
   patternall = '\+[0-9]* to all Attributes'
   m = re.search(patternall, item_stats)
   if m:
      att_value = parse_ints(m.group())[0]
   elif attr:
      patternspec = '\+[0-9]* to '+attr
      m = re.search(patternspec, item_stats)
      if m:
         att_value = parse_ints(m.group())[0]
   return att_value

def get_pattr(item_stats, attr = ''):
   att_value = 0
   patternall = '[0-9]*% Bonus to all Attributes'
   m = re.search(patternall, item_stats)
   if m:
      att_value = parse_ints(m.group())[0]
   elif attr:
      patternspec = '[0-9]*% Bonus to '+attr
      m = re.search(patternspec, item_stats)
      if m:
         att_value = parse_ints(m.group())[0]
   return att_value
   
def get_life(item_stats):
   life = 0
   pattern = '\+[0-9]* to Life'
   m = re.search(pattern, item_stats)
   if m:
      life = parse_ints(m.group())[0]
   return life
   
def get_frw(item_stats):
   frw = 0
   pattern = '[0-9]*% Faster Run/Walk'
   m = re.search(pattern, item_stats)
   if m:
      frw = parse_ints(m.group())[0]
   return frw