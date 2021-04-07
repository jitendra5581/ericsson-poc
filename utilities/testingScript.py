from netmiko import ConnectHandler

# cisco_881 = {
#     'device_type': 'cisco_ios',
#     'host':   '10.10.10.2',
#     'username': 'admin',
#     'password': 'cisco',
#     "session_log": "output2.txt",
#     #'port' : 22,          # optional, defaults to 22
#     'secret': 'cisco',     # optional, defaults to ''
# }
cisco_881 = {
    'device_type': 'cisco_ios',
    'host':   '9.9.9.2',
    'username': 'admin',
    'password': 'cisco',
    #'port' : 22,          # optional, defaults to 22
    "session_log": "output.txt",
    'secret': 'cisco',     # optional, defaults to ''
}
net_connect = ConnectHandler(**cisco_881)
enable = net_connect.enable()
# show ip interface brief
# show run interface f0/0
# show run 
output = net_connect.send_command('show run interface f0/0')
print(output)