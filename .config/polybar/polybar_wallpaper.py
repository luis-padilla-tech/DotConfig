from pathlib import Path
from polybar_color import COLOR_THEMES
from polybar import get_file_config_location


def main():
	file_location = get_file_config_location()

	if not file_location.exists():
		return
	
	line = get_line(file_location)
	config_name = get_config_name(line)

	if config_name is None:
		return

	wallpaper_directory = get_wallpaper(config_name)
	
	if wallpaper_directory is None:
		return

	start_wallpaper(wallpaper_directory)


def get_line(file_location: Path):
	with open(file_location) as reader:
		return reader.readline()

def get_config_name(line:str) -> str|None:
	import re

	pattern = ';PYTHON_CONFIG_NAME=(.*)'
	match_result = re.search(pattern, line)

	if not bool(match_result):
		return None
	
	return match_result.group(1)


def get_wallpaper(config_name:str) -> Path|None:

	if config_name not in COLOR_THEMES:
		return None

	theme = COLOR_THEMES[config_name]
	wallpaper_directory = Path(theme.wallpaper_directory).expanduser()

	if wallpaper_directory.exists():
		return wallpaper_directory

	return None

def start_wallpaper(wallpaper_directory: Path):
	import subprocess
	subprocess.call(['feh', '--bg-fill','--randomize', wallpaper_directory])


if __name__ == '__main__':
	main()