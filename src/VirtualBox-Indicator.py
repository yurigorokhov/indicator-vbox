#!/usr/bin/python

import gobject
import gtk
import appindicator
import commands
import os.path

# Check that VirtualBox and VBoxManage are installed correctly
def check_deps():
    # Make sure VirtualBox and VBoxManage exist
    if not os.path.exists("/usr/bin/VirtualBox"):
        sys.stderr.write('/usr/bin/VirtualBox was not found')
        exit(1)
    if not os.path.exists("/usr/bin/VBoxManage"):
        sys.stderr.write('/usr/bin/VBoxManage was not found')
        exit(1)

# Retrieve the names of the VM's
def get_vm_list():
    return commands.getoutput("VBoxManage list vms | sed -e 's/^.*\\\"\(.*\)\\\".*$/\\1/'").split('\n')

def update_menu(menu):
  # Get the list of VM's
  vm_list = get_vm_list()

  # Generate menu items for each VM
  for vm in vm_list:
    menu_items = gtk.MenuItem(vm)
    menu.append(menu_items)
    menu_items.connect("activate", launch_VM, vm)
    menu_items.show()

  menu_items = gtk.SeparatorMenuItem()
  menu.append(menu_items)
  menu_items.show()
  
  #  Virtual Box menu item
  menu_items = gtk.ImageMenuItem("Control Panel") 
  
  menu.append(menu_items)
  menu_items.connect("activate", launch_VBox)


  menu_items.show()

# Launch VirtualBox Control Panel
def launch_VBox(self):
    commands.getoutput("VirtualBox")
    
# Launch a VM by name
def launch_VM(self, vmname):
    commands.getoutput("VirtualBox --startvm \"" +vmname + "\"")

if __name__ == "__main__":
    
  check_deps()
  
  ind = appindicator.Indicator ("VirtualBox Indicator",
                              "VBox-gray",
                              appindicator.CATEGORY_APPLICATION_STATUS)
  ind.set_status (appindicator.STATUS_ACTIVE)
  ind.set_attention_icon ("VBox")

  # create menu
  menu = gtk.Menu()
  
  update_menu(menu)

  ind.set_menu(menu)

  gtk.main()


