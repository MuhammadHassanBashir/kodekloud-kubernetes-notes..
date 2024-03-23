eted
----  

It is a reliable key values store that is sure and fast. y sary cluster sa related information ko apny under store kerta ha, ap jb "kubectl get "ki command ko use kerty hn tu is server sa hi kube-api server apko data retrive ker k la ker deta ha... ap binary sa isko install ker sakhty hn, ap is ma kude sa data put b ker sakhty hn "etcdctl set key1 value1" and with get you can get the data..

Information like.

-nodes,pods,config,secrets,service account,role binding 

kube api server
---------------

y primary management component ha.. jb hum koi command terminal sa execute kerty hn like "kubectl get po" tu y command kube api server per jati ha, kube api server isko phily authentication and validate kerta ha, phir kube-api server apko etcd sa data retrive ker k la ker deta ha..

1- authentication
2- Validate Request
3- Retrieve data
4- Update etcd
5- Scheduler
6- Kubelet

example of create pod and function worked behind..
--------------------------------------------------

1-jo terminal sa hum pod create kerny k lye command ko use kerty hn tu is k behind kya kya process hoty hn... command sab sa phily cluster ma kube-api server sa interact kerti ha... 
2- kube api server isko authenticate or validate kerta ha,, then pod creation ki information ko etcd ma update kerta ha.. 
3- Scheduler etcd ma unschedular pod sa related information ko observer kerta ha.. or then us pod k resources k according node ko search kerta ha jub wo node select kerta then kube-server ko infor kerta ha or kube api server us worker node ma kubelet ko inform kerta ha or kubelet pod create kerta ha or CRI ko khta ha k is ma application image ko update kery.. 
4- then kubelet y sari information ko api-server ko btata ha kerta ha or kube api server etcd ma information update kerta ha k pod kis node ma schedule hoi ha...


ap binary k through kube api server ko install ekr sakhty hn... or kubeadm sa kry gye tu y kube-system ma as pod bny ga.. iski jb hum manifest file open kery gye tu hmy is ma etcd k address mily ga... is address ka through y etcd sa communication ker rha hota ha..

kube-controller
---------------

kubecontroller cluster k aik important component ha... kubernetes ki term ma y aik process ha job continously monitor kerta ha state of various component and bringing toward the whole system to the desire state..

1- node controller 

    y node k status ko monitor kerta ha or neccessay action kerta if require to keep the applicaiton running.

    node controller y kube api server k through nodes ko monitor ekr rha hota ha or every 5s ma node ki health ko check kerta ha k sab nodes reachable hn k ni.. or agr koi node unreachable hoti ha tu wo isko 40s tk wait kerta ha unreachable kerny sa phily agr wo reacable ni hoti tu wo isko unreachable ki state ma dal dye ga or agr wo relicaset ka through bani ha tu wo isko again create kery ga...

2- Relication controller

    y continously pod k status ko monitor kerta ha, or ensure kerta ha k desire no of relicas running ma rhy. if pod dies, it will create it again...

y sirf 2 example hn , jitny b intelligence base kam hoty hn wo kisi na kisi controller sa horhy hoty hn... jo k kubecontroller ma hoty hn...

list of used controller
----------------------

1-node controller
2-replication controller
3-replicaset
4-deployment controller
5-stateful-set
6-Namespace-controller
7-service account controller
8-cronjob
9-namespace-controller
10-PV-Binder-controller
11-endpoint controller
12-pv protection controller

it is a brain behind kubernetes.. y sab kubernetes controller manager ma hoty hn... ap kubernetes controller manager ko cluster ma ker sakhty hn kubernetes release page sa..

by default sab controller enable hoty hn, but ap apni marzi k according jin jin ko disable kerna hota ha disable ker sakhty hn,.

agr isko veiw kerna ha tu kubeadm sa install kry gye tu y kube-system ma as pod bny ga..  or apko "ps -aux | grep kube-controller-manager" sa b running proccess dekh sakhty hn k wha cheezy pari hn,

