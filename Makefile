INSTALL_DIR=/usr/local/bin
VERSION=1.3

install:
	install -m 644 ./images/* /usr/share/pixmaps/
	install -m 644 ./src/indicator-vbox.py ${INSTALL_DIR}/indicator-vbox
	install -m 644 ./src/VBox.pyc ${INSTALL_DIR}/
	chmod +x ${INSTALL_DIR}/indicator-vbox
	
uninstall:
	rm -r -f /usr/share/pixmaps/VBox-gray.png
	rm -r -f ${INSTALL_DIR}/indicator-vbox
	rm -r -f ${INSTALL_DIR}/VBox.pyc
	
dist:
	mkdir indicator-vbox
	cp -r -f Makefile TODO README src images screenshot.png indicator-vbox
	tar -c indicator-vbox > indicator-vbox-${VERSION}.tar
	gzip indicator-vbox-${VERSION}.tar
	rm -r -f indicator-vbox

clean:
	rm -r -f *.tar.gz 
