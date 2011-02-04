#!/bin/sh

INSTALL_DIR=/usr/local/bin

install -m 644 ./images/* /usr/share/pixmaps/
install -m 644 ./src/VirtualBox-Indicator.py $INSTALL_DIR/VirtualBox-Indicator
chmod +x $INSTALL_DIR/VirtualBox-Indicator
