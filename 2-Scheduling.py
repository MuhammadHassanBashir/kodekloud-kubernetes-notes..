Manual scheduling
-----------------

hota yha k jb hum kubectl k through pod creation ki command use kerty hn tu hmri command kube api server per jati ha. kube api server isko authenticate or validate kerta ha or etcd jo pod creation k lye update kerta ha. abi etcd ma pod pending state ma hoti hn.. is state ko kube schedular observe kerta ha or pod scheduling k lye node find kerta ha or is node ko etcd ma update kerta ha... mean pod ab selected node ma jye gi.. or kubeapi server is information ko etcd sa read kerta ha or kubelet ko us node ma inform kerta ha, or kubelet pod create kerta ha.... is tarha sa us node ma pod create hoti hn..

ab kya ho agr hmry ps kube schedular cluster ma as pod run na horha ho kubesystem ma .. is case ma jb kubeapi server etcd ma pod ko update kery ga.. tu pod pending rhy gi because us pod ki scheduling k lye node search kerny wala kube schedular hi ni ha... 

so is case ma pod ki scheduling kerny k lye hum "manual scheduling" use krty hn jis ma hota y ha k hum pod ki yaml file ma hardcordedly likh dety hn nodename jaha per pod na jana ha.... jis ko api server etcd ma update kerta ha or pod ko us node ma provision kerta ha...

likethis..

apiVersion: v1
kind: Pod
metadata:
  name: nginx
spec:
  containers:
  -  image: nginx
     name: nginx
     ports:
       - ContainerPort: 8080
  nodeName: node01   ----------> pod ki yaml file ma hardcordedly likh dety hn nodename jaha per pod na jana ha.... jis ko api server etcd ma update kerta ha or pod ko us node ma provision kerta ha...

2nd we can do this with "binding" as well..

apiVersion: v1
kind: Binding
metadata:
  name: nginx
target:
    apiVersion: v1
    kind: Node
    name: node01 -------> name of the node

Labels and Selector
-------------------

it is a standard method to group thing together..


command to select pod with labels
---------------------------------

    kubectl get pod --selector "app=App1"  ----> get the pod that have this label
    kubectl get all --selector "app=App1"  -----> it will get information of all resources that have this label..
    kubectl get pod --selector "env=prod,bu=finance,tier=frontend"  ---> get the pod that have 3 labels..
    kubectl get pod --selector "app=App1" --no-headers | wc -l --> get output in no...
Annotations:
-------------

it is use to record information for informatory purpose...

check error method
------------------

agr kisi file ma error ha.. tu hum isko simply apply ker tu wo apply tu ni hogi but humy file k error zaroor btye gi k khana ha... or ap error "describe" or "logs" dono sa pta ker sakhty hn

Taints and Tolerations
----------------------

with this we can restrict what pod will go to what nodes... it has nothing to do with the security but its a basic rule so Tolerations pod will go to the taints node..

use case: let say we have a dedicated resources in node1 for a perticular use case.. so hum chahye gye k un pod ko jin ka is node ka resources sa taluk ha wo isy node ma schedule ho... so taint and Tolerations sa y possible hoga... is sa hoga y k taint node kisi b pod ki scheduling ko accept ni kery gi siway us Tolerations pod k.. is trha sa hmra pod successfully schedul hojye us node ma jha per dedicate resouces pary hn mean jis node per hum pod ko bhjana chahty thy..

Tainsts -Node
-------------

    kubectl taint node "node-name" key=value:taint-effect  --> command to set taint on node..

    we have 3 taint effect... ---> taint effect means what happend to the pods that do not tolerate this taints

    - NoSchedule  ---> mean non Tolerations pod will not be schedule to taint node ... and maybe(need to check) existing non toleration pod on taint node would left that node..
    - PreferNoSchedule  --> mean system will try to avoid to place those pod that have no Tolerations to the taint node but have no gurantee.. 
    - NoExecute  ---> mean new non Tolerations pod will not be schedule to taint node. but the existing none Tolerations pods on this node will execute..

    kubectl taint node node app=blue:NoSchedule


yaml example:
------------

apiVersion: v1
kind: Pod
metadata:
  name: nginx
spec:
  containers:
  -  image: nginx
     name: nginx
     ports:
       - ContainerPort: 8080
  tolerations:  ---list/array
  - key: "app"
    operator: "Equal"
    value: "blue"
    effect: "NoSchedule" 

note: i have seen if i set taint on node and not set tolerations on pod according to taint node then no toleration pod will go to taint node...

limitation:
----------

