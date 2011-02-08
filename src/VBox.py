import commands
import subprocess

# VirtualBox Class to interface with the program
class VBox: 
    
    # list of running vm's
    running_vms = []
    # existing VM's
    existing_vms = []
    
    def __init__(self):
        self.update()
    
    # does vm exist?
    def exists(self, vm):
        return (self.existing_vms.count(vm) > 0)
    
    # Populate existing vms
    def populate_existing_vms(self):
        self.existing_vms = commands.getoutput("VBoxManage list vms | sed -e 's/^.*\\\"\(.*\)\\\".*$/\\1/'").split('\n')
    
    # Retrieve the names of installed VM's
    def get_vm_list(self):
        return self.existing_vms
    
    # populate list of running vms
    def populate_running_vms(self):
        del self.running_vms[:]
        for vm in self.get_vm_list():
            if(self.__vm_running(vm) == 1):
                self.running_vms.append(vm)
    
    # Check if a vm is running by querying running_vms[]
    def is_vm_running(self, vm):
        return (self.running_vms.count(vm) > 0)
    
    # Check if a vm is running
    def __vm_running(self, vmname):
        output = commands.getoutput("VBoxManage showvminfo \"" + vmname + "\" | grep State")
        if(output.count("running") > 0):
            return 1
        else:
            return 0  
    
    # Suspend all running vms
    def suspend_all_running(self):
        self.populate_running_vms()
        ret_code = 0
        for vm in self.running_vms:
            ret_code = self.suspend_VM(vm)
        return ret_code
    
    def launch_VBox(self):
        return subprocess.call(["VirtualBox"])
    
    # Suspend VM by name
    def suspend_VM(self, vmname):
        return subprocess.call(["VBoxManage", "controlvm", vmname,"savestate"])
        
    # Launch a VM by name
    def launch_VM(self, vmname):
        return subprocess.call(["VBoxManage", "startvm", vmname])
    
    # Update lists
    def update(self):
        self.populate_running_vms()
        self.populate_existing_vms()
        