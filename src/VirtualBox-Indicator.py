import gobject
import gtk
import appindicator
import commands

def menuitem_response(w, buf):
  print buf

def get_vm_list():
    return commands.getoutput("VBoxManage list vms | sed -e 's/^.*\\\"\(.*\)\\\".*$/\\1/'").split('\n')

def update_menu(menu):
 # get the list of VM's
  vm_list = get_vm_list()
  print "List of Virtual Machines: %s" % vm_list

  for vm in vm_list:
    menu_items = gtk.MenuItem(vm)
    menu.append(menu_items)
    menu_items.show()

  menu_items = gtk.SeparatorMenuItem()
  menu.append(menu_items)
  menu_items.show()
  
  #  Virtual Box menu item
  menu_items = gtk.MenuItem("Launch VirtualBox")
  menu.append(menu_items)
  menu_items.connect("activate", launch_VBox)

  menu_items.show()

def launch_VBox(self):
    commands.getoutput("VirtualBox")

if __name__ == "__main__":

  ind = appindicator.Indicator ("VirtualBox Indicator",
                              "indicator-messages",
                              appindicator.CATEGORY_APPLICATION_STATUS)
  ind.set_status (appindicator.STATUS_ACTIVE)
  ind.set_attention_icon ("indicator-messages-new")

  # create menu
  menu = gtk.Menu()
  
  update_menu(menu)

  ind.set_menu(menu)

  gtk.main()