hum na node ko taint ker k set ker lya ha k wo non toleration pod ko accept ni kery gi or toleration pod ko accept kery gi.. but is cheez ki gurantee ni ha k toleration pod is cheez k lye restrict ha k wo taint node ma hi schedule ho wo ho b sakhti ha or ni b hosakhti...  pod per restriction k lye hum node Affinity ko use kerty hn..

remember to note:
----------------

hum na y note kiya ha sab node per scheduling hojati ha but new pod ki masternode(controlplane) scheduling ni hoti. iski waja y ha k master node per start sa hi by default taint for NOSchedule set hota ha... is lye is per pod schedule ni hota or best practices b y hi ha...

command to check this
---------------------

    kubectl describe node kubemaster | grep taint

Untaint the node
----------------

To untaint a node in Kubernetes, you can use the kubectl taint command with the - prefix to remove the taint. The syntax is as follows:

    kubectl taint nodes controlplane node-role.kubernetes.io/control-plane:NoSchedule-      -----> same command like taint but end with "-" to untaint the node...

    kubectl taint nodes node01 app=blue:NoSchedule-      -----> same command like taint but end with "-" to untaint the node...


Node Selector
-------------

node selector sa hum apni pod ko jis node ma schedule kerna chahye ker skahty hn..

let discuss a scenarios we have 3 node(node1 , node2 , node3), node1 have a high resource then other node... and we also have a data process image that need high pod resource. so it need to schedule this pod on a node that has high resource..

so what to do:
-------------

1- Humy simply us node per label lagana ha jis node per hum apni pod ko move kerna chahty hn. 

    kubectl label nodes "node-name" "label-key=label-value"

    like:

    kubectl label nodes node-1 size=large             ---> set label no node. here size=large is a label key and value.
    
    once it done. now give this label in your pod.yaml file under nodeselector. so kubernetes samj jye ga ka is pod na kis node ma schedule hona ha...

yaml example:
------------

apiVersion: v1
kind: Pod
metadata:
  name: nginx
spec:
  containers:
  -  image: nginx
     name: nginx
     ports:
       - ContainerPort: 8080
  nodeSelector:
    size=large

limitation:
----------

node selector work for the simple condition. but it will not work with the difficult condition like "OR and NOT"... 

like: 

- pod find node that have large OR medium resources.... 
- not small..

for difficult condition we use "node Affinity"

Node Affinity
-------------


let discuss a scenarios we have 3 node(node1 , node2 , node3), node1 have a high resource and node2 has medium resources and node3 has small resource... 

now this time a want k meri pod higher or medium resource wali node ma jye... nodeselect ma hum or , not use ni kerskhty thy waha simple chalta tha...

what gona do
------------

1- First need to set the label on nodes... with command like "size=large" on high resource node and "size=medium" on medium resource node

    kubectl label nodes node-1 size=large 
    kubectl label nodes node-2 size=medium

2- Now give this label as value to that pod, which you want to schedule on nodes...

yaml example:
------------

apiVersion: v1
kind: Pod
metadata:
  name: nginx
spec:
  containers:
  -  image: nginx
     name: nginx
     ports:
       - ContainerPort: 8080
  affinity:
    nodeAffinity:
        requiredDuringSchedulingIgnoredDuringExecution:  ----> type of node affinity(simply tell what it gona do, if  he cannot find the mention label on node..)
            nodeSelectorTerms:  ---> list/array
            - matchExpressions:
              - key: size           ----------> label is "siz in large or medium" 
                operator: In
                values:  -------->list/array
                - Large
                - Medium                   ----> you can add list of value labels at once..  

            or

            - matchExpressions:
              - key: size           ----------> label is "siz in large or medium" 
                operator: NotIn
                values:  -------->list/array
                - small      ----> you can add list of value labels at once..  
            or   
            - matchExpressions:
              - key: size           ----------> label is "size" 
                operator: Exists ----> it simply check the label is exist 
example:

affinity:
        nodeAffinity:
          requiredDuringSchedulingIgnoredDuringExecution:
            nodeSelectorTerms:
            - matchExpressions:
              - key: color
                operator: In
                values:
                - blue

type of node affinity
---------------------

    simply tell what it gona do, if  he cannot find the mention label on node..

