#!/bin/bash

function CheckAPT(){
    which apt-get &> /dev/null
    if [[ $? -eq 0]]; then
        echo "DPKG package manager found"
        _Package="apt-get"
        echo "updating link to repository"
        eval "$_Package update"
        return 0
    else
        return 1
    fi
    
}
function CheckDNF(){
    which dnf &> /dev/null
    if [[ $? -eq 0]]; then
        echo "Dandified YUM package manager found"
        _Package="dnf"
        echo "updating link to repository"
        eval "$_Package clean all" 
        return 0
    else
        return 1
    fi
    
}
function CheckYUM(){
    which yum &> /dev/null
    if [[ $? -eq 0 && -z $_Package ]]; then
        echo "Yellowdog Updater Modified package manager found"
        _Package="yum"
        echo "updating link to repository"
        eval "$_Package clean all"
        return 0 
    else
        return 1
    fi
}

function LinuxInstallation() {
    echo "finding package manager"
    
    CheckAPT || CheckDNF || CheckYUM

    if [[ $? -gt 0]]; then
        echo "package manager not handled"
        return 1    
    fi
    
    env python3 --version &> /dev/null
    if [ $? -gt 0 ]; then
        echo "python not found --> installing python3"
        eval "$_Package -y install python3"
    fi
    
    echo "installing python package"
    eval "$_Package -y install python3-venv"
    
    return 0
}


function DarwinInstallation() {
    echo "not implemented yet"
    return 1
}

unameOut="$(uname -s)"
if [[ $unameOut == Darwin ]]; then
    echo "darwin"
    DarwinInstallation
elif [[ $unameOut == Linux ]]; then
    echo "linux detected"
    
    #if we have sudo priviledge, we exectue the function LinuxInstallation
    #else we request sudo priviledge only to install python and other essential package, then the script continue without the priviledge
    if [[ $EUID -eq 0 ]]; then
        LinuxInstallation
    else
      echo "resquesting sudo privilege to install/check essential package"
      sudo $0 TEMP
    fi
    
    if [[ $1 == TEMP ]] ; then
      echo "end of escalation"
      exit
    fi
    
    echo "generating a virtual environnement"
    mkdir ProjectEnvironnement &>/dev/null
    python3 -m venv ./ProjectEnvironnement
    ./ProjectEnvironnement/bin/python3 -m pip install --upgrade pip
    
    echo "installing dependancy"
    ./ProjectEnvironnement/bin/pip install click
    ./ProjectEnvironnement/bin/pip install flask

else
    echo "OS not recognised or handled by the script script : manual installation required" 1>&2s
    exit 1
fi