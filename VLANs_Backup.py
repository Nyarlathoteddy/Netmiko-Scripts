from netmiko import ConnectHandler

NETWORK = '10.175.134'
HOSTADDRESS = 200
USER_SETUP = "grotz"
PW_SETUP = "Penncollege1"
TFTP_IP = '10.175.134.195'

config_commands = [
        'vlan 10',
        'vlan 20',
        'vlan 30',
        'vlan 40',
        'vlan 50',
        ]

for x in range(10):
        ip = f'{NETWORK}.{HOSTADDRESS}'
        net_connect = ConnectHandler(
        device_type = "cisco_ios",
        host = ip,
        username = USER_SETUP,
        password = PW_SETUP,
        secret = PW_SETUP,
        )
        file_Name = f"switch-{ip}"
        backup_Command = f'copy running-config tftp://{TFTP_IP}/{file_Name}.txt'
        
        net_connect.enable()
        output = net_connect.send_config_set(config_commands)
        print(output)
        #backup = net_connect.send_command_timing(backup_Command)
        #print(backup)
        result = net_connect.send_command_timing(backup_Command)
        print(result)
        if 'Address or name of remote host' in result:
                result += net_connect.send_command_timing('\n')
                print(result)
        if 'Destination filename' in result:
                result += net_connect.send_command('\n')
                print(result)
        HOSTADDRESS += 1
