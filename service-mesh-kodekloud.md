-----------------------
Service mesh with IStio
-----------------------

Course Objectives
-----------------

-   Monoliths & Microservices
-   Service Mesh
-   Istio
-   Install Istio
-   Visualizing with kiali


with we move to **istio concept** such as

-   Gatways
-   Virtual Services
-   Destination Rules 
-   Subsets
-   Timeouts
-   Retries
-   Circuit Breaking
-   Fault Injection
-   Request Routing
-   A/B Testing

then we look at the **security concepts**. such as

-   Certificate Management
-   Authentication
-   Authorization

then we look at the **Observerbility concepts**. such as

-   Veiwing and Collecting Metrics (with promethous and grafana)
-   Kiali in Detail
-   Distributed Tracings


What is service mesh...
------------------------

-   Each microservices, we replace them with a **single proxy** in the form of **sidecar container**. The proxy communicate with each other through **data plane**. And they communicate to the server side component called **Control Plane**.  

-   Control plane manages all the traffic into and out of your services via **proxies**. so all the networking logic is abstracted from your business code.. And this approach is known as **service mesh**.

-   A service mesh is a dedicated and configurable infrastructure layer that handles the communication b/w services without having to change the code in a microservice architecture.

-   With the service mesh, you can dynamically configure how services talk to each other.

-   When services talk to one another, you will have **mutual TLS**. so your work load can be secure( mean communicaiton b/w service can secure..)

-   You can see things better, 

-For example , how application is doing end-to-end... 
- Where it is having issues and bottlenecks, and service discovery which cover 3 main topics..

-   In a **dynamic cluster**, we will need to know at which **IP and port services are expoxed** so they can find each other... **Health check** help you dynamically keep services that are up in the mesh while **servics that are down are left out.**

- **Load balancing** routes the traffic to healthy instances and cuts it off from the onces who have been failing..

Istio
-----------

Now we have a look at istio, how it works its architecture and core components.

-   It is a free and open source service mesh that provide an efficient way to secure, connect and monitor services. 

-   It work with kubernetes and traditional workloads, thereby bring universal **traffic management** and **telemetry and security** to complex deployments.

- It support leading cloud provider and consultants....

sir khty hn hum abi proxies services ki bt ker rhy thy jo take care krti ha all task ko jo outsourced hony chahye microservices sa...

- y proxies or in k **b/w comminication dataplane** k through hoti ha.k istio in proxies ko implement kerta ha high-performance proxy known as **Envoy** k through.

- proxies communicate krti ha service side component sa known as **control plane**...

Generally control plane consists of 3 component known as 

-   Citadel  -- it manage certificate generation
-   Pilot  -- it helped with service discovery
-   Galley  -- it validing configuration files..

-   these 3 component combined into single daemon called **ISTIO**

-   each service and port has a saperate component in it, along with the envoy proxy called the **ISTIO AGENT**. It is responsible for passing **configuration secrets** to the ENvoy proxies.

Installing istio in cluster..
-----------------------------

3 approaches to install istio...

-   Install with istioctl      ----install istio with commandline utilty **istioctl**
-   Istio Operator Install   
-   Install with Helm


installing istio in cluster through istioctl
--------------------------------------------

-   **istioctl install --set profile=demo -y**

-   after running this command istio. it deployed in the cluster in form of a deployment named **istiod** in the namespace named **istio-system**

-   istiod deploys 3 service ,  **Citadel ,Pilot ,  Galley**. Along with these , it also deploys two other service known **istio-engressgateway, istio-ingressgateway**. and bunch of kubernetes service objects to expose these services.

once installed verify it with verification command.

    **istioctl verify-install**

Deploying first application with istio
-----------------------------


Ab sir na **kubectl apply -f <file-name>** ko use krty howy application ko deployment ma deploy kya ha... 

**kubectl get all** krny k bd 

ab sir khty hn k because hum na cluster ma istio install kya ha tu sab microservice mean pods ma 2 container hogye aik ma main application or dosary ma **Envoy proxies** lgye gi as sidecar chaly ga ... or because namespace define ni kya tha, so y default namespace ma chal rha hoga... but abi sirf main application container hi pod ma arha ha. 

Reason
-------

**istioctl analyze** is a command. it gives output **namespace is not enabled for istio injection** what does it mean.. **is lye namespace ma istio as side car available ni ha**. or sirf main application container hi mil rha ha pod ma..

so,

**so you must explicity enable istio sidecar injection at a namespace level. if you would like istio to inject proxy services as sidecar to the applications deployed in a namespace**

is k lye jesa k **istioctl analyze** command na output di ha. use this **kubectl label namespacce default istio-injection=enabled** 

mean run **kubectl label** command and specify the namespace(in my case it is default, because i had deployed application in default namespace.) where you want to enable sidecar injection by setting the value.

for **disabling** must set this label to disabled using the same command.

agr apna istio-injection namespace ma enable krny sa phily us namespace ma koi deployment ki ha tu wo tu isko injention us ko automatically side car ni dye ga. **you need to inject istio in namespace first through label command** then **deploy application in that namespace**. 

**once command is run every new app in the default namespace will get sidecar automatically..** agr injection sa phily namespace ma koi deployment chal rhi tha tu usy delete kr do(mean need to recreate deployment)... or istio injection k bd isko apply kro again..


after this apply again **istioctl analyze** command will give you the message **no validation issues is found when analyzing default namespace**

ab ap kubectl get pod kro gye tu wo apko dekha rha hoga k hr microservice pod ma 2 container ha, aik main container jis ma application ha or aik sidecar container for **Envoy proxies**.

summary:
-------

cluster ma istio install tha but namespace ma inject ni tha. so jb deployment us namespace ma ki tu sirf pod ma main application container hi chal or envoy proxies as side car ni chal pod ma. main contianer k sath. so deployment ko delete kya... then kubectl label command k istio ko inject kya us name space ma then again us name space ma application ko deploy kya. so ap jb hr microservice pods k main application containers create hoga tu automatically envoy proxies as side car is namespace sa in container ko mil jye ga...


