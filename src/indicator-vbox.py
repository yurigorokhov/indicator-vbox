# This is a UI wrapper for VirtualBox that allows
# you to quickly start and stop VM's
#!/usr/bin/python

import gobject
import gtk
import appindicator
import commands
import os.path
import string
import time
import subprocess
import pynotify
import VBox

# Dictionary of menu items and their associated function
event_dict = {}

def launch_VM(self, vm, vbox):
    notify("Launching " + vm)
    ret_code = vbox.launch_VM(vm)
    if(ret_code != 0):
        notify("Error launching " + vm)
    
def suspend_VM(self, vm, vbox):
    notify("Suspending " + vm)
    ret_code = vbox.suspend_VM(vm)
    if(ret_code != 0):
        notify("Error suspending " + vm)
        
def suspend_all(self, vbox):
    notify("Suspending all virtual machines")
    ret_code = vbox.suspend_all_running()
    if(ret_code != 0):
        notify("Error suspending all virtual machines")
    
def launch_VBox(self, vbox):
    ret_code = vbox.launch_VBox()
    if(ret_code != 0):
        notify("Error launching VirtualBox")

# Check that VirtualBox and VBoxManage are installed correctly
def check_deps():
    if not os.path.exists("/usr/bin/VirtualBox"):
        error('/usr/bin/VirtualBox was not found')
    if not os.path.exists("/usr/bin/VBoxManage"):
        error('/usr/bin/VBoxManage was not found')

# Add VM to menu
def add_vm_menu(menu, vm, vbox):
    menu_items = gtk.MenuItem(vm)
    menu.append(menu_items)
    menu_items.show()
    # start
    if(vbox.is_vm_running(vm) == 0):
        menu_items = gtk.ImageMenuItem("Run")
        set_image(menu_items, "run")
        menu.append(menu_items)
        event_dict[vm] = menu_items.connect("activate", launch_VM, vm, vbox)
        menu_items.show()
    else:
        menu_items = gtk.ImageMenuItem("Suspend")
        set_image(menu_items, "suspend")
        menu.append(menu_items)
        event_dict[vm] = menu_items.connect("activate", suspend_VM, vm, vbox)
        menu_items.show()
        # separator
    menu_items = gtk.SeparatorMenuItem()
    menu.append(menu_items)
    menu_items.show()
    
# Remove VM from menu
def remove_vm_menu(menu, vm):
    remove_next_items = 0
    items = menu.get_children()
    for item in items:
        if(item.get_name() == "GtkMenuItem"):
            if(item.get_label() == vm):
                menu.remove(item)
                remove_next_items = 2
        else:
            if(remove_next_items > 0):
                menu.remove(item)
                remove_next_items -= 1

# sets the image of a menu item
def set_image(menu_item, image_type):
    if(image_type == "run"):
        stock = gtk.STOCK_MEDIA_PLAY
    elif(image_type == "suspend"):
        stock = gtk.STOCK_STOP
    else:
        stock = gtk.STOCK_EDIT
    img = gtk.image_new_from_stock(stock, gtk.ICON_SIZE_MENU)
    menu_item.set_image(img)
    img.show()

# update menu
def update_menu(menu, vbox, ind):
  vbox.update()
  
  is_running = 0
  previous_item = 0
  
  items = menu.get_children()
  for item in items:
      if(item.get_name() == "GtkMenuItem"):
          if(vbox.is_vm_running(item.get_label())):
              is_running = 1
	      are_any_running = 1
          else:
              is_running = 0
          previous_item = item
      else:
          if(is_running == 0 and item.get_label() == "Suspend"):
              item.set_label("Run")
              set_image(item, "run")
              item.disconnect(event_dict[previous_item.get_label()])
              event_dict[previous_item.get_label()] = item.connect("activate", launch_VM, previous_item.get_label(), vbox)
              
          elif(is_running == 1 and item.get_label() == "Run"):
              item.set_label("Suspend")
              set_image(item, "suspend")
              item.disconnect(event_dict[previous_item.get_label()])
              event_dict[previous_item.get_label()] = item.connect("activate", suspend_VM, previous_item.get_label(), vbox)
  ind.set_menu(menu)
    # remove VM's that do not exist anymore
  return (vbox.running_vms.__len__() != 0)

# Populates the Menu
def create_menu(menu, vbox, ind):
  # Get the list of VM's
  vm_list = vbox.get_vm_list()

  # Generate menu items for each VM
  for vm in vm_list:
    add_vm_menu(menu, vm, vbox)

  # Suspend all 
  menu_items = gtk.ImageMenuItem("Suspend All") 
  set_image(menu_items, "suspend")
  menu.append(menu_items)
  menu_items.connect("activate", suspend_all, vbox)
  menu_items.show()
  menu_items = gtk.SeparatorMenuItem()
  menu.append(menu_items)
  menu_items.show()
  
  #  VirtualBox Control Panel menu item
  menu_items = gtk.ImageMenuItem("Control Panel") 
  set_image(menu_items, "control panel")
  menu.append(menu_items)
  menu_items.connect("activate", launch_VBox, vbox)

  menu_items.show()
  ind.set_menu(menu)

# Display Error Message 
def error(msg):
    sys.stderr.write(msg)
    exit(1)

def notify(msg):
    n = pynotify.Notification("VirtualBox", msg, "VBox")
    n.show()

if __name__ == "__main__":
    
  check_deps()
  
  menu = gtk.Menu()
  
  vbox = VBox.VBox()
  
  ind = appindicator.Indicator ("VirtualBox Indicator",
                              "VBox-gray",
                              appindicator.CATEGORY_APPLICATION_STATUS)
  ind.set_status (appindicator.STATUS_ACTIVE)
  ind.set_attention_icon ("VBox")

  create_menu(menu, vbox, ind) 
  
  count = 0 
  while(True):
    gtk.main_iteration(False)
    if(count == 50):
      if( update_menu(menu, vbox, ind) == 1):
	   ind.set_status(appindicator.STATUS_ATTENTION)
      else:
	   ind.set_status(appindicator.STATUS_ACTIVE)
      count = 0
    count = count + 1
    time.sleep(0.05)
      
    


