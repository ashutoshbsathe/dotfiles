# Copyright (c) 2010 Aldo Cortesi
# Copyright (c) 2010, 2014 dequis
# Copyright (c) 2012 Randall Ma
# Copyright (c) 2012-2014 Tycho Andersen
# Copyright (c) 2012 Craig Barnes
# Copyright (c) 2013 horsik
# Copyright (c) 2013 Tao Sauvage
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

import os 
import subprocess

from typing import List  # noqa: F401

from libqtile import bar, layout, widget, hook
from libqtile.config import Click, Drag, Group, Key, Match, Screen
from libqtile.lazy import lazy
from libqtile.utils import guess_terminal

mod = "mod4"
# terminal = guess_terminal()
my_term = "alacritty"
my_browsers = ["firefox", "google-chrome-stable -incognito"]
# Could send a notification with `notify-send`
screenshot_cmd = 'scrot -q 100 /home/ashutosh/Pictures/screenshots/%Y-%m-%d_%H:%M:%S.jpg'

keys = [
    # Switch between windows
    Key([mod], "h", lazy.layout.left(), desc="Move focus to left"),
    Key([mod], "l", lazy.layout.right(), desc="Move focus to right"),
    Key([mod], "j", lazy.layout.down(), desc="Move focus down"),
    Key([mod], "k", lazy.layout.up(), desc="Move focus up"),
    Key([mod], "space", lazy.layout.next(),
        desc="Move window focus to other window"),

    # Move windows between left/right columns or move up/down in current stack.
    # Moving out of range in Columns layout will create new column.
    Key([mod, "shift"], "h", lazy.layout.shuffle_left(),
        desc="Move window to the left"),
    Key([mod, "shift"], "l", lazy.layout.shuffle_right(),
        desc="Move window to the right"),
    Key([mod, "shift"], "j", lazy.layout.shuffle_down(),
        desc="Move window down"),
    Key([mod, "shift"], "k", lazy.layout.shuffle_up(), desc="Move window up"),

    # Grow windows. If current window is on the edge of screen and direction
    # will be to screen edge - window would shrink.
    Key([mod, "control"], "h", lazy.layout.grow_left(),
        desc="Grow window to the left"),
    Key([mod, "control"], "l", lazy.layout.grow_right(),
        desc="Grow window to the right"),
    Key([mod, "control"], "j", lazy.layout.grow_down(),
        desc="Grow window down"),
    Key([mod, "control"], "k", lazy.layout.grow_up(), desc="Grow window up"),
    Key([mod], "n", lazy.layout.normalize(), desc="Reset all window sizes"),
    # For XMonad like layouts 
    Key([mod, "control"], "d", lazy.layout.shrink()),
    Key([mod, "control"], "i", lazy.layout.grow()),
    Key([mod], "space", lazy.layout.flip()),

    # Toggle between split and unsplit sides of stack.
    # Split = all windows displayed
    # Unsplit = 1 window displayed, like Max layout, but still with
    # multiple stack panes
    Key([mod], "Return", lazy.layout.toggle_split(),
        desc="Toggle between split and unsplit sides of stack"),
    Key([mod, "shift"], "t", lazy.spawn(my_term), desc="Launch terminal"),

    # Toggle between different layouts as defined below
    Key([mod], "Tab", lazy.next_layout(), desc="Toggle between layouts"),
    Key([mod, "shift"], "c", lazy.window.kill(), desc="Kill focused window"),

    Key([mod, "control"], "r", lazy.restart(), desc="Restart Qtile"),
    Key([mod, "control"], "q", lazy.shutdown(), desc="Shutdown Qtile"),
    Key([mod, "shift"], "r", lazy.spawncmd(),
        desc="Spawn a command using a prompt widget"),
    Key([mod], "r", lazy.spawn("dmenu_run -p 'dmenu >'"), desc="Run launcher"),
    Key([mod], "w", lazy.spawn(my_browsers[0]), desc="Normal browser"),
    Key([mod, "shift"], "w", lazy.spawn(my_browsers[1]), desc="Incognito browser"),
    Key([mod, "shift"], "p", lazy.spawn(screenshot_cmd), desc='Take a screenshot'),

]

groups = [Group(i) for i in "123456789"]

for i in groups:
    keys.extend([
        # mod1 + letter of group = switch to group
        Key([mod], i.name, lazy.group[i.name].toscreen(),
            desc="Switch to group {}".format(i.name)),

        # mod1 + shift + letter of group = switch to & move focused window to group
        Key([mod, "shift"], i.name, lazy.window.togroup(i.name, switch_group=True),
            desc="Switch to & move focused window to group {}".format(i.name)),
        # Or, use below if you prefer not to switch to that group.
        # # mod1 + shift + letter of group = move focused window to group
        # Key([mod, "shift"], i.name, lazy.window.togroup(i.name),
        #     desc="move focused window to group {}".format(i.name)),
    ])

my_green = '#094507'
my_blue = '#202734'

layouts = [
    # layout.Columns(border_focus_stack=['#d75f5f', '#8f3d3d'], border_width=4),
    # Try more layouts by unleashing below layouts.
    # layout.Stack(num_stacks=2),
    # layout.Bsp(),
    # layout.Matrix(),
    layout.MonadTall(border_focus=my_green, margin=4),
    layout.MonadWide(border_focus=my_green, margin=4),
    layout.Max(border_focus=my_green),
    layout.Floating(border_focus=my_green),
    # layout.Tile(),
    # layout.TreeTab(),
    # layout.VerticalTile(),
    # layout.Zoomy(),
]

