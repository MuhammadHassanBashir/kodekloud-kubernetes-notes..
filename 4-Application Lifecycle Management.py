Deployment updates(mean updating new application version) and rollback
----------------------------------------------------------------------

when new rollout trigger(applicable upgrade) then us k against new deployment revision create hoti ha... it helps us keep track changes and enable us to rollback to older deployment version if neccessay..

for my understanding
--------------------

    hota kya ha let say k tum na kubernetes component deployment k through application ko deploy kya ha.. "ab kubernetes deployment create kery ga... us ma replicaset or replicaset ma mention replicas mean pods create hogye.." or is k against "deployment revision" backend per create hogi... to keep track the change. let say k abi "deployment revision-1" create hoi ha phily application update per... ab ap apni application ma koi changes kerty hn
    or is changes ko deploy kerty hn. so hoga kya ka deployment ma new replicaset create hoga.. or apki mention stragety ka according pods is ma create hogye. or is doraan service sa traffic dono replicset per arhi hogi until or unless k sab pod older replicas sa down hojye. phir new service per traffic shift hogi. or backend ma is k against "new deployment revision" create hoga tu keep track changes...  
    ab let say ap ki new application koi masla ker rhi ha tu ap "older deployment revision" per move back ker sakhty hn "rollout undo" ki command use kerty howy jis sa application ki older state per wapis ajye gi. because ab service sa traffic older replicaset per jye gi..

above explaination "rolling update strategy" k hawaly sa ha..

You can see replicaset with this command

    kubectl get replicasets

Rollout command
---------------
    is ma ap rollout trigger k process ko dekh sakthy hn.. mean older replicaset sa new replicaset or iska pod create hony k process..

    kubectl rollout status deploymemt/deployment-name

command to see deployment revision and history of rollout
---------------------------------------------------------

    kubectl rollout history deployment/deploymentname

    output:  1- revision-1
             2- revision-2

Deployment stragety
-------------------

1- recreate  -->>  is ma older version  waly sary pod aik sath down hoty phily or newer version waly pods up hoty hn aik sath... is ma 2 masly hn... 1- k pods down or up k b/w kuch time k lye applicaiton down rhy gi.. 2- agr application k newer version koi masla kery tu ap rollback ni ker sakthy older pod per becasue wo tu delete hogye hn... or y default stratgye b ni ha..

2- rolling update    is ma simultaneously older version waly pods down hogye or newer version waly pods up hogye. is traha sa application kbi down ni hogi or upgrage seemless hogi.. it's a default deployment strategye..

you can roll back on previous deployment revision
-------------------------------------------------

    kubectl rollout undo deployment/deploymentname

    with this you can rollback to previons deployment revision.. and deployment will delete pods on new replicaset and create pods on older replicasets and your application is back to older format..
    

so what mean upgration in application
-------------------------------------


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

mean upgrading -->version, label or no of replicas, image

then use "kubectl apply" command to apply this change...  ab is sa aik new rollout trigger hoga or or aik new deployment revision backend ma create hoga..

you can also update image with kubectl set image command
--------------------------------------------------------

    kubectl set image deployment/deployment-name container-name=new-image-name

    is sa directly deployment ma new replicaset create hoga or pod ma new image update hojuye gi.. or backend per new deployment revision ajye ga..

    but remember apki yaml file ma b apko manually changes kerni pary gi.. future purpose k lye..

Configure Applications
----------------------

Configuring applications comprises of understanding the following concepts:

    Configuring Command and Arguments on applications
    Configuring Environment Variables
    Configuring Secrets
    
    We will see these next

Command and argument for pod defination file
--------------------------------------------

jis tarha "cmd" or "entrypoint" hum docker ma use kerty hn... is trha hi "Command" or "Argument(Arg)" ko hum kubernetes ma use kerty hn... 



we can understand this with example
-----------------------------------

