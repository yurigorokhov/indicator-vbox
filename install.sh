#!/bin/sh

INSTALL_DIR=/usr/local/bin

if [ "$1" = "--uninstall" ]; then
	rm -r -f /usr/share/pixmaps/VBox-gray.png
	rm -r -f $INSTALL_DIR/indicator-vbox
	rm -r -f $INSTALL_DIR/VBox.pyc
else
	install -m 644 ./images/* /usr/share/pixmaps/
	install -m 644 ./src/indicator-vbox.py $INSTALL_DIR/indicator-vbox
	install -m 644 ./src/VBox.pyc $INSTALL_DIR/
	chmod +x $INSTALL_DIR/indicator-vbox
fi

