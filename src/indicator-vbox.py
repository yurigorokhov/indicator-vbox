#!/usr/bin/python

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
# flag to update menu
menu_changed = False

def launch_VM(self, vm, vbox):
    notify("Launching " + vm)
    ret_code = vbox.launch_VM(vm)
    if(ret_code != 0):
        notify("Error launching " + vm)
    else:
        global menu_changed
        menu_changed = True
    
def suspend_VM(self, vm, vbox):
    notify("Suspending " + vm)
    ret_code = vbox.suspend_VM(vm)
    if(ret_code != 0):
        notify("Error suspending " + vm)
    else:
        global menu_changed
        menu_changed = True
        
def suspend_all(self, vbox):
    notify("Suspending all virtual machines")
    ret_code = vbox.suspend_all_running()
    if(ret_code != 0):
        notify("Error suspending all virtual machines")
    else:
        global menu_changed
        menu_changed = True
    
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

# Add VM to menu. If -1 is supplied for position, the last position will be used
def add_vm_menu(menu, vm, vbox, position, is_vm):
        menu_items = VBox.VBoxImageMenuItem(vm, is_vm)
        if(position <= -1):
            menu.append(menu_items)
        else:
            menu.insert(menu_items, position+1)
        if(vbox.is_vm_running(vm) == 0):
            menu_items.set_state(0)
            set_image(menu_items, "run")
            event_dict[vm] = menu_items.connect("activate", launch_VM, vm, vbox)
        else:
            menu_items.set_state(1)
            set_image(menu_items, "suspend")
            event_dict[vm] = menu_items.connect("activate", suspend_VM, vm, vbox)
        menu_items.show()
    
# Remove VM from menu
def remove_vm_menu(menu, vm):
    items = menu.get_children()
    for item in items:
        if(item.get_label() == vm):
            menu.remove(item)
     
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
  global menu_changed
  menu_changed = False
  vbox.update()
  is_running = 0
  remove_list = []
  vm_list = []
  
  items = menu.get_children()
  for item in items:
      if(item.get_name() == "VBoxImageMenuItem" and item.is_vm):
          # Check if VM still exists
          if(vbox.exists(item.get_label()) == False):
              remove_list.append(item.get_label())
          else:
              vm_list.append(item.get_label())
          if(vbox.is_vm_running(item.get_label())):
              if(item.get_state() == 0):
                  item.set_state(1)
                  set_image(item, "suspend")
                  item.disconnect(event_dict[item.get_label()])
                  event_dict[item.get_label()] = item.connect("activate", suspend_VM, item.get_label(), vbox)
          elif(item.get_state() == 1):
              item.set_state(0)
              set_image(item, "run")
              item.disconnect(event_dict[item.get_label()])
              event_dict[item.get_label()] = item.connect("activate", launch_VM, item.get_label(), vbox)
     
  # Remove deleted VM's
  for vm in remove_list:
      remove_vm_menu(menu, vm)
  # TODO Must be added in the correct place
  # Add new VM's to menu
  for vm in vbox.existing_vms:
      if(vm_list.count(vm) < 1):
        add_vm_menu(menu, vm, vbox, vm_list.__len__()-1, True)
  
  ind.set_menu(menu)
    # remove VM's that do not exist anymore
  return (vbox.running_vms.__len__() != 0)

# Populates the Menu
def create_menu(menu, vbox, ind):
  # Get the list of VM's
  vm_list = vbox.get_vm_list()

  # Generate menu items for each VM
  for vm in vm_list:
    add_vm_menu(menu, vm, vbox, -1, True)

  # Suspend all 
  menu_items = gtk.SeparatorMenuItem()
  menu.append(menu_items)
  menu_items.show()
  menu_items = VBox.VBoxImageMenuItem("Suspend All", False) 
  set_image(menu_items, "suspend")
  menu.append(menu_items, )
  menu_items.connect("activate", suspend_all, vbox)
  menu_items.show()
  menu_items = gtk.SeparatorMenuItem()
  menu.append(menu_items)
  menu_items.show()
  
  #  VirtualBox Control Panel menu item
  menu_items = VBox.VBoxImageMenuItem("Control Panel", False) 
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
    if(menu_changed == True or count == 500):
      if( update_menu(menu, vbox, ind) == 1):
	   ind.set_status(appindicator.STATUS_ATTENTION)
      else:
	   ind.set_status(appindicator.STATUS_ACTIVE)
      count = 0
    count = count + 1
    time.sleep(0.05)
      
    