widget_defaults = dict(
    # font='Nimbus Sans, sans',
    font='FiraCode Sans Mono',
    fontsize=14,
    padding=3
)
extension_defaults = widget_defaults.copy()

powerline_left_sep = ''
powerline_right_sep = ''
powerline_fontsize = 25
powerline_font = 'FiraCode Sans Mono'
powerline_padding = 0

screens = [
    Screen(
        top=bar.Bar(
            [
                widget.GroupBox(
                    background=my_blue,
                    borderwidth=0,
                    highlight_method='block'
                ),
                widget.CurrentLayoutIcon(
                    background=my_blue,
                ),
                widget.Prompt(),
                widget.WindowName(),
                widget.Spacer(),
                widget.TextBox(
                    text=powerline_left_sep,
                    font=powerline_font,
                    fontsize=powerline_fontsize,
                    foreground=my_green,
                    padding=powerline_padding
                ),
                widget.Image(
                    filename='~/.config/qtile/icons/arrow-up.png',
                    margin=5,
                    padding=0,
                    background=my_green,
                ),
                widget.Net(format='{up}', background=my_green),
                widget.Image(
                    filename='~/.config/qtile/icons/arrow-down.png',
                    margin=5,
                    padding=0,
                    background=my_green,
                ),
                widget.Net(format='{down}  ', background=my_green),
                widget.TextBox(
                    text=powerline_left_sep,
                    font=powerline_font,
                    fontsize=powerline_fontsize,
                    foreground=my_blue,
                    background=my_green,
                    padding=powerline_padding
                ),
                widget.Image(
                    filename='~/.config/qtile/icons/cpu.png',
                    margin=5,
                    background=my_blue 
                ),
                widget.CPU(format='{load_percent}%  ', background=my_blue),
                widget.TextBox(
                    text=powerline_left_sep,
                    font=powerline_font,
                    fontsize=powerline_fontsize,
                    foreground=my_green,
                    background=my_blue,
                    padding=powerline_padding
                ),
                widget.Image(
                    filename='~/.config/qtile/icons/pie-chart.png',
                    margin=5,
                    background=my_green
                ),
                widget.Memory(format='{MemUsed: .0f}{mm}  ', background=my_green),
                widget.TextBox(
                    text=powerline_left_sep,
                    font=powerline_font,
                    fontsize=powerline_fontsize,
                    foreground=my_blue,
                    background=my_green,
                    padding=powerline_padding 
                ),
                widget.Image(
                    filename='~/.config/qtile/icons/nvidia-10.png',
                    margin=3,
                    background=my_blue,
                ),
                widget.NvidiaSensors(format='{temp}°C/{fan_speed}RPM/{perf}  ', background=my_blue),
                widget.TextBox(
                    text=powerline_left_sep,
                    font=powerline_font,
                    fontsize=powerline_fontsize,
                    foreground=my_green,
                    background=my_blue,
                    padding=powerline_padding
                ),
                widget.Image(
                    filename='~/.config/qtile/icons/calendar.png',
                    margin=5,
                    background=my_green
                ),
                widget.Clock(format='%Y %b %d %a %I:%M %p  ', background=my_green),
                widget.TextBox(
                    text=powerline_left_sep,
                    font=powerline_font,
                    fontsize=powerline_fontsize,
                    foreground=my_blue,
                    background=my_green,
                    padding=powerline_padding
                ),
                widget.Systray(
                    background=my_blue
                ),
            ],
            24,
        ),
    ),
]

# Drag floating layouts.
mouse = [
    Drag([mod], "Button1", lazy.window.set_position_floating(),
         start=lazy.window.get_position()),
    Drag([mod], "Button3", lazy.window.set_size_floating(),
         start=lazy.window.get_size()),
    Click([mod], "Button2", lazy.window.bring_to_front()),
    Click([mod, "shift"], "Button1", lazy.window.toggle_floating()),
]

dgroups_key_binder = None
dgroups_app_rules = []  # type: List
follow_mouse_focus = True
bring_front_click = False
cursor_warp = False
floating_layout = layout.Floating(float_rules=[
    # Run the utility of `xprop` to see the wm class and name of an X client.
    *layout.Floating.default_float_rules,
    Match(wm_class='confirmreset'),  # gitk
    Match(wm_class='makebranch'),  # gitk
    Match(wm_class='maketag'),  # gitk
    Match(wm_class='ssh-askpass'),  # ssh-askpass
    Match(title='branchdialog'),  # gitk
    Match(title='pinentry'),  # GPG key password entry
])
auto_fullscreen = True
focus_on_window_activation = "smart"
reconfigure_screens = True

# If things like steam games want to auto-minimize themselves when losing
# focus, should we respect this or not?
auto_minimize = True

# XXX: Gasp! We're lying here. In fact, nobody really uses or cares about this
# string besides java UI toolkits; you can see several discussions on the
# mailing lists, GitHub issues, and other WM documentation that suggest setting
# this string if your java app doesn't work correctly. We may as well just lie
# and say that we're a working one by default.
#
# We choose LG3D to maximize irony: it is a 3D non-reparenting WM written in
# java that happens to be on java's whitelist.
wmname = "LG3D"

@hook.subscribe.startup_once
def autostart():
    home = os.path.expanduser('~/.config/qtile/autostart.sh')
    subprocess.call([home])
