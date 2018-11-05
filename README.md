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

You can also use DNS for discover with
`dig @127.0.0.1 -p 8600 factorize.service.consul SRV`

## Part 2: Linking Nodes
This part will require you to have some sort of VM software installed. I use virtualBox. You will also need HashiCorp Vagrant installed.

The Vagrantfile used comes from HashiCorp example.

Commands:

1. `vagrant up`  
This provisions the VMs we will be using (n1 and n2).

2. `vagrant ssh n1`  
This will ssh us into the n1 VM. Command 3 is in this ssh session.

3. `consul agent -server -data-dir=/tmp/consul -node=agent-one -bind=172.20.20.10 -enable-script-checks=true -config-dir=/etc/consul.d -bootstrap-expect=1`  
This sets up this node as the server.

4. `vagrant ssh n2`  
This runs from outside the ssh session. It gets us into the second VM for the next command.

5. `consul agent -data-dir=/tmp/consul -node=agent-two -bind=172.20.20.11 -enable-script-checks=true -config-dir=/etc/consul.d -bootstrap-expect=1`  
This setups up the node as a client.

6. `consul members`  
Run this from both VMs. They will only list themselves, because the don't know the other one exists yet.  

7. `consul join 172.20.20.10`  
Run this if you are in n2. From n1 run `consul join 172.20.20.11`. This tells the node that there is another node at the given location. Using the Gossip Protocol, the clusters will eventually merge into one.

8. `consul members`  
Run from n1, n2, or both. They now know about each other.


## Part 3: KV Store
The key value store allows for dynamic configurations and secret sharing.

1. `consul kv put redis/username admin`  
Put this in either VM.
2. `consul kv put redis/password passw0rd`  
Put this in either VM.
3. `echo "login:$(consul kv get redis/username) password:$(consul kv get redis/password)"`  
Since n1 and n2 are in the same cluster, they share the kv store (in the server n1), so this can be run from either VM or both.

## Part 4: Health-Checks

1. `echo '{"check": {"name": "ping",
  "args": ["ping", "-c1", "google.com"], "interval": "30s"}}' > /etc/consul.d/ping.json`  
  This creates a health check for the machine that makes sure it can ping google.com. Do the this and following command in either VM.

2. `consul reload`  
Have consul recheck is config directory and update as required. The ping check should pass.

3. `echo '{"service": {"name": "web", "tags": ["rails"], "port": 80,
  "check": {"args": ["curl", "localhost"], "interval": "10s"}}}' > /etc/consul.d/web.json`
Do this and the following command in either VM. This creates a health check for a web service, which does not exist.

4. `consul reload`  
The terminal running the consul agent on this VM will list the web service as failing, since no web server is running.  

5. Turn off your internet
Right now localhost consul is running a health check by pinging google every 10 seconds. Verify this in the ui, then turn off your internet and watch the health check fail. Turn it back on and watch the check start passing again.

## Bonus and Cleanup
### Bonus
From your localhost run `ngrok tcp 9192` (this will require ngrok and a free-tier ngrok account). Then connect to the tcp connection from another machine (example: `nc 0.tcp.ngrok.io 17369`, where the second two values depend on what ngrok gives you).

### Cleanup
* Ctrl-C from a running ngrok, socat processes.  
* Ctrl-C from a running consul agent, or `consul leave` on that machine.  
* End the VMs by using `vagrant destroy`