Available:
    1- requiredDuringSchedulingIgnoredDuringExecution (summary: pod ki node ma scheduling k time label match hoga. hogya tu schedule ker dye ga ni howa tu pending ma rhy ga pod or schedule node ma pod hony k bd node k label change b hojye tu pod node ma ha rhy ga..)                                               ---> "requiredDuringScheduling" DuringScheduling is a state where a pod does not exist and create for the first time(schedule for the firsttime)... so affinity rule takeplace to place the pod at right node.. what if k node per label available na ho. mean you forget to add label on node. where type of node affinity comes into play... if you select the type "required" it mean the schedular will mandaded(mandatory(lazmi)) node affinity rule k according label match kerty howy pod ki node ma scheduling kery ga.. agr usko pod per dya label kisi node per ni mily ga tu wo pod schedule(pending ma rhy ga) ni hoga. use case pod place on set node is crucial(importane).. summary "required" mean label match compulsary ha otherwise pod schedule ni hoga.. now  "Ignoredduringexecution" let say k hmry pods node ma schedule hogy thy or apna kam ker rhy thy..ab hota kya ha k enviroment ma koi changes ker deta ha mean node k label ko change ker deta ha... ab asolan node affinity k rule k according pod ko node chore deni chahye but "ignoreDuringExecution" set kerny k waja sa jo pods node ma schedule hogi hn wo node ka label change hony k bawajood b node ma hi rhy gye.;..
    2- preferredDuringSchedulingIgnoredDuringExecution  (summary: pod ki node ma scheduling k time label match hoga. hogya tu schedule ker dye ga ni howa tu pending ma ni rakhy ga kis or node ma pod ko schedule ker dyeg ga or schedule node ma pod hony k bd node k label change b hojye tu pod node ma ha rhy ga..) ----> "preferredDuringScheduling" let say pod place on exact is less important... mean exact node ma schedule hojjye pod tu sahi(label matching kerty howy tu sahi)  but agr label na mily tu koi masla ni. wo pod ko kisi or node ma b place ker sakhta ha.. summary "perferred" mean label match hojye tu sahi. us k according node ma pod ko schedule kery or agr na ho tu wo kisi or node ma pod ko schedule kery.. pod ko pending ma na rkahy... "Ignoredduringexecution" let say k hmry pods node ma schedule hogy thy or apna kam ker rhy thy..ab hota kya ha k enviroment ma koi changes ker deta ha mean node k label ko change ker deta ha... ab asolan node affinity k rule k according pod ko node chore deni chahye but "ignoreDuringExecution" set kerny k waja sa jo pods node ma schedule hogi hn wo node ka label change hony k bawajood b node ma hi rhy gye.;..


planned:
    1- requiredDuringSchedulingRequiredDuringExecution   (summary: pod ki node ma scheduling k time label match hoga. hogya tu schedule ker dye ga ni howa tu pending ma rhy ga pod or schedule node ma pod hony k bd node k label change b hojye tu pod node ma "ni" rhy ga.. bilky node chore dye ga.. because of set "requiredDuringExecution")                                               
    2- preferredDuringSchedulingRequiredDuringExecution  (summary: pod ki node ma scheduling k time label match hoga. hogya tu schedule ker dye ga ni howa tu pending ma ni rakhy ga kis or node ma pod ko schedule ker dyeg ga or schedule node ma pod hony k bd node k label change b hojye tu pod node ma "ni" rhy ga.. bilky node chore dye ga.. because of set "requiredDuringExecution")


limitation and solutions
------------------------

node affinity ma pod per hum restrict ker dety hn k us na kis kis node ma schedule kerna ha or wo us k according hi nodes ma schedule hoti hn "but" other pods jin per node affinity rules set ni unko rokny k lye node per koi restriction set ni ha so wo b node ma schedule ho sakhti han...

so humy asi restriction set kerni hogi node or pod dono per k. jis pod ko kha jaye k us na kis node ma schedule hona ha wo waha per hi ho or node ko kha jye k in pods k alwa asy pods jin per koi rule set ni ha inko tum na schedule ni hony dena..

y dono kam taints/toleration or node affinity k combination sa hosakhty hn.. mean node per taints lga do... or pod per toleration + node affinity...

is sa y hoga k taint lgny sa node non toleration pods ko accept ni kery gi.. or pod per toleration lgny sa pod tolerate hojye gi(abi pod unbound hogi wo kisi b node ma schedule hoskhti hn) or node affinity pod per lgnye sa pod bound hojye k k us na taint wali node ma hi jana h... id tarha sa jin pods ko hum jin node ma jany k lye khy gye wo waha hi jye gi or baki pods un node ma ni jye gi... because node per taint set ha or wo non toleration pod ko accept ni kery ga...


Resource limits
---------------

jb hum pod creation k lye kubectl apply command use kerty hn. tu hmri command information ko cluster ma kubi api server k ps lye ker jata ha wo isko authenticate kerta ha or phir validate kerta ha or etcd ma pod ko update kerta ha in pending state... ?

