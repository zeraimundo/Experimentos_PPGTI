#!/usr/bin/env python

from mininet.topo import Topo
from mininet.net import Mininet
from mininet.node import Node  
from mininet.log import setLogLevel, info
from mininet.cli import CLI
from mininet.link import TCLink
from mininet.link import Intf


class LinuxRouter(Node):
    "A Node with IP forwarding enabled."

    def config(self, **params):
        super(LinuxRouter, self).config(**params)
        # Enable forwarding on the router
        self.cmd('sysctl net.ipv4.ip_forward=1')

    def terminate(self):
        self.cmd('sysctl net.ipv4.ip_forward=0')
        super(LinuxRouter, self).terminate()

class NetworkTopo(Topo):
    "A network topology with three routers and four hosts."

    def build(self, **_opts):
        # Add routers
#        r1 = self.addNode('r1', cls=LinuxRouter, ip='10.0.1.1/24')
      #  r2 = self.addNode('r2', cls=LinuxRouter, ip='10.0.2.2/24')
      #  r3 = self.addNode('r3', cls=LinuxRouter, ip='10.0.3.1/24')

        r1 = self.addNode('r1', cls=LinuxRouter)
        r2 = self.addNode('r2', cls=LinuxRouter)
        r3 = self.addNode('r3', cls=LinuxRouter)

        s1, s2= [ self.addSwitch( s ) for s in ( 's1','s2' )]

        
        # Add hosts
        h1 = self.addHost('h1', ip='10.0.1.100/24', defaultRoute='via 10.0.1.1')
        h2 = self.addHost('h2', ip='10.0.4.100/24', defaultRoute='via 10.0.4.1')

        enlace = {'cls': TCLink, 'bw': 1000}

        # Add links between routers
        self.addLink(r1, r2, intfName1='r1-eth2', intfName2='r2-eth1', **enlace)
        self.addLink(r2, r3, intfName1='r2-eth2', intfName2='r3-eth2', **enlace)

        # Add links between routers and switchs
        self.addLink(r1, s1, intfName2='r1-eth1', **enlace)
        self.addLink(r3, s2, intfName2='r3-eth1', **enlace)

        # Add links between hosts and switchs
        self.addLink(h1, s1, **enlace)
        self.addLink(h2, s2, **enlace)

def run():
    "Test network topology"
    topo = NetworkTopo()
    net = Mininet(topo=topo, waitConnected=True)

    _intf1 = Intf('ens19', node=net['s1'])
    _intf2 = Intf('ens20', node=net['s2'])

    net.start()

    # Configure the interfaces on the routers
    net['r1'].cmd('ifconfig r1-eth1 10.0.1.1/24')
    net['r1'].cmd('ifconfig enp7s0 10.0.1.50/24')
    net['r1'].cmd('ifconfig r1-eth2 10.0.2.1/24')
    net['r2'].cmd('ifconfig r2-eth1 10.0.2.2/24')
    net['r2'].cmd('ifconfig r2-eth2 10.0.3.1/24')
    net['r3'].cmd('ifconfig r3-eth2 10.0.3.2/24')
    net['r3'].cmd('ifconfig r3-eth1 10.0.4.1/24')
    net['r3'].cmd('ifconfig enp8s0 10.0.4.50/24')

    # Add static routes
    net['r1'].cmd('ip route add 10.0.3.0/24 via 10.0.2.2')
    net['r1'].cmd('ip route add 10.0.4.0/24 via 10.0.2.2')
    net['r2'].cmd('ip route add 10.0.4.0/24 via 10.0.3.2')
    net['r2'].cmd('ip route add 10.0.1.0/24 via 10.0.2.1')
    net['r3'].cmd('ip route add 10.0.1.0/24 via 10.0.3.1')
    net['r3'].cmd('ip route add 10.0.2.0/24 via 10.0.3.1')

 # Set buffer sizes (example: 10MB = 81920 KB)
    buffer_size_kb = 51200     # Adjust the buffer size as needed (10MB)
    net['r1'].cmd('tc qdisc add dev r1-eth1 root handle 1: htb default 11')
    net['r1'].cmd(f'tc class add dev r1-eth1 parent 1: classid 1:1 htb rate 1000mbit burst 15k')
    net['r1'].cmd(f'tc qdisc add dev r1-eth1 parent 1:1 handle 10: bfifo limit {buffer_size_kb}kbyte')

    net['r2'].cmd('tc qdisc add dev r2-eth1 root handle 1: htb default 11')
    net['r2'].cmd(f'tc class add dev r2-eth1 parent 1: classid 1:1 htb rate 1000mbit burst 15k')
    net['r2'].cmd(f'tc qdisc add dev r2-eth1 parent 1:1 handle 10: bfifo limit {buffer_size_kb}kbyte')

    net['r3'].cmd('tc qdisc add dev r3-eth1 root handle 1: htb default 11')
    net['r3'].cmd(f'tc class add dev r3-eth1 parent 1: classid 1:1 htb rate 1000mbit burst 15k')
    net['r3'].cmd(f'tc qdisc add dev r3-eth1 parent 1:1 handle 10: bfifo limit {buffer_size_kb}kbyte')


    info('*** Routing Table on Router r1:\n')
    info(net['r1'].cmd('route'))
    info('*** Routing Table on Router r2:\n')
    info(net['r2'].cmd('route'))
    info('*** Routing Table on Router r3:\n')
    info(net['r3'].cmd('route'))

    info('*** Testing network connectivity\n')
    net.pingAll()

    CLI(net)
    net.stop()

if __name__ == '__main__':
    setLogLevel('info')
    run()
