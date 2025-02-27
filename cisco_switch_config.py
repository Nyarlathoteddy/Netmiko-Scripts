from netmiko import ConnectHandler

def command_creator(ip,DS,nameport):
    """Create the commands for netmiko to run on a switch based off 
    of provided info + basic config needed for SSHv2"""

    user = "grotz"
    pw = "Penncollege1"
    name = 'n/a'
    if DS == 'dumb':
        name = f'IOU-{nameport}'
    elif DS == 'smart':
        name = input("Provide a hostname:")

    default_config = [
    'no spanning-tree vlan 1',
    'int vlan 1', 
    f'ip add {ip} 255.255.255.192',
    'no shut', 
    'exit', 
    'ip routing',
    f'hostname {name}',
    f'ip domain-name {name}',
    'ip default-gateway 10.175.134.193', 
    f'enable secret {pw}',
    'ip route 0.0.0.0 0.0.0.0 10.175.134.193', 
    'crypto key generate rsa modulus 2048', 
    'ip ssh version 2', 
    f"username {user} privilege 15 secret {pw}",
    'line vty 0 4',
    'transport input all',
    'login local',
    'end'
    ]

    final_array = default_config
    return final_array

USER_SETUP = "grotz"
PW_SETUP = "Penncollege1"
NETWORK = '10.175.134'
HOSTADDRESS = 200
dOrS = input("Dumb or smart config?")
outputQ = input("Do you want to see the output? Y/N")

# Dumb setup is with an array of ports, smart is interactive.
if dOrS == "smart":
    while True:
        question = input("Enter port or end to stop:")
        if question == "end":
            break
        print("Editing port: " + question)
        net_connect = ConnectHandler(
            device_type = "cisco_ios_telnet",
            host = "10.175.134.194",
            port = question,
            username = USER_SETUP,
            password = PW_SETUP,
            secret = PW_SETUP
        )
        # Creates IP for next switch based off of network
        # address and starting host address given before loop.
        IP = f'{NETWORK}.{HOSTADDRESS}'
        net_connect.enable()

        # Run command_creator function created earlier to create commands to send to switch.
        commands = command_creator(IP,dOrS,question)
        output = net_connect.send_config_set(commands)
        print(output)
        HOSTADDRESS += 1
elif dOrS == 'dumb':
    # Array of ports to configure.
    ports = ['5002', '5003', '5004', '5005', '5006']
    for p in ports:
        print("Editing port: " + p)
        net_connect = ConnectHandler(
            device_type = "cisco_ios_telnet",
            host = "10.175.134.194",
            port = p,
            username = USER_SETUP,
            password = PW_SETUP,
            secret = PW_SETUP
    )
        # Creates IP for next switch based off of network
        # address and starting host address given before loop.
        IP = f'{NETWORK}.{HOSTADDRESS}'
        net_connect.enable()

        # Run command_creator function created earlier to create commands to send to switch.
        commands = command_creator(IP,dOrS,p)
        output = net_connect.send_config_set(commands)
        if outputQ == 'Y':
            print(output)
        HOSTADDRESS += 1
