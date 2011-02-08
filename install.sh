#!/bin/sh

INSTALL_DIR=/usr/local/bin

install -m 644 ./images/* /usr/share/pixmaps/
install -m 644 ./src/indicator-vbox.py $INSTALL_DIR/indicator-vbox
install -m 644 ./src/VBox.pyc $INSTALL_DIR/
chmod +x $INSTALL_DIR/indicator-vbox
