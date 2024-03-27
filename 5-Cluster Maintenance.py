cluster Maintenance ma below process ko learn kery gye..

1- cluster upgrade process 
2- OS upgrades
3- Backup and restore Methodologies (disaster recovery)

OS upgrades
------------

is ma hum scenario dekhy gye k apko apny cluster ki nodes ko down kerna per sakhta ha for "maintenance purpose" k lye...

like: 

- upgrading software
- apply security patches in cluster.

so for this we will see the option to handle the cluster..

let say k apki nodes ma nodes chal rhy hn... ab nodes ma sa aik node bnd hojati ha tu us ma pods b bnd hojye. ab agr replicas set ki waja sa kuch pod aik application k other nodes ma ha tu user ki traffic waha per jye gi.. but agr asa pod jo replicaset k sath na bna ho.. or us pod ki node down hojye tu us traffic ni aye gi..

ab agr wo node wapis up hojati ha tu kube control process start hoga or pod b us node ki running ma ajye gi.. 

but agr "5min" tk node wapis ni aye gi tu pod us node sa "terminate" hojye gye.. kubernetes consider it to dead.. if that dead pods was created by replicaset then y pod kisi or node ma create hojye gi...  or jo pods replicaset sa ni bni hogi wo ni create hogi kisi other node ma.. it just gone..

or ab jb node up hogi after the node eviction timeout.. tu y black..

ab scene y ha k ap na node ma koi upgradation kerni ha.. or ap sure ni ha k node kuch time ma restart hokr wapis ajye gi.. so "safer way" y ha k ap node ma mojood workload(pods) ko kisi or nodes ma move kery or then us node per koi upgradation kery.. 

y kam ap "node ko drain mode" ma lye jakr ker skahty hn... node ko drain kerny sa workload other node ma move hojye ga.. but techically pod asi hi dosri node ma move ni hoti. pod phily apni nodes jis ko drain kerna ha us sa delete hoti hn then other nodes ma recreate hoti ha.. ab ap us drain node ma play ker sakhty hn..

    kubectl drain "node-name"

jb ap node ko drain kro tu apko y error a sakhta ha k. node ma daemonset ko delete ni ker sakthy so y command drain wali execute ni hogi... so hum command k through daemonset delete node sa ignore ker sakhty hn...

    
    kubectl drain node01 --ignore-daemonsets

or is k sath sath hum drain node ko "cordon or unschedulabe" b ker sakhty hn. tky is node ma pod kube-schedular schedule ni kery. jb tk y restrict node sa remove ni hoti...

command for cordon node is:
-----------------------------

    kubectl cordon "node-name"    ------> node ma pod kube-schedular schedule ni kery

command for uncordon node is:
-----------------------------

    kubectl uncordon "node-name"  ---> removing this restriction...

ab jb node up  hojye gi upgration k bd.. tu jo workload(pod) is node sa other nodes gya tha wo wapis automatically ni aye ga... until k wo pod unnodes sa delete na ho or phir kube-schedular is node ma schedule ker saktha ha..


remember:
---------
let say k ap k node ma workload(pod) replicaset k through created tha.. ab ap na is node per koi kam kerna ha like upgradation kerni ha. so ap is case ma jis ma apky ps replicaset k through workload ha node ma , single pod ni ha node ma, ap workload ko simple drain ki command sa move ker sakhty hn...

     kubectl drain node01 --ignore-daemonsets
but jis node ma workload(pod) replicaset sa bana ha or single pods without replicaset k b hn. so inko hum agr simple command sa kery gye tu error dye ga.. humy inko forcefully move kerna hoga like this. 

    kubectl drain --force node-name --ignore-daemonsets

but remember is single pod on node without (replicaset, replicationcontroller, job, daemonset, statefulset) sa create lost hojye gi...

Run: kubectl get pods -o wide and you will see that there is a single pod scheduled on node01 which is not part of a replicaset.

The drain command will not work in this case. To forcefully drain the node we now have to use the --force flag


    kubectl describe node | grep taints --> is command sa hum node ki detail ko describe ker k information ko grep ker sakthy hn..
    
    or kubectl describe node node-name | grep taints    --> getting taints output for specfic nodes.. 

kubernetes software version and release
---------------------------------------

    kubectl get nodes     ->> it will give the information of nodes in cluster and also give information of node version.

