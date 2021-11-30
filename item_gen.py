import sys
import re
from item_data import Item

def main():
  if len(sys.argv) != 2:
    sys.exit('Missing directory path.')

  workroot = sys.argv[1]
  print(f'Reading data from "{workroot}".')

  base_file = workroot + '/base.md'
  material_file = workroot + '/material.md'
  prefix_file = workroot + '/prefix.md'
  output_file = workroot + '/output.csv'

  base: list[dict] = parseFile(base_file)
  material: list[dict] = parseFile(material_file)
  prefix: list[dict] = parseFile(prefix_file)

  base_components = ['Greeble', 'Flonk', 'Bingle', 'Toff', 'Rund']

  total_items = len(base) * len(material) * len(prefix)
  print(f'Generating {total_items} items')

  item_data: list[Item] = []
  for b in base:
    for m in material:
      for p in prefix:
        item_data.append(Item(b,m,p))

  with open(output_file, 'w+') as f:
    f.write('id,name,tags,damage,defense,speed\n')
    for item in item_data:
      f.write(f'"{item.id()}","{item.name()}","[{", ".join(item.tags())}]","{item.damage()}","{item.defense()}","{item.speed()}"\n')

  print(f'Wrote {total_items} items to "{output_file}".')


def parseFile(path: str) -> list[dict]:
  parsed = []
  print(f'Reading "{path}"...')
  with open(path, 'r') as f:
    lines = f.readlines()
    is_markdown_table = lines[0][0] == '|'
    field_names = ['name']
    if is_markdown_table:
      clean = lines[0].strip()[1:-1].strip()
      field_names = re.split(r'\s*\|\s*', clean)
      print(f'- Markdown table detected with {len(field_names)} fields: {field_names}')
      lines = lines[2:]

    for line in lines:
      clean = line.strip()
      if is_markdown_table:
        clean = clean[1:-1].strip()

      line_dict = {}
      line_values = re.split(r'\s*\|\s*', clean)
      for i in range(len(field_names)):
        line_dict[field_names[i]] = line_values[i]

      parsed.append(line_dict)

  print(f'- Read {len(parsed)} items from "{path}".')
  return parsed

if __name__ == '__main__':
  main()