then schedular etcd ma pending pod ko observer kerta ha. and it get to know k pod ko abi tk kisi node ko assign ni kya.. so wo pod k resources k according nodes find kerta ha. ab isko resource kha sa pta chalty hn... basically hum pod ki yaml file ma under the container section resources ko define kerty hn kis ma hum btaty hn k pod ma contianer ko kitny cpu or memory chahye... is k according node find kerta schedular or etcd ma node name update kerta ha . then kubeapi server etcd sa pod or node name ki information leta ha.. or us node ma kubelet ko inform kerta ha so kubelet us node ma pod create kerta ha...ab jb pod node ma schedule hojata ha tu pod k container requested resources nodes sa lye rha hota ha, "is lye hum pod ki yaml file ma under the container section resources add ker rhy hoty hn"..... or jb sab node ma sa resource khtm hojty hn tu wo further schedule ni hoty or pod describe sa hum dekh sakhty hn insuffient cpu ka error arha hota ha... jis ko hum no of node y node resource increase ker k resolve ker sakhty hn...

pod resources k lye  hum "limit" b set ker sakhty hn. mean set limit sa upper wo node sa resources ni lye ga..

remember
--------
jb pod node ma schedule hota ha mean create hojta ha tu wo define limits ko pod ma set ker lenta ha.. pod set limit sa upper "CPU"" ni lye ga(throttle kery ga mean cpu limit sa upper ni leny dye ga) but "memory" lye sakhta ha... or agr pod constantly apni limit sa upper memory lena start hojye ga tu pod terminate hona start hojye gye.. or (log or describe command sa dekhy gye tu apko) OOM(out of memory) k error ana start hojye ga.. 

yaml example:
------------

apiVersion: v1
kind: Pod
metadata:
  name: nginx
spec:
  containers:
  -  image: nginx
     name: nginx
     ports:
       - ContainerPort: 8080
    resources:
        requests:
            memory: 1Gi
            cpu: 1
        limits:
            memory: 2Gi
            cpu: 2



Default Behavior
----------------

by default kubernetes does not have cpu and memory request or limit set. is k matlab ha k koi b pod zayada resources lye sakhta ha node k or iski waja sa us node ma other pods or processes b distrub hosakhty hn... 

let we have some scenarios
--------------------------

--------------------------
1- no request and no limit
--------------------------

is case ma hum na koi limit set ni ki ha mean default pod create howa ha... ab kya hoga let sa k aik pod ko resource chahaye limit set na hony ki wja sa wo sara cpu comsume ker lye wo baki pod pendiing m arhy gye,. same case for pod memory


---------------------------
2- no request and set limit
---------------------------

request=limit=3vcpu mean hr pod 3 vcpus lye sakthi ha... is limit sa zayada ni lye gi...


--------------------------
3- set request and set limit(not ideal)
--------------------------

request=1vcpu's
limit=3vcpu's

mean each pod have "gurantee" to get 1vcpu's' and maximum will get 3vcpus....  ab agr kis pod ko 3vcpus sa upper chahye tu wo ni lye sakhti because limit set ha..

--------------------------
4- set request and no limit(ideal case)
--------------------------

request=1vcpu's
limit= no limit

mean each pod have gurantee to get 1vcpus and no limit set mean if pod require more then it will get more..

how to define default values for container in pod with limit ranges
-------------------------------------------------------------------


how do we insure that every pod created have some default sets(for cpu and memory).. this can be done by "limit Ranges". it help you define default values to be set for containers in pod. jb b koi pod jis per "resource request limit" set ni ha wo  create hoga node ma tu usko wo limit range mili gi by defualt. 

or y namespace level per applicable hota ha..

limit-range-cpu.yaml
--------------------

apiVersion: v1
kind: LimitRange
metadata:
    name: cpu-resource-constraint
spec:
    limits: ----> list/array
    -   default:
            cpu: 500m  ---> defaultcpulimit 
        defaultRequest:
            cpu: 500m  ----->defaultrequest
        max:
            cpu: "1"
        min: 
            cpu: 100m
        type: Container


limit-range-memory.yaml
--------------------

apiVersion: v1
kind: LimitRange
metadata:
    name: cpu-resource-constraint
spec:
    limits: ----> list/array
    -   default:
            memory: 1Gi  ---> defaultmemorylimit 
        defaultRequest:
            memory: 1Gi  ----->defaultmemorylimit
        max:
            memory: 1Gi
        min: 
            memory: 500Mi
        type: Container

remember
--------

existing pod per y effect implement ni hoga.. but limit range create hony k bd jo b pod by default create hogi usker implement hoga..


is there any way to restrict the total amount of resource that can be consume an application deployed in kubernates cluster :
---------------------------------------------------------------------------------------------------------------------------

this can be done with "resource quota". it is a "namespace" level object. it is use to set hard limit. mean all the pod together should not consume this much of cpu and memory..

resouces-quota.yaml
-------------------