the version ha 3 part.... like

    v1.11.3 --> here v1 represent "major part", 11 represent "minor version", 3 represent "patch"

    minor version ----> release feature or functionality.
    patch         ----> release bugfix

    version k phily ALPHA version, phir beta version, phir final version ata ha..

    jb ap version download kerty ho. tu control plane k lye sab version same hogye.. jb k baki servie k lye alg hosakhty hn...

    like:
        api-server:v1.13.4
        controller manager:v1.13.4
        kube-schedular:v1.13.4
        kubelet:v1.13.4
        kube-proxy:v1.13.4
    other different version:
        ETCD CLUSTER: V3.218
        CoreDNS: v1.1.3

Reference
---------

https://kubernetes.io/docs/concepts/overview/kubernetes-api/

Here is a link to kubernetes documentation if you want to learn more about this topic (You don’t need it for the exam though):

https://github.com/kubernetes/community/blob/master/contributors/devel/sig-architecture/api-conventions.md

https://github.com/kubernetes/community/blob/master/contributors/devel/sig-architecture/api_changes.md


-------------------------------------
cluster upgrade process in kubernetes
-------------------------------------

it is mandatory k control plane k sab component k version same ho.. component k different release version ho sakthy hn... but kuo k kube-apiserver primary component ha. or is na sab component sa bt kerni hoti ha. so kubeapi server k version sa upper kisi or component k version ni hoga...

controller manager or kube-schedular k version kube-api server sa kam hoga.. or kubelet or kubeproxy ka controller manager or kube-schedular sa km hoga...  

recommended way to upgrade the cluster is to upgrade step by step from lower version to higher version....ak dum lower version sa greater version per ni lye ker jana, step by step lower sa higher tk lye ker jana ha..


remember:
--------

managed kubernetes ma hum cluster upgradation  gui(console) sa few click ker ker sakhty hn... like gke cluster ki upgradation hum gke console ker ker sakhty hn... 

but non managed kubernetes like kubeadmin sa bany cluster ma upgradation k procceess alg ha...

is lecture ma hum kubeadm k through cluster ki upgradation kerna dekhy gye,,
----------------------------------------------------------------------------

let say k you have 1 master node and 3 worker node in cluster. each node have same version. ab ap na version upgrade kerna ha.. ap phily "master node or phir worker node" k version ko upgrade kery gye..

ab jb master node upgrade horhi hogi tu isky component like api-server or other down hojye gye... or master node down hojye gi. but master node k down hony sa application workload mean pod ko koi fakr ni pary ga... wo worker node ma sahi sa chalti rhy gi,,,

but upgradation k b/w ap cluster ko access ni ker sakthy or koi function perform ni ker sakhty..

node ko upgrade kerny k lye humry ps different stratgies hn. like

1- one way is k sab node aik sath upgrade ho,, jis sa upgrade proccess k b.w pods or is ma pari application down rhy gi... 

2- one way ma hum nodes ko one by one ker k upgrade kerty hn,, or jo node upgrade horhi hoti hn iska workload(pod) baki node ma chala jata ha.. 

3- ap new version wali nodes ko provision kery or apna workload older version nodes sa newer ma move ker dye..

now we will see how to do this:
-------------------------------

