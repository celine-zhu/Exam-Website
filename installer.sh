#!/bin/bash

function LinuxInstallation() {
    env python3 --version &> /dev/null
    if [ $? -gt 0 ]; then
        echo "python non trouvé --> installation de python"
        echo "detection du package manager:"
        which apt-get &> /dev/null
        if [[ $? -eq 0 && -z $enc pyt   _Package ]]; then
            echo "DPKG package manager found"
            _Package="apt-get"
        fi
        which dnf &> /dev/null
        if [[ $? -eq 0 && -z $_Package ]]; then
            echo "Dandified YUM package manager found"
            _Package="dnf"
        fi
        which yum &> /dev/null
        if [[ $? -eq 0 && -z $_Package ]]; then
            echo "Yellowdog Updater Modified package manager found"
            _Package="yum"
        fi

        if [[ -z $_Package ]]; then
            echo "package manager not handled"
            return 1
        fi

        eval "$_Package install python3"


    fi
    mkdir ProjectEnvironnement &>/dev/null
    python3 -m venv ./ProjectEnvironnement
    ./ProjectEnvironnement/bin/python3 -m pip install --upgrade pip
    ./ProjectEnvironnement/bin/pip install click
    ./ProjectEnvironnement/bin/pip install flask
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
    echo "machine linux"
    if [[ $EUID -neq 0 ]]; then
        echo "resquesting sudo privilege"
        exec sudo $0
    fi
    LinuxInstallation
else
    echo "machine non reconnue ou nongérer par le script : installation manuel obligatoire"
fi






