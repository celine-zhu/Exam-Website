#!/bin/bash

function CheckAPT(){
    which apt-get &> /dev/null
    if [[ $? -eq 0 ]]; then
        echo "DPKG package manager found"
        _Package="apt-get"
        echo "updating link to repository"
        $_Package update
        return 0
    fi
	return 1  
}

function CheckDNF(){
    which dnf &> /dev/null
    if [[ $? -eq 0 ]]; then
        echo "Dandified YUM package manager found"
        _Package="dnf"
        echo "updating link to repository"
        $_Package clean all
        return 0
    fi
		return 1
}

function CheckYUM(){
    which yum &> /dev/null
    if [[ $? -eq 0 && -z $_Package ]]; then
        echo "Yellowdog Updater Modified package manager found"
        _Package="yum"
        echo "updating link to repository"
        $_Package clean all
        return 0 
    fi
    return 1
}

function LinuxInstallation() {
    echo "finding package manager"
    
    CheckAPT || CheckDNF || CheckYUM

    if [[ $? -gt 0 ]]; then
        echo "package manager not handled"
        return 1    
    fi
    
    env python3 --version &> /dev/null
    if [ $? -gt 0 ]; then
        echo "python not found --> installing python3"
        $_Package -y install python3
    fi
    
    echo "installing python package"
    $_Package -y install python3-venv
    $_Package -y install wkhtmltopdf
}


function DarwinInstallation() {
    echo "not implemented yet"
    exit 1
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
      sudo bash $0 TEMP
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
	#manque un module pour les fichier exel dans le requirements.txt
    source ./ProjectEnvironnement/bin/activate 
    pip3 install Flask 
    pip3 install Flask-Images
    pip3 install geopandas
    pip3 install pdfkit
    pip3 install click
    pip3 install openpyxl
    pip3 install matplotlib
    deactivate

else
    echo "OS not recognised or handled by the script script : manual installation required" 1>&2
    exit 1
fi