3- kube-Scheduler

    it is using for scheduling the pod on the node... but remeber y khud y kam ni kerna y pod ki requirement mean require resources k according best node select kerta ha or btata ha k kis node ma pod jye gye... or basically api-server us node jis ko kube sedular na pod k lye select kya ha iska kubelet ko instruct kerta ha or kubelet ha wo jo basically us node ma pod ko bnata ha or CRI k through is ma image update kerwata ha..

    ap pod ki scheduling apny according ma ker sakhty hn... with 

    1- resource requirements and limits
    2- Taints and Tolerations
    3- Node Selector/Affinity

    bnaniers k through ap inko install ker sakthy hn.. or veiw ker skahty hn...  "ps -aux | grep kube-scheduler" sa running process ko grap ker sakhty hn...

4- kubelet

    - Register the Node in the cluster        
    - Create Pod on the node

        kube scheduler jb pod k lye node k btata ha tu kube api server us node ma kubelet ko pod create kerny k khta ha... kubectl pod create kerna ha or cri ko khta ha wo require image ko pull ker k us pod ma application container run kery,,, or phir kubeapi server k though etcd ko update kerna ha.. kubelet sa hi node ki sari information kube api server ko jati hn..
    - monitor node and pod

        y node or pod ko monitor kerta ha or in sa related information ko kube api ko update kerta ha..

    kubelet kubeadm k through install ni hota... apko sab nodes ma one by one ker k install kerna parta ha...  ps -aux | grep kube-scheduler" sa running process ko grap ker sakhty hn...

    "learn later" 

        - how to configure kubelet
        - Generate certificate
        - How to tls boot trap kubelet later in this course..

5- Kube proxy

    y node ki networking k lye use hota ha... pod to pod communication k lye pod k network use hota ha... because pod crush or recreate k case ma pod k ip change hosakhta ha is lye service k though pod k sath communication kerty hn, service apny behind pod ka ip ko resource ker rhi hoti ha mean jo request service per ati ha wo us k behind pod per jye gi... ab service cluster k component ha.. so node ma kube proxy hoti ha jo service tk jany k lye ip route create krti ha. jis sa aik pod dosary pod tk through service chala jata ha.. kube proxy route ma service ip or destination pod ip btati ha... jis sa aik source pod destination pod tk jata ha..

        
        pod to pod communication
        ------------------------

        Kubernetes Networking Model

            Pod-to-Pod Communication within the Same Node:

                When multiple pods are scheduled on the same node, they can communicate with each other directly using localhost or the loopback interface.

            Pod-to-Pod Communication across Nodes:

                When pods need to communicate across different nodes in the cluster, Kubernetes employs various networking solutions, such as Container Network Interfaces (CNIs) and software-defined networking (SDN) technologies. These solutions create a virtual network overlay that spans the entire cluster, enabling pod-to-pod communication across nodes. Some popular CNIs include Calico, Flannel, Weave, and Cilium. These networking solutions ensure that the pod’s IP address remains reachable and provides transparent network connectivity regardless of the pod’s location within the cluster.

        Cluster-Internal Communication
            
            By default, pods within a Kubernetes cluster can communicate with each other using their internal IP addresses. This communication happens over a virtual network overlay provided by the underlying container runtime or network plugin. 

        DNS-Based Service Discovery

        Service Load Balancing

        Network Policies

        External Communication

        Service Mesh
            
            For advanced networking scenarios, a service mesh can be employed to enhance pod-to-pod communication. A service mesh, such as Istio or Linkerd, sits as a layer on top of the Kubernetes cluster and provides features like traffic management, observability, and security. With a service mesh, you can control and monitor the communication between pods with advanced routing rules, circuit breaking, and distributed tracing.


pod with YAML
------------

