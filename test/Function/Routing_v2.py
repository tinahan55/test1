__author__ = 'mandy.wu'
from lib.Configuration import *
from lib.Device import *
import os
from time import gmtime, strftime
from lib.TelnetConsole import *

def device_check_info(logger, device, checkitem, checkcommand, checkmatch):
    title = "[%s][%s]" % (checkitem, checkcommand)
    logger.info("%s starting" % (title))
    checkresult = device.device_send_command_match(checkcommand, 5, checkmatch)
    logger.info("%s check %s result: %s" % (title, checkmatch, checkresult))
    if checkresult == False:
        logger.info("%s check %s error: %s" % (title, checkmatch, device.target_response))

def get_port_type(device, port_index_type1,port_index_type2):
    platform = device.device_get_response("show platform type")
    #Due to LMS's port type is different from DTS/STS, we get platform to decide port type
    if "DTS" in platform or "STS" in platform:
        port_index = port_index_type1
    else:
        port_index = port_index_type2

    return port_index

def get_cellular_type(device, cellular_index_type1,cellular_index_type2):
    platform = device.device_get_response("show platform type")
    #Due to LMS's port type is different from DTS/STS, we get platform to decide port type
    if "DTS" in platform or "LMS" in platform:
        cellular_index = cellular_index_type1
    else:
        cellular_index = cellular_index_type2

    return cellular_index

def client1_config(device):
    configlist = list()
    #set vlan
    vlan_index = 10
    vlan_description = "client1_vlan10"
    ip_mode = "static"
    ipaddress = "192.168.10.1"
    netmask = "255.255.255.0"
    # set port
    port_index_type1 = 1
    port_index_type2 = "2/1"
    port_type = "port"
    vlan_tagged = "untagged"
    port_tagged = "untagged"
    #set route
    route_type = "ip"
    route_mode = "default"
    gateway = "192.168.10.254"

    #get platform to decide port type
    port_index = get_port_type(device,port_index_type1,port_index_type2)

    function_client1 = Function("client1_vlan")
    configlist.extend(function_client1.get_vlan(vlan_index, vlan_description, ip_mode, ipaddress, netmask))
    configlist.extend(function_client1.get_route(route_type, route_mode, "", "", gateway, "", "", "", ""))
    interface_client1 = Interface("client1_port")
    configlist.extend(interface_client1.get_port_interface(port_index, port_type, vlan_index, vlan_tagged, port_tagged))

    device.device_set_configs(configlist)


    checkitem = "client1_config"
    checkcommandlist = ["show interface all", "show interface vlan %s detail"%(vlan_index)]
    checkitemlist = ["vlan %s" % (vlan_index), "IP address : %s" % (ipaddress)]
    logger.info("[%s]Starting" % (checkitem))
    for index, value in enumerate(checkcommandlist):
        checkmatch = checkitemlist[index]
        device_check_info(logger, device, checkitem, value, checkmatch)

def client2_config(device):
    configlist = list()
    # set vlan
    vlan_index = 20
    vlan_description = "client2_vlan10"
    ip_mode = "static"
    ipaddress = "192.168.20.1"
    netmask = "255.255.255.0"
    #set port
    port_index_type1 = 2
    port_index_type2 = "2/2"
    port_type = "port"
    vlan_tagged = "untagged"
    port_tagged = "untagged"
    # set route
    route_type = "ip"
    route_mode = "default"
    gateway = "192.168.20.254"
    # get platform to decide port type
    port_index = get_port_type(device, port_index_type1, port_index_type2)

    function_client2 = Function("client2_vlan")
    configlist.extend(function_client2.get_vlan(vlan_index, vlan_description, ip_mode, ipaddress, netmask))
    configlist.extend(function_client2.get_route(route_type, route_mode, "", "", gateway, "", "", "", ""))
    interface_client2 = Interface("client2_port")
    configlist.extend(interface_client2.get_port_interface(port_index, port_type, vlan_index, vlan_tagged, port_tagged))

    device.device_set_configs(configlist)

    checkitem = "client2_config"
    checkcommandlist = ["show interface all", "show interface vlan %s detail" % (vlan_index)]
    checkitemlist = ["vlan %s" % (vlan_index), "IP address : %s" % (ipaddress)]
    logger.info("[%s]Starting" % (checkitem))
    for index, value in enumerate(checkcommandlist):
        checkmatch = checkitemlist[index]
        device_check_info(logger, device, checkitem, value, checkmatch)