Visualizaing service mesh through kaili
---------------------------------------

jb apki kafi microservice ho. it is important to observe them. so ap in ki availability dekh sakhy...

kiali is a very comman and powerful add-on used with istio.it has GUI. and helpful for visualizing and managing service mesh..

it is used for observing connecitons and microservices of istio service mesh and also for defining and validating them.

it visualizes service mesh topology and provides visibility, into feature like request routing, circuit breakers, request rates, latency and more..


Demo installing kiali
---------------------

Install kiali in cluster.


kubectl apply -f samples/addons ------------> sir k ps file thi is lye sir na ka through kiali ko cluster ma install kya...


once kaili starts running... with this command **istioctl dashboard kiali** start kaili dashboard.. it will start browser and land on pages..

Pre-requisites
----------------

kubernetes services..
--------------------


side cars
---------   it share same network and storage with main container..

simple file for side car container..

containers:
    -   name: nginx-container
        image: nginx
        volumeMounts:
        -   name: share-data
            mountPath: /usr/share/nginx/html
    -   name: sidecar-container
        image: fluent/fluentd     ---> use for shipping application logs to server..
        volumeMounts:
        -   name: shared-data
            mountPath:  /pod-data

Envoy
--------

It is one of the most common proxies you here.


Traffic Management
------------------

we are going to learn how to manage traffic in your istio service mesh.. you can do it without changing your application code.

Traffic Management core components
----------------------------------

-   Gateways 
-   Virtual Services
-   Destination Rule
-   Subsets
-   Timeouts
-   Retries
-   Circuit Breaking 
-   Fault Injection
-   Request Routing 
-   A/B Testing


Gateways
--------

let's have a look at gateways. He have deploy application with service mesh how can we make is services accessible to external users?

as we know ingress controlls traffic coming into the kubernetes cluster. with ingress(nginx controller) we can configure rules to say any traffic to the kubernetes cluster with hostname should be directed to the product service.


sample ingress object
---------------------

    apiVersion: networking.k8s.io/v1beta1
    kind: Ingress
    metadata:
        name: ingress
    spec:
        rules:
        -   host: bookinfo.app
            http:
                paths: /
                backend:
                    serviceName: productpage
                    servicePort: 8000

this is kubernetes ingress. While istio support kubernetes ingress.

**but there is also another approach that istio offers and recommends that supports more istio features such as advanced monitoring and routing rules that is called gateway**

**Gateways are load balancers that sit at the edge of the mesh**  

**they are the main configuration that manage inbound and outbound traffic to service mesh** y recommended approach ha k hum isko istio ma use kry jesy hum ingress ko kubernetes ma use kryt hn.

hum na phily b dekha tha k jb hum istio ko cluster ma install krty hn tu y 2 main component **istio-ingressgateway** or **istio-egressgateway** ko deploy krta ha..

**istio-ingressgateway** manages all inbound traffic to the services. and **istio-egressgateway** manages all outbound traffic from these services.

we discussed that kubernetes ingress is deployed using controller like NGINX. on the other hand istio id deploys ingress gateways using Envoy proxies. and envoy proxies is deploy as side car container with main application containers 

**however the ingress and egress gateways are just standalone Envoy proxies sitting at the edge of the service mesh. they do not work as a side car** this was deployed while istio was deployed on the cluster.


however we can have our own set of custom gateway controllers as well.

**Our goal here is to catch all traffic coming through this istio-ingress gateway controller and route all traffic at hostname bookinfo.app to our product page**

for this we first create a gateway object.

bookeinfo-gateway.yaml
----------------------

    apiVersion: networking.istio.io/v1alpha3
    kind: Gateway
    metadata:
        name: bookinfo-gateway
    spec:
        selector:            --> through this you can specfically select ingress controller from multiple ingress controller using labels and selectors.
            istio: ingressgateway
        servers:
        -   port:
                number: 80
                name: http
                protocol: HTTP
            hosts"
            -   "bookinfo.app"        with * you can allow all host..


to list the created gateway run the **kubectl get gateway** or for more details **kubectl describe gateway <gatwayname>**,  **kubectl edit gateway <gatwayname>** 


traffic is coming from this **"bookinfo.app"** but how and where it is routed to.. we will see this in virtual services.

Virtual Services
-----------------

let us learn about virtual services and istio. how do you route traffic through this gateway to actual services.

**all routing rules** are configure through **virtual services**.

**virtual services** it defines a set of routing rules for traffic coming from ingress gateway into the service mesh. it is fexible and powerfull with rich traffic option.

you can specify traffic behaviour for one or more hostname. manage traffic within different version of services. **standard and regex pass are supported**.

jb virtual service create hoti ha, istio control plane applies the new configuration to all envoy side proxies. 

virtual service.yaml
--------------------     always refer to the istio documentation to get the latest supported API version while creating virtual service.

        apiVersion: networking.istio.io/v1alpha3
        kind: VirtualService
        metadata:
            name: bookinfo
        spec:
            hosts:
            -   "bookinfo.app"    ---> **host name jis sa traffic aye gi. mean is name k host k traffic ko hi y virtual service accept kry ga. it should match with gateway hosts**
            gateways:
            -   bookinfo-gateway    ---> **object name of ingress-gateway jis sa virtual host per traffic arhi hogi..**
            http:                   ----> ** here we add routing rules**
            -   match:              ---> match session specify the uri should be match
                -   uri:
                        exact:  /productpage 
                -   uri:
                        prefix: /static
                -   uri:
                        exact: /login
                -   uri:
                        exact: /logout
                -   uri:
                        prefix: /api/v1/products
            route:    ---> **All the uri are then routed to the destination**
            -   destination:
                    host:   productpage  ---> **All of the traffic matches URI pattern are then routed to the destination specficed in the route section**
                    port:
                        number: 9000
                
How to manage traffic in istio service mesh
-------------------------------------------

let understand it with the example. let say i have 3 deployments named v1 having 2 pods , v2 having 1 , and v3 deployments having 2 pods.

