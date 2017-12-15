#!/usr/bin/env bash

declare -r remote_repo="https://github.com/alfredo-milani/ParseScript"
declare -r tmp_path="/dev/shm"
declare -r software_name="ParseScript"
declare -r desktop_entry="ParseScript/support/setup_scripts/linux/parsescript.desktop"
declare -r launcher_script="ParseScript/launchers/launcher_linux.sh"
declare -r desktop_entry_sys_path="/usr/share/applications"
declare -r software_sys_path="/opt"

echo "Questo script scaricherà l'ultima versione del tool ${software_name} e la installerà nel sistema."
echo -e "Continuare?\t[Yes / No]\n"
read choise

if [ "${choise}" == "Yes" ]; then
    echo "Download tool in ${tmp_path}. Attendere..."
    cd ${tmp_path}
    git clone ${remote_repo}

    echo "Creazione desktop entry"
    sudo chmod 0644 ${tmp_path}/${desktop_entry}
    sudo mv ${tmp_path}/${desktop_entry} ${desktop_entry_sys_path}

    echo "Spostamento ${software_name} in ${software_sys_path}"
    sudo chmod +x ${tmp_path}/${launcher_script}
    sudo mv ${tmp_path}/${software_name} ${software_sys_path}

    echo "Operazione completata. Riavviare il sistema o il Desktop Environment."
else
    echo "Nessuna operazione effettuata. Uscita."
fi

exit 0