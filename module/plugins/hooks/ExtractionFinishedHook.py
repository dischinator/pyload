# -*- coding: utf-8 -*-

from module.plugins.internal.Addon import Addon

import subprocess

class ExtractionFinishedHook(Addon):
    __name__    = "ExtractionFinishedHook"
    __type__    = "hook"
    __version__ = "0.03"
    __status__  = "testing"
    __config__ = [ ("activated" , "bool" , "Activated"  , "True" ) ]

    def init(self):
        self.event_map = {"package_extracted" : "postExtraction"}
        self.log_debug(_("Started."))

    def postExtraction(self, pyfile):
        self.log_debug(_("PostExtraction log message."))
        # fix permissions in extraction folder recursively
        CMD = ["chmod", "-R", "ug+rwX", "/storage/pool1/downloads" ]
        self.log_info("Fixing permissions...")
        self.log_debug(" ".join(CMD))
        subprocess.call(CMD)

        # remove empty folders in download folder
        self.log_info("Removing empty directories...")
        CMD = "rmdir /storage2/downloads/*"
        self.log_debug(CMD)
        subprocess.Popen(CMD, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        
        self.log_info("Moving known episodes...")
        CMD = "/usr/local/bin/move_serien.sh"
        self.log_debug(CMD)
        p = subprocess.Popen(CMD, stdout=subprocess.PIPE)
        for line in iter(p.stdout.readline, b''): self.log_info("Moved: "+line.rstrip()),
        p.wait()

        self.log_debug(_("PostExtraction hook done."))
