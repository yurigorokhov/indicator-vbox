#!/bin/sh

INSTALL_DIR=/usr/local/bin

install ./images/* /usr/share/pixmaps/
install ./src/VirtualBox-Indicator.py $INSTALL_DIR/VirtualBox-Indicator
chmod +x $INSTALL_DIR/VirtualBox-Indicator