jb ap command

    kubeadm upgrade plan

    use kerty hn tu wo apko versions dekhta ha,,,

    - cluster version
    - kubeadm version
    - latest stable version

    or other kubernetes component k versions. or apko khta ha k after this apna hr node ma "kubelet" k version manually install krena ha.. remember kubeadm kubelet ko bydefault install ni kerta, alg sa install kerna parta ha..

    is k sath sath apko kubeadm k through upgrade apply kerny ki command btata ha or btata ha k ap na kubeadm ko sab sa phily install kerna ha with is command or phir y sab version install hoogye..

    - so install kubeadmin first 

        apt-get upgrade -y kubeadm=1.122.0.00

        kubeadm upgrade plan 
        kubeadm upgrade apply v1.12.0

    once done...   apka cluster ki controlplane node new version ma upgrade hojye gi..

        kubectl get nodes... --> ap dekhy gye k node k version abi upgrade ni howa... iski waja y ha k apna kubelet k version ni install kya..

    upgrade kubelet version.....  --> remember kubelet k version install kerny sa phily ap na make sure kerna ha k. drain k through ap na workload ko other nodes ma move krwa

        kubectl drain "node-name"  --ignore-daemonsets  --> abi control plane ko upgrade ker rhy hn tu node name controlplane hoga.. so we can shift our workload from controlplane to other nodes..
        apt-get upgrade -y kubelet=1.12.0.00  

    once done, restart the kubelet process. with service command..

        sudo systemctl daemon-reload
        sudo systemctl restart kubelet

        kubectl get nodes... ---> now with this you will see controlplane k version upgrade hogya ha...

    now time to upgrade nodes version... is k lye apko "drain" command ko use kerty howy workload ko other nodes ma move kerna hoga.. or "cordon" command ko use ker k isko unschedulable bnana ha tky kube schedular is ma pod ko schedule na kery...

        like:
        kubectl drain node-name  --ignore-daemonsets  --> only when you have pod with replicaset on nodes or kubectl drain node-name  --ignore-daemonsets --force  --> only when you have pod with replicaset on nodes or also have pods provision without replicaset...
        kubectl cordon node-name..  ---> for unschedulable pod on this node.

        then add below commands to upgrade the node...

        apt-get upgrade -y kubeadm=1.12.0.00
        apt-get upgrade -y kubelet=1.12.0.00
        kubeadm upgrade node config --kubelet-version v1.12.0
        systemctl restart kubelet.

        jb node wapis sa up hojye tu apny node ko "uncordon" kerna ha tky unschedulable is sa khtm hojye to kube-schedular pods ko is node per b schedule kery... furan sa scheduling ni hogi older pod in other node sa in node per... koi new pod create hogi tu wo is node ma ajye y older pod other node sa delete hogye tu ajye gye..

        is tarha hi apko sab nodes k sath one by one kerna hoga.. is tarha sa apki sab nodes upgrade hojye gi...


lab:
---
with this you can see the node version
--------------------------------------

    kubectl get nodes..  get node information and version...

how to make alaise
-----------------

    alias k=kubectl


get the pod detail information also got to know on what node , pod can schedule
-------------------------------------------------------------------------------

    kubectl get pod -o wide

is command k through sab component k lye latest version ko dekhty hn
--------------------------------------------------------------------
    kubeadm upgrade plan

