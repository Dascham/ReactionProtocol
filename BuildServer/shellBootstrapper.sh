#!/bin/sh

#1, Pox controller
gnome-terminal -e "$HOME/Desktop/poxDart/pox/pypy/bin/pypy $HOME/Desktop/poxDart/pox/pox.py log.level --DEBUG forwarding.l2_multi openflow.discovery PoxModule.ThrottleManager misc.gephi_topo host_tracker"

#sflow forwarding, because of sflow dashboard and fastnetmon
gnome-terminal -e "sflowtool -f 127.0.0.1/7001 -f 127.0.0.1/7002"

gnome-terminal -e "sudo sh $HOME/Desktop/sflow-rt/start.sh"

#Open our Command Server
gnome-terminal -e "python $HOME/Desktop/P5ReactionProtocol/Attacker/CommandServer.py"
#sleep 2
#All Mininet related stuff
#gnome-terminal -e "python $HOME/Desktop/P5ReactionProtocol/BuildServer/Bootstrapper.py"

#Fastnetmon
#sleep 20
#gnome-terminal -e "/opt/Fastnetmon/Fastnetmon"

#

#(Forwader is launched by FNM, when an attack is detected)
#The networks/hosts FNM should monitor, should have been configured by a function in the Mininet-thing