and we have set same label on each on pods under deployment section so we can match it with service. now 40% traffic will go to the deployment v1 version. and 20% traffic will go to the deployment v2 version. and 40% will go to deployment v3 version.

this is a kubernetes native way to distributes traffic across multiple deployments. but it has some issues.


what if we want to send 1% of traffic to version 2. and 99% to version 1. since version 1 deployment have 3 pod and version 2 deploy have 1 pod and kubernetes service is natively design to send traffic equally mean 75% traffic would go to version 1 and 25% would go in version 2. mean kubernetes k native behaviour sa hum isko acheive ni ker sakhty. **the only way is to use istio service mesh virtual service..**

so in kubernetes the only way to change the distributed persentage is to play around with the number of pods available in differnet services. it is a kubernetes **limitation**


**solution:**

**with istio and the virtual service, we can now create a virtual service instead of kubernetes service..**

virtual service
---------------

        apiVersion: networking.istio.io/v1alpha3
        kind: VirtualService
        metadata:
            name: reviews
        spec:
            hosts:
                -   reviews
            http:
            -   route:
                -   destination:
                        host:   reviews    ---> name of the virtual services
                        subset: v1
                    weight: 99             --> traffic weight   

                -   destination:
                        host:   reviews        ---> name of the virtual services
                        subset: v2
                    weight: 1                  --> traffic weight
                    
    99% traffic will go to v1 subset and 1% will go to v2 subset. 

    if we increase the v2 deployments replica (pods) then still 1% of traffic will go to v2 deployment.

    **mean no of instance has nothing to do with traffic distribution.**

    **And we can easily controll traffic through virtual service.**


    now you might wondering what a subset is. just now you think. it is a way to grouping multiple objects together using a label. 


Destination Rules:
------------------

it applies router polices after the traffic is routed to specfic service.

in virtual service, we have seen **subsets**. like 


virtual service
---------------

        apiVersion: networking.istio.io/v1alpha3
        kind: VirtualService
        metadata:
            name: reviews
        spec:
            hosts:
                -   reviews        
            http:
            -   route:
                -   destination:
                        host:   reviews    ---> name of the virtual services
                        subset: v1
                    weight: 99             --> traffic weight   

                -   destination:
                        host:   reviews        ---> name of the virtual services
                        subset: v2
                    weight: 1                  --> traffic weight

but question is where the subset define. **it defines in destination rule**

destination rules
-----------------

        apiVersion: networking.istio.io/v1alpha3
        kind: DestinationRule
        metadata: 
            name: reviews-destination
        spec:
            hosts: reviews  ------> nname of kubernetes service
            subsets:
            -   name: v1
                labels    --> these are the labels set on the pods for the respective version of deployments. mean pod per dye v1 label ko hum destination subsets ma bta ker uska subset bna rhy hn.  **for 1st deployment**
                    version: v1
            -   name: v2
                labels:
                    version: v2                   --> **for 2nd deployment**


        pod section
        -----------

        apiVersion: apps/v1
        kind: Deployment
        metadata:
            name:   reviews-v1
        spec:
            replicas:   3
            <...>
            template:
                metadata:
                    labels:
                        app: reviews
                        version: v1  --> put in destination rule under subset to make a destination subset.


by define envoy loadbalance traffic in round robin feshion.. **this can be customized through the destination rules by specifing a traffic policy in loadbalancer**


like:

destination rules
-----------------

apiVersion: networking.istio.io/v1alpha3
kind: DestinationRule
metadata: 
    name: reviews-destination
spec:
    hosts: reviews  ------>name of kubernetes service
    trafficPolicy:
        loadBalancer:
            simple: PASSTHROUGH  ---> this will route traffic to the host that has fewer active requests.
    subsets:
    -   name: v1
        labels    --> these are the labels set on the pods for the respective version of deployments. mean pod per dye v1 label ko hum destination subsets ma bta ker uska subset bna rhy hn.  **for 1st deployment**
            version: v1
    -   name: v2
        labels:
            version: v2     


Other simple Algorithms:
------------------------

-   ROUND_ROBIN
-   LEAST_CONN
-   RANDOM
-   PASSTHROUGH

**What if we want to set up a different loadbalancer policy for specfic subset...**

in that case.. We set traffic policy at subset level...


destination rules
-----------------

        apiVersion: networking.istio.io/v1alpha3
        kind: DestinationRule
        metadata: 
            name: reviews-destination
        spec:
            hosts: reviews  ------> name of kubernetes service
            trafficPolicy:
                loadBalancer:
                    simple: PASSTHROUGH  ---> this will route traffic to the host that has fewer active requests.
            subsets:
            -   name: v1
                labels    --> these are the labels set on the pods for the respective version of deployments. mean pod per dye v1 label ko hum destination subsets ma bta ker uska subset bna rhy hn.  **for 1st deployment**
                    version: v1
            -   name: v2
                labels:
                    version: v2     
                    trafficPolicy:
                        loadBalancer:
                            simple: RANDOM

With this way, we can configure one loadbalancer policy for all subsets and a saparate one for the selected subset as required..


there are many more configuration support by destination rules.. like **for configuring client TLS** specify **simple TLS** or **matual TLS**

set the mode to mutual and provide the path to the certificate file... like

destination rules
-----------------

        apiVersion: networking.istio.io/v1alpha3
        kind: DestinationRule
        metadata: 
            name: reviews-destination
        spec:
            hosts: reviews  ------> name of kubenetes service. it is the short name of service "reviews.defualt.svc.cluster.local"
            trafficPolicy:
                loadBalancer:
                    simple: PASSTHROUGH  ---> this will route traffic to the host that has fewer active requests.
                tls:
                    mode: MUTUAL
                    clientCertificate: /myclientcert.pem
                    privateKey: /client_private_key.pem
                    caCertificates: /rootcacerts.pem
            subsets:
            -   name: v1
                labels    --> these are the labels set on the pods for the respective version of deployments. mean pod per dye v1 label ko hum destination subsets ma bta ker uska subset bna rhy hn.  **for 1st deployment**
                    version: v1
            -   name: v2
                labels:
                    version: v2     
                    trafficPolicy:
                        loadBalancer:
                            simple: RANDOM


