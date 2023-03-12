"""
Install/Update Polybar config.ini

Edit Colors:
Add more key, value pairs to get_colors() function. All values must be supplied except for 

Edit Config:
Create/Update polobar_template.init. Place all none color relating code there.
Reference colors like like normal
"""
from pathlib import Path
from typing import Dict, Tuple

from polybar_color import DEFAULT_COLOR_SCHEME, COLOR_THEMES, PolybarColor, get_default_color_tuple

def get_polybar_config() -> str:
	template_path = Path('~/.config/polybar/polybar_template.ini').expanduser()
	with open(template_path) as reader:
		return reader.read()


def pick_color() -> Tuple[str, 'PolybarColor']:
	
	if DEFAULT_COLOR_SCHEME is not None:
		return get_default_color_tuple()

	if len(COLOR_THEMES) == 1:
		return list(COLOR_THEMES.items())[0]
	elif len(COLOR_THEMES) == 0:
		raise Exception('No Colors Defined')

	print_color_choices(COLOR_THEMES)

	while True:
		user_chosen_color = input('Choose color name: ')
		if user_chosen_color in COLOR_THEMES:
			return user_chosen_color, COLOR_THEMES[user_chosen_color]
		else:
			print(f'{user_chosen_color} is not a valid name')

def print_color_choices(color_dict:Dict[str, 'PolybarColor']):
	line_sep = '\n' + '-'*25 + '\n'

	color_header =  f'{line_sep}Colors{line_sep}'
	color_footer = f'{line_sep}END Colors{line_sep}'

	print(color_header)

	for index, name in enumerate(color_dict):
		print(f'{index}: {name}')
	
	print(color_footer)

def is_overwriteable() -> bool:
	while True:
		user_input = input('Config Exists. Do you want to overwrite? Y/N (defaults to Y): ').upper()

		if user_input == '' or user_input == 'Y':
			return True
		elif user_input == 'N':
			return False

def write_config_file(polybar_ini_location: Path, content:str):
	with open(polybar_ini_location, 'w') as writer:
		writer.write(content)

def get_file_config_location() -> Path:
	return Path('~/.config/polybar/config.ini').expanduser()

def main():

	name, color_chosen  = pick_color()
	other_polybar_config = get_polybar_config()
	color_config = color_chosen.get_color_config_string(name)
	final_config_content = color_config + '\n\n' + other_polybar_config
	polybar_ini_location = get_file_config_location()

	if not polybar_ini_location.exists() or (polybar_ini_location.exists() and is_overwriteable()):
		write_config_file(polybar_ini_location, final_config_content)
		

if __name__ == '__main__':
	main()