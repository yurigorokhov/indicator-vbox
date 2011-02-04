#!/usr/bin/python

import gobject
import gtk
import appindicator
import commands
import os.path
import string
import time
import thread
import subprocess

event_dict = {}

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

def is_vm_running(vmname):
    output = commands.getoutput("VBoxManage showvminfo \"" + vmname + "\" | grep State")
    if(output.count("running") > 0):
        return 1
    else:
        return 0  

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

def update_menu(menu):
  is_running = 0
  previous_item = 0
  for item in menu.get_children():
      if(item.get_name() == "GtkMenuItem"):
          if(is_vm_running(item.get_label())):
              is_running = 1;
          else:
              is_running = 0
          previous_item = item
      else:
          if(is_running == 0 and item.get_label() == "Suspend"):
              item.set_label("Run")
              set_image(item, "run")
              item.disconnect(event_dict[previous_item.get_label()])
              event_dict[previous_item.get_label()] = item.connect("activate", launch_VM, previous_item.get_label())
              
          elif(is_running == 1 and item.get_label() == "Run"):
              item.set_label("Suspend")
              set_image(item, "suspend")
              item.disconnect(event_dict[previous_item.get_label()])
              event_dict[previous_item.get_label()] = item.connect("activate", suspend_VM, previous_item.get_label())
              
def create_menu(menu, ind):
  # Get the list of VM's
  vm_list = get_vm_list()

  # Generate menu items for each VM
  for vm in vm_list:
    menu_items = gtk.MenuItem(vm)
    menu.append(menu_items)
    menu_items.show()
    # start
    if(is_vm_running(vm) == 0):
        menu_items = gtk.ImageMenuItem("Run")
        set_image(menu_items, "run")
        menu.append(menu_items)
        event_dict[vm] = menu_items.connect("activate", launch_VM, vm)
        menu_items.show()
    else:
        menu_items = gtk.ImageMenuItem("Suspend")
        set_image(menu_items, "suspend")
        menu.append(menu_items)
        event_dict[vm] = menu_items.connect("activate", suspend_VM, vm)
        menu_items.show()
    # separator
    menu_items = gtk.SeparatorMenuItem()
    menu.append(menu_items)
    menu_items.show()
  ind.set_menu(menu)

  #  Virtual Box menu item
  menu_items = gtk.ImageMenuItem("Control Panel") 
  set_image(menu_items, "control panel")
  menu.append(menu_items)
  menu_items.connect("activate", launch_VBox)

  menu_items.show()
  return menu

# Launch VirtualBox Control Panel
def launch_VBox(self):
    commands.getoutput("VirtualBox")
    
# Suspend VM by name
def suspend_VM(self, vmname):
    subprocess.Popen(["VBoxManage", "controlvm", vmname,"savestate"])
    
# Launch a VM by name
def launch_VM(self, vmname):
    subprocess.Popen(["VirtualBox", "--startvm", vmname])

if __name__ == "__main__":
    
  check_deps()
  
  menu = gtk.Menu()
  
  ind = appindicator.Indicator ("VirtualBox Indicator",
                              "VBox-gray",
                              appindicator.CATEGORY_APPLICATION_STATUS)
  ind.set_status (appindicator.STATUS_ACTIVE)
  ind.set_attention_icon ("VBox")

  create_menu(menu, ind) 

  while(True):
    gtk.main_iteration(False)
    update_menu(menu)
    #time.sleep(0.05)
      
    