apiversion: v1
kind: Pod
metadata:  -------------->dictionary-------------------metadata ma define information k alws koi or information ni aye gi.. but label ma ap jitny b chahye labels bna sakhty hn
    name: myapp  ---------> sibiling
    labels: ------------ dictionary
        app:myapp
        type: front-end
        tier: fronted
spec:--------------------------> dictionary
    containers: -------------------> List/Array
        - name: nginx-containers                       "-" indicate k y array k first element ha. 
          image: nginx                                 "if your image is placed on the dockerhub then you have to give the full path here"
        - name:                                        "In that way you can create other containers as well" 
          image:    
once file done.. you can create pod with command...

    kubectl create -f filename.YAML        "create/apply command both works same if you are creating the new object"

see the pod

    kubectl get pod
    kubectl describe pod "podname"    "koi b issue hum describe or logs ki command sa dekh sakhty hn"

declarative way to create pod
-----------------------------

kubectl run "nameofpod" --image ""

apiversions
-----------
POD------> v1
Service------->v1
ReplicsSet------->apps/v1
Deployment-------->apps/v1

ReplicSets
----------

replication controller..
------------------------ 
1- it continously monitor all pod on the nods through api server, if any issue accure with pods it can bring it back to normal state. if pod of node get crush it will re-create and maintain the desire state.
2- scaling: if the traffic on application pod increases, it will simply scale the application pod across node.
 

replication controller is older and replicaset is newer and recommended...

replication controller yaml file
--------------------------------

apiversion: v1
kind: ReplicationController
metadata:  -------------->dictionary-------------------metadata ma define information k alws koi or information ni aye gi.. but label ma ap jitny b chahye labels bna sakhty hn
    name: myapp  ---------> sibiling
    labels: ------------ dictionary
        app:myapp
        type: front-end
        tier: fronted
spec:--------------------------> dictionary(ReplicationController)
    replicas: 3  ----------------(no of pod in ReplicationController)
    template:-----------------==>(pod)
        metadata:  -------------->dictionary-------------------metadata ma define information k alws koi or information ni aye gi.. but label ma ap jitny b chahye labels bna sakhty hn
            name: myapp  ---------> sibiling
            labels: ------------ dictionary
                app:myapp
                type: front-end
                 tier: fronted
        spec:--------------------------> dictionary
            containers: -------------------> List/Array
                - name: nginx-containers                       "-" indicate k y array k first element ha. 
                  image: nginx 

then create: 
-----------
once file done.. you can create pod with command...

    kubectl create -f filename.YAML        "create/apply command both works same if you are creating the new object"

see the pod

    kubectl get pod
    kubectl describe pod "podname"    "koi b issue hum describe or logs ki command sa dekh sakhty hn"

replicaset and ReplicationController are difference at somewhere..

ReplicSet 
---------

apiversion: apps/v1  ---------->(different from ReplicationController)
kind: ReplicaSet
metadata:  -------------->dictionary-------------------metadata ma define information k alws koi or information ni aye gi.. but label ma ap jitny b chahye labels bna sakhty hn
    name: myapp  ---------> sibiling
    labels: ------------ dictionary
        app:myapp
        type: front-end
        tier: fronted
spec:--------------------------> dictionary(ReplicaSet)
    selector: ------------------------------------------>(different from ReplicationController) 
        matchLabels:    
            type: front-end -------------------------------------------->(matches labels of the pods)
    replicas: 3  ----------------(no of pod in ReplicaSet)
    template:-----------------==>(pod-section)
        metadata:  -------------->dictionary-------------------metadata ma define information k alws koi or information ni aye gi.. but label ma ap jitny b chahye labels bna sakhty hn
            name: myapp  ---------> sibiling
            labels: ------------ dictionary
                app:myapp
                type: front-end
                tier: fronted
        spec:--------------------------> dictionary
            containers: -------------------> List/Array
                - name: nginx-containers                       "-" indicate k y array k first element ha. 
                  image: nginx 

then create: 
-----------
once file done.. you can create pod with command...

    kubectl create -f filename.YAML        "create/apply command both works same if you are creating the new object"

