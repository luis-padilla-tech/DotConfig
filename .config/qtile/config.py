from libqtile import bar, layout, widget
from libqtile.config import Click, Drag, Group, Key, Match, Screen
from libqtile.lazy import lazy
from libqtile.utils import guess_terminal
from libqtile import qtile
from pathlib import Path
import time
import qtile_themes
import random
import os
import subprocess

from libqtile.log_utils import logger
from libqtile import hook

theme = qtile_themes.Purple

@hook.subscribe.startup_once
def on_start_of_qtile():
    loc = os.path.expanduser('~/.config/qtile/autorun.sh')
    subprocess.Popen([loc])


@hook.subscribe.startup
def on_start_or_restart():
    logger.warning(f"{theme} is the theme")
    if theme.wp_dir is not None:

        logger.info(f'wallpaper directory {theme.wp_dir}')

        wallpapers = [file for file in  Path(theme.wp_dir).expanduser().iterdir()]
        wallpaper_path = random.choice(wallpapers)

        # for screen in qtile.screens:
        #     screen.cmd_set_wallpaper(wallpaper_path,'fill')

mod = "mod4"
terminal = guess_terminal()

groups = [
    Group(name='1', label='1'),
    Group(name='2', label='2'),
    Group(name='3', label='3',matches=[
        Match(wm_class='discord')
    ]),
    Group(name='4', label='4', matches=[
        Match(wm_class='vscodium'),
    ]),
    Group(name='5', label='5', matches=[
        Match(wm_class='desmume'),
        Match(wm_class='Steam'),
        Match(wm_class='Minecraft Launcher'),
    ]),
    Group(name='6', label='6', matches=[
        Match(wm_class='Spotify'),
    ]),
    Group(name='7', label='7', matches=[
        Match(wm_class='liferea')
    ]),
    Group(name='8', label='8'),
    Group(name='9', label='9')
]

keys = [
    # Moving app windows around
    Key([mod, "shift"], "h", lazy.layout.shuffle_left(), desc="Move window to the left"),
    Key([mod, "shift"], "l", lazy.layout.shuffle_right(), desc="Move window to the right"),
    Key([mod, "shift"], "j", lazy.layout.shuffle_down(), desc="Move window down"),
    Key([mod, "shift"], "k", lazy.layout.shuffle_up(), desc="Move window up"),

    # Grow app windows
    Key([mod, "control"], "h", lazy.layout.grow_left(), desc="Grow window to the left"),
    Key([mod, "control"], "l", lazy.layout.grow_right(), desc="Grow window to the right"),
    Key([mod, "control"], "j", lazy.layout.grow_down(), desc="Grow window down"),
    Key([mod, "control"], "k", lazy.layout.grow_up(), desc="Grow window up"),
    Key([mod, "shift"], "n", lazy.layout.normalize(), desc="Reset all window sizes"),
    # Toggle between split and unsplit sides of stack.
    # Split = all windows displayed
    # Unsplit = 1 window displayed, like Max layout, but still with
    # multiple stack panes
    Key(
        [mod, "shift"],
        "Return",
        lazy.layout.toggle_split(),
        desc="Toggle between split and unsplit sides of stack",
    ),
    Key([mod], "q", lazy.window.kill(), desc="Kill focused window"),
    Key([mod, "control"], "r", lazy.reload_config(), desc="Reload the config"),
    Key([mod, "control"], "q", lazy.shutdown(), desc="Shutdown Qtile"),
]

for index, _group in enumerate(groups):
    keyboard_number = str(index+1)
    keys.extend(
        [
            # mod1 + letter of group = switch to group
            Key([mod],keyboard_number,lazy.group[_group.name].toscreen(),desc="Switch to group {}".format(_group.name)),
            #mod1 + shift + letter of group = move focused window to group
            Key([mod, "shift"], keyboard_number, lazy.window.togroup(_group.name),desc="move focused window to group {}".format(_group.name)),
        ]
    )

USELESS_GAP = 10


layout_config = {
    "margin": USELESS_GAP,
    "border_width": 0
}

layouts = [
    layout.Tile(**layout_config),
    layout.Max(**layout_config),
    layout.MonadTall(**layout_config),
    layout.MonadWide(**layout_config),
]

widget_defaults = dict(
    font='fira code',
    fontsize=24,
    padding=5,
    background=theme.background,
    foreground=theme.foreground
)
extension_defaults = widget_defaults.copy()
SEP_ICON = ''

screens = [Screen(), Screen()]

# Drag floating layouts.
mouse = [
    Drag([mod], "Button1", lazy.window.set_position_floating(), start=lazy.window.get_position()),
    Drag([mod], "Button3", lazy.window.set_size_floating(), start=lazy.window.get_size()),
    Click([mod], "Button2", lazy.window.bring_to_front()),
]

dgroups_key_binder = None
dgroups_app_rules = []  # type: list
follow_mouse_focus = True
bring_front_click = False
cursor_warp = False
floating_layout = layout.Floating(
    float_rules=[
        # Run the utility of `xprop` to see the wm class and name of an X client.
        *layout.Floating.default_float_rules,
        Match(wm_class="confirmreset"),  # gitk
        Match(wm_class="makebranch"),  # gitk
        Match(wm_class="maketag"),  # gitk
        Match(wm_class="ssh-askpass"),  # ssh-askpass
        Match(title="branchdialog"),  # gitk
        Match(title="pinentry"),  # GPG key password entry
    ]
)
auto_fullscreen = True
focus_on_window_activation = "smart"
reconfigure_screens = True

# If things like steam games want to auto-minimize themselves when losing
# focus, should we respect this or not?
auto_minimize = True

wl_input_rules = None

# XXX: Gasp! We're lying here. In fact, nobody really uses or cares about this
# string besides java UI toolkits; you can see several discussions on the
# mailing lists, GitHub issues, and other WM documentation that suggest setting
# this string if your java app doesn't work correctly. We may as well just lie
# and say that we're a working one by default.
#
# We choose LG3D to maximize irony: it is a 3D non-reparenting WM written in
# java that happens to be on java's whitelist.
wmname = "LG3D"

