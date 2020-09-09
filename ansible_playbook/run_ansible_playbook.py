#!/usr/bin/env python3
# Copyright (c) 2020, Palo Alto Networks
#
# Permission to use, copy, modify, and/or distribute this software for any
# purpose with or without fee is hereby granted, provided that the above
# copyright notice and this permission notice appear in all copies.
#
# THE SOFTWARE IS PROVIDED "AS IS" AND THE AUTHOR DISCLAIMS ALL WARRANTIES
# WITH REGARD TO THIS SOFTWARE INCLUDING ALL IMPLIED WARRANTIES OF
# MERCHANTABILITY AND FITNESS. IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR
# ANY SPECIAL, DIRECT, INDIRECT, OR CONSEQUENTIAL DAMAGES OR ANY DAMAGES
# WHATSOEVER RESULTING FROM LOSS OF USE, DATA OR PROFITS, WHETHER IN AN
# ACTION OF CONTRACT, NEGLIGENCE OR OTHER TORTIOUS ACTION, ARISING OUT OF
# OR IN CONNECTION WITH THE USE OR PERFORMANCE OF THIS SOFTWARE.

# Authors: Scott Shoaf, Nathan Embery

import json
from subprocess import PIPE, Popen

import click


@click.command()
@click.option("-ip", "--TARGET_IP", help="device IP address", type=str, default='')
@click.option("-u", "--TARGET_USERNAME", help="API username", type=str, default='admin')
@click.option("-p", "--TARGET_PASSWORD", help="API password", type=str, default='Paloalto1')
def cli(target_ip, target_username, target_password):
    """
    run ansible playbook for global Cortex Data Lake configuration
    :param cdl_preshared_key: firewall onboarding PreShared_Key for Cortex Data Lake
    :param TARGET_IP: part of the provider defining device to configure
    :param TARGET_USERNAME: username to access the device
    :param TARGET_PASSWORD: password to access the device
    :return: None
    """

    # install ansible panos role
    try:
        print('install PaloAltoNetworks.paloaltonetworks role')
        install_panos = Popen('ansible-galaxy install -c -f PaloAltoNetworks.paloaltonetworks', shell=True, stdout=PIPE,
                              stderr=PIPE)
        stdout, stderr = install_panos.communicate()
        # if ERROR in output message then raise to force except
        if 'ERROR' in stderr.decode('ascii'):
            raise ValueError(stderr.decode('ascii'))
            # create WARNING output if already installed
        elif 'WARNING' in stderr.decode('ascii'):
            print(stderr.decode('ascii'))
        print(stdout.decode('ascii'))
        install_panos.wait()
    except ValueError as err:
        print(err.args)
        exit(1)

    # install ansible skillet player collection
    try:
        print('install nembery.skillets collection as skillet player')
        install_panos = Popen('ansible-galaxy collection install -c -f nembery.skillet', shell=True, stdout=PIPE,
                              stderr=PIPE)
        stdout, stderr = install_panos.communicate()
        # if ERROR in output message then raise to force except
        if 'ERROR' in stderr.decode('ascii'):
            raise ValueError(stderr.decode('ascii'))
        # create WARNING output if already installed
        elif 'WARNING' in stderr.decode('ascii'):
            print(stderr.decode('ascii'))
        print(stdout.decode('ascii'))
        install_panos.wait()
    except ValueError as err:
        print(err.args)
        exit(1)

    # create a simple provider dict to convert to json and pass as ansible extra-var
    provider_dict = {}
    provider_dict['provider'] = {}
    provider_dict['provider']['ip_address'] = target_ip
    provider_dict['provider']['username'] = target_username
    provider_dict['provider']['password'] = target_password
    xvar_provider = json.dumps(provider_dict)

    print(f'configuring device {target_ip} as user {target_username}\n')

    # ansible command line entry with extra vars
    playbook_cmd = f'ansible-playbook -i inventory.ini homeskillet_playbook.yml' \
                   f' -e "{xvar_provider}"'

    # run the playbook and wait until complete
    run_playbook = Popen(playbook_cmd, shell=True)
    run_playbook.wait()


if __name__ == '__main__':
    cli()
