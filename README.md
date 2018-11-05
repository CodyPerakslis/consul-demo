# consul-demo
Consul is a service-mesh with load-balancing, a key/vault store, and health checks.

This will demo the capabilities to add a service. Along with connecting nodes and watching the Gossip protocol in action.

This demo is heavily based on the official setup guide for HashiCorp Consul.

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

# Part 3: Health-Checks

# Part 4: KV Store