apiVersion: v1
kind: ResourceQuota
metadata:
    name: my-resource-quota
spec:
    hard:
        requests.cpu: 4               -------> request for the total pod in nodes is 4vcpus  and 4Gi and it need will maximun reach to 10 vcpu and 10Gi memory..
        requests.memory: 4Gi
        limits.cpu: 10
        limits.memory:10Gi

----------------------------------------------
A quick note on editing PODs and Deployments
----------------------------------------------
Edit a POD
----------

***Remember, you CANNOT edit specifications of an existing POD other than the below.***

spec.containers[*].image
spec.initContainers[*].image
spec.activeDeadlineSeconds
spec.tolerations
For example you cannot edit the environment variables, service accounts, resource limits (all of which we will discuss later) of a running pod. But if you really want to, you have 2 options:

1. Run the kubectl edit pod <pod name> command.  This will open the pod specification in an editor (vi editor). Then edit the required properties. When you try to save it, you will be denied. This is because you are attempting to edit a field on the pod that is not editable.


A copy of the file with your changes is saved in a temporary location as shown above.

You can then delete the existing pod by running the command:

    kubectl delete pod webapp

Then create a new pod with your changes using the temporary file

    kubectl create -f /tmp/kubectl-edit-ccvrq.yaml

2. The second option is to extract the pod definition in YAML format to a file using the command

    kubectl get pod webapp -o yaml > my-new-pod.yaml

Then make the changes to the exported file using an editor (vi editor). Save the changes

    vi my-new-pod.yaml

Then delete the existing pod

    kubectl delete pod webapp

Then create a new pod with the edited file

    kubectl create -f my-new-pod.yaml

Edit Deployments
With Deployments you can easily edit any field/property of the POD template. Since the pod template is a child of the deployment specification,  with every change the deployment will automatically delete and create a new pod with the new changes. So if you are asked to edit a property of a POD part of a deployment you may do that simply by running the command

    kubectl edit deployment my-deployment

Daemonset
---------

it run one copy of pod on each node in a cluster. jb b koi new node y nodes cluster ma register hoti ha... tu wo us pod ko new nodes ma deploy kera ha.. or jesy hi node delete hoti ha pod b delete hojati ha...

summary: it ensure to run a copy of a pod to all the nodes in the cluster..

use case
--------

- Monitoring solutions  ------> it run monitoring agent as pod on all node to get node metrics
- logs viewer

we also learn that everynode have a kube-proxy for node networking..  so kube proxy can also deploy as daemonset.

other networking solution like "weave-net". it is also deploy as daemonset on all node in cluster.

creating daemonset is like creating replicaset..

Daemonset.yaml
--------------


apiversion: apps/v1  ---------->(different from ReplicationController)
kind: DaemonSet
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

    kubectl get daemonset
    kubectl describe daemonset "name"    "koi b issue hum describe or logs ki command sa dekh sakhty hn"

How does it works?
------------------

hum na previous lecture ma manual scheduling kerty howy dekha tha ka hum kis tarha sa, schedular ko bypass kerty howy kube hi pod ma nodename dye dety thy... wo kubeapi server request ko authenticate or validate kerny k bd inko etcd ma update kerta tha.. or pod na jis node ma jata ha wo b information hum sath hi bta dety thy so... schedular ki zaroorat ni hoti thi or kubeapi server us node ma kublet ko instruct ker k pod bnata tha.. 

same y hi kam daemonset use kerta tha, pod ko node ma schedule kerny lye version v1.12 ma... from v1.12 sa above daemonset use nodeAffinity and default scheduler to run pod on all nodes...

command to check resource in all namespace
==========================================

  kubectl get daemonsets --all-namespaces  
  or
  kubectl get daemonsets -A

we can create deployment through "kubectl create deployment command" but we cannot create daemonset with this command nor replicaset... 

so for daemonset create with command... because daemonset is pretty much similar with deployment, so we first create deployment with kubctl create command and then redirect to make yaml file.. once done we can modify this to use the same file for daemonset.

we will be modifing in file
---------------------------

change in kind deployment to -----> DaemonSet
removing replicas and strategy section  under spec..  save it and apply file with "kubectl apply -f file.yaml"

Static Pods
------------

what if k cluster na ho, na master node ho.. you only play with node.. so how would you give instruction to single node to schedule pod in node..

so you can configure the kubelet to read the pod.yaml from "specfied directory inside the node" like /etc/kubernetes/manifest.. so kubeclt read those file from directory and create pod inside the node...

kubeclt not only create the pods but also make sure pods will stay alive... if application get crush kubelet will restart it make it availabe.. if you do some change in pod.yaml file.. it will apply that change... if you remove file from that directory. pod will also remove..

