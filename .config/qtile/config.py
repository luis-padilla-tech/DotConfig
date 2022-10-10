from libqtile import bar, layout, widget
from libqtile.config import Click, Drag, Group, Key, Match, Screen
from libqtile.lazy import lazy
from libqtile.utils import guess_terminal
from libqtile import qtile
from pathlib import Path
import time
import colors as my_themes
import random
import os
import subprocess

from libqtile.log_utils import logger
from libqtile import hook


theme = my_themes.Dracula

@hook.subscribe.startup_once
def on_start_of_qtile():
    loc = os.path.expanduser('~/.config/qtile/autorun.sh')
    subprocess.Popen([loc])


@hook.subscribe.startup
async def on_start_or_restart():
    logger.info(f"{theme} is the theme and {theme.wallpaper_directory} is the dir")
    if theme.wallpaper_directory is not None:

        wallpapers = [file for file in  Path(theme.wallpaper_directory).expanduser().iterdir()]
        wallpaper_path = random.choice(wallpapers)

        for screen in qtile.screens:
            screen.cmd_set_wallpaper(wallpaper_path,'fill')

mod = "mod4"
terminal = guess_terminal()

groups = [
    Group(name='home', label=''),
    Group(name='terminal', label='', matches=[
        Match(title='Alacritty'),
    ]),
    Group(name='browser', label='', matches=[
        Match(wm_class='firefox'),
    ]),
    Group(name='explorer', label=''),
    Group(name='code', label='', matches=[
        Match(wm_class='Code'),
    ]),
    Group(name='games', label=''),
]

keys = [

    # Switch between app windows
    Key([mod], "h", lazy.layout.left(), desc="Move focus to left"),
    Key([mod], "l", lazy.layout.right(), desc="Move focus to right"),
    Key([mod], "j", lazy.layout.down(), desc="Move focus down"),
    Key([mod], "k", lazy.layout.up(), desc="Miove focus up"),
    Key([mod], "space", lazy.layout.next(), desc="Move window focus to other window"),

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
    Key([mod], "n", lazy.layout.normalize(), desc="Reset all window sizes"),
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
    Key([mod], 'e', lazy.spawn(f'{terminal} -e ranger'), desc='Open File Explorer'),
    Key([mod], "Return", lazy.spawn(terminal), desc="Launch terminal"),
    Key([mod], "Tab", lazy.next_layout(), desc="Toggle between layouts"),
    Key([mod], "q", lazy.window.kill(), desc="Kill focused window"),
    Key([mod, "control"], "r", lazy.reload_config(), desc="Reload the config"),
    Key([mod, "control"], "q", lazy.shutdown(), desc="Shutdown Qtile"),
    Key([mod], "r", lazy.spawncmd(), desc="Spawn a command using a prompt widget"),
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
    fontsize=20,
    padding=3,
    background=theme.background,
    foreground=theme.foreground
)
extension_defaults = widget_defaults.copy()
SEP_ICON = ''

screens = [
    Screen(
        top=bar.Bar(
            [
                widget.GroupBox(highlight_method='block', disable_drag=True, active=theme.active, inactive=theme.inactive, block_highlight_text_color=theme.foreground),
                widget.Prompt(),
                widget.Spacer(length=bar.STRETCH),
                widget.Net(interface='enp0s3', prefix='M',format='{down}:{up}'),
                widget.TextBox(text=SEP_ICON),
                widget.CPU(format='{load_percent}%'),
                widget.TextBox(text=SEP_ICON),
                widget.Memory(measure_mem='G', format='{MemUsed:.2f}{mm}'),
                widget.TextBox(text=SEP_ICON),
                widget.Clock(format="%H:%M %m/%d/%Y"),
                widget.TextBox(text=SEP_ICON),
                widget.QuickExit(default_text='',countdown_format='{}'),
            ],
            24,
        ),
    ),
]

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