see the pod

    kubectl get pod
    kubectl get replicaset
    kubectl describe pod "podname"    "koi b issue hum describe or logs ki command sa dekh sakhty hn"

#####it's like letter having envolop### on the letter we have apiversion,kind,metadata and inside envolop we have spec

Scale
-----

1- for scaling, edit the yaml file and increase the replicas value... it will scale the no of pods..

    then use "kubectl replace -f .yamlfile" for apply the new changes..

2- 2nd way for scale.. "kubectl scale --replicas="updatedno" -f .yamlfile"

3- kubectl scale --replicas="updateno" replicaset myapp-replicaset..   # here replicaset is type and myapp-replicaset is name...

there is another way where replicas can automatically scale up. once having traffic load on it..

for deleting
------------

    kubectl delete replicaset "replicasetname"

explain
-------

    kubectl explain replicaset...        "this command is use to see the exact format.."

Deployment
----------
it is a kubernetes object, it provide the capability to upgrade the underline instances seemlessly using rolling update.

we have other deployment stratgies as well... or agr deploy ma koi masla ajye tu ap usy undo b ker sakhty hn..   

and replicaset and deployment both are almost same... only the kind section is change..


apiversion: apps/v1  ---------->(different from ReplicationController)
kind: Deployment  -------------->(difference from replicasets)
metadata:  -------------->dictionary-------------------metadata ma define information k alws koi or information ni aye gi.. but label ma ap jitny b chahye labels bna sakhty hn
    name: myapp  ---------> sibiling
    labels: ------------ dictionary
        app:myapp
        type: front-end
        tier: fronted
spec:--------------------------> dictionary(ReplicaSet)
    selector: ------------------------------------------>(different from ReplicationController) 
        matchLabels:    
            type: front-end -------------------------------------------->(matches labels of the pods)
    replicas: 3  ----------------(no of pod in ReplicaSet)
    template:-----------------==>(pod-section)
        metadata:  -------------->dictionary-------------------metadata ma define information k alws koi or information ni aye gi.. but label ma ap jitny b chahye labels bna sakhty hn
            name: myapp  ---------> sibiling
            labels: ------------ dictionary
                app:myapp
                type: front-end
                tier: fronted
        spec:--------------------------> dictionary
            containers: -------------------> List/Array
                - name: nginx-containers                       "-" indicate k y array k first element ha. 
                  image: nginx 

then create: 
-----------
once file done.. you can create pod with command...

    kubectl create -f filename.YAML

    once deployment creation done it will automatically create the replicaset..
 
    kubectl get deployments
    kubectl get replicaset
    kubectl get pods
    kubectl get all

'''Here’s a tip!

As you might have seen already, it is a bit difficult to create and edit YAML files. Especially in the CLI. During the exam, you might find it difficult to copy and paste YAML files from browser to terminal. Using the kubectl run command can help in generating a YAML template. And sometimes, you can even get away with just the kubectl run command without having to create a YAML file at all. For example, if you were asked to create a pod or deployment with specific name and image you can simply run the kubectl run command.

Use the below set of commands and try the previous practice tests again, but this time try to use the below commands instead of YAML files. Try to use these as much as you can going forward in all exercises

Reference (Bookmark this page for exam. It will be very handy):

https://kubernetes.io/docs/reference/kubectl/conventions/

    Create an NGINX Pod

    kubectl run nginx --image=nginx

Generate POD Manifest YAML file (-o yaml). Don’t create it(–dry-run)

    kubectl run nginx --image=nginx --dry-run=client -o yaml

Create a deployment

    kubectl create deployment --image=nginx nginx

Generate Deployment YAML file (-o yaml). Don’t create it(–dry-run)

    kubectl create deployment --image=nginx nginx --dry-run=client -o yaml

Generate Deployment YAML file (-o yaml). Don’t create it(–dry-run) and save it to a file.

    kubectl create deployment --image=nginx nginx --dry-run=client -o yaml > nginx-deployment.yaml

Make necessary changes to the file (for example, adding more replicas) and then create the deployment.

    kubectl create -f nginx-deployment.yaml

OR

In k8s version 1.19+, we can specify the –replicas option to create a deployment with 4 replicas.

    kubectl create deployment --image=nginx nginx --replicas=4 --dry-run=client -o yaml > nginx-deployment.yaml
'''

