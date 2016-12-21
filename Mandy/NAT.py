


class NAT(object):
    def __init__(self, type):
        self.type = type

    def snat(self, interface, interface_index, priority):
        commandlist = list()
        commandlist.append("config snat out-interface %s %s priority %s"%(interface, interface_index, priority))
        return commandlist

    def dnat(self, classifier_index, description, protocol_type, dport):
        commandlist = list()
        commandlist.append("config add classifier %s"%(classifier_index))
        commandlist.append("config classifier %s description \"%s\""%(classifier_index, description))
        if protocol_type == "tcp" | "udp":
            commandlist.append("config classifier %s match ip protocol %s dport %s"%(classifier_index, protocol_type, dport))
        else:
            commandlist.append("config classifier %s match ip protocol %s"%(classifier_index, protocol_type))