import re
from dataclasses import dataclass

@dataclass
class Item:
  base: dict[str]
  material: dict[str]
  prefix: dict[str]

  def id(self) -> str:
    '''
    The formatted id for the item.

    Displays as `<prefix>_<material>_<base>`.
    '''
    return f"{self.prefix.get('name','ERR')}_{self.material.get('name','ERR')}_{self.base.get('name','ERR')}".lower()
  
  def name(self) -> str:
    '''
    The formatted id for the item.

    Displays as `<Prefix> <Material> <Base>`.
    '''
    return f"{self.prefix.get('name','ERR')} {self.material.get('name','ERR')} {self.base.get('name','ERR')}"

  def tags(self) -> set[str]:
    '''
    A set containing all the tags of the item.
    '''
    tag_string = f"{self.prefix.get('tags','')},{self.material.get('tags','')},{self.base.get('tags','')}"
    return set(re.split(r',\s*', tag_string))
  
  def stat(self, key: str) -> float:
    stat = float(self.prefix.get(key, '0')) + float(self.material.get(key, '0')) + float(self.base.get(key, '0'))
    global_multiplier = float(self.prefix.get('global_multiplier','1')) * float(self.material.get('global_multiplier','1')) * float(self.base.get('global_multiplier','1'))
    multiplier_name = f'{key}_multiplier'
    stat_multiplier = float(self.prefix.get(multiplier_name,'1')) * float(self.material.get(multiplier_name,'1')) * float(self.base.get(multiplier_name,'1'))
    return stat * global_multiplier * stat_multiplier

  def damage(self) -> float:
    return self.stat('damage')

  def defense(self) -> float:
    return self.stat('defense')

  def speed(self) -> float:
    return self.stat('speed')