Services
--------

serivices enable communicate b/w various component within and outside of the application.

note: internal pod network sa pod ip leta ha...

one of the use case of service is it listen the traffic coming to the nodeport and forward request on that pod to a port on the pod running the web application.. this type of service is nodeport service..

mostly aaj kal cloud ma hi kubernetes ki deployment hoti ha so hum service type loadbalance use kerty hn for standard way to accept the traffic coming from outside. or isi service ma hum loadbalancer k lye certificate b create ker k "annotation" seciton ma dety hn. tky certificate loadbalancer k sath attach hojye... service ma type loadbalancer select kerny sa kubernetes actual ma cloud ma load balancer create ker deta ha job http/https per listen ker rha hota ha apki request ko or node port per forward kerta ha or waha sa service or serivice backend pod per  jrhi hoti ha.. describe serivice for troubleshooting kerty time ap endpoint dekh sakhty hn k node ko mila ha k ni...
serive type
-----------

- nodeport     nodeport port range 30000 to 32766. it open the port on all the nodes inside the cluster and forward that traffic coming on that node to internal serivice.. and then from serivce to pod port where web application running...
- cluster ip  --> y default serivice type ha. y inside the cluster various component ki communication k lye use hoti ha. clusterip k case ma service virtual ip create kerti ha inside the cluster to enable communication b/w different services such as frontend pod(servers) communicate to backend
- loadbalancer  ---> it is a standard way to communication accept the traffic coming from the internet to node..

note: toport or targetport dono same b hosakhti ha or different b... agr ap toport koi set ni kerty tu wo targetport wali port ko toport consider ker lye ga... and if you donot set the nodeport then free port invilid range will set to nodeport...

example of nodeport:
-------------------

apiVersion: v1
kind: Service
metadata:
    name: my-appservice
    labels:
        type: my-appservice
spec:
    selector:         --------> with this thing(mean with selector and label) basically we are selecting the pod for this service from all the other pods..  mean link service with pod..
        type: front-end    ------->
    type: NodePort  ---------use case when use on prime or directly access the service from nodeip without loadbalancer...
    ports: ------------------------------> list/array
     - targetport: 80  ----------> pod port, where pod expose
       port: 80 ----------------->  where service expose..
       nodeport: 30008 

pod can be expose with serivice....


then create: 
-----------
once file done.. you can create pod with command...

    kubectl create/apply -f filename.YAML

    kubectl get services
    
    curl http://nodeip:nodeport

with the case of same application running on multiple pod. you can set same labels on each pod and select that label from service.. 

cluster ip
----------

apiVersion: v1
kind: service
metadata:
    name: back-end
    label:
        type: backend
spec:
    selector:   -----------link(select) service with backend pod..
        type: back-end
    type: ClusterIP
    ports:
        targetport: 80           where pod expose
        port: 80                where service expose

then create: 
-----------
once file done.. you can create pod with command...

    kubectl create/apply -f filename.YAML

    kubectl get services


loadbalancer   it is a standard way to accept the traffic from internet..
------------   

for loadbalancer service case you just need to change the nodeport service to loadbalancer, else same.. loadbalancer will send the traffic to nodeport and from nodeport to service and then backend pod. kuberneter support that once we uses loadbalancer in that case gcp/aws/azure will create a native loadbalancer in cloud...   (you can provision loadbalancer in vm)

apiVersion: v1
kind: Service
metadata:
    name: my-appservice
    labels:
        type: my-appservice
