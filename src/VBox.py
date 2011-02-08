import commands
import subprocess

# VirtualBox Class to interface with the program
class VBox: 
    
    # list of running vm's
    running_vm = []
    
    def __init__(self):
        pass
    
    # Retrieve the names of installed VM's
    def get_vm_list(self):
        return commands.getoutput("VBoxManage list vms | sed -e 's/^.*\\\"\(.*\)\\\".*$/\\1/'").split('\n')
    
    # Check if a vm is running
    def is_vm_running(self, vmname):
        output = commands.getoutput("VBoxManage showvminfo \"" + vmname + "\" | grep State")
        if(output.count("running") > 0):
            return 1
        else:
            return 0  
    
    def launch_VBox(self):
        return subprocess.call(["VirtualBox"])
    
    # Suspend VM by name
    def suspend_VM(self, vmname):
        return subprocess.call(["VBoxManage", "controlvm", vmname,"savestate"])
        
    # Launch a VM by name
    def launch_VM(self, vmname):
        return subprocess.call(["VBoxManage", "startvm", vmname])
        