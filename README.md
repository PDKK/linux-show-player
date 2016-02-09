# Linux Show Player [![GitHub version](https://badge.fury.io/gh/FrancescoCeruti%2Flinux-show-player.svg)](https://badge.fury.io/gh/FrancescoCeruti%2Flinux-show-player) [![Code Health](https://landscape.io/github/FrancescoCeruti/linux-show-player/master/landscape.svg?style=flat)](https://landscape.io/github/FrancescoCeruti/linux-show-player/master) [![Code Issues](https://www.quantifiedcode.com/api/v1/project/c419c19d00ce403a82f16a4505161e49/badge.svg)](https://www.quantifiedcode.com/app/project/c419c19d00ce403a82f16a4505161e49)
Linux Show Player (LiSP) - Sound player designed for stage productions

---

Every component on which LiSP relies (python3, GStreamer and Qt5) is multi-platform, but the program is currently tested and developed only for **GNU/Linux**.

No special hardware is required to run LiSP, but some processing operations would surely take benefit from a recent CPU.

For bugs/requests an issue can be open on the GitHub issues-tracker, any other question can be asked on the [user-group](https://groups.google.com/forum/#!forum/linux-show-player---users).

---

### Installation

####1. Package installation

**For Ubuntu/Debian users:** Download the ".deb" package in the releases page on GitHub (only tested on Ubuntu).

**For ArchLinux users:** there is an AUR Package.

####2. Manual Installation

#####2.1 Get the source

Download the archive from the release page on GitHub.

#####2.2 Install dependencies

*The following names are based on "Arch Linux" packages.*
<pre>
* python(3) >= 3.4
* python(3)-pyqt5
* python(3)-gobject
* python(3)-setuptools
* qt5-svg
* gstreamer 1.x
* gst-plugins-base
* gst-plugins-good
* gst-plugins-ugly
* gst-plugins-bad
* gst-libav				(optional, for larger format support)
* portmidi				(optional, for portmidi support)
* mido					(auto-installed via pip)
* python-rtmidi			(auto-installed via pip)
* JACK-Client			(auto-installed via pip)
* sortedcontainers      (auto-installed via pip)
* libasound-dev			(if installing in debian/ubuntu)
* libjack-jackd2-dev	(if installing in debian/ubuntu)
</pre>

#####2.3 Install LiSP

	# pip(3) install --pre <archive-name>

for example:
	
	# pip(3) install --pre linux-show-player-0.3.1.zip

### Usage

Use the installed launcher from the menu (for the package installation), or

	$ linux-show-player                                  # Launch the program
	$ linux-show-player -l [debug/warning/info]          # Launch with different log options
	$ linux-show-player -f <file/path>                   # Open a saved session

*Currently no user documentation is available.*