ap is tarha sa sirf "pods" bna sakhty hn... other component like "deployment" , "replicaset" ni bna sakhty... kubelet only understand the pod...


what is the designated folder or how could we create this
---------------------------------------------------------

y directory koi b hosakhti ha node ma. you just need to give the location to the directory to kubelet. while runing the kubelet service.. so kubelet get to know. where to find the directory for pod.yaml file..

option
------

kubelet.service
---------------
so open the kubelet service and give the directory path, so kubelet get to know where to find the pod.yaml file 

"kubelet.service"

ExecStart=/usr/local/bin/kubelet \\
  --pod-manifest-path=/etc/kubernetes/manifests \\

other option to do the same thing
---------------------------------

ap kubelet ko "config" flage k through apni "kubeconfig.yaml" file k btao or us file ma ap basically apny directory jis ma pod.yaml ki file hn uska path dye do..

like
----

"kubelet.service" ===> var/lib/kubelet/config.yaml(kubelet file location)

ExecStart=/usr/local/bin/kubelet \\
  --config=kubeconfig.yaml \\   -------------->  kubeconfig.yaml -->  staticPodPath=/etc/kubernetes/manifests \\ (directory path)
  
jb hmry pod bn jye gye tu hum unko "kubectl get" sa get ni kery gye.. because we are not working or dealing with the cluster... hum "docker ps" sa get kery gye..

or for cri-o -------> crictl ps
or for containerd --------> nerdctl ps --> its command look same as docker..


is it possible to create static pod as well as pod through kube api server instruction..
----------------------------------------------------------------------------------------

ap static pod sa node ma directly pod b create ker sakhty hn... isk lye pod.yaml ki file node directly ma dena hogi. kubelet waha sa file ko lye ga or pod create ker dye ga.. or ap sametime ma kubeapi server sa b pod create ker sakthy hn node ma.. mean complete cluster ma jis ma cluster k sary component ho.. 

or ab kubectl get sa ap static pod sa bnye pod ko is case ma dekh(read) b sakhty hn. because node kubelet iski aik copy banata ha jisko ap kubectl get sa sirf read ker sakhty hn...   you cannot delete or modify it... y kam ap node ma majod directory jaha s pod.yaml file read ker rhy how wha ker sakhty ho... edit k lye pod.yaml ko edit kro... delete k lye is directory ma jaker delete ker do..

but jb ap simple node ma static pod sa pod create ker rhy hogye tu ap "kubectl get" pod ko ni dekh sakhty becasue y cluster k feature ha. ap "docker ps" sa dekh skahty hn/// ap mention above..

why would static pod use
------------------------

kuo k static pod kubernetes k control plane per depend ni ker rhy hoty... ap single node(without cluster) waly ma ap control plane k component nodes ma as pod run ker sakhty hn.

y kam ap same jis tarha sa pod.yaml ko ap na node ki specfic directory ma rha... ap control plane k component like etcd , control manager, apiserver ki yaml file ko ma is directory ma rakhy kubelet sab file ko yha sa pick ker node ma as pod create ker dye ga sab component ko..

difference b/w static pods and daemonsets
------------------------------------------

- static pod on node created by the kubelet while daemonset created pod on each node by kubeapi server(eye on daemonset controller)
- you can deploy control plane component in node as pod with kubelet while use case of daemonset to deploy monitory agent and logging agent.
------------------
Multiple Schedular
------------------

let say apka ps aik application ha jo scheduling k lye require kerti ha additional checks. after perfoming that check schedular component ko node ma place kry ga... 

ap y kam default schedular ki bjye custom schedular sa ker sakhty hn. so ap decide kerty hn k apka apna schedular ho jo ka pod ko nodes ma schedule kery after checking some custom check... kubernetes ma y kam  hosakhta... most of the application default schedular k ps jye gi scheduling k lye(mean default schedular in k lye node find kery ga).. but kuch specfic application jin ko ap choice kery gye wo custom schedular k ps jye gi(mean custom schedular in k lye kam ker rha hoga or node find ker k dye ga..tky wo application un nodes ma schedule hojye..)

remember
--------

ap apni pod or deployment create kerty time custom schedular k btataty hn is ma. so kubernetes get to know k in pod or deployment(sa bani pod) ko custom schedular schedule kery gye...

default schedular k name uski yaml file ma "default-schedular" hi hota ha jb k custom ko hum koi b name dye sakthy hn

Deploying addition schedular
----------------------------

so same binary k through hum custom schedular ko setup kery gye server ma... or hr aik ki service file ko hum point ker dye gye custom schedular ki yaml file ki tarf...( mean service file ma custom schedulaer ki yaml file k name dye gye..)

