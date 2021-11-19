import sys
import re

def parseFile(path):
  parsed = []
  print(f'Reading "{path}"...')
  with open(path, 'r') as f:
    lines = f.readlines()
    is_markdown_table = lines[0][0] == '|'
    if is_markdown_table:
      print('- Markdown table detected, dropping two rows')
      lines.reverse()
      lines.pop()
      lines.pop()
      lines.reverse()

    for line in lines:
      clean = line.strip()
      if is_markdown_table:
        clean = clean[1:-1].strip()

      parsed.append(re.split(r'\s*\|\s*', clean))

  print(f'- Read {len(parsed)} items from "{path}".')
  return parsed

if len(sys.argv) != 2:
  sys.exit('Missing directory path.')

workroot = sys.argv[1]
print(f'Reading data from "{workroot}".')

base_file = workroot + '/base.md'
material_file = workroot + '/material.md'
prefix_file = workroot + '/prefix.md'
output_file = workroot + '/output.csv'

base = parseFile(base_file)
material = parseFile(material_file)
prefix = parseFile(prefix_file)
  
base_components = ['Greeble', 'Flonk', 'Bingle', 'Toff', 'Rund']

total_items = len(base) * len(material) * len(prefix)
print(f'Total Possible Items: {total_items}')

with open(output_file, 'w+') as f:
  f.write('item,tags\n')
  for _base in base:
    for _material in material:
      for _prefix in prefix:
        p = _prefix[0]
        px = _prefix[1] if len(_prefix) > 1 else ""
        m = _material[0]
        mx = _material[1] if len(_material) > 1 else ""
        b = _base[0]
        bx = _base[1] if len(_base) > 1 else ""

        f.write(f'"{p} {m} {b}",[Item.Material.{m}, Item.Prefix.{p}, Item.Type.{b}, Item.{bx}]\n')