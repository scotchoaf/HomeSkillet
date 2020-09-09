# Cortex Data Lake Enablement and Configuration Playbook

The playbook `cdl.yml` enables, configures, and validates CDL in a NGFW.

The CDL global configuration playbook will configure:

    * global CDL with EAL enabled including the region
    * configuration and system logs using CDL forwarding
    
    
The playbook can be run natively using Ansible, using the python script to also
ensure the associated roles/coleections are installed, or within panHandler.

> After completion of the playbook, administrators will need to create or
> update log forwarding profiles to use CDL with Enhanced Application Logging
> enabled. Aso ensure security policies are configured to use the log forwarding
> profiles.

### Prerequisites

    * NGFW using sw version 9.0.6 or later
    * Onboarding pre-shared key created in the Cortex Data Lake app
    * API access to the NGFW
    * Internet access allowing Ansible to clone git repositories
    * NGFW access to the Palo Alto Networks cloud platforms

### Running as a Skillet

The easiest way to run the playbook is using panHandler.

Input the preshared key and device information and panHandler will implement
the python virtual environment and run the playbook.

### Creating a Virtual Environment and Running the Python Script

The script is designed to run in a python virtual environment. Create/activate the
virtual environment and install packages listed in the requirements.txt file.

Example of creating the virtual environment called `env` from within the playbook
directory:

```angular2
python3 -m venv env
source env/bin/activate
pip install -r requirements.txt
```
Within the venv, run the python script with the preshared key and device IP and
credentials.

```angular2
python run_ansible_playbook.py -k {preshared key} -ip {device ip} -u {user} -p {password}
```

The user credentials are apped to a json dictionary call 'provider' used within
the ansible playbook.

### Running the Ansible Playbook Natively

The playbook can be run natively without python or as a skillet yet does assume
a python virtual environment is created to installed needed packages. Instructions
for creating the venv are shown in the prior section.

```angular2
ansible-playbook -i inventory.ini cdl.yml
```

> Before running update the preshared key and provider values in vars.yml
> or use the -e extra_vars input. Example syntax in the python file.