spec:
    selector:         --------> with this thing(mean with selector and label) basically we are selecting the pod for this service from all the other pods..  mean link service with pod..
        type: front-end    ------->
    type: Loadbalancer  ---------use case when use on prime or directly access the service from nodeip without loadbalancer...
    ports: ------------------------------> list/array
     - targetport: 80  ----------> pod port, where pod expose
       port: 80 ----------------->  where service expose..
       nodeport: 30008 

then create: 
-----------
once file done.. you can create pod with command...

    kubectl create/apply -f filename.YAML

    kubectl get services

----------
remember
----------

    service create kerty time jb hum pod ko service sa select(link) kery gye tu hum service k selector ma "matchLabels" use ni kery gye.. sedha serivce ka selector ma jo b label pod k set kya ha wo dye gye... 


Namespace
--------- you can create your saparate isolate enviroment with namespaces and provision resource in that enviroment.. 

by-default we have namespaces like....

- default
- kubesystem
- kubepublic

example:

1- let say you have your webapp as pod in one namespace that need to connect with db that are also in the same namespace..

    mysql.connect("db-service")  --> define in webapp

2- now web-app and db service both are in saparate namespace. how to connect in that case...

    mysql.connect("db-servicename on other namespace."othernamespace-name".svc.cluster.local")

    #- db-servicename on other namespace 
    #- namespace --> name of the namespace
    #- svc --> is the sub domain.
    #- cluster.local--> is the default name of the kubernetes cluster

remember
----------

by default all resources default namespace ma create hoty hn... other namespace ma create kerny k lye apko, resource creation command k sath namespace b mention kerni hoti ha...

same jb him  "get" ki command use kerty hn tu etcd humy default namespace ma pari resource ki information share kerta ha.... other namespace ki information leny k lye us namespace k name b apko btana hoga...

create namespace
----------------

apiVersion: v1
kind: Namespace
metadata:
    name: dev

command:
    kubectl create -f namespace.yaml

create namespace with command
-----------------------------

    kubectl create namespace dev


pod example with namespace:
--------------------------

apiVersion: v1
kind: Pod
metadata: 
    name:
    labels:
        app: myapp
    namespace: dev
spec:
    containers:
        - name: nginx-container
          image: nginx
          port:
            - name:
              port:

-------------
remember
-------------

same jb him  "get" ki command use kerty hn tu etcd humy default namespace ma pari resource ki information share kerta ha. hum is bahviour ko change ker sakhty hn.. or kisi or namespace ko as default namespace set ker sakhty hn.. 

    kubectl config set-context $(kubectl config current-context) --namespace=dev

ab jis namespace ko apna default rakha ha us k alwa namespaces k lye apko command k sath namespace k name btana hoga...

get for all pod
---------------

    kubectl get pod --all-namespaces
    kubectl get pod -n namespace

with resource quota
-------------------

    to limit resources within a namespace we can create a resource quota..

resource quota yaml file:
-------------------------

    apiVersion: v1 
    kind: ResourceQuota
    metadata
        name: compute-quota
        namespace: dev
    spec:
        hard:
            pods: "10"
            requests.cpu: "4"
            requests.memory: 5Gi
            limit.cpu: "10"
            limit.memory: 10Gi

Imperative/declarative
----------------------

Imperative appraoch to manage the object in kubernetes...

create object
-------------
- kubectl run nginx --image=nginx  ---------> create pod
- kubectl create deployment nginx --image=nginx  ---------> create deployment
- kubectl set image deployment nginx --image=nginx:1.18
- kubectl expose deployment nginx --port 80 --------> expose service

update object
-------------
- kubectl edit deployment nginx  ------> edit existing running deployment, just edit it will update the effect on running deployment.
- kubectl scale --raplicas=3 -f filename.yaml
- kubectl scale deployment nginx --replicas=5
- kubectl set image deployment nginx --image=nginx:1.18

