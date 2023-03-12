"""Config For Colors for Polybar"""
from typing import Dict, Tuple
from dataclasses import field, dataclass

@dataclass
class PolybarColor:
	foreground: str
	background: str
	background_alt: str
	primary: str
	alert: str
	disabled: str
	wallpaper_directory: str = field(default = None)

	def get_color_config_string(self, config_name:str) -> str:
		return '\n'.join([
			f';PYTHON_CONFIG_NAME={config_name}',
			'[colors]',
			f'foreground = {self.foreground}',
			f'background = {self.background}',
			f'background-alt = {self.background_alt}',
			f'primary = {self.primary}',
			f'alert = {self.alert}',
			f'disabled = {self.disabled}'
		])


polybar_default = PolybarColor('#C5C8C6', '#282A2E', '#373B41', '#F0C674', '#A54242', '#707880')
orange = PolybarColor('#FBF2EE', '#FB6542', '#fb8367', '#8C3D59', '#000', '#FC9C85', '~/wallpaper/orange')
purple = PolybarColor('#FFF', '#5F4B8B', '#6F5D96', '#D98E7E', '#0000', '#b2b2b2', wallpaper_directory='~/wallpaper/purple' )

DEFAULT_COLOR_SCHEME = purple

COLOR_THEMES: Dict[str, 'PolybarColor'] = { 
	name: value for name, value in globals().items() if isinstance(value, PolybarColor) and name != 'DEFAULT_COLOR_SCHEME'
}

def get_default_color_tuple() -> Tuple[str, 'PolybarColor']:

	if not isinstance(DEFAULT_COLOR_SCHEME, PolybarColor):
		raise Exception('Bad Default Color Scheme. Ensure its an instance PolybarColor')

	for name, value in COLOR_THEMES.items():
		if value == DEFAULT_COLOR_SCHEME:
			return name, value

	raise Exception('Default Color Sch')