upgrade cluster to latest version
---------------------------------

    for this you have to upgrade the kubeadm version it self, once it upgrade... use below command to upofgrade the whole cluster version with kubeadm command. 

    kubeadm upgrade apply version-name    

    but apko phily kubeadm k apna version upgrade kerna ha. is k lye apko kubernetes k documentation sa y kam krna hoga.... 

    documentation > search upgrade > upgrading kubeadm cluster..

    - cat /etc/*release*   ---> get to know about OS disbritution.... like ubuntu ha k other...

    is ka hisab sa ap na kubeadm k latest version find ker k install kerna ha...

    apt update
    apt-cache madison kubeadm  --> command to find latest version of kubeadm or is hisab sa apko version find ker k apny version sa up wala version krna hoga... let sa apka 1.19 version ha or upwala version ab apna kerna ha jo 1.20.0.00 ha. so do this..

    apt-get --version
    apt-update  && \ 
        apt-get install -y --allow-change-held-packages kubeadm=1.20.0.00   or any other version..

    once kubeadm done... update cluster version...

    kubeadm version
    kubeadm upgrade plan
    kubeadm upgrade apply v(version no)

    now for kubelet version...

    drain and cordon the workload from other node. use below to install kubelet

     apt-update  && \ 
        apt-get install -y --allow-change-held-packages kubelet=1.20.0-00 kubectl=1.20.0-00  or any other version. with this you can install kubelet and kubectl version..

    then restart the service and uncordon the node....

    sudo systemctl daemon-reload
    sudo systemctl restart kubelet

    kubectl uncordon node-name..  


    do the same thing with other node to upgrade the version...

get node ip
-----------

    kubectl get nodes -o wide

------------------
Backup and restore
------------------

is ma hum various backup and restore Methodologies ko dekhy gye...

so far hum is result per hn k, jo b cheezy hum create kerty hn wo like pod , statefulset, daemonset.. declartive way sa uski yaml file hmry ps hoti ha, isko hum github ma backup k tor per rakh sakhty hn...
    
etcd ma cluster ki information hoti ha..
    
storage ma volume hota ha..

    kubectl get all --all-namespace -o yaml > deploy-all-services.yaml   ---> in this way you can get backup of all service in yaml file..

"VELERO" is a tool that is use for taking backup of kubernetes resources..

Backup ETCD
-----------

    etcd cluster store the information about state of the cluster... mean jo b resources cluster ma provision hoty hn.. unki information etcd ma hoti ha....

    so backing up k process ma you have to make this sure k "etcd" k b backup lya jye...

    etcd controlplane k component ha or contorlplane ma hi host hota ha... "etcd ki configuration file ma ap btaty ho k etcd ka data(key-value-pair) kis location ma store hoga.."

    like:   data-directory to store etcd data,,  --data-dir=/var/lib/etcd


        etcd.service
            ExecStart=/usr/local/bin/etcd \\
            --name $(ETCD_NAME)
            --.....
            --.....
            --.....
            --.....
            --data-dir=/var/lib/etcd

        it can be configure to be backed up buying backup tool...
    
    snapshot
    --------
    - etcd ma "snapshot" k b built-in feature hota ha.     ap etcd database k snapshot(backup) lye sakthy hn by using etcd control utility "snapshot save" command..

    like: 

        ETCDCTL_API=3 etcdctl \
            snapshot save "snapshot-name"   ---> is sa etcd k snapshot dye gye name k mutabik current directory ma create hojye ga...

    - ap saved snapshot k status check ker skahty hn...

        ETCDCTL_API=3 etcdctl \
            snapshot status "snapshot-name"   ---> is sa etcd k snapshot dye gye name k mutabik current directory ma create hojye ga...

    for etcd snapshot(backup) restoration:
    --------------------------------------

    - apko sab sa phily "kube-api-server" ko "stop" kerna hoga...

        service kube-apiserver stop    --> then restart etcd server

    after that :
    ------------

    ETCD_API=3 etcdctl \ 
        snapshot restore snapshot.db \   --> snapshot.db etcd datastore ki snapshot ha jis ko hum na backup kya tha ab isko restore kerwa rhy hn...
        --data-dir /var/lib/etcd-from-backup   ---> it is a path of the backup file...

    backup leny k bd y initailized kerta ha new cluster configuration or configure the member or etcd as new member to the new cluster. it provent to accidently joining for existing cluster... 

    is command ko run kerny sa new data directory create hoti ha(may be jb snapshot save ultility sa backup bnta ha tu wo new directory ma bnta ha)...  like "etcd-from-backup" will create a new directory once create backup... so is directory sa hum backup restore kerwa rhyn hn "/var/lib/new-directory"


     ETCD_API=3 etcdctl \ 
        snapshot restore snapshot.db \  
        --data-dir /var/lib/etcd-from-backup   ---> it is a path of the backup file...

    ab apna y directory name apny "etcd.service" ma mention kerna ha.... so cluster ki state ko etcd is directory ma further store kerwata rhy... 
    
    etcd.service
            ExecStart=/usr/local/bin/etcd \\
            --name $(ETCD_NAME)
            --.....
            --.....
            --.....
            --.....
            --data-dir=/var/lib/etcd-from-backup  --> like this..

    then restart the "etcd service"

    systemctl daemon-reload
    service etcd restart

    finalllly --> jo kubeapi service ap na stop ki thi y process kerny sa phily isko "start" ker dye...  

     service kube-apiserver start

quicknote:
---------

    with all the etcd command remember to add the certificate file for authentication

            ETCDCTL_API=3 etcdctl \
            snapshot save "snapshot-name" \

            --endpoints=https://127.0.0.1:2379   --> endpoint of etcd server
            --cacert=/etc/etcd/ca.crt \
            --cert=/etc/etcd-server.crt \
            --key=/etc/etcd/etcd-server.key

so we see 2 things for backup 1-resource configuration  2- ETCD Cluster 

ab sir khty hn k jb ap manage service ko use kerty hn tu etcd service ki apko access ni hoti... so is case ma backup by quering the kubeapi server is a better way..

--------------------
Working with ETCDCTL
--------------------

WORKING WITH ETCDCTL

 

etcdctl is a command line client for etcd.

 

In all our Kubernetes Hands-on labs, the ETCD key-value database is deployed as a static pod on the master. The version used is v3.

"To make use of etcdctl for tasks such as back up and restore, make sure that you set the ETCDCTL_API to 3."

 

You can do this by exporting the variable ETCDCTL_API prior to using the etcdctl client. This can be done as follows:

export ETCDCTL_API=3

On the Master Node:


To see all the options for a specific sub-command, make use of the -h or –help flag.

 

For example, if you want to take a snapshot of etcd, use:

etcdctl snapshot save -h and keep a note of the mandatory global options.

Since our ETCD database is TLS-Enabled, the following options are mandatory:

–cacert                verify certificates of TLS-enabled secure servers using this CA bundle

–cert                    identify secure client using this TLS certificate file

–endpoints=[127.0.0.1:2379] This is the default as ETCD is running on master node and exposed on localhost 2379.

–key                  identify secure client using this TLS key file

 

For a detailed explanation on how to make use of the etcdctl command line tool and work with the -h flags, check out the solution video for the Backup and Restore Lab.

lab:
---
1- The master node in our cluster is planned for a regular maintenance reboot tonight. While we do not anticipate anything to go wrong, we are required to take the necessary backups. Take a snapshot of the ETCD database using the built-in snapshot functionality.

 ETCDCTL_API=3 etcdctl --endpoints=https://[127.0.0.1]:2379 \
--cacert=/etc/kubernetes/pki/etcd/ca.crt \
--cert=/etc/kubernetes/pki/etcd/server.crt \
--key=/etc/kubernetes/pki/etcd/server.key \
snapshot save /opt/snapshot-pre-boot.db  ---> create snapshot with name "snapshot-pre-boot.db" at location "/opt/snapshot-pre-boot.db"


Solution: Backup and Restore
----------------------------

- what is the version of etcd running on the cluster ...
    will get the version by "describe" etcd pod available in controlplane.....  aksar jb ap koi deployment kerny ha. cicd sa tu apni latest image ka version ap... pod ko describe ker k dekh rhy hoty hn..

- At what addresses can you reach the ETCD cluster from the controlplane node.. 
    mean etcd k entrypoint kya ha jis per wo listen ker rha ha...

    you can get the entrypoint by "describe" etcd pod available in controlplane.. > under command(entrypoint) > etcd > --listen-client-urls="ip_address"

- Where is the ETCD server certificate file located?

    you can get it by "describe" etcd pod available in controlplane.. > under command(entrypoint) > etcd > --cert-file=/etc/kubernetes/pki/etcd/server.crt

- Where is the ETCD ca certificate file located?

    you can get it by "describe" etcd pod available in controlplane.. > under command(entrypoint) > etcd > --trusted-ca-file=/etc/kubernetes/pki/etcd/ca.crt

- take etcd backup and store the backup file /opt/snapshot-pre-boot.db
    
    localhost sa pod tk data volume k through kesy lye ker jaty hn.. same as dockerbindmount...

    - create directory and put data.. > volume k through wo directory select kro,> ab is volume ko pod k sath mount kerwa do... or pod ki yaml file under "command" --data-dir= "directory_name".. so is tarha sa pod ko localhost directory sa data mil jye ga.. y sab kam ap pod ky yaml file ma btye gye...

    is tarha sa wo aik volume k through pod ko localhost ma pari authentication ki lye pari certification files ki access dye raha ha or other volume attach ker k wo pod ko localhost ma directory ki acces dye rha ha tky etcd cluster ki state(key value pair information ko waha store kery)... pod ko attach directroy ki traf ap "command" ko use kerty wohy path dye ker redirect kerwaty hn
  

   now agr ap "etcdctl" ki command ko kubernetes cluster ma terminal per without "ETCDCTL_API=3" set kry bna command ko execute kery gye tu apko error aye ga....

   like: simple 
   
    "etcdctl"  ---> it will not recognized the command..

    ETCDCTL_API=3 etcdctl snapshot      --> now it will recognized the command..

    apko br br "ETCDCTL_API=3" use kerny ki zaroorat ni ha... ap "export ETCDCTL_API=3"  use kery then you can use "etcdctl" with out using ETCDCTL_API=3... you will not be facing any error... 

    so,,,

    after using  "export ETCDCTL_API=3"  You can freely use "etcdctl"

    take etcd backup
    ----------------

    "etcdctl snapshot save --endpoint="entrypoint of etcd where it listens like 127.0.0.1:2379" \
     --cacert=/etc/kubernetes/pki/etcd/ca.crt \
     --cert=/etc/kubernetes/pki/etcd/server.crt \   --->> ca files for authentication..
     --key=/etc/kubernetes/pki/etcd/server.key \
     /opt/snapshot-pre-boot.db    -------> location where etcd backup will be store...

ab sir khty hn k let say k node start hoti ha or koi cheez ni chalti.. ap na deployment , pods , or services ko dekha kuch b ni tha .. "luckily ap na etcd k backup lya tha. so ap backup ko restore ker sakhty hn."

    ab is k lye hum na volume k through us directory ko select kerna ha, jis ma etcd ka latest backup pra ha or us volume ko hum na etcd k pod k sath through mount point k mount kerwa dena ha, or pod ma under> command  > --data-dir k through us path ki tarf isko redirect ker dena ha... so etcd pod ma data restore hojye ga.
    

    sir na asy restore kya ha :

        etcdctl snapshot restore --data-dir "new directory name jaha per data lana ha extract kerwa ker" "directory name jaha sa data lana ha"
        etcdctl snapshot restore --data-dir /var/lib/etcd-from-backup /opt/snapshot-pre-boot.db   ---> sir na kha tha k restore aik tarha sa locally hota ha is k lye, apko certification file for authentication k lye ni chahye hoti..

        ab sir na y kya ha " ab is k lye hum na volume k through us directory ko select kerna ha, jis ma etcd ka latest backup pra ha or us volume ko hum na etcd k pod k sath through mount point k mount kerwa dena ha, or pod ma under> command  > --data-dir k through mountpoint k path ki tarf isko redirect ker dena ha... so etcd pod ma data restore hojye ga."

        sir khty hn k command wala path or mount point wala path same hona chahye.. because hum command k through redirect ker k rhy mountpoint k path ki tarf.. so it should be same..


        etcd successfully restore kerny bd hmri deployment , pod , service successfully chalna start hojye gi..


Solution: Backup and Restore 2
------------------------------


command to view the all cluster:

    kubectl get node
    kubectl config view

- how many nodes are the part of cluster-1 ----cluster-1 is a cluster name..

    first you need to switch to the cluster.. with switching command...

    kubectl config use-context "cluster-name"

    then

    kubectl get nodes

how to find the detail formation of etcd
----------------------------------------

    ps -ef | grep -i etcd   --------> with this you can find information of etcd server..


how many nodes are part of the ETCD cluster:
--------------------------------------------

     ETCDCTL_API=3 etcdctl --endpoints=https://[127.0.0.1]:2379 \
--cacert=/etc/kubernetes/pki/etcd/ca.crt \
--cert=/etc/kubernetes/pki/etcd/server.crt \
--key=/etc/kubernetes/pki/etcd/server.key \
  member list            -------> with this you can see the ETCD cluster members..

take etcd backup and save it to remote server
---------------------------------------------

export ETCDCTL_API=3

    "etcdctl snapshot save --endpoint="entrypoint of etcd where it listens like 127.0.0.1:2379" \
     --cacert=/etc/kubernetes/pki/etcd/ca.crt \
     --cert=/etc/kubernetes/pki/etcd/server.crt \   --->> ca files for authentication..
     --key=/etc/kubernetes/pki/etcd/server.key \
     /opt/snapshot-pre-boot.db    -------> location where etcd backup will be store...


     In this way take a backup and for move this backup to remote cluster use "SCP" command.

     scp k through ap source per beth ker destination per file move ker sakthy hn or same source per beth ker destination sa source per file move ker sakhty hn.

     scp destinationserver user@ipaddress:directorypathofdestinationserver "source server directory path"

took etcd backup and send it to remote server and restore backup
----------------------------------------------------------------

use scp to get backup from remote server,  restore it to etcd...

export ETCDCTL_API=3 

    etcdctl snapshot restore "store from this directory" --data-dir /var/lib/etcd-data-new
    etcdctl snapshot restore /root/cluster-2 --data-dir /var/lib/etcd-data-new

    go to this directory and change ownership /var/lib/etcd-data-new  from root to user

    chown -R user:group /var/lib/etcd-data-new  --> path

    and go to the "etcd.service" file and change the path... 
    
    ===> vi /etcd/systemd/system/etcd.service

    change --data-dir=new path

    then restart service...

    systemctl daemon-reload
    systemctl restart etcd

    how restart the control plane component.. like kube controller and kube schedular  ,, for this you have to delete the pod and it will come back again automically, because hosakta ha y deployment sa bnye ho,,,


    kubectl delete "controlplane pod" "schedular pod name"

    and restart kubelet service

Certification Exam Tip!
----------------------
Here’s a quick tip. In the exam, you won’t know if what you did is correct or not as in the practice tests in this course. You must verify your work yourself. For example, if the question is to create a pod with a specific image, you must run the the kubectl describe pod command to verify the pod is created with the correct name and correct image.

References
----------

https://kubernetes.io/docs/tasks/administer-cluster/configure-upgrade-etcd/#backing-up-an-etcd-cluster

https://github.com/etcd-io/website/blob/main/content/en/docs/v3.5/op-guide/recovery.md

https://www.youtube.com/watch?v=qRPNuT080Hk