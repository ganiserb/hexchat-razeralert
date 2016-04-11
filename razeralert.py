#!/usr/bin/env python3
import hexchat
import os
import subprocess
from threading import Thread

__module_name__ = "Blinking Razer Keyboard"
__module_version__ = "0.1"
__module_description__ = "Whenever an alert is triggered a command is issued to" \
                         "make a Razer Keyboard blink until the alert is dismissed " \
                         "by focusing on the Hexchat window. " \
                         "This plugin is based on SoundAlert plugin: " \
                         "https://github.com/hexchat/hexchat-addons/blob/master/python/sound-alert/soundalert.py " \
                         "by NoiSek."

# TODO: rename commands and change descriptions
#       call the right commands

class RazerAlert():
    def __init__(self):
        hexchat.prnt("Razer Alert plugin loaded.")

        if hexchat.get_pluginpref("razeralert_active") is None:
            hexchat.set_pluginpref("razeralert_active", True)

        if not hexchat.get_pluginpref("razeralert_active"):
            hexchat.prnt("Alerts are currently disabled. Re-enable them with /alertson")

    def disable(self, word, word_eol, userdata):
        hexchat.prnt("Sound alerts will now be off until you enable them again with /alertson.")
        hexchat.set_pluginpref("razeralert_active", False)

    def enable(self, word, word_eol, userdata):
        hexchat.prnt("Sound alerts are now on.")
        hexchat.set_pluginpref("razeralert_active", True)

    def set_options(self, word, word_eol, userdata):
        if len(word) < 3:
            hexchat.prnt("Not enough arguments given. See /help soundalert")

        else:
            if word[1] == "set":
                if os.path.isdir(word_eol[1]):
                    hexchat.set_pluginpref("soundalert_dir", word_eol[1])

                else:
                    hexchat.prnt("Not a valid directory.")

        return hexchat.EAT_ALL

    def handle_stop_blinking(self):
        subprocess.call(['/home/gabriel/dev/hexchat-razeralert/keyboard_controller.py', 'normal'])

    def handle_start_blinking(self):
        if hexchat.get_prefs('away_omit_alerts') and hexchat.get_info('away'):
            return

        if hexchat.get_prefs('gui_focus_omitalerts') and \
           hexchat.get_info('win_status') == 'active':
            return

        active = hexchat.get_pluginpref("razeralert_active")

        if not active:
            return False

        subprocess.call(['/home/gabriel/dev/hexchat-razeralert/keyboard_controller.py', 'blink'])

    def start_blinking(self, word, word_eol, userdata):
        do_thread = Thread(target=self.handle_start_blinking)
        do_thread.start()

    def stop_blinking(self, word, word_eol, userdata):
        do_thread = Thread(target=self.handle_stop_blinking)
        do_thread.start()

alert = RazerAlert()

hexchat.hook_command("soundalert", alert.set_options, help="/soundalert set <directory> -- Sets a directory for Sound Alert to pull sounds from.")
hexchat.hook_command("alertson", alert.enable, help="Turns on soundalert alerts.")
hexchat.hook_command("alertsoff", alert.disable, help="Turns off soundalert alerts.")
hexchat.hook_print("Channel Action Hilight", alert.start_blinking)
hexchat.hook_print("Channel Msg Hilight", alert.start_blinking)
hexchat.hook_print("Private Message", alert.start_blinking)
hexchat.hook_print("Focus Window", alert.stop_blinking)
