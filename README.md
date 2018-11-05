# consul-demo
Consul is a service-mesh with load-balancing, a key/vault store, and health checks.

This will demo the capabilities to add a service. Along with connecting nodes and watching the Gossip protocol in action.

This demo is heavily based on the official setup guide for HashiCorp Consul.

This was created for a demo in CSCI8980 Fall 2018, UMN-TC.

## Part 1: Linking Services
Make sure to download the consul binary and put it in your path.  

Make sure you have `socat` installed. We are using socat to bind to a port and control data streams. There are many other ways to do this as well for different applications, but this suites are purpose.

Commands:  

1. `socat -v tcp-listen:8182,fork exec:"python3 $(pwd)/factorize.py"`  
This will set up the factorizer code to listen to port 8182. Further commands will run in a different terminal.

2. `consul agent -dev -data-dir=/tmp/consul -config-dir=$(pwd)/consul.d -ui`  
This will start the agent given our specifications and will give us a ui at localhost:8500/ui. Further commands will run in a different terminal. The configurations set up a service for whatever is bound to port 8182 and then makes a proxy to it through port 9192.

3. `nc 127.0.0.1 9192`  
This will connect us to our proxy, try giving it numbers to factorize.

You can see the status of our cluster at localhost:8500/ui.

To "discover" to proxy use the API `curl http://127.0.0.1:8500/v1/agent/service/web-proxy`

Also use `consul catalog services` to list the services and `curl http://127.0.0.1:8500/v1/agent/services` for more details on the services.

# Part 2: Linking Nodes
This part will require you to have some sort of VM software installed. I use virtualBox. You will also need HashiCorp Vagrant installed.

The Vagrantfile used comes from HashiCorp example.

Commands:

1. `vagrant up`  
This provisions the VMs we will be using (n1 and n2).

2. `vagrant ssh n1`  
This will ssh us into the n1 VM. Command 3 is in this ssh session.

3. `consul agent -server -data-dir=/tmp/consul -node=agent-one -bind=172.20.20.10 -enable-script-checks=true -config-dir=/etc/consul.d`  
This sets up this node as the server.

4. `vagrant ssh n2`  
This runs from outside the ssh session. It gets us into the second VM for the next command.

5. `consul agent -data-dir=/tmp/consul -node=agent-two -bind=172.20.20.11 -enable-script-checks=true -config-dir=/etc/consul.d`  
This setups up the node as a client.

6. `consul members`  
Run this from both VMs. They will only list themselves, because the don't know the other one exists yet.  

7. `consul join 172.20.20.10`  
Run this if you are in n2. From n1 run `consul join 172.20.20.11`. This tells the node that there is another node at the given location. Using the Gossip Protocol, the clusters will eventually merge into one.

8. `consul members`  
Run from n1, n2, or both. They now know about each other.

9. `consul join 172.20.20.10`  
It doesn't matter if you connect to n1 or n2, but connect from our localhost node (outside of any ssh session).

10. `consul members`
You will now see all three nodes (2 server, 1 client). You can view the other nodes in the ui (although it may take a little time to list the other VM).

# Part 3: Health-Checks

# Part 4: KV Store