binary  --> you can download it from internet and setup in server
------

wget https://storage.googleapis.com/kubernetes-release/v1.12.0/bin/linux/amd64/kube-schedular

service files
-------------

servicefile for default schedular and custom schedular(yha hum service ma default or custom schedular ki yaml file ki taraf pointing ker rhy hn)
------------------------------------------------------------------------------------------------------------------------------------------------
----------------------
kube-schedular.service
----------------------
  ExecStart=/usr/local/bin/kube-schedular \\
    --config=/etc/kubernetes/config/kube-scheduler.yaml(default schedular yaml file name)

----------------------
my-schedular.service
----------------------
  ExecStart=/usr/local/bin/kube-schedular \\
    --config=/etc/kubernetes/config/my-scheduler-config-yaml(custom schedular yaml file name)

my-schedular-config.yaml
------------------------
  apiversion: kubeschedular.config.k8s.io/v1
  kind: kubeSchedularConfiguration
  profiles:
  - schedulerName: my-scheduler

----------------------
my-schedular-2.service
----------------------
  ExecStart=/usr/local/bin/kube-schedular \\
    --config=/etc/kubernetes/config/my-scheduler-2-config-yaml(custom schedular-2 yaml file name)

my-schedular-2-config.yaml
------------------------
  apiversion: kubeschedular.config.k8s.io/v1
  kind: kubeSchedularConfiguration
  profiles:
  - schedulerName: my-scheduler-2

  aaaj kal 99% ap is tarha sa kam ni ker rhy hoty ap.. schedular ko as pod run ker k kam ker rhy hoty hn..

Deploying addition schedular as pod
-----------------------------------

apiversion: v1
kind: Pod
metadata:  -------------->dictionary-------------------metadata ma define information k alws koi or information ni aye gi.. but label ma ap jitny b chahye labels bna sakhty hn
    name: my-custom-scheduler  ---------> sibiling
    namespace: kube-system
spec:--------------------------> dictionary
    containers: -------------------> List/Array
    - command:                             "-" indicate k y array k first element ha. 
      - kube-schedular
      - --address=127.0.0.1
      - --kubeconfig=/etc/kubernetes/scheduler.conf    ---> it is the path of scheduler.config file... it has the authentication property to connect to kubernetes api-server..
      - --config=/etc/kubernetes/my-scheduler-config.yaml  --> ap "--config" ko use kerty howy. custom schedular ki yaml file ki traf point ker sakhty hn
      name: kube-schedular                
      image: k8s.gcr.io/kubernetes-scheduler-amd64:v1.11.3                                "if your image is placed on the dockerhub then you have to give the full path here"
                                              
my-schedular-config.yaml
------------------------
  apiversion: kubeschedular.config.k8s.io/v1
  kind: kubeSchedularConfiguration
  profiles:
  - schedulerName: my-scheduler
  leaderElection:               ------------> leader election option is use when you have multiple copies of schedular running on different master nodes.. "as high availability setup"... only can be active.. that way leader option is helpful to choice the leader..
    leaderElect: true
    resourceNamespace: kube-system
    resourceName: lock-object-my-scheduler

Deploying addition schedular as deployment
------------------------------------------

with this you can create multiple schedular at the same time..

go to kubernetes home page and search configure multiple schedulers...

is ma pod ma under spec --config section ma jo custom schedular k yaml file ki tarf point ker rhy hoty hn..   y basically yaml file ko configmap sa rakhty hn or us configmap ko is pod k volume ko dety hn or volume ko pod k sath mount ker dety hn... ab yaml file config map ma ha but wo pod k mount volume ki waja sa yaml file ko found ker leta ha.. mean configmap sa file isko pass horhi hoti ha..

once done you can see it running as pod in kubesystem namespace..

Once Done
---------

ap apni pod or deployment create kerty time custom schedular k btatana hn. so kubernetes get to know k in pod or deployment(sa bani pod) ko custom schedular schedule kery gye...

like this
----------

apiVersion: v1
kind: Pod
metadata:
  name: nginx
spec:
  containers:
  - image: nginx
    name: nginx
  schedulerName: my-custom-scheduler   --------> mean is pod ko default schedular ni custom scheduler scheduler kery ga(mean is k lye node find ker k la ker dye ga..)

jb sab sahi(mean apky pod ma btya howa scheduler as pod kubesystem namespace ma chal rha hoga then) hoga pod running ma ajye ga. or jb koi masla hoga tu pod pending ma rhy gye..

Veiw events
-----------

  kubectl get events -o wide

  is sa ap dekho gye k last pod jo abi chala ha isko custom schedular na schedule kya ha node ma..

