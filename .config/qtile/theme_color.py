from dataclasses import dataclass, field

@dataclass
class ThemeColor:
    """
    Qtile Color Theme picker
    """

    foreground:str
    """Main foreground/font color"""

    background:str
    """Main background color"""

    active:str = field(default=None)
    """Font Color of active group(active meaning theres an app in the group)"""

    inactive:str = field(default=None)
    """Font Color of inactive group(inactive meaning there is no apps in the group)"""

    colors:list = field(default_factory=lambda: [])
    """List of extra colors you may want to use that may not fall under the other fields"""

    wallpaper_directory:str = field(default_factory=lambda: None)
    """Directory of wallpapers"""