important:

    hosts: reviews  ------> name of virtual service. it is the short name of service "reviews.defualt.svc.cluster.local"

when using short names, instead of fully qualified domain names, Istio will interpret the short name based on the rules namespace and not the service actual namaspace. **This might lead to misconfigurations if your service is another namespace.** 

**to void this use fully qualified names over short names is recommmeded.** like.

destination rules
-----------------
        apiVersion: networking.istio.io/v1alpha3
        kind: DestinationRule
        metadata: 
            name: reviews-destination
        spec:
            hosts: reviews.defualt.svc.cluster.local  ------> name of name of kubernetes service. it is the short name of service "reviews.defualt.svc.cluster.local"
            trafficPolicy:
                loadBalancer:
                    simple: PASSTHROUGH  ---> this will route traffic to the host that has fewer active requests.
                tls:
                    mode: MUTUAL
                    clientCertificate: /myclientcert.pem
                    privateKey: /client_private_key.pem
                    caCertificates: /rootcacerts.pem
            subsets:
            -   name: v1
                labels    --> these are the labels set on the pods for the respective version of deployments. mean pod per dye v1 label ko hum destination subsets ma bta ker uska subset bna rhy hn.  **for 1st deployment**
                    version: v1
            -   name: v2
                labels:
                    version: v2     
                    trafficPolicy:
                        loadBalancer:
                            simple: RANDOM

DEMO GATEWAY
------------

deploy deployment and see it on kaili..

while deploying file you can you **istioctl analyze** to see not to have istio namespace injection issue..

**you can also apply and modify your services yamls files through kiali interface.**

DEMO VIRTUAL SERVICE
--------------------

**how we can manage that specfic user can only see the specfic page of the application....**



we can managed it with **match** section in virtual service... like...

virtual service
---------------

        apiVersion: networking.istio.io/v1alpha3
        kind: VirtualService
        metadata:
            name: reviews
        spec:
            hosts:
                -   reviews        
            http:
            -   match:
                -   headers:
                        end-users:
                            exact: kodekloud    ---> match this user an only give view to v2 application, you can add multiple users like this to see specfic application pages views..
                route:
                    -   destination:
                        host:   reviews        ---> name of the virtual services
                        subset: v2
                    
            -   route:
                -   destination:
                        host:   reviews    ---> name of the virtual services
                        subset: v1
                   
Demo destination rules
----------------------


CHAT GPT SHARES
---------------

    **simple deployment using istio without destination rules.**

    In Istio service mesh, external traffic can reach the deployment pods through an Istio Gateway and a VirtualService. The Gateway defines the entry points into the mesh from outside, and the VirtualService routes the traffic to the appropriate services inside the mesh.

    Here's a step-by-step guide along with example YAML files to set up the necessary components:

Install Istio

    First, make sure you have Istio installed on your Kubernetes cluster. You can follow the Istio installation guide if you haven't done this yet.

    Define an Istio Gateway

    Create a Gateway resource that will handle incoming traffic from outside the mesh.


        apiVersion: networking.istio.io/v1beta1
        kind: Gateway
        metadata:
        name: my-gateway
        namespace: default
        spec:
            selector:
             istio: ingressgateway # use istio default controller
        servers:
        - port:
            number: 80
            name: http
            protocol: HTTP
          hosts:
          - "*"

   
Define a VirtualService

    Create a VirtualService that routes the traffic received by the Gateway to the appropriate service.


    apiVersion: networking.istio.io/v1beta1
    kind: VirtualService
    metadata:
    name: my-virtualservice
    namespace: default
    spec:
    hosts:
    - "*"
    gateways:
    - my-gateway
    http:
    - match:
        - uri:
            prefix: / # route all traffic to the service
        route:
        - destination:
            host: my-service          ---> "kubernetes service object name and service port or y service apny behind deployment pod per traffic send kerti ha"
            port:
            number: 80

Deploy Your Application

    Deploy your application (e.g., a simple web application) along with its Kubernetes service.

Deployment YAML:


    apiVersion: apps/v1
    kind: Deployment
    metadata:
    name: my-service
    namespace: default
    spec:
    replicas: 1
    selector:
        matchLabels:
        app: my-service
    template:
        metadata:
        labels:
            app: my-service
        spec:
        containers:
        - name: my-service
            image: <your-application-image>
            ports:
            - containerPort: 80

Service YAML:


    apiVersion: v1
    kind: Service
    metadata:
    name: my-service
    namespace: default
    spec:
        selector:
            app: my-service
         ports:
    - protocol: TCP
        port: 80
        targetPort: 80
    Apply the Configurations

    Apply all the YAML files using kubectl:

   
    kubectl apply -f gateway.yaml
    kubectl apply -f virtualservice.yaml
    kubectl apply -f deployment.yaml
    kubectl apply -f service.yaml
    Once all the configurations are applied, your external traffic should reach the deployment pods through the Istio Gateway and be routed by the VirtualService.

    Explanation
    Gateway: Manages ingress traffic to the service mesh. It listens for traffic on the specified port (80) and for the specified hosts (in this case, all hosts "*").
    VirtualService: Defines how traffic routed by the Gateway should be directed to the backend services. It routes all traffic to my-service.
    Deployment and Service: Standard Kubernetes resources that define your application's deployment and service.
    This setup allows external traffic to enter the Istio service mesh and be routed to your application's pods.


with destination rules..
----------------------

    In Istio, the complete flow from external traffic to your deployment pods involves several components, including Gateway, VirtualService, and DestinationRule. Here's an explanation of each component and their role in the flow, along with the necessary YAML configurations.

    Complete Flow of External Traffic in Istio
    Gateway: The entry point for external traffic into the Istio service mesh.
    VirtualService: Defines the routing rules for the traffic received by the Gateway.
    DestinationRule: Configures policies that apply to traffic intended for a specific service.