def server_set_vlan_port(device, server_maintenance_ip):
    configlist = list()
    # set vlan and port
    vlan_index_list = [10, 20]
    vlan_description_list = ["server_vlan10", "server_vlan20"]
    ip_mode = "static"
    ipaddress_list = ["192.168.10.254", "192.168.20.254"]
    netmask = "255.255.255.0"
    port_index_type1 = [1, 2]
    port_index_type2 = ["2/1", "2/2"]
    port_type = "port"
    vlan_tagged = "untagged"
    port_tagged = "untagged"

    # get platform to decide port type
    port_index = get_port_type(device, port_index_type1, port_index_type2)

    for index, vlan_index in enumerate(vlan_index_list):
        function = Function("server_vlan")
        configlist.extend(function.get_vlan(vlan_index, vlan_description_list[index], ip_mode, ipaddress_list[index], netmask))
        interface = Interface("server_port")
        configlist.extend(interface.get_port_interface(port_index[index], port_type, vlan_index_list[index], vlan_tagged,port_tagged))
        configlist.extend(interface.get_maintenance_interface(server_maintenance_ip, "255.255.255.0"))

        device.device_set_configs(configlist)

        # check config
        checkitem = "server_set_vlan_port"
        checkcommandlist = ["show interface all", "show interface vlan %s detail" % (vlan_index_list[index]),"show interface maintenance 0 brief"]
        checkitemlist = ["vlan %s" % (vlan_index_list[index]), "IP address : %s" % (ipaddress_list[index]),"IP address : %s"%(server_maintenance_ip)]
        logger.info("[%s]Starting" % (checkitem))
        for index, value in enumerate(checkcommandlist):
            checkmatch = checkitemlist[index]
            device_check_info(logger, device, checkitem, value, checkmatch)

def server_set_dialer(device):
    configlist = list()
    # profile and dialer
    profile_name = "LTE"
    access_name = "internet"
    dialer_index = 0
    cellular_index_1 = "0/1"
    cellular_index_2 = 0

    #Due to STS's celluar type is different from DTS/LMS, we get platform to decide celluar type
    cellular_index = get_cellular_type(device, cellular_index_1, cellular_index_2)

    profile = Profile("Profile")
    configlist.extend(profile.get_cellular_profile(profile_name, access_name))
    interface_dialer = Interface("server_dialer")
    configlist.extend(interface_dialer.get_dialer_interface(dialer_index, profile_name, cellular_index))

    device.device_set_configs(configlist)

    time.sleep(20)
    checkitem = "server_set_dialer"
    checkcommandlist = ["show interface all", "show interface dialer %s detail" % (dialer_index)]
    checkitemlist = ["dialer %s" % (dialer_index), "Operational : up"]
    logger.info("[%s]Starting" % (checkitem))
    for index, value in enumerate(checkcommandlist):
        checkmatch = checkitemlist[index]
        device_check_info(logger, device, checkitem, value, checkmatch)

def server_set_classifier(device):
    configlist = list()
    # classifier
    index_list = [10, 20]
    description_list = ["client1 to public network", "client2 to internal network"]
    ip_type = "source"
    protocol_type = ""
    port_mode = ""
    port_no = ""
    ip_address_list = ["192.168.10.0/24", "192.168.20.0/24"]

    for index, classifier_index in enumerate(index_list):
        classifier = Function("Classifier")
        configlist.extend(classifier.get_classifier(index_list[index], description_list[index], ip_type, protocol_type, port_mode, port_no, ip_address_list[index]))

        device.device_set_configs(configlist)

        # check_config
        checkitem = "server_set_classifier"
        checkcommandlist = ["show classifier %s" % (index_list[index])]
        checkitemlist = ["Classifier ID : %s" % (index_list[index])]
        logger.info("[%s]Starting" % (checkitem))
        for index, value in enumerate(checkcommandlist):
            checkmatch = checkitemlist[index]
            device_check_info(logger, device, checkitem, value, checkmatch)