you can also see custom schedular logs.
--------------------------------------

  kubectl logs my-custom-scheduler --name-space=kube-system


Configure Schedular profile
--------------------------------

jb ap pod create krty hn, apki request kubeapi server k ps jati ha, server isko authenticate or validate kerta ha... or etcd ko update kerta ha... kube schedular observe kerta ha k pod pending ma ha... ab yha or kam b horhy hoty hn further koi kam hony sa phily..like pod k lye node find kerny sa phily..

like:
-----
1- scheduling Quene: yha per pod wait kr rhy hoty hn node ma schedule hony k lye... is stage ma pod sorted honty hn base on the priorty define on pods... mean jis ki priorty class zayada hogi ho phily schedule hoga..

so is k lye humy priortyclass bna ker isko pod ma refer kerna hota ha..

like:
-----
apiversion: scheduling.k8s.io/v1
kind: PriorityClass
metadata: 
  name: high-Priority
value: 100000
globalDefault: false
description: "This priority class should be used for XYZ service pods only"

now refer priorityclasse to pod...

pod-defination.yaml
-------------------

apiVersion: v1
kind: Pod
metadata:
  name: simple-webapp
spec:
  priorityClassName: high-priority
  container:
  - name: simple-webapp-color
    image: simple-webapp-color
    resources:
      request:
        memory: "1Gi"
        cpu: 10

2- Filting: then sorted pod come on the "filter phase". is phase ma wo nodes jo is pod ko run kerny k lye resources ni rakhti ho filter out hojati hn..
3- Scoring: then pod come on the scoring phase. In this phase nodes are score with different weights.. like y dekhta ha k jo nodes is pod ko chalny k lye resources rakhti ha un k ps free space kitni ha.. or jis node k ps zayada free space hoti ha wo select hojati ha...
4- binding: is phase ma pod bound hojata ha us node k sath jis ma free space zayada hoti ha..

all of this operations can acheive with certain plugins..

like:
-----
- scheduling queue(PrioritySort)
- Filtering
  
  NodeResourcesFit

     filter kro un nodes ko jin k ps resources ni is pod ko chalny k 
  
  NodeName
    
      remember we did this in NodeSelector. in which we gave node name to pod so schedule will schedule this pod to mention node. so scheduler is case ma node name match kery ga or baki sab ko filter out ker dye ga.

  NodeUnschedulable

      it filter out node that have unschedulable flage. so y make sure kerta ha k pods us node ma schedule na ho. like case of taint on node..

- Scoring

  NodeResourcesFit:

      is ma wo filtered nodes k free resources dekhta ha.. jis k ps zayada space hoti ha us node ko select kerta ha.

  ImageLocality

    is ma wo us node ko prefer kerta ha jis k ps pod k lye image locally pari hoti ha..  in basics per wo node ko select kerta ha..

- Binding

  DefaultBinder: it simply provide the binding mechanisem. sorted pod ko select node k sath bind ker dye ga..

"kubernetes k ps in stages(phase) k lye extensions hoti hn jis ma wo plugins koo rakhtha ha stage(phase k lye..)"

like: 

1 --"stage"--> scheduling  quenu-->"extension" -->>queueSort-->>>"plugin"--->>>>PrioritySort
2 --"stage"--> Filtering-->"extension" -->>preFilter, filter, postFilter-->>>"plugin"--->>>>NodeResourcesFit,NodeName,NodeUnschedulable, NodeResourcesFit, tainttoleration, nodeport,nodeaffinity
3 --"stage"--> Scoring-->"extension" -->>PreScore, score, reserve-->>>"plugin"--->>>>NodeResourcesFit,ImageLocality, NodeResourcesFit, tainttoleration, nodeaffinity
4 --"stage"--> Binding-->"extension" -->>preBind, bind, postBind-->>>"plugin"--->>>>DefaultBinder

Schedular profile
-----------------

default schedular k sath sath jb ap one or more custom schedular ap create kerty ho scheduling k lye... tu wo scheduling k process k lye aik race ma lg jaty hn, jo k itna better ni ha...

so newer version ma hum y ker sakhty hn aik hi schedularconfiguration ki yaml file ma. hum under the "profile" multiple custom schedular bta sakhty hn... or configure ker sakhty hn.

example:
-------

apiVersion: kubescheduler.config.k8s.io/v1
kind: kubeSchedularConfiguration
profiles:
- schedularName: my-schedular-2
  plugins:
    score:
      disabled:
        - name: TainstToleration
      enabled:
        - name: MyCustomPluginA
        - name: MyCustomPluginB
- schedularName: my-schedular-3
  plugins:
    preScore:
      disabled:
        - name: '*'
    score:
      disable:
        - name: '*'
- schedularName: my-schedular-4