Step-by-Step Guide with YAML Files
    
    1. Install Istio
    
    Ensure Istio is installed and running on your Kubernetes cluster. You can follow the Istio installation guide if needed.

    2. Define an Istio Gateway
    
    Create a Gateway resource to handle incoming HTTP traffic on port 80.


    apiVersion: networking.istio.io/v1beta1
    kind: Gateway
    metadata:
    name: my-gateway
    namespace: default
    spec:
    selector:
        istio: ingressgateway # use istio default controller
    servers:
    - port:
        number: 80
        name: http
        protocol: HTTP
        hosts:
        - "*"

    3. Define a VirtualService
    Create a VirtualService to route the traffic from the Gateway to the appropriate service.


    apiVersion: networking.istio.io/v1beta1
    kind: VirtualService
    metadata:
    name: my-virtualservice
    namespace: default
    spec:
    hosts:
    - "*"
    gateways:
    - my-gateway            #gateway object name
    http:
    - match:
        - uri:
            prefix: "/" # route all traffic to the service
        route:
        - destination:
            host: my-service    #kubernetes service name 
            port:
            number: 80

    4. Define a DestinationRule
    Create a DestinationRule to specify traffic policies like load balancing, connection pool settings, and outlier detection for the service.


    apiVersion: networking.istio.io/v1beta1
    kind: DestinationRule
    metadata:
    name: my-destinationrule
    namespace: default
    spec:
    host: my-service                --> represent name of kubernetes service as destination
    trafficPolicy:
        loadBalancer:
        simple: ROUND_ROBIN
        connectionPool:
        tcp:
            maxConnections: 100
        http:
            http1MaxPendingRequests: 1000
            maxRequestsPerConnection: 100
        outlierDetection:
        consecutiveErrors: 5
        interval: 5s
        baseEjectionTime: 30s
        maxEjectionPercent: 100



    5. Deploy Your Application
    Deploy your application and its corresponding Kubernetes service.

Deployment YAML:


    apiVersion: apps/v1
    kind: Deployment
    metadata:
    name: my-service
    namespace: default
    spec:
    replicas: 1
    selector:
        matchLabels:
        app: my-service
    template:
        metadata:
        labels:
            app: my-service
        spec:
        containers:
        - name: my-service
            image: <your-application-image>
            ports:
            - containerPort: 80

Service YAML:

        apiVersion: v1
        kind: Service
        metadata:
        name: my-service       kubernetes service name..
        namespace: default
        spec:
        selector:
            app: my-service
        ports:
        - protocol: TCP
            port: 80
            targetPort: 80

6. Apply the Configurations
Apply all the YAML files using kubectl:


    kubectl apply -f gateway.yaml
    kubectl apply -f virtualservice.yaml
    kubectl apply -f destinationrule.yaml
    kubectl apply -f deployment.yaml
    kubectl apply -f service.yaml
    Explanation of the Flow
    Gateway: The Istio Gateway resource listens for HTTP traffic on port 80 and allows any host ("*"). It acts as the entry point for external traffic into the service mesh.

    VirtualService: The VirtualService routes the incoming traffic from the Gateway to the backend service my-service. The match rule ensures all traffic with a URI prefix of "/" is routed to the service.

    DestinationRule: The DestinationRule applies traffic policies to the my-service. This can include load balancing (ROUND_ROBIN), connection pool settings, and outlier detection to ensure resilience and reliability of the service.

    Deployment and Service: These are standard Kubernetes resources that deploy your application and expose it internally within the cluster.

    By following these steps, external traffic is able to reach the deployment pods within the Istio service mesh, with the Gateway handling ingress, the VirtualService managing routing, and the DestinationRule applying traffic policies.

**In the context of the DestinationRule in Istio, the host field represents the name of the service to which the traffic policies defined in the DestinationRule apply. This should match the name of the service as defined in the Kubernetes Service resource.**

Here is the DestinationRule example with the host field explained:


    apiVersion: networking.istio.io/v1beta1
    kind: DestinationRule
    metadata:
    name: my-destinationrule
    namespace: default
    spec:
    host: my-service             ---> represent name of kubernetes service as destination
    trafficPolicy:
        loadBalancer:
        simple: ROUND_ROBIN
        connectionPool:
        tcp:
            maxConnections: 100
        http:
            http1MaxPendingRequests: 1000
            maxRequestsPerConnection: 100
        outlierDetection:
        consecutiveErrors: 5
        interval: 5s
        baseEjectionTime: 30s
        maxEjectionPercent: 100

    Explanation
    host: The name of the service to which this DestinationRule applies. In this example, my-service is the name of the service. This should match the name defined in the Service YAML:


    apiVersion: v1
    kind: Service
    metadata:
    name: my-service
    namespace: default
    spec:
    selector:
        app: my-service
    ports:
    - protocol: TCP
        port: 80
        targetPort: 80

    How It Fits into the Complete Flow
    Gateway: Manages external traffic entry into the Istio mesh.
    VirtualService: Routes traffic from the Gateway to the backend service.
    DestinationRule: Applies traffic policies to the specified service (my-service).
    When traffic reaches my-service through the Gateway and VirtualService, the DestinationRule ensures that the traffic adheres to the specified policies, such as load balancing (ROUND_ROBIN), connection pooling, and outlier detection.

    By setting the host field to my-service, you are linking the DestinationRule to the service named my-service so that Istio applies the defined traffic policies whenever traffic is routed to this service.

Complete flow with virtual service feild "subsets" and "weights"
---------------------------------------------------------------

    Certainly! The subset and weight fields in Istio's VirtualService and DestinationRule are used for advanced traffic management, such as canary deployments or traffic splitting between different versions of a service.

    Explanation of subset and weight

    subset: Defines a specific subset of instances (a subset of a service) that are selected based on labels. This is typically used for routing traffic to different versions of a service.
        
    weight: Used in VirtualService to distribute traffic between different subsets of a service.
        Step-by-Step Guide with subset and weight

    

Step-by-Step Guide with Complete YAML Files

