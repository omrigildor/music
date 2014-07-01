import os
import sys
import subprocess

x = subprocess.Popen(["pfind", "afplay"]).returncode
print x, "please"