let say we are trying to create ubuntu container... with command

    "kubectl run ubuntu"..

    is sa howa y ha k container start howa or apna task complete kya or exist hogya ...  y cheez hum "docker ps" sa dekhy gye tu container humy running ma ni milt ga. or "docker ps -a" sa dekhy gye tu container exist state ma milge ga..

    because container OS tu host kerny k lye bna ni(because y host operating system k kernal use ker rha hota ha) na kerta ha container tu task/process k lye bnata ha or jesy hi task complete hota ha y container ma webservice crush hoti ha tu container b exist ker jata ha..

    error is lye aya... jb ap ubuntu image ki dockerfile dekhy gye tu apko idea hoga ka... 

    "DOckerfile"

    FROM ubuntu:14:04
    RUN \
        apt-get update && \
        apt-get -y upgrade && \
        rm -rf /var/lib/apt/lists/*

    ADD root/.bashrc /root/.bashrc
    ADD root/.gitconfig /root/.gitconfig
    ADD root/.scripts /root/.scripts

    ENV HOME /root
    WORKDIR /root
    CMD [bash]

basically CMD command tb use kerty hn k jesy hi hmra container run(start) ho tu sab sa phily jo command chaly wo CMD ma hum dety hn.. "basically CMD define kerta ha k container ma kon sa process chalna chahye. like nginx ki image ma process cmd [ngnix] hota mean y process chalna chahye same for mysql k case ma mysql " ab container chalta ha or cmd [bash] command execute hoti ha. bash is not a process. bash is for listening the command from terminal. mean container ko terminal chahye.

but by-default container k sath docker terminal ko attach ni kerta. so container ko terminal ni milta.. or container k ps ab koi or task/process kerny ko ha ni so exist hojata ha..

"kubectl run ubuntu".. --> asy kerny sa container create hony k bd kuo exist howa
---------------------------------------------------------------------------------

"simple answer" is k container ko terminal ni mila mean terminal attach ni ha, kuo k by-default docker container k sath terminal attach ni kerta.. "cmd [bash] executed once container run but bash progrom does not find terminal." so container k ps koi or process kerny ko tha ni... is lye or exist hogya.. because container tb tk live rahta ha jb tk usky under k process live rakhta...

is k solution k lye hum command ma "-it" lgty hn.. to interact with terminal... or "-d" run container processes in backgroud... 

like:
----

    kubectl run -itd ubuntu

cmd ---------> will override the effect in the container when do changes in dockerfile cmd section .... but entrypoint will append the effect in the container when do changes in dockerfile entrypoint section.

--------------------------------------
COMMANDS & ARGUMENTS in kubernetes pod
--------------------------------------

remember
--------

-------------------------------------------------------------------------------------
| Description                           | Docker field name | Kubernetes field name |
-------------------------------------------------------------------------------------
| The command run by the container      | Entrypoint(append)| command               |
| The arguments passed to the command   | Cmd(override)     | args                  |
-------------------------------------------------------------------------------------

COmmand example:
---------------

apiVersion: v1 
kind: Pod 
metadata:
  name: ubuntu-sleeper-2 
spec:
  containers:
  - name: ubuntu
    image: ubuntu
    command:  ---------------> for append
      - "sleep"
      - "5000"


----
ENV
----

ENV is enviroment variable... it is a array

apiVersion: v1 
kind: Pod 
metadata:
  name: ubuntu-sleeper-2 
spec:
  containers: -----------------> list/array
  - name: ubuntu
    image: ubuntu
    command:  ---------------> for append -----------------> list/array
      - "sleep"
      - "5000"
    env: -----------------> list/array ----------> simple way(is ma ap pod ma directly enviromental variable dye rhy hn)
      - name: APP_COLOR  
        value: green 

other way to set the enviromental variable is "configMAP" and "secret"

like for configmap our env would look like.
-------------------------------------------

env: -----------------> list/array ----------> with configmap way(to get specfic key value pair from configmap)
      - name: APP_COLOR  
        valueFrom:
            configMAPKeyRef:
                name:    -----> configmap name
                key:     ---> key on configmap jis k against ap na value leni ha env k lye..
                 

like for Secret our env would look like.
-------------------------------------------

env: -----------------> list/array ----------> with secret way(to get specfic secret from secret)
      - name: APP_COLOR  
        valueFrom:
            secretKeyRef:
------------
ConfigMaps  for me easytoundersatand, y aik centerized place ha jaha per information like "env" ko rakh sakhty hn tky sab pod is information ko configmap sa lye sakhy...
------------

when we have a lot of pod defination yaml with these file we would provision pod in cluster.. it would be difficult to manage enviroment variable on each file... so hum is env ki information ko pod defination file sa bahir aik "centralized place like configmap" ma lye ja sakhty hn. so jis pod ko hum na configmap k through enviroment variable dena ha tu hum is pod ko configmap k name ref ker dye gye... tk wo configmap sa variable lye lyee..

for this we have 2 step..

- create configmap
- refer it to pod for getting enviromental variable..

configmap
--------
APP_COLOR: blue
APP_MODE: prod


pod
---
apiVersion: v1 
kind: Pod 
metadata:
  name: ubuntu-sleeper-2 
spec:
  containers: -----------------> list/array
  - name: ubuntu
    image: ubuntu
    ports:
      - containerPort: 8080
    command:  ---------------> for append -----------------> list/array
      - "sleep"
      - "5000"
    envFrom:          -------> here we referring name of configmap to pod  so pod can get env information from configmap.
        - configMapRef:
            name: app-config        --> configmap name

command to create configMAP
===========================

 1-   kubectl create configmap <configmap-name> --from-literal=<key>=<value> --------> imperative way
      kubectl create configmap app-config  --from-liberal=APP_COLOR=blue     ---------> --from-literal   is sa hum key value pair command ma dety hn..

      for adding multiple key value pair with same command use multiple "--from-literal".. 
      like: kubectl create configmap app-config  --from-liberal=APP_COLOR=blue --from-liberal=AP=brown


      we can do the same thing by put env key value pair information in file and give the file path to configmap during configmap creation...

      like:
      kubectl create configmap <configmap-name> --from-file=<path-to-file> --------> imperative way
      kubectl create configmap app-config  --from-file=app_config.properties    ---------> --from-literal   is sa hum key value pair command ma dety hn..
      

 2-   kubectl create -f filename.yaml ------> declarative way

      apiVersion: v1
      kind: ConfigMap
      metadata:
        name: app-config ---->configmap name
      data:             -----> under data we give env key value pair
        APP_COLOR: blue
        APP_MODE: prod  

once done then create configmap with apply command "kubectl create -f filename.yaml"

you can create as much as config map and use it with pod.. but name of every configmap should be unique.

view
----

    kubectl get Configmaps or kubectl get cm
    kubectl describe configmaps

Refer configmap to pod
----------------------

pod
---
apiVersion: v1 
kind: Pod 
metadata:
  name: ubuntu-sleeper-2 
spec:
  containers: -----------------> list/array
  - name: ubuntu
    image: ubuntu
    ports:
      - containerPort: 8080
    command:  ---------------> for append -----------------> list/array
      - "sleep"
      - "5000"
    envFrom:          -------> here we referring name of configmap to pod,  so pod can get env information from configmap.(ingesting the entire ConfigMap as a single environmental variable.)
        - configMapRef:
            name: app-config      ---> configmap name

ingests the entire ConfigMap as a single environmental
------------------------------------------------------

mean: This approach ingests the entire ConfigMap as a single environmental variable. It's suitable when your application requires access to multiple configuration parameters encapsulated within a single variable. For instance, if your application needs a variety of settings or configurations grouped together, this method simplifies the injection process by allowing the entire ConfigMap to be accessed as one variable.

 envFrom:          
    - configMapRef:
        name: app-config    -----> configmap name

ingest as single enviromental variable
--------------------------------------

mean: In this approach, a specific key-value pair from the ConfigMap is injected into the pod as an environment variable. This is useful when you need to configure your application with a few specific settings and those settings are best represented as environment variables.
    
env:
  - name: APP_COLOR    --- env "key name"....
    valueFrom:
        configMapKeyRef:
            name: app-config   ------> represent name of the config map
            key: APP_COLOR     ---------> represent the key against with we get the value from configmap


ingest whole data as file in volume
--------------------------------------

mean: Mounting ConfigMap as a File in a Volume..   Best for applications that expect configuration data in file format. Useful when configuration files are structured or when applications are designed to read configuration from files.


volumes:
-   name: app-config-volume  --> name of the volume.  
    configMAP:
        name: app-config  ---> name of the configmap

--------------
Secrets
--------------

Let say k hmra backend python per writen ha or hum application k through hi "mysql.connection" use kerty howy "user , host , password , port parameter" dety howy backend ki database ka sath connectivity kerwa rhy hn... 

but this is not good to share information openly on code. becasue apka code koi b read ker k sensitive information lye sakhta ha.  so we need to make it sure k sensitive information open na ho... so hum is ko "config map or secret" sa ker sakhty hn.

but configmap ma information plane text ma hoti hn... tu is ma hum sensitive information ni rakha sakhty yha sa b read hojye gi...

"but secret are use to store sensitive information"  mean hum apni sensitive information yha rakh ker pod ko iska name refer ker sakhty hn..


for this we have 2 step..

- create secret
- refer it to pod for getting secret..

command to create Secret
===========================

 1-   kubectl create secret generic <secret-name> --from-literal=<key>=<value> --------> imperative way
      kubectl create secret generic app-secret  --from-liberal=DB_HOST=mysql     ---------> --from-literal   is sa hum key value pair command ma dety hn..

    for adding multiple key value pair of secret with same command use multiple "--from-literal".. 
    like: kubectl create secret app-secret  --from-liberal=DB_Host=mysql --from-liberal=DB_User=root --from-liberal=DB_Password=passwd ---> --from-literal "is sa wo value ko encode form ma bna ker secret ma dalta ha.."

controlplane ~ ✖ kubectl create secret generic db-secret --from-literal=DB_Host=sql01 --from-literal=DB_User=root --from-literal=DB_Password=password123 --dry-run=client -o yaml > secret.yaml ---> "is sa wo value ko encode form ma bna ker secret ma dalta ha.."
     
      we can do the same thing by put secret information in file and give the file path to secret during secret creation...

      like:

      kubectl create secret generic <secret-name> --from-file=<path-to-file> --------> imperative way
      kubectl create secret generic <secret-name>  --from-file=app_secret.properties    --------->  app_secret.properties  is a file name/path
      

 2-   kubectl create -f filename.yaml ------> declarative way

      apiVersion: v1
      kind: Secret
      metadata:
        name: app-secret ---->configmap name
      data:             -----> under data we give env key value pair
        DB_Host: bXlzcWw=   --> key and value.. "remember secret ma data section ma apko data encoded format ma rakhna ha"
        DB_User: cm9vdA==
        DB_Password: cGFzd3Jk

how to convert data into encoded format
---------------------------------------

linux ma ap y command use ker k information ko encoded format ma convert ker k. usko apky secret file ma under data section rakh sakhty hn..

like:
    echo -n mysql | base64    ---> bXlzcWw=          is command na humy "mysql" ki encode format "bXlzcWw=" dya ha.. "now you can paste thi in you secret file under data section" jesy uper file ma mention ha..
    echo -n root | base64     ---> cm9vdA==          is command na humy "root" ki encode format "cm9vdA=="  dya ha.. "now you can paste thi in you secret file under data section" jesy uper file ma mention ha..
    echo -n passwrd | base64  ---> cGFzd3Jk          is command na humy "passwrd" ki encode format "cGFzd3Jk" dya ha.. "now you can paste thi in you secret file under data section" jesy uper file ma mention ha..

once done then create secret with apply command "kubectl create -f filename.yaml"

you can create as much as secret and use it with pod.. but name of every secret should be unique.

view
----

    kubectl get secrets     -->
    kubectl describe secrets   -->with this command you can get secret information.. but secret hidden hogye..

    to see the information with Secrets. ap running secret ki -o yaml k through aik output file bna lo... 

    like: 
        kubectl get secret/secret-name -o yaml > secret.yaml   ---> is sa output ma ap information k sath sath secrets b dekh sakhty hn.. or usko decode b ker sakthy hn..

How to decode secrets
---------------------

same echo command to hum reverse ker dye gye.. secret file sa hum.. encode secret lye gye.. or isko base64 k through decode kery gye..

like: echo -n bXlzcWw=  | base64  --decode            ---> mysql            decode hokr output mysql i..
      echo -n cm9vdA==  | base64  --decode            ---> root       
      echo -n cGFzd3Jk  | base64  --decode            ---> passwrd     


Refer secret to pod
----------------------

pod
---
apiVersion: v1 
kind: Pod 
metadata:
  name: ubuntu-sleeper-2 
spec:
  containers: -----------------> list/array
  - name: ubuntu
    image: ubuntu
    ports:
      - containerPort: 8080
    command:  ---------------> for append -----------------> list/array
      - "sleep"
      - "5000"
    envFrom:          -------> here we referring name of the app-secret to pod,  so pod can get env information from secret.(ingesting the entire app-secret as a single environmental variable.)
        - secretRef:
            name: app-secret    ------> secret name    :-  giving entire secret as enviromental variable to pod



ingests the entire Secret as a single environmental
------------------------------------------------------

mean: This approach ingests the entire ConfigMap as a single environmental variable. It's suitable when your application requires access to multiple configuration parameters encapsulated within a single variable. For instance, if your application needs a variety of settings or configurations grouped together, this method simplifies the injection process by allowing the entire ConfigMap to be accessed as one variable.

 envFrom:       -----------> list -so add as much as you can     
    - secretRef:
        name: app-secret   -----> secret name

ingest as single enviromental variable
--------------------------------------

mean: In this approach, a specific key-value pair from the ConfigMap is injected into the pod as an environment variable. This is useful when you need to configure your application with a few specific settings and those settings are best represented as environment variables.
    
env:
  - name: APP_COLOR    --- env "key name"....
    valueFrom:
        secretKeyRef:
            name: app-secret   ------> represent name of the secret
            key: APP_COLOR     ---------> represent the key against with we get the value from secret


ingest whole data as file in volume
--------------------------------------

mean: Mounting secret as a File in a Volume..   Best for applications that expect configuration data in file format. Useful when configuration files are structured or when applications are designed to read configuration from files.


volumes:
- name: app-secret-volume  --> name of the volume.  
  secret:
    name: app-secret  ---> name of the secret

    is tarha kerny sa secret ki hr "value"(DB_HOST, DB_Password, DB_User) k name ki file... "/opt/app-secret-volume" ma bny gi.. jis ko ap open kery gye tu apko secret ki against uski value mily gi.. like "DB_Passwd" name ki file ma "passwrd" value hogi.


remember:
---------

- secrets are not encrypted. it only encode.. and can be decode.. do not share it to public github repo.
- secret are not encrypted in ETCD... but can be with configuration.
- "Anyone able to create pods/deployments in the same namespace can access the secrets.." , so for this you can consider RBAC to restrict access.
- you can also use thrid-party secrets store providers. like AWS PROVIDER, AZURE PROVIDER, GCP PROVIDER. VAULT PROVIDER...


------------------------------------
Demo: Encrypting Secret Data at Rest
------------------------------------
because secrets are not encrypted, it is encoded that is why one's how made access to the secret. it will decode it easily... 

like this:

  kubectl get secret/secretnaem -o yaml   :- it will show you the running secret output in terminal..

  echo -n "secret" | base64 --decode

  for this solution:
  ------------------

  we can send encoded secret to etcd server. but in etcd secret also in text format. but we can encrypt in etcd..

  1- for this we need to install "etcdctl" command line to use etcd command on terminal.

    apt-get  install etcd-client

  then use this,

  2- "ETCDCTL_API=3 etcdctl \ 
      --cacert=/etc/kubernetes/pki/etcd/ca.crt \
      --cert=/etc/kubernetes/pki/etcd/server.crt \
      --key=/etc/kubernetes/pki/etcd/server.key \
      get /registry/secrets/default/"secret-name"      ----> sirf itna hi likho gye tu secret apko text ma nazr aye ga.. tu use "hex" also.

  like this..

    "ETCDCTL_API=3 etcdctl \ 
      --cacert=/etc/kubernetes/pki/etcd/ca.crt \
      --cert=/etc/kubernetes/pki/etcd/server.crt \
      --key=/etc/kubernetes/pki/etcd/server.key \
      get /registry/secrets/default/"secret-name" | hexdump -C     ----> with "hexdump -C" it will encrypt the secret..  the output would be store in etcd... but in etcd also you see your data in unencrpted format.. anyone can access it and read it.. this is a problem.. 

  so need to convert it in encrypted formation
  --------------------------------------------

  ps -aux | grep kub-api | grep "encryption-provider-config"

  it will not show any result...now...  because encrypt option is not configured here,  ap same chez to "/etc/kubernetes/manifest/kube-apiserver.yaml" file ko open ker k b verify ker sakhty hn.

3- now with encryption file you can encrypt the resources mention in file,... like in our case me encrypt "secrets"

file:
=====
apiVersion: apiserver.config.k8s.io/v1
kind: EncryptionConfiguration
resources:
  - resources:   -------> give resources that need to encrypt(secret, pod , deployment..)
      - secrets   
    providers:    ---> in which we have eryption module
      - identity: {}   ----> for none
      - aesgcm:
          keys:
            - name: key1
              secret: ""
            - name: key2
              secret: ""
      - aescbc:
          keys:
            - name: key1
              secret: ""
            - name: key2
              secret: ""
      - secretbox:
            keys:
              - name: key1  
                secret: ""

do the same thing with the simple version of file..

enc.yaml
--------

apiVersion: apiserver.config.k8s.io/v1
kind: EncryptionConfiguration
resources:
  - resources:   -------> give resources that need to encrypt(secret, pod , deployment..)
      - secrets   
    providers:    ---> in which we have eryption module
      - aescbc:
          keys:
            - name: key1
              secret: ""
      - identity: {}


head -c 32 /dev/urandom | base64  --> use it and get random value and use this value to enc.yaml file as secret

4- now make this file available to pod.... hum isko volume ma rakh ker.. us volume ko pod ki kisi aik directory k sath mount kerwa dye gye tu wo file pod k lye available hojye gi,,,

for this:

  mkdir /etc/kubernetes/enc  --> make directory
  mv enc.yaml /etc/kubernetes/enc  --> move file in directory

  now add below configuration to kube-apiserver yaml file. so kube-api pod can have access of all the require this.. to do this task     /etc/kubernetes/manifest/kubeapiserver.yaml 

  " - --encryption-provider-config=/etc/kubernetes/enc/enc.yaml"
  
  volumeMounts:
  - name: enc
    mountPath: /etc/kubernetes/enc
    readyonly: true

  volumes:
  - name: enc
    hostPath:
      path: /etc/kubernetes/enc
      type: DirectoryOrCreate

now you can see encryption configuration option is available with kubeapiserver.. can verify with below commands.

  ps -aux | grep kub-api | grep "encryption-provider-config"

now to check our secrets will now be encrypt or not... 
-------------------------------------------------------

1- create secret now.... kuo k hum na encryption configure ker li ha ab hum jo b secret create ker k etcd server ma bhjye gye wo plan text na ni hogi...

  kubectl create secret generic my-secret-2 --from-literal=key=top-secret...

now secret create send it to etcd server..

  "ETCDCTL_API=3 etcdctl \ 
      --cacert=/etc/kubernetes/pki/etcd/ca.crt \
      --cert=/etc/kubernetes/pki/etcd/server.crt \
      --key=/etc/kubernetes/pki/etcd/server.key \
      get /registry/secrets/default/"my-secret-2" | hexdump -C     ----> with "hexdump -C" --> ab hmra data encrypt rhy ga.. etcd server ma b.

kubectl get secret --all-namespaces -o json | kubectl replace -f -

  is traha sa wo sab namespace sa secret ki file lye rha ha or new k sath replace ker rha ha...


A note on Secrets
-----------------

Remember that secrets encode data in base64 format. Anyone with the base64 encoded secret can easily decode it. As such the secrets can be considered not very safe.
--------
The concept of safety of the Secrets is a bit confusing in Kubernetes. The kubernetes documentation page and a lot of blogs out there refer to secrets as a “safer option” to store sensitive data. They are safer than storing in plain text as they reduce the risk of accidentally exposing passwords and other sensitive data. In my opinion it’s not the secret itself that is safe, it is the practices around it.

Secrets are not encrypted, so it is not safer in that sense. However, some best practices around using secrets make it safer. As in best practices like:

Not checking-in secret object definition files to source code repositories.
Enabling Encryption at Rest for Secrets so they are stored encrypted in ETCD.
Also the way kubernetes handles secrets. Such as:

A secret is only sent to a node if a pod on that node requires it.
Kubelet stores the secret into a tmpfs so that the secret is not written to disk storage.
Once the Pod that depends on the secret is deleted, kubelet will delete its local copy of the secret data as well.
Read about the protections and risks of using secrets here

Having said that, there are other better ways of handling sensitive data like passwords in Kubernetes, such as using tools like Helm Secrets, HashiCorp Vault. I hope to make a lecture on these in the future.

------------------------
Multi Container Pods(sidecar container)
------------------------

hum aik pod ma multiple container run ker sakhty hn..  for getting multiple benefits..

like: main application container k logs or metric leny k lye or other process ma help kerny k lye hum main application container k sath other cantainer create ker sakhty hn job hmry lye y kam kery. 

it has a shared lifecycle mean they are created or destory to gather. or wo same network or storage ko share ker rhy hoty hn... same network hony ki waja sa pod ma container locally communicaton ker rhy hoty hn...

exmple:
------

apiVersion: v1
kind: pod
metadata: 
  name: simple-webapp
  labels:
    name: simple-webapp
spec:
  containers:   --------> because it is an array so we can add multiple containers under the spec section...
  - name: simple-webapp
    image: simple-webapp        -------> container-1
    ports:
      containerPort: 8080
  - name: log-agent              -------> container-2
    image: log-agent

because inside the pod container shared network(aik hi) us ker rhy hoty hn. so containers ki communication "locally(localhost)" horhi hoti ha..

-------------------------------------
Multi-container Pods Design Patterns
-------------------------------------

There are 3 common patterns, when it comes to designing multi-container PODs. The first and what we just saw with the logging service example is known as a "side car" pattern. The others are the "adapter" and the "ambassador" pattern.

But these fall under the CKAD curriculum and are not required for the CKA exam. So we will be discuss these in more detail in the CKAD course.

---------------
Init Containers
---------------

In a multi-container pod, each container is expected to run a process that stays alive as long as the POD’s lifecycle. For example in the multi-container pod that we talked about earlier that has a web application and logging agent, both the containers are expected to stay alive at all times. The process running in the log agent container is expected to stay alive as long as the web application is running. If any of them fails, the POD restarts.

 

But at times you may want to run a process that runs to completion in a container. For example a process that pulls a code or binary from a repository that will be used by the main web application. That is a task that will be run only one time when the pod is first created. Or a process that waits for an external service or database to be up before the actual application starts. That’s where initContainers comes in.

 

An initContainer is configured in a pod like all other containers, except that it is specified inside a initContainers section, like this:

 

apiVersion: v1
kind: Pod
metadata:
  name: myapp-pod
  labels:
    app: myapp
spec:
  containers:
  - name: myapp-container
    image: busybox:1.28
    command: ['sh', '-c', 'echo The app is running! && sleep 3600']
  initContainers:
  - name: init-myservice
    image: busybox
    command: ['sh', '-c', 'git clone <some-repository-that-will-be-used-by-application> ;']
 

When a POD is first created the initContainer is run, and the process in the initContainer must run to a completion before the real container hosting the application starts.

You can configure multiple such initContainers as well, like how we did for multi-containers pod. In that case, each init container is run one at a time in sequential order.

If any of the initContainers fail to complete, Kubernetes restarts the Pod repeatedly until the Init Container succeeds.

apiVersion: v1
kind: Pod
metadata:
  name: myapp-pod
  labels:
    app: myapp
spec:
  containers:
  - name: myapp-container
    image: busybox:1.28
    command: ['sh', '-c', 'echo The app is running! && sleep 3600']
  initContainers:
  - name: init-myservice
    image: busybox:1.28
    command: ['sh', '-c', 'until nslookup myservice; do echo waiting for myservice; sleep 2; done;']
  - name: init-mydb
    image: busybox:1.28
    command: ['sh', '-c', 'until nslookup mydb; do echo waiting for mydb; sleep 2; done;']
 

Read more about initContainers here. And try out the upcoming practice test.

https://kubernetes.io/docs/concepts/workloads/pods/init-containers/

-------------------------
Self Healing Applications
-------------------------

Kubernetes supports self-healing applications through ReplicaSets and Replication Controllers. The replication controller helps in ensuring that a POD is re-created automatically when the application within the POD crashes. It helps in ensuring enough replicas of the application are running at all times.

Kubernetes provides additional support to check the health of applications running within PODs and take necessary actions through "Liveness" and "Readiness Probes". However these are not required for the CKA exam and as such they are not covered here. These are topics for the Certified Kubernetes Application Developers (CKAD) exam and are covered in the CKAD course.