1. Create a Gateway resource to handle incoming HTTP traffic on port 80.


    apiVersion: networking.istio.io/v1beta1
    kind: Gateway
    metadata:
    name: my-gateway
    namespace: default
    spec:
    selector:
        istio: ingressgateway # use istio default controller
    servers:
    - port:
        number: 80
        name: http
        protocol: HTTP
        hosts:
        - "*"
2. Define a VirtualService with Traffic Splitting
Create a VirtualService to split traffic between the subsets based on weight.


    apiVersion: networking.istio.io/v1beta1
    kind: VirtualService
    metadata:
    name: my-virtualservice
    namespace: default
    spec:
    hosts:
    - "*"    ----> represent coming traffic
    gateways:
    - my-gateway
    http:
    - match:
        - uri:
            prefix: "/" # route all traffic to the service
        route:
        - destination:
            host: my-service   ---> represent name of kubernetes service as destination
            subset: v1
            weight: 80
        - destination:
            host: my-service   ---> represent name of kubernetes service as destination
            subset: v2
            weight: 20

3. Define a DestinationRule with Subsets
Create a DestinationRule to define subsets for different versions of the service.


    apiVersion: networking.istio.io/v1beta1
    kind: DestinationRule
    metadata:
    name: my-destinationrule
    namespace: default
    spec:
    host: my-service              ---> represent name of kubernetes service as destination
    subsets:
    - name: v1
        labels:
        version: v1
    - name: v2
        labels:
        version: v2
    trafficPolicy:
        loadBalancer:
        simple: ROUND_ROBIN


4. Define a Service

    Expose your application with a Kubernetes Service.


    apiVersion: v1
    kind: Service
    metadata:
    name: my-service        --> service name
    namespace: default
    spec:
    selector:
        app: my-service
    ports:
    - protocol: TCP
        port: 80
        targetPort: 80       

5. Define a Deployment with Version Labels
    
    Create two versions of your application.
     

    Deployment for Version v1:


    apiVersion: apps/v1
    kind: Deployment
    metadata:
    name: my-service-v1
    namespace: default
    spec:
    replicas: 1
    selector:
        matchLabels:
        app: my-service
        version: v1
    template:
        metadata:
        labels:
            app: my-service
            version: v1
        spec:
        containers:
        - name: my-service
            image: <your-application-image-v1>
            ports:
            - containerPort: 80

    Deployment for Version v2:


    apiVersion: apps/v1
    kind: Deployment
    metadata:
    name: my-service-v2
    namespace: default
    spec:
    replicas: 1
    selector:
        matchLabels:
        app: my-service
        version: v2
    template:
        metadata:
        labels:
            app: my-service
            version: v2
        spec:
        containers:
        - name: my-service
            image: <your-application-image-v2>
            ports:
            - containerPort: 80

    
important:

**in vertual service under route destination host represent kubernetes service** and **in destination rules, host name also represent kubernetes service**
 

        Applying the YAML Files
        Apply all the configurations using kubectl:

        sh
        Copy code
        kubectl apply -f deployment-v1.yaml
        kubectl apply -f deployment-v2.yaml
        kubectl apply -f service.yaml
        kubectl apply -f gateway.yaml
        kubectl apply -f virtualservice.yaml
        kubectl apply -f destinationrule.yaml
        Summary
        Gateway: Manages ingress traffic.
        VirtualService: Routes and splits traffic based on weights to different subsets.
        DestinationRule: Defines subsets for different versions of the service.
        Service: Exposes the application.
        Deployments: Different versions of the application.
        Flow Chart
        Here's a flowchart to illustrate the complete flow:

        Gateway: Entry point for external traffic.
        VirtualService: Routes and splits traffic based on weights to different subsets.
        DestinationRule: Defines subsets (versions) of the service.
        Service: Exposes the application.
        Deployments: Different versions of the application.
        mermaid
        Copy code
        graph TD
        A[Gateway] -->|External Traffic| B[VirtualService]
        B[VirtualService] -->|Route to Subset v1 (80%)| C[Deployment v1]
        B[VirtualService] -->|Route to Subset v2 (20%)| D[Deployment v2]
        C[Deployment v1] --> E[Service]
        D[Deployment v2] --> E[Service]
        By following this guide and applying the provided YAML configurations, you can manage external traffic, route it to different versions of your application, and implement traffic splitting using Istio.


flow from external traffic to internal service
----------------------------------------------

**ingress-gateway  ---> virtual-service ---> destination rules --> kubernetes service --> kubernetes deployments on envoy proxisy runninga as side --> main application container.**


fault injection
---------------

it helps us to see if are policies run efficiently and are not too restrivtive.

we can inject errors in our virtual services and these could be **two different types of errors**, **delays and aborts**

delay example:
-------------

    apiVersion: networking.istio.io/v1alpha3
    kind: VirtualService
    metadata:
        name: my-service
    spec:
        hosts:
        - my-service  
        http:
        - fault:
            delay:          ---> in this example, we are injecting a delay type of fault in the mesh. it will a delay for 10% of requests. and it is configure as five seconds...
                percentage:
                    value: 0.1   ---> itna deplay hoga 
                fixedDelay: 5s    ---> or itny time k lye hoga...
        route:
        - destination:
                host: my-service  --> kubernetes service name
                subnet: v1   

    adding delay can lead the service to work slowly..

Abort example:
-------------

    apiVersion: networking.istio.io/v1alpha3
    kind: VirtualService
    metadata:
        name: my-service
    spec:
        hosts:
        - my-service 
        http:
        - fault:
            abort:          ---> in this example, we are injecting a abort type of fault in the mesh to simulate errors by rejecting requests and returning specfic error codes.
                percentage:
                    value: 0.1   
                httpStatus: 5s  
        route:
        - destination:
                host: my-service  --> kubernetes service name
                subnet: v1  

Demo: Fault Injection
---------------------


Timeouts
-----------

is ma sir btaty hn k agr koi microservice fail hogi ha or apki traffic us per jarhi ha tu wo quened ma ajye gi.. 

