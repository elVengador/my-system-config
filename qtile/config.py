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

from libqtile.config import Key, Screen, Group, Drag, Click
from libqtile.lazy import lazy
from libqtile import layout, bar, widget, hook

from typing import List  # noqa: F401

from os import listdir,path
import subprocess

# AUTOSTART
@hook.subscribe.startup_once
def autostart():
    subprocess.call(["/home/el_vengador/.config/qtile/autostart.sh"])

# COLORS
colors={
	"primary":"#FF5C4D",
	"secondary":"#FF9636",
	"dark":"#382445",
	"light":"#FFCD58",
	"extra":"#DAD870"
}

# KEYS
mod = "mod4"
keys = [
    # Switch between windows in current stack pane
    Key([mod], "k", lazy.layout.down()),
    Key([mod], "j", lazy.layout.up()),

    # Move windows up or down in current stack
    Key([mod, "control"], "k", lazy.layout.shuffle_down()),
    Key([mod, "control"], "j", lazy.layout.shuffle_up()),

    # Switch window focus to other pane(s) of stack
    Key([mod], "space", lazy.layout.next()),

    # Swap panes of split stack
    Key([mod, "shift"], "space", lazy.layout.rotate()),

    # Toggle between split and unsplit sides of stack.
    # Split = all windows displayed
    # Unsplit = 1 window displayed, like Max layout, but still with
    # multiple stack panes
    Key([mod, "shift"], "Return", lazy.layout.toggle_split()),
    Key([mod], "Return", lazy.spawn("alacritty")),

    # Toggle between different layouts as defined below
    Key([mod], "Tab", lazy.next_layout()),
    Key([mod], "w", lazy.window.kill()),

    Key([mod, "control"], "r", lazy.restart()),
    Key([mod, "control"], "q", lazy.shutdown()),
    Key([mod], "r", lazy.spawncmd()),
]

# GROUPS
groups = [Group(i) for i in ["NET","DEV1","DEV2","FS","MEDIA","MISC"]]

for i in range(len(groups)):
    #cada workspace es identificado por un numero comenzando en 1
    actual_key=i+1
    keys.extend([
        # mod1 + letter of group = switch to group
        Key([mod], str(actual_key), lazy.group[groups[i].name].toscreen()),

        # mod1 + shift + letter of group = switch to & move focused window to group
        Key([mod, "shift"], str(actual_key), lazy.window.togroup(groups[i].name)),
        # Or, use below if you prefer not to switch to that group.
        # # mod1 + shift + letter of group = move focused window to group
        # Key([mod, "shift"], i.name, lazy.window.togroup(i.name)),
    ])

# LAYOUTS
layout_conf = {
    'border_focus':colors['secondary'],
    'border_width':2,
    'margin':2
}

layouts = [
    layout.Max(),
    #layout.Stack(num_stacks=2),
    # Try more layouts by unleashing below layouts.
    # layout.Bsp(),
    # layout.Columns(),
    # layout.Matrix(),
    layout.MonadTall(**layout_conf),
    layout.MonadWide(**layout_conf),
    # layout.RatioTile(),
    layout.Tile(**layout_conf),
    # layout.TreeTab(),
    # layout.VerticalTile(),
    # layout.Zoomy(),
]

widget_defaults = dict(
    font='sans',
    fontsize=12,
    padding=3,
)
extension_defaults = widget_defaults.copy()
fortune = "..."
# MOUSE CALLBACKS
def get_fortune(qtile):
    qtile.cmd_spawn('fortune')
def open_dolphin(qtile):
    qtile.cmd_spawn('dolphin')
def screenshoot_window(qtile):
    qtile.cmd_spawn('scrot -s')
def screenshoot(qtile):
    qtile.cmd_spawn('scrot')
def update(qtile):
    qtile.cmd_spawn('alacritty -e sudo pacman -Syu')
def htop(qtile):
    qtile.cmd_spawn('alacritty -e htop')
def open_albert(qtile):
    qtile.cmd_spawn('albert')

screens = [
    Screen(
        top=bar.Bar(
            [            
                # Current layout
                widget.TextBox("",fontsize=28,background=colors['secondary']),
                widget.CurrentLayout(background=colors['secondary']),
                # Groups
                widget.GroupBox(background=colors['primary']),
                # Terminal
                widget.Prompt(foreground=colors['extra']),
                # Window name
                widget.Sep(linewidth=4,background=colors['dark'],foreground=colors['dark']),
                widget.WindowName(background=colors['dark']),
                widget.Sep(linewidth=4,background=colors['dark'],foreground=colors['dark']),
                # Ethernet
                widget.Net(interface="enp4s0",background=colors['secondary'],format="{down} ↓↑ {up}"),
                widget.TextBox("",fontsize=28,background=colors['secondary']),
                # Memory
                widget.Memory(background=colors['primary']),
                widget.TextBox("",fontsize=28,background=colors['primary'],mouse_callbacks={'Button1':htop}),
                # Phrace
                widget.TextBox("理",fontsize=28,background=colors['secondary'],mouse_callbacks={'Button1':open_albert}),
                # Update
                widget.Pacman(background=colors['primary']),
                widget.TextBox("ﮮ",fontsize=28,background=colors['primary'],mouse_callbacks={'Button1':update}),
                # Screen shoot
                widget.TextBox("",fontsize=28,background=colors['secondary'],mouse_callbacks={'Button1':screenshoot}),
                widget.TextBox("",fontsize=28,background=colors['primary'],mouse_callbacks={'Button1':screenshoot_window}),
                # File Manager
                widget.TextBox("",fontsize=28,background=colors['secondary'],mouse_callbacks={'Button1':open_dolphin}),
                # Date
                widget.Clock(background=colors['primary'],format='%d-%m-%Y %a %I:%M %p'),
                widget.TextBox("",fontsize=28,background=colors['primary']),
                # Language
                widget.KeyboardLayout(background=colors['secondary'],configured_keyboards=['es','us'],padding_x=6)
            ],
            24,
        ),
    ),
]

dgroups_key_binder = None
dgroups_app_rules = []  # type: List
main = None
follow_mouse_focus = True
bring_front_click = False
cursor_warp = False
floating_layout = layout.Floating(float_rules=[
    # Run the utility of `xprop` to see the wm class and name of an X client.
    {'wmclass': 'confirm'},
    {'wmclass': 'dialog'},
    {'wmclass': 'download'},
    {'wmclass': 'error'},
    {'wmclass': 'file_progress'},
    {'wmclass': 'notification'},
    {'wmclass': 'splash'},
    {'wmclass': 'toolbar'},
    {'wmclass': 'confirmreset'},  # gitk
    {'wmclass': 'makebranch'},  # gitk
    {'wmclass': 'maketag'},  # gitk
    {'wname': 'branchdialog'},  # gitk
    {'wname': 'pinentry'},  # GPG key password entry
    {'wmclass': 'ssh-askpass'},  # ssh-askpass
])
auto_fullscreen = True
focus_on_window_activation = "smart"

# XXX: Gasp! We're lying here. In fact, nobody really uses or cares about this
# string besides java UI toolkits; you can see several discussions on the
# mailing lists, GitHub issues, and other WM documentation that suggest setting
# this string if your java app doesn't work correctly. We may as well just lie
# and say that we're a working one by default.
#
# We choose LG3D to maximize irony: it is a 3D non-reparenting WM written in
# java that happens to be on java's whitelist.
wmname = "LG3D"