def server_set_route_table(device):
    configlist = list()
    # route table
    route_type = "table"
    route_mode = "default "
    route_ip = ""
    route_netmask = ""
    gateway = ""
    interface = ""
    metric = ""
    table_index_list = [10, 20]
    classifier_index_list = [10, 20]
    priority_list = [1, 2]
    default_interface = ["dialer 0", "maintenance 0"]

    for index, table in enumerate(table_index_list):
        route = Function("Route")
        configlist.extend(route.get_route(route_type, route_mode, route_ip, route_netmask, gateway, interface, metric, table_index_list[index], default_interface[index]))
        configlist.extend(route.get_policy_route(classifier_index_list[index], table_index_list[index], priority_list[index]))

        device.device_set_configs(configlist)

        # check_config
        checkitem = "server_route_table"
        checkcommandlist = ["show route table all"]
        #checkitemlist = ["%s" % (table_index_list[index])]
        checkitemlist = ["%s(.*)0.0.0.0(.*)0.0.0.0(.*)0.0.0.0(.*)S" % (table_index_list[index])]
        logger.info("[%s]Starting" % (checkitem))
        for index, value in enumerate(checkcommandlist):
            checkmatch = checkitemlist[index]
            device_check_info(logger, device, checkitem, value, checkmatch)



def set_log(filename, loggername):
    logpath = os.path.join(os.getcwd(), 'log')
    if not os.path.exists(logpath):
        os.makedirs(logpath)
    filepath = os.path.join(logpath, filename)
    logger = logging.getLogger(loggername)
    logger.setLevel(logging.INFO)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s -%(message)s')
    fh = logging.FileHandler(filepath)
    fh.setLevel(logging.INFO)
    fh.setFormatter(formatter)
    logger.addHandler(fh)
    console = logging.StreamHandler()
    console.setLevel(logging.DEBUG)
    console.setFormatter(formatter)
    logger.addHandler(console)
    return logger

if __name__ == '__main__':

    logfilename = "Routing%s.log"%((strftime("%Y%m%d%H%M", gmtime())))
    logger = set_log(logfilename, "Routing_test")

    #connectType = "telnetConsole"
    #if connectType == "telnetConsole":
    #add paging command

    #We have 1 server and 2 clients in this architecture
    #server --> do routing work
    #client1 --> public route testing
    #client2 --> private route testing

    telnet_ip = "10.2.66.50"

    client1_port = 2035
    client2_port = 2040
    server_port = 2038
    server_maintenance_ip = "10.2.66.64"

    public_ping_ip = "8.8.8.8"
    private_ping_ip = "10.2.8.1"


    # set_up_device_config
    port_list = [client1_port, client2_port, server_port]
    for index, port in enumerate(port_list):
        device = Device_Tool(telnet_ip, port_list[index], "telnet", "admin", "admin", "Routing_test")
        if device:
            if port == client1_port:
                print "client1 connected"
                client1_config(device)
            elif port == client2_port:
                print "client2 connected"
                client2_config(device)
            elif port == server_port:
                print "server connected"
                device.device_send_command("update terminal paging disable")
                server_set_vlan_port(device, server_maintenance_ip)
                server_set_dialer(device)
                server_set_classifier(device)
                server_set_route_table(device)



    #routing_test
    telnet_port_list = [client1_port, server_port, client2_port, server_port]
    command_list = ["ping %s"%(public_ping_ip), "tcpdump -i usb1 icmp" ,"ping %s"%(private_ping_ip) ,"tcpdump -i eth0 icmp"]
    print "Routing test starting"
    for index, port in enumerate(telnet_port_list):
        TelnetConsole = Telnet_Console(telnet_ip, telnet_port_list[index],"admin", "admin", "Routing_test")
        TelnetConsole.login()
        if port == client1_port or port == client2_port:
            TelnetConsole.send_command("no config interface maintenance 0 enable", 5, "lilee", checkResponse="localdomain",logflag=True)
            TelnetConsole.send_command(command_list[index], 5, "lilee", checkResponse="localdomain", logflag=True)
        else:
            TelnetConsole.send_command(command_list[index], 5, "shell", checkResponse="bash-4.2#", logflag=True)
            time.sleep(1)
            if "%s: ICMP echo request"%(public_ping_ip) in TelnetConsole.telnetresult:
                print "public routing test successful"
            elif "%s: ICMP echo request"%(private_ping_ip) in TelnetConsole.telnetresult:
                print "private routing test successful"
            else:
                print "routing test fail"
            TelnetConsole.telnet.write(("\x03").encode('ascii'))

    #stop ping and tcpdump --> to be revised
    for index, port in enumerate(telnet_port_list):
        TelnetConsole = Telnet_Console(telnet_ip, telnet_port_list[index], "admin", "admin", "Routing_test")
        TelnetConsole.login()
        TelnetConsole.telnet.write(("\x03").encode('ascii'))