so it must not keep the dependent service waiting forever.

it must fail after a period of time and return an error message.

That way the dependent service gets an errors message and is not impacted.

that what a timeout is.....

we can either configure a timeout at the data service for it to fail.


we can add time out to reject request if it takes more than given time..

example:
-------
    apiVersion: networking.istio.io/v1alpha3
    kind: VirtualService
    metadata:
        name: bookinfo
    spec:
        hosts:
        -   "bookinfo.app"
        gateways:
        -   bookinfo-gateway  
        http:
        - match:
        - uri:
                exact: /productpage
        - uri:
                exact: /static
        route:
        - destination:
                host: productpage   --> kubernetes service name
                port:
                    number: 9000
        timeout: 3s

Demo timeout
------------



Retries
-------

When a service tries to reach another service, and for some reason it fails, we can configure the virtual service to attempt that operation again.. 

This way, you do not have to handle the retries within the application code.

example:
-------

    apiVersion: networking.istio.io/v1alpha3
    kind: VirtualService
    metadata:
        name: my-service
    spec:
        hosts:
        - my-service
        http:
        - route:
          - destination:
                host: my-service
                subset: v1
          retries:
            attempts: 3
            perTryTimeout: 2s  ---> it is basically says the number of times to try and the interval b/w them.

**Istio, by default, has a retry behavior which is 25 milliseconds b/w reties and retrying 2 times before an error returns..**

Circuit Breaking
----------------

we know that services can communicate with other services. if for some reason communication b/w the services break or slow down.. it essentaily creating a delay...

in such case we would like to mark the service fail immediately. this is know as **circuit breaking**

This allows us to create resilient microservice applications that will limit the impact of failures or other network-related issues..

**The same is true if we would like to limit the number of requests coming to the service itself**

Circuit breaks is configure in **destination rules**

example:
-------

apiVersion: networking.istio.io/v1alpha3
kind: DestinationRule
metadata:
    name: productpage
spec:
   host: productpage
   subsets:
   -    name: v1
        labels:
            version: v1
        trafficPolicy:
            connectionPool:
                tcp:
                    maxConnections: 3  ---> In this example, we limit the number of concurrent connecitons to 3...
DEMO
------

A/B Testing
--------------

A/B testing is a very popular and powerful approach to understand user behavior. It boosts experimentations and helps our software professionals to not guess how our applications will be interacted but to see it in real data.

with istio and virtual services, we can now create virtual service instead of services. and then define 2 destination routes for traffic destribution subset v1 and subset v2, and we set weight for each...

virtual service
---------------

        apiVersion: networking.istio.io/v1alpha3
        kind: VirtualService
        metadata:
            name: reviews
        spec:
            hosts:
                -   reviews
            http:
            -   route:
                -   destination:
                        host:   reviews    ---> name of the virtual services
                        subset: v1
                    weight: 99             --> traffic weight   

                -   destination:
                        host:   reviews        ---> name of the virtual services
                        subset: v2
                    weight: 1                  --> traffic weight

99% traffic will go to subset v1 and 1% will go to subsets v2. the number of instances now has nothing to do with the traffic distribution.

and we can easily control that through the virtual service configuration..



Security
-------------

jb aik service dosari service sa communicate krti ha. y possible ha k middle man communication ko intercept kr sakhta ha.. it is called man in middle attack..

is ko rokny k lye service k b/w communication encrypted honi chahye... for this istio allows to use **encryption** 

secondly certain services need to implement access control restrictions. so istio allows **mutual TLS** and fine gain access policies.

or kis na kya kyaaaa y check krny k lye. istio allows to use **audit logs**.

Istio security architecture
---------------------------


authenticaton:
--------------

agr aik service kisi dosary service k sath communication ker rhi ha tu dosari service ko pta hona chahye k y service kon si ha. 

so traffic b/w once service to others need to be verify...

-    mutaul tls 
-    json token 

with mutual TLS
---------------

with mutual TLS each service get its own identity with is enfore using certificate TLS... in certificates ki generation and distribution sab managed kerta ha **istiod**.

**another area to be authenticated is the end users access to services..**

For this istio support request **authentication using json web token validation** or **openid connect providers** some of which are **JWT, ORY Hydra, keycloak, firebase, google**  

example for peer authentication config
-------------------------------

authentication policies are defined by **peer authentication and request authentication**

        apiVersion: security.istio.io/v1beta1
        kind: peerAuthentication
        metadata:
            name:   "example-peer-policy"
            namespace: "book-info"
        spec:
            selector:
                matchLebels:
                    app: reviews
            mtls:
                mode: STRICT

this policy will only be effective on workloads labeled with **key app** and value **reviews**. and it says that these workload must strictly use **Mutual TLS**

is tarha sa apki policy sirf aik service per lg rhi ha jis k label **app: reviews** ha. agr ap na entire namespace ma mojood services per lgana ha tu ap **selector** ko hata dye...


like:
----

apiVersion: security.istio.io/v1beta1
kind: peerAuthentication
metadata:
    name:   "example-peer-policy"
    namespace: "book-info"
spec:



    mtls:
        mode: STRICT

ab y namespace wise policy bn gi ha. jo k namespace ma mojood sab workload per lg rhi hogi...


or agr ap apni policy file ma **namespace: "isti-system"** mention kr dety hn jo k actuclly ma istio ko apni namespace ha. so y policy entire mesh per lg rhi hogi...

like this.
---------

apiVersion: security.istio.io/v1beta1
kind: peerAuthentication
metadata:
    name:   "example-peer-policy"
    namespace: "istio-system"  ----> y root namespace istio ko apni namespace ha..
spec:



    mtls:
        mode: STRICT


DEMO
----


In this demo, we will see the difference b/w no peer authentication policy and mutual TLS enable.



Authorization
-----------------

Authorization in istio provides a flexible approach to access control for inbound traffic.

We can control which service can reach which service, which is referred to as east-west traffic using authorization configuration

how it works. and what about access control..

