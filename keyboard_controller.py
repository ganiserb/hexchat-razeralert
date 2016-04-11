#!/usr/bin/env python3
# coding=utf-8
import razer.daemon_dbus
import razer.profiles
import sys

daemon = razer.daemon_dbus.DaemonInterface()
profiles = razer.profiles.ChromaProfiles(daemon)

action = sys.argv[1]

if action == 'blink':
    daemon.set_effect('wave', 1)
elif action == 'normal':
    profiles.activate_profile_from_file('gabriel')