- kubectl create -f nginx.yaml     ---> create the file...
- kubectl replace -f nginx.yaml  ---> let assume you have a deployment file name as nginx.yaml. and you have applied the changes with this file in infrastructure... but you need to make some change.. 1way to make edit the existing running deployment, 2nd way is, you have the deployment file in your local system... make changes on that file and use the replace command.. it will update the infrastructer..  
- kubectl replace -f nginx.yaml  ---> sometime you need to do this forcefully...
- kubectl delete -f nginx.yaml ---> it would delete the effect


you can update the same thing with "apply" command.. kubernetes is smart enough to observer the already created object in order to make update on object yaml file.. and apply yaml file with apply command... it will update the changes on existing running object...

"While you would be working mostly the declarative way – using definition files, imperative commands can help in getting one time tasks done quickly, as well as generate a definition template easily. This would help save considerable amount of time during your exams.

Before we begin, familiarize with the two options that can come in handy while working with the below commands:

--dry-run: By default as soon as the command is run, the resource will be created. If you simply want to test your command , use the --dry-run=client option. This will not create the resource, instead, tell you whether the resource can be created and if your command is right.

-o yaml: This will output the resource definition in YAML format on screen.

 

Use the above two in combination to generate a resource definition file quickly, that you can then modify and create resources as required, instead of creating the files from scratch.

 

POD
Create an NGINX Pod

    kubectl run nginx --image=nginx

 

Generate POD Manifest YAML file (-o yaml). Don’t create it(–dry-run)

    kubectl run nginx --image=nginx --dry-run=client -o yaml

 

Deployment
Create a deployment

    kubectl create deployment --image=nginx nginx

 

Generate Deployment YAML file (-o yaml). Don’t create it(–dry-run)

    kubectl create deployment --image=nginx nginx --dry-run=client -o yaml

 

Generate Deployment with 4 Replicas

    kubectl create deployment nginx --image=nginx --replicas=4

 

You can also scale a deployment using the kubectl scale command.

    kubectl scale deployment nginx --replicas=4 

Another way to do this is to save the YAML definition to a file and modify

    kubectl create deployment nginx --image=nginx --dry-run=client -o yaml > nginx-deployment.yaml

 

You can then update the YAML file with the replicas or any other field before creating the deployment.

 

Service
Create a Service named redis-service of type ClusterIP to expose pod redis on port 6379

    kubectl expose pod redis --port=6379 --name redis-service --dry-run=client -o yaml

(This will automatically use the pod’s labels as selectors)

Or

    kubectl create service clusterip redis --tcp=6379:6379 --dry-run=client -o yaml (This will not use the pods labels as selectors, instead it will assume selectors as app=redis. You cannot pass in selectors as an option. So it does not work very well if your pod has a different label set. So generate the file and modify the selectors before creating the service)

 

Create a Service named nginx of type NodePort to expose pod nginx’s port 80 on port 30080 on the nodes:

    kubectl expose pod nginx --type=NodePort --port=80 --name=nginx-service --dry-run=client -o yaml

(This will automatically use the pod’s labels as selectors, but you cannot specify the node port. You have to generate a definition file and then add the node port in manually before creating the service with the pod.)

Or

    kubectl create service nodeport nginx --tcp=80:80 --node-port=30080 --dry-run=client -o yaml

(This will not use the pods labels as selectors)

Both the above commands have their own challenges. While one of it cannot accept a selector the other cannot accept a node port. I would recommend going with the `kubectl expose` command. If you need to specify a node port, generate a definition file using the same command and manually input the nodeport before creating the service.

Reference:
https://kubernetes.io/docs/reference/generated/kubectl/kubectl-commands

https://kubernetes.io/docs/reference/kubectl/conventions/""...

create pod and expose it on same command:
-----------------------------------------

    kubectl run httpd --image=httpd:alpine --port=80 --expose=true---> mean pod create ker rha ho jis ma container ma image httpd:alpine hogi or wo container port 80 per expose hoga. or sath hi cluster service b create hogi... 