for example we need to only allow the product page service to access the review service and not the details or any other services.

also let say the product page service is only supposed to run GET calls to review service and not POST or UPDATE calls.


So for this purpose istio provides authorization mechanisms that allows us to define policies to allow or deny requests based on certain criteria.


As discussed before, these services do not require any changes to implement authorization.


This is implemented by envoy proxies authorization engine in runtime.

when a request comes through the proxy, the authorization engine evaluates the request context against the current authorization policies. and returns the authorization results either allow or deny.


There are 3 actions that authorization policies support,

**CUSTOM** It allows an extension to handle the request.
**DENY** It denies the request .
**ALLOW** it allows the request.

authorization policies can also be configured to audit requests.

with this option when a request hits the matching rule, it gets audited.


authorization policies examples..

apiVersion: security.istio.io/v1beta1
kind: AuthorizationPolicy
metadata:
    name: authdenypolicy
    namespace: bookinfo
spec:
    action: DENY
    rules:
    -   from:
        -   source:
            namespaces: ["bar"]
        to:
        -   operation:
                methods:    ["POST"]

***This policy denies all POST request frome the bar namespace to the bookinfo namespace...***


DEMO:
----

apiVersion: security.istio.io/v1beta1
kind: AuthorizationPolicy
metadata:
    name: *productpage-viewer*
    namespace: default
spec:
    selector:
        matchLabels:
            app: productpage
    action: ALLOW
    rules:
    - to:
      -  operation:
            methods: ["GET"]

allowing only get method...


and 

apiVersion: security.istio.io/v1beta1
kind: AuthorizationPolicy
metadata:
    name: *details-viewer*
    namespace: default
spec:
    selector:
        matchLabels:
            app: details
    action: ALLOW
    rules:
    -   from:
        -   source:
                principals: ["cluster.local/ns/default/sa/bookinfo-productpage"]
    - to:
      -  operation:
            methods: ["GET"]

            this policy allow service account to GET method in default namespace...

Certificate Management
----------------------

let have a look for certificate management in istio..


As we talked about it **istiod has a built in certificate authority**.

The istio agent creates a private key and a certificate signing request, and then sends the certificate signing request with its credentials to istiod for signing..


The CA in istiod validates the credentials carried in the CSR Upon successfull validation, it signs the CSR to generate the certificate.

The istio agent sends the certificates received from istiod and the private key to **envoy**

istio agent monitors the expiration of the workload certificate.

the above process repeats periodically for certificates and key rotation...

for production grade cluster, you should use a production-ready CA such as "HashiCorp vault"

and put your certificates in an oven machine or the fridge..


DEMO:
---- 

Let see how to configure istio with a root certificate of our own when we set up our istio cluster...

1- first we need to create a folder in istio root directory... and generate a root certificate with this command..

like:

    mkdir ca-certs
    
    cd ca-certs

    make -f ../tools/certs/Makefile.selfsigned.mk root-ca    ---> creating root certificate..


after this you will find for file.. named 

- root-ca.conf   --> it is the configuration for openssl to generate the root certificate..
- root-cert.csr  --> is a generated CSR for the root certificate.
- root-cert.pem  --> is a generated root certificate.
- root-key.pem  ---> is a generated root key..

root certificates should not be used directly, because it is very dangerous, and also not very practical to use them, here they are also created..


**before moving on i need to remind you that you need to delete if you pre-installed istio, or at least delete the istio system namespace to configure istio to use our certificates.** 

clean the istio default namespace "istio-system".. and create things again...

    kubectl creat namespace istio-system

and create certificate file as secret...

    kubectl create secret generic cacerts -m istio-system \
    --from-file=ca-cert_pem
    --from-file=ca-key.pem \
    --from-file=root-cert.pem \
    --from-file=cert-chain.pem

and again install the istio so that istio CA will read this certificates and key from the secret mount files.

**now up your neccesary files like gateway , virtual service , destination rule deployments.. and services....and also apply "authentication" policy...**

to only accept mutual TLS traffic...


like:

kubectl apply -f - <<EOF
apiVersion: security.istio.io/v1beta1
kind:   PeerAuthentication
metadata:
    name:   "default"
spec:
    mtls:
        mode: STRICT
EOF>>


now check if the workloads are signed with the exact same certificate

    kubectl exec "$(kubectl get pod -l app=details -o jsonpath=(.items..metadata.name))" -c istio-proxy -- openssl s_client -showcerts -connect productpage:9000 > httpbin-proxy-vert.txt

    make sure to wait 50sec at least..


lets check again.. and you will see the results..

kubectl exec "$(kubectl get pod -l app=details -o jsonpath=(.items..metadata.name))" -c istio-proxy -- openssl s_client -showcerts -connect productpage:9000 > httpbin-proxy-vert.txt


like..  

    verify error:num19:self signed certificate in certificate chain    ... this error is expected..

    DONE..


now in this file **httpbin-proxy-vert.txt** we have all the certificate information..

and we will clear the rest of the certificates details with the SED commands...


**sed -ne '/-----BEGIN CERTIFICATE------/,/------END CERTIFICATE-----/p' httpbin-proxy-cert.txt | sed 's/^\s *//' > certs.pem**


cat certs..  ---> here are the certificate extracted b/w 2 services...

you can split this into 4 different files..

**NOw, we will verify if the root certificate is the same as the one we specified**..


**openssl x509 -in ca-certs/localcluster/root-cert.pem -text -noout > /tmp/root-cert.crt.txt**  --> dump certificate information of a root certificate...


**openssl x509 -in ./proxy-ca-certs3.pem -text -noout > /tmp/pod-root-cert.crt.txt**  ->> dump certificate information of a we just extracted from the traffic itself...

let check these matches. it should be identical..

diff -s /tmp/root-cert.crt.txt /tmp/pod-root-cert.crt.txt


also verify the CA certificate both should be matched...


also verify the certificate chain both should be matched...

OBservations
-----------

- KAILI  DASHBOARD
- Visualizing metrics with promethous and grafana
- Distributed tracing with Jaegar


































