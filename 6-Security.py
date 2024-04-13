Security in kubernetes
----------------------

- is ma hum dekhy gye k kis tarha sa koi kubernetes cluster ki access leta ha... or kis tarha sa uska action ko control kya jasakhta ha.
- hum various "available authentication" method ko dekhy gye.
- hum "default configuration" ko dekhy gye... or practics kery gye.
- Hum "TLS certificate" ko dekhy gye or dekhy gye k kis tarha sa various kubernetes component secure hoty hn  in certificate ki waja sa.
- agr ap na cluster provision kya ha tu ap definatily TLS certificate ma issue face kery gye.. so we will see it and make it easy..

is k bd ap security of certificate k issue na nikal jye gye...

- we also learn about "autherization and specfically learn RBAC" 
- we also learn how to "secure your image" with security content..
- And finally learn "network policies"

Security Primitives in kubernetes
---------------------------------

In this lecture we will look at the various security primitives in kubernetes..

Of all access of hosts must be secured, like "root access disable", "password based authentication ", "but only SSH based authentication to be made available"

hmra focus is lecture ma kubernetes related security per hoga...  mean risks kya hn or ap kya steps lo gye us risk ko dor kerny k lye is per focus hoga...

- first line of defence hmra "kube api server" ha... jo b request outside the cluster sa ati ha wo sab sa phily is per ati ha... y aik tarha ha cluster k "gateway" ha.  y any wali request ko phily "authenticate" or "autherized"  or "validate" kerta ha,, phir update kerta ha information ko etcd ma.  kubeapi server k through hi sab component k dosary sa communication ker rhy hoty...

- kube api server 2 tarha k decisions leta ha.

    1- Who can access the cluster 
    2- and what can they do..

1- Who can access the cluster 
------------------------------

- ab is ki detail y ha k, who can access the cluster is ko hmra kube api ka "authentication mechanisms" dekh rha hota ha..

- different authentication k ways hn jis sa ap kube api server ko authenticate ker sakhty hn.

like:

    1- Files - User IDs and Passwords(stored in static files)
    2- Files - User IDs and Token(stored in static files)
    3- Certificates
    4- External Authentication Provider -LDAP (intregration with external authentication providers like "LDAP"),
    5- Service account(for machine(nodes) we create service accounts) 

or jb koi authenticate ker leta ha tu wo cluster ma kya kery ga... y "authorization mechanism" k under ata ha..

2- What can they do?
--------------------

or jb koi authenticate ker leta ha tu wo cluster ma kya kery ga... y "authorization mechanism" k under ata ha..

authorization implement hoti ha 

1- RBCA(Role base access control) sa, where user are associated with group with specfic permissions.
2- ABAC authorization(attributes base access control)
3- node authorization
4- webhook Mode

cluster ma sab component aik dosary k sath kube api server k through communication ker rhy hoty hn. or wo TLS encryption k through secure hoty hoti ha..

application ki communication k hawaly sa y ha k, by default all pod can communication with each other but you can restrict the access by using "network polices"

Authentication:
---------------

- We have users like administrators that access the cluster to perform administrative tasks.
- The developers that access to cluster to test or deploy applications. 
- We have end user who access the application deployed on the cluster.
- we have third party applications accessing the cluster for intregration purposes..

is section ma hum discuss kery gye k kis tarha sa hum secure ker sakhty hn cluster ko by securing communication b/w internal components(internaly securing k lye TLS encryption use hoti ha). and securing management access to the cluster through authentication and authorization.

is lecture ma hum authentication mechanism per focus kery gye.. mean un users k lye jo cluster jo access kerty hn administrative task k lye...

so for this we have two users...

1- is "Humans"(is user) access the cluster for administrative task
2- is "Robot(machine)(use service account fo this)" access the cluster to perform task such as other processes/services or application that require access to the cluster.

remember 
   
    1-kubernetes manage ni user accounts ko natively. y relie kerta ha external source like "file with user detail" or "certificate per" or third party identity service like "LDAP" per to manage these users.

    is lye ap kubernetes cluster ma users create ni ker sakthy but "user list" ker sakhty hn.. like "kubectl list users"

    2- but In case of "service account" kubernetes can manage them.

        like: 
        
            kubernetes create serviceaccount "serviceaccount name"

            you can create and manage service account using kubernetes API.


is lecture ma hum user access per focus kery gye... 

- "all user access managed by kube api server whether you  are accessing cluster through kubelet tool and other API directly" 
-  apki request sab sa phily kube api server k ps jati ha, kube api server request ko authenticate kerta or phir processing kerta ha,,

kube api server authentication kis tarha sa ker rha hota ha
-----------------------------------------------------------

there are different authentication mechanism. like:

- Static password file:     

   - is ma apky ps list of "username or password" hoty hn static password file ma. you can create list of username and their password in "csv file"(like file name "user-details.csv"). isko ap users ki information k source k tor per use ker sakhty hn
   - file k "3 colume hogye," "password" , "username and userid". ap is file ko kube api server ko pass ther do gye jis sa is file ma mojod user ko kub api server authenticate kery ga.. 
   - pass file to kube api server (--basic-auth-file=user-details.csv)  ---> agr hmra cluster "kubeadm" k through bna ha tu hum is information ko y to hum kub api server k pod ma under "command" dye rhy hogye. or volume k through directory path ko select ker k usko pod ksath mount kerwye gye...  otherwise "kube api service ki service file" ma dye rhy hogye. after this "you must restart" the service to take this effect.

   API Ka through hum kube api server ko is tarha sa authenticate ker sakhty hn by using username and password..
   ------------------------------------------------------------------------------------------------------------

        curl -v -k "kube-api-server address" -u "username:password"
        
    
   assign users to group
   ---------------------   

   same csv file ma hmry ps 4th coloume ma group name hota ha.. like this,,

      - file k "3 colume hogye," "password" , "username , userid and group"  .. ap is trha sa multiple users ko multiple groups k sath belong kerwa sakhty hn. or in groups per different permission lga sakthy hn.. is  
- Static token file: 

     - is ma apky ps list of "username or token" hoty hn static token file ma.

     - same static password file ki tarha , apki static token file hoti ha,. but is ma users k sath sath tokens hoty hn
     - pass file to kube api server (--token-auth-file=user-token-details.csv)  ---> agr hmra cluster "kubeadm" k through bna ha tu hum is information ko y to hum kub api server k pod ma under "command" dye rhy hogye.. otherwise "kube api service ki service file" ma dye rhy hogye. after this "you must restart" the service to take this effect.

    API Ka through hum kube api server ko is tarha sa authenticate ker sakhty hn..
    ------------------------------------------------------------------------------

        curl -v -k "kube-api-server address" --header "Authorization: "Username" "token""
       
    -"but remember above method is not remmended in authentication mechanism.. because it is not secure 
    - ap is static csv files ko jis ma user ki information ha ko "kubeadm sa set howy cluster ma kube api server k sath as volume attach ker k is volume ko pod sa mount kerwa sakthy hn. is trha sa host per pra data pod ko mil jye ga "
    - you can also set up RBAC for new users..
- certificate:

    ap certificate k through b authentication ker sakhty hn...

- identity services

    ap third party authentication protocal like "LDAP, kerberos" sa b authenticate ker sakhty hn.

-------------------------------------------    
Article on Setting up Basic Authentication
-------------------------------------------
Setup basic authentication on Kubernetes (Deprecated in 1.19)
Note: This is not recommended in a production environment. This is only for learning purposes. Also note that this approach is deprecated in Kubernetes version 1.19 and is no longer available in later releases

Follow the below instructions to configure basic authentication in a kubeadm setup.
----------------------------------------------------------------------------------
Create a file with user details locally at /tmp/users/user-details.csv

# User File Contents
password123,user1,u0001
password123,user2,u0002
password123,user3,u0003
password123,user4,u0004
password123,user5,u0005
Edit the kube-apiserver static pod configured by kubeadm to pass in the user details. The file is located at /etc/kubernetes/manifests/kube-apiserver.yaml

apiVersion: v1
kind: Pod
metadata:
  name: kube-apiserver
  namespace: kube-system
spec:
  containers:
  - command:
    - kube-apiserver
      <content-hidden>
    image: k8s.gcr.io/kube-apiserver-amd64:v1.11.3
    name: kube-apiserver
    volumeMounts:
    - mountPath: /tmp/users
      name: usr-details
      readOnly: true
  volumes:
  - hostPath:
      path: /tmp/users
      type: DirectoryOrCreate
    name: usr-details
Modify the kube-apiserver startup options to include the basic-auth file

apiVersion: v1
kind: Pod
metadata:
  creationTimestamp: null
  name: kube-apiserver
  namespace: kube-system
spec:
  containers:
  - command:
    - kube-apiserver
    - --authorization-mode=Node,RBAC
      <content-hidden>
    - --basic-auth-file=/tmp/users/user-details.csv
Create the necessary roles and role bindings for these users:

---
kind: Role
apiVersion: rbac.authorization.k8s.io/v1
metadata:
  namespace: default
  name: pod-reader
rules:
- apiGroups: [""] # "" indicates the core API group
  resources: ["pods"]
  verbs: ["get", "watch", "list"]

---
# This role binding allows "jane" to read pods in the "default" namespace.
kind: RoleBinding
apiVersion: rbac.authorization.k8s.io/v1
metadata:
  name: read-pods
  namespace: default
subjects:
- kind: User
  name: user1 # Name is case sensitive
  apiGroup: rbac.authorization.k8s.io
roleRef:
  kind: Role #this must be Role or ClusterRole
  name: pod-reader # this must match the name of the Role or ClusterRole you wish to bind to
  apiGroup: rbac.authorization.k8s.io
Once created, you may authenticate into the kube-api server using the users credentials

curl -v -k https://localhost:6443/api/v1/pods -u "user1:password123"

----------------
TLS CERTIFICATES(basic)   ----Also we learn in which how to create certificate for webapplication deployed in server for securing http communication(traffic) on webserver.
----------------

- What are TLS Certificates?
- How does kubernetes use Certificates?
- How to generata them?
- How to configure them?
- How to view them?
- How to troubleshoot issues related to Certificates.


we will see.... What are TLS Certificates, why we use them, and how it can be configure.

- "A certificate is used to guarantee trust b/w two parites during a transaction" 
-  for example, "when a user tries to access a web server, TLS certificates ensure that the communication b/w the user and the server is encrypted" and the server is who it say it is.

let take a scenario
-------------------

- let say k user na TLS certificate enable ni kya. or wo online backing application ko access kerta ha. so without tls certificate user k credentails plain text ma jye gy.. so hacker network traffic ko sniff ker k easily credentail ko retrive ker saktha ha. or user k bank account ko hack ker sakhta ha. 

- so iska hal k lye hum apny credentail ko encrypt ker k send kerna hoga... jis sa hacker agr network traffic ko snif ker k lye b leta ha tu use ni ker pye ga... same apka server b data ko decrypt ni ker pye ga... so apko key ki aik copy server per b rakhni hogi tky encrypted data ko decrypt ker sakhty.. 

- ab because key b ap same network sa send ker rhy hogye tu attacker(hacker) network traffic ko sniff ker k key ko b hack kker k us ko use ker k apka data ko decrypt ker lye ga..

This is known as "SYMMETRIC ENCRYPTION"  Y Secure way ha encryption ka "but y use kerta ha same key ko encrypt or decrypt" kerny k lye.. ab kuo ko key sender(user) or receiver(server) k b/w exchange hoti ha. so risk ha k hacker isko access ker sakhta. or data ko key sa decrypt ker sakhta ha..

so is k hal k lye "ASYMMETRIC ENCRYPTION" use hota ha 
-----------------------------------------------------

    instead of using a single key to encrypt and decrypt data "ASYMMETRIC ENCRYPTION" uses a pair of keys(private key and public key(understand k lye isko public lock b kha skahty hn..))

    y dono keys ap "ssh-keygen" command ko terminal ma use ker k create ker sakthy hn. 

    like:

    "ssh-keygen"  ----------> 

    and it will make "id_rsa   id_rsa.pub" . jo yha pr raki hoti ha "/.ssh/authorzied_key.."  
    
    - "mean" ab hoga kya k ap apny webserver ma (public(lock(lock ki movement hogi mean public key publicky move hogi b/w user and server)) or private key create ki(jo server ma hi hogi).  ab ap user jb first time webserver ko access kerta ha tu usy public key mily gi... or ap khud b user ko public key dye sakhty hn. agr movement ma hacker key lye ga tu wo public key hogi because abi wo travel hoi ha.. 
    -  ab apka user(mean uska browser) SYMMETRIC key ko apki public key k sath encrypt ker k usko webserver per send kery ga. "apki publickey(lock) isko server ma pari private key decrypt kery gi and retrive the SYMMETRIC key". ab apky server ma "SYMMETRIC key"  safely pohan gi ha... because agr hacker na is br data lya tu isk ps SYMMETRIC key+public key aye gi.. becasue abi wo travel ker rhithi... "but publickey ko decrypt kerny k lye private key ni hogi.. so hacker decrypt ker k SYMMETRIC key ni lye sakha"
    - ab ap "SYMMETRIC key" k through data user(mean uska browser) sa encrypt ker k send kery. or wo websever per jakr SYMMETRIC key decrypt kery gi.. is tarha sa data safely user sa websever tk jye ga or dono k b/w communication secure rhy gi....  

    sir kha rhy hn public key(id_rsa.pub) k through apka server lock hoga.. jis ko ap apni private key(id_rsa) sa unlock kery gye... 

    if you have multiple server then you need to take a copys of keys and set for on multiple server.. 

    "or agr multiple users na key generate ker k session bnana ho.  tu other users "ssh-keygen" sa key create ker k public key ko server ma dye, unki public key sa server lock hojye ga, jo k  unki private key ko use ker k wo open kery gye..."   mean server ko agr multiple users na access kerna ha tu wo apni private or public key create kery "ssh_keygen" sa, phir us key ko server ko dye dye so wo private key jo server ma ha public key ko unlock ker. mean ap multiple public key(for multiple users) dye sakhty hn "/.ssh/authorized_key" ma..

same:
----

    SSL k case ma hum "openssl genrsa -out my-back.key 1024" or "openssl rsa -in my-back.key -pubout > mybanck.pem" is a hum server ma public or private key create kery gye..

    ab hoga kya k ap apny webserver ma (public(lock(lock ki movement hogi mean public key publicky move hogi b/w user and server)) or private key create ki(jo server ma hi hogi).  ab user jb first time webserver ko access kerta ha tu usy public key mily gi... or ap khud b user ko public key dye sakhty hn. agr movement ma hacker key lye ga tu wo public key hogi because abi wo travel hoi ha.. 
    -  ab apka user(mean uska browser) SYMMETRIC key ko apki public key k sath encrypt ker k usko webserver per send kery ga. "apki publickey(lock) isko server ma pari private key decrypt kery gi and retrive the SYMMETRIC key". ab apky server ma "SYMMETRIC key"  safely pohan gi ha... because agr hacker na is br data lya tu isk ps SYMMETRIC key+public key aye gi.. becasue abi wo travel ker rhithi... "but publickey ko decrypt kerny k lye private key ni hogi.. so hacker decrypt ker k SYMMETRIC key ni lye sakha"
    - ab ap "SYMMETRIC key" k through data user(mean uska browser) sa encrypt ker k send kery. or wo websever per jakr SYMMETRIC key decrypt kery gi.. is tarha sa data safely user sa websever tk jye ga or dono k b/w communication secure rhy gi....  

    So is tarha sa hum ASYMMETRIC way sa 2 key create kerty hn (public or private) then in key ko use kerty howy SYMMETRIC key ko hum safely hacker sa bachty(track ma na aty howy) howy webserver per lye ker aty hn. jb key server per ajti ha tu data ko hum SYMMETRIC key k sath encrypt ker k webserver per send kerty hn jo k webserver ki SYMMETRIC key sa decrypt hota ha. or is trha sa user(browser sa paki communication safely webserver k sath horhi hoti ha.)

but: 

    hacker is way ko track ker k b apki key ko hack ker sakhty hn.. like wo apki website ki trha ki same website apky destination server ma rakhy gye.. or apki network traffic ko sniff ker k destination ip apny webserver ka dye dye gye... ab jb apki request webserver per jye gi... webserver per (dono public or private ki hn) wo apki request ka against public key apko dye ga... then an k brower SYMMETRIC key ko publickey k sath encrypt ker k webserver per send kery ga... jis sa hack ka webserver ki private key sa wo publickey ko decrypt ker k SYMMETRIC key lye lye ga... or jb b ap important information(data) SYMMETRIC key k through encrypt ker k send kery gye tu hacker k ps b SYMMETRIC KEY hogi tu wo isko use kerty howy decrypt ker k data ko lye lye ga.

Solution:    once you create public and private key on your server
--------

    - is sab k solution certificate ha. certificate aik proper "CA" organization k through issue hota ha. ap certificate creation k lye information like (publickey + domain ) dety  hn. jis per wo apko certificate issue kerta ha. "jis per mention hota ha k kis ko issue howa ha or kb issue howa, publickey of server, domain, jis organization na issue kya uska signature(jo k private key sa hota ha), location of server etc(y sab information ap certificate creation k time dety hn)" CA isko validate kerta ha, then apko y certificate deta ha.. ha proper information hoti ha.. y certificate hum webserver k sath attach kerty hn, 
    
    - so user ki request k against "certificate jis per publickey hoti ha" milta ha user ko websever sa ,user(browser isko validate kerta ha). 

    web-browser validation kesy kerta ha
    -----------------------------------

    well know "Certificate authority CA" certificate ko sign kerti ha.. some of the "popular  CA certificate provider is"  

    - Symantec
    - GlobalSign
    - digicert
    - COMODA
    - certboard

    in ka b certificate issue kerny k aik process ha... y b public or private key ko use kerti hn. in sab ki CA's ki public keys user browser ma store hoti ha(ap isko browser ki certificate setting ma dekh sakhty hn). or private key sa CA's certificate ko sign kerti hn.. so jb browsers k ps certificate ata ha tu wo public key or private use kerty howy certificate ki validation ko confirm kerta ha..

    
    
    or agr hacker certificate banaye ki kosish kerta ha tu wo certificate per signature b apny kery ga y ksis k b kery, tu apka brower itna smart ha wo unvalid signature jo certificate per howy hoty hn ko(public or private key ki help sa) detect ker lena ha jo , or SYMMETRIC key ko ni deta.. 
    all the browser have the certificate validation mechanisms. fake certificate k case ma browser apko warn kery ga..



How to generate certificate:
----------------------------

    ap "key or domain name k through certificate ko create ker sakthy hn"

    like:
    -----

      openssl req -new -key my-bank.key -out my-bank.csr
        -subj "/C=US/ST=CA/O=MYOrg, Inc./CN=my-bank.com"   --> "here my-bank-key is a public key" and "CN=my-bank.com" represents domain.  k ap Certificate authority ko apni information send ker rhy hn. ab certificate authority apki information ko validate kery gi, then wo apko certificate issue kery gi.. 

different website ko access kerty hn so un per jo Certificate lgye howty hn unki website k lye wo public CA's hoty hn. ap apni private website ko access kerny k lye private CA's b lga sakthy hn.. for that we can create private symmetic server internally within the company..

Summary
-------

- sir khty hn k admin use kerta ha pair of keys for securing connectivity.  ---> y kam hum "ssh-keygen" k through keys(public/private key) create ker k ker rhy hoty hn.  is ma public key server k ps hoti ha or private admin k ps...
- servers uses the pair of key's to secure https traffic'. ---> is k lye certificate create kerna hota ha ---> jis k lye humy certificate authority ko information deni hoti ha.. like -> (public/private key create krny k bd)  -->  "openssl req -new -key my-bank.key -out my-bank.csr /-subj "/C=US/ST=CA/O=MYOrg, Inc./CN=my-bank.com" --> we are giving the domain ma publickey to CA. CA information ko validate kery ga or CA organization apni private key sa certificate ko sign ker k humy dye ga. hum is certificate ko server k sath attach kerty hn.
  
  ab certificate per server ki public key or CA ki private ki sa sign howa ha.. jb user ki request webserver k ps jye gi.. wo is certificate ko user(browser) ko dye ga. user(browser) per certificate ki private key k against CA ki public key store or available hogi.  "brower CA KI private/public key ko use kerty howy retrive kery ga webserver ki publickey" 

  phir browser SYMMETRIC key(jo k communication k lye hoti ha) ko webserver ki publickey k sath encrypt kery ga or is webserver per wapis send kery ga.. ab server apni private key jo publickey k sath us na bnai thi usko use kerty howy public key ko decrypt ker ga or SYMMETRIC key ko retrive ker lye ga.  jis sa safely SYMMETRIC key webserver k ps hogi.. 


ab client na tu validate ker lya ha ks server trusted ha but server na tu y validate ker ni kya k client trusted ha.
--------------------------------------------------------------------------------------------------------------------

so what can server do to validate client:
-----------------------------------------

is k lye server client sa "client certificate" mangta ha... so client valid pair ko keys ko generate kerta ha or key information ko CA ko dye ker sign kerwata ha phir isko server ko deta ha. tky wo client ko verify ker sakhy k wo authentica ha y ni...


is complete process ko PKI(PUBLIC KEY INFRASTRUCTURE) khty hn..

publickey(lock) or private key
------------------------------

is k bary ma sir na y btaya ha k "public key sa encrypted data ko private key decrypt ker sakhti or private key sa encrypted data ko public key decrypt ker sakhti ha"    

but remember:
------------ 

private key sa encrypted data ko koi b public key decrypt ker lye gi.

Naming conventions
------------------

certificate(public.key) "*.crt , *.pem"

- server.crt  ------|
- server.pem  ------| --> (usually certificate with public key are named ".crt", ".pem" . these are server certificate ) 
- client.crt  ------|
- client.pem  ------| -->  ( these are client certificate )


certificate(private.key) "*.key , *-key.pem"

- server.key         ---> jis k agy ".key" hoga, wo "private ki hogi". or jis k agye key ni hogi .. wo ya tu public key , y certificate hoga..
- server-key.pem
- client.key
- client-key.pem

-------------------------------
Kubernetes-Certificate creation(for client and server services)   ----> : client/server service basically these are the kubernetes cluster component which we are saparated by their services to attach certificate with them for secure communication b.w the cluster component..
-------------------------------

Naming conventions
------------------

certificate(public.key) "*.crt , *.pem"

- server.crt  ------|
- server.pem  ------| --> (usually certificate with public key are named ".crt", ".pem" . these are server certificate ) 
- client.crt  ------|
- client.pem  ------| -->  ( these are client certificate )


certificate(private.key) "*.key , *-key.pem"

- server.key         ---> jis k agy ".key" hoga, wo "private ki hogi". or jis k agye key ni hogi .. wo ya tu public key , y certificate hoga..
- server-key.pem
- client.key
- client-key.pem

kubernetes cluster (master or workernodes )  per mushtamil hota ha.. master ki sab worknodes k sath communication secure or encrypted hoti ha..

for example administrators cluster component k sath kube api server k through communication kerta ha wo secure honi chahye..

so we have 2 requirements for this.....
---------------------------------------

"all services within a cluster use server certificate. and all client use client certificate to verify how they say they are( mean kon hn wo)_"

so lets explore component within a cluster and identity various server or clients ko k kis na kis sa bt kerni ha
----------------------------------------------------------------------------------------------------------------------



server component in kubernetes cluster..
----------------------------------------

------------------------------
let start with kube api server(server ha is per server certificate hoga)
------------------------------

jesa k hum janty hn k kube api server expose HTTP service ko jisko other component k sath sath external users use to managed the kubernetes cluster. 

to y server ha or y require kerta ha certificate to secure communication with it clients.  so is k lye hum certificate or key pair generate kerty hn.. jis ko hum ("api server.crt or api server.key" kahty hn.)


as i mentioned earliar "anything with .crt(1) is sa certificate or any thing with .key is a private key".. remember certificate ki naming convention different taraha sa banye cluster ma different hoti ha.

(1)- jasa k hum na phily learn kya ha k certificate jo organization deti hn us certificate per apki "publickey(or other information like domain etc), us organization ka signature(with private key) hoty hn" 

-----------
ETCD server
-----------

another server is etcd server. etcd server cluster ki state(information) ko apny under store kerta ha.. so isko b pair of certificat or key chahye apny lye..

jisko hum(etcdserver.crt or etcdserver.key) khty hn.

--------------
Kubelet server
--------------

y worker node k component ha.. y b "HTTP API ENDPOINT" service ko expose kerta ha jis sa kube-api server bt ker sakhy worker nodes sa interact kerny k lye. isko b "certificate or key pair" chahye hota ha..(kis ko hum "kubelet.crt and kubelet.key" khty hn)


these are server component in kubernetes cluster..


client component in kubernetes cluster..
----------------------------------------

who are the clients, who access these services.

admin(us)
--------
client ko jo access kerta ha "kube api server" wo "hum hn" mean the administrators. through "kubectl or REST API"

ab admin users require hota ha "certificate or key pair" to authenticate the kube-api server. jis ko hum(admin.crt or admin.key) khty hn.

schedular
---------

schedular communication kerta ha kube-api server k sath to look for pods(showing in pending state in etcd) that require scheduling. or pending pods k pta chalny k bd y worker nodes find kerta ha or kube api server ko btata ha(phir kubeapiserver is info ko etcd ma update kerta ha)

"so kubi api server k lye schedular aik client ha like admin(us). schedular ko apni identity ko validate kerwana hota ha client TLS certificate k sath.." so iski apni pair of keys hoti hn ("schedular.crt , schedular.key")   

Kube Controller-Manager
-----------------------

y aik or kube api server k client ha jo kube api server ko access kerta ha. isko b apni identity ko validate kerwany k lye certificate chahye hota ha,("controller.crt . controller.key" is k certificates hn).. it is use to manage the controller..(like deployemnt, replicaset , replication controller , service  so on so far....(get the controller list form  google))

kube proxy
----------------

y aik or kube api server k client ha jo kube api service ko access kerta ha. isko b apni identity ko validate kerwany k lye certificate chahye hota ha,(we will call it "kube-proxy.crt . kube-proxy.key" is k certificates hn)... y basically kubernetes nodes ki networking ki reponsibility ko manager ker rha hota ha..


remember
---------- 
"sab component ma sa kube api server hi ha jo etcd sa bt kerta ha..." so etcd k lye kube api server aik client ha.. so kube api server ko apni identity ko validate kerwana hota ha jis k lye wo apny certificate(api server.crt , apiserver.key)  or "you can create saparate certificates for kube api server to specfically communicate to etcd."

same for kubelet, kube api server kubelet sa bt kerta ha... node ki activity ko jany k lye y instruction ps kerny k lye.. so kubelet k lye kube api server aik client ha.. so kube api server ko apni identity ko validate kerwana hota ha jis k lye wo apny certificate(api server.crt , apiserver.key)   or it can create saparate certificates for kube api server to specfically communicate to kubelet.


y sab certificate ko hum, certificate authority(CA) sa sign kerwye gye.. kubernetes requires atleast aik CA hona chahye jis sa ap certificate ko sign kerwye. or multiple CA's b hosakhty hn..

"you know CA ki apny pair of certificate or key hoti ha.. (isko hum ca.crt or ca.key)"


TLS in kubernetes certificate creation
--------------------------------------

"how to generate certificate for a cluster" 

certificate ko generate kerny k lye different tools available ha such as "EASYRSA " , "OPENSSL " , "CFSSL"

HUM "OPENSSL" per focus kery gye...
-----------------------------------

- firstly hum private key ko create kery gye. openssl command ko use kerty howy..

   openssl genrsa -out ca.key 2048       -->ca.key

- then we use open SSL request command along with the key to generate a "certificate siging request":

    openssl req -new -key ca.key -subj "/CN=KUBERNETES-CA" -o     -->ca.crs       is ma apki detail hogi but signature ni hoga,..

- finally we sign in the certificate using the openssl x509 command:

    openssl x509 -req -in ca.csr -signkey ca.key -out ca.crt   ---> ca.crt  
    
ab y CA ki taraf sa certificate ha, tu isko CA hi sign kery ga using its own private key that it generated in first step.

"sir kh hry hn k is k alawa all other certificate k lye hum CA key pair ko use kery gye sign kerny k lye..."now CA has it private key and root certificate file. 

let now look at generating the client certificate:
--------------------------------------------------

admin user
----------

Follow the same steps to create certificate.

- openssl genrsa -out admin.key 2048  --> admin.key(private key)
- openssl req -new -key admin.key -subj \
          "/CN=kube-admin" -out admin.csr   ---> admin.csr   "kube-admin" k jaga koi b name hosakhta ha.. y wo name ha jisko kubectl client authenticate kerta ha jb wo run kerta ha kubectl command ko.. so audit log or else where ma y name humy dekhta ha..
finally generate certificate 
- openssl x509 -req -in admin.csr -CA ca.crt -CAkey ca.key -out admin.crt     --> admin.crt

y aik valid certificate create ker dye ga cluster k lye.. y wo certificate hoga jis ko admin user(like us) use kery gye cluster ko authenticate kerny k lye..


how to differentiate this user with any other user. user account needs to be identical as an admin user and not just another basic user. you do that by adding the group detail for the user in the certificate. in this case SYSTEM:MASTER group name mentioned in the certificate..

but you need to mention like this,

- openssl req -new -key admin.key -subj \
          "/CN=kube-admin/O=system:master" -out admin.csr 

          once it sign we now have certificate for admin user with admin privalages..

like this ap other cluster component(schedular,kube controller , kube proxy) k lye b certificates create ker sakhty hn.

kube schedular server
---------------------

kube schedular kubernetes control plane k system component k part ha.. is lye iska name pre-fixed hoga with the key word like "system"


kube controller manager
-----------------------

same kube controller manager kubernetes control plane k system component k part ha.. is lye iska name pre-fixed hoga with the key word like "system"

kube proxy
----------

same process...


is trha sa ap "services for clients k lye certificate" create ker lye gye... follow same process to create other client certificate(job hum specfically kisi service k lye create kerty hn) for api server and kubelet..

what do you do with these certificates
--------------------------------------

like admin(user) jo admin certificate ko use ker k cluster ko access ker saktha ha..(cluster ka "authentication mechanisms" ma b hum na "certificate" k through authentication dekhi thi i think wo y ha.) 

like access cluster with REST API KEY:
--------------------------------------
curl https://kube-apiserver:6443/api/v1/pods \               --> represent http end point expose service by kube-apiserver.... mean admin certificate k through cluster ma kube api server k expose end point access ker k certificate k through authenticate ekr rha ha..
        --key admin.key --cert admin.crt  --cacert ca.crt 

other way to do the same thing with yaml file:
----------------------------------------------

apiVersion: v1
clusters: --list/array
- cluster:
    certificate-authority: ca.crt
    server: https://kube-apiserver:6443
  name: kubernetes
kind: Config
users:
- name: kubernetes-admin
  user:
    client-certificate: admin.crt
    client-key: admin.key

ab sir kha rhy hn k jis tarha sa hum na dekha k certificate creation with web application k case ma (server or client dono ko aik dosary ko authenticate kerna hota tha) jis k lye wo aik dosary sa certificate exchange kerty thy tky wo aik dosaey ki validity ko check ker lye....

same isi tarha kubernetes cluster ma client or server service aik dosary ki validity ko check kerny k lye copy of certificate ko exchange kerty hn..

------------------------------
certificate for server servics
------------------------------

etcd server
-----------

same procedure ko follow kerty howy jesy hum na client services k lye above ma certificate bnye hn, same isi tarha sa hum server services k lye certificate create kery gye. but with the name "ETCD-SERVER".

- ca.key |
- ca.crt |  --->  y hum na upper dekha tha ka kesy create kerty hn.
- etcdserver.crt  |
- etcdserver.key  | ---> same process follow mention above to create this like we have created certificates for client component.        


sir khty hn "ETCD server can be deployed as a cluster accross multiple servers as an high availability enviroment"

in that case to secure communication b/w the different members in the cluster, we must "generate additional peer certificate". Once the certificates are generated specify them while starting the ETCD server.


matalbe aik cluster ma aik sa zayada etcd server ho sakthy hn... for high availability k lye.. ab in etcd server ki aps ma secure communication k lye b hum certificate chahye.. like  general additional peer certificate... 

ab apko "etcd.yaml"(i think in case of kubeadm) or "etcd.service file(otherwise)" ma inka(etcd's') btana hoga.....

like:  vi etcd.yaml  or etcd.service

  --peer-cert-file=/path-to-certs/etcpeer1.crt

And finally as we discussed earler it requires the CA root certificate to verify the clients connecting to etcd server is valid.

kube api server
---------------

Everyone talk to the kube api server. Every operation goes through the kube api server. anything moves in the cluster kube api server knows about it...

sir na kha ha k people kube api server ko differnent name sa call kerty hn... jis name sa b call kery usko certificate ma hona chahye.... tb hi valid connection bn sakhta ha. hum kube api server ko kube api server hi khty hn, so kube api server ka certificate ma kube api server k hi name hoga...

 1- openssl genrsa -out apiserver.key 2048    ---> apiserver.key          it will create a private key

 2- openssl req -new -key apiserver.key -subj \
      "/CN=kube-apiserver" -out apiserver.csr  --> apiserver.csr     hum abi certificate ma kube api server mention ker rhy hn...


alternate name:
--------------

  is k lye apko "openssl.cnf"  ma under "[alt names]" ma alternate names add kerna hogye.

like:

openssl.cnf
[alt names]

  DNS.1= kubernetes
  DNS.2= kubernetes.default
  DNS.3= kubernetes.default.service
  DNS.4= kubernetes.default.svc.clustur.local
  IP.1=
  IP.2=

  then pass the openssl.cnf file name in command...

  openssl req -new -key apiserver.key -subj \
      "/CN=kube-apiserver" -out apiserver.csr -config openssl.cnf

  3- openssl x509 -req -in apiserver.csr -CA ca.crt -CAkey ca.key -CAcreateserial -out apiserver.crt -extensions v3_req -extfile openssl.cnf -days 1000  ---> apiserver.crt   --yha per ap certificate signing kerwa rhy hn..


  y wo certificate ha jo kube api server use kery ga "etcd" or "kubelet" sa communication k lye. in files ko hum kubeapi service ki service file ma dye gye(y executable ma dye gye)..

  "kube api server ki service file ma etcd or  kubelet dono k certificate hogye.. because  client or server dono aik dosary k certificate mangty hn validation k lye.." ab kube api server client ha etcd or kubelet ka.. so dono(client or server) ki file ma i think aik dosary k certificate hogye validation k lye..(y confirm kerna ha)

kubelet 
--------

it is an HTTPs API server(1) that runs on each node and it is responsible for managing the node. That's where the API server talks to monitor the node as well as any information regarding what pods to schedule on this node'. is k lye apky ps key or certificate pair ki zaroorat hogi for each node in the cluster. each certificate per name (node1 , node2 , node3 ..) hoga..


1- mean y http API end point ko expose kerta ha jis sa kube api server is sa bt kerta ha or isko instructure ps kerta ha. or cluster ki update leta ha..

kubelet-config.yaml
-------------------

apiVersion: kubelet.config.k8s.io/vibeta1
kind: kubeletConfiguration
authentication:
  x509:
    clientCAFile: "/var/lib/kubernetes/ca.pem"   ---> certificate file..
autherization:
  mode: webhook
clusterDomain: "Cluster.local"
clusterDNS:
  - "ip"
podCIDR: "$(POD_CIDR)"
resolvConf: "/run/systemd/resolve/resolv.conf"
runtimeRequestTimeout: "15m"
tlsCertFile: "/var/lib/kubelet-node01.crt"-------------------|
tlsPrivateKeyFile: "/var/lib/kubelet/kubelet-node01.key"  ---|> kubelet node certificates


y hr node ma hoga...


"or client certificates of kubelet jo k hum kube api server ko dye gye certificate validation k lye that will be used by the kubelet to communicate with kube api server."

y certificate kubelet ki authentication kube api server sa kery gye.. 

the api server needs to know which node is authenticated and give it the right set of permissions. so it requires the nodes to have the right names in the right format.

since the nodes are system components, like the kube-schedular and controller manager. so the format of name on certificate of nodes will start from "system:node:nodename".

or api server per right set of permission deny k lye wo nodes ko add kery ga group ma "system=nodes" it will mention in the certificate.. 
once the certificate generate it will go into the "kube-config" file



easy to understand
-------------------
let say k ap usy kerty hn command "kubectl run pod-name --image=image-name"  matlab ap aik pod ko schedule kerna chah rhy hn node ma... ab backend ma isky jo process hoty hn wo interesting hn...

- command kubectl(terminal) jo k admin use ker rha ha sa kube-api server k ps jye... kube api server isko authenticate kery ga phir validate kery ga phir authorzied kery ga.. or then information ko etcd ma update kery ga... 

- ab abi tk 3 service ma aps ma bt ki(admin(kubectl sa), kubeapi server, etcd ) in sab services ki communication secure or encrypt ho is k lye y apny apny certificate use kerty hn or client or server certification k validation k lye y aik dosary ko apny apny certificate exchange kerty hn(inko ap aik dosry ki service ma khud b rakh sakhty hn)..

mean kubeapi server k apny certificate k sath sath client certificate b hoty hn jo y other service like kubelet or etcd ko deta ha authentication or communication ko successfull kerny k lye. same etcd or kubelet kerty hn.

ab kube schedular kube api server k sath communicate kery ga tky wo etcd ma pr pod jo abi pending state ma hn ko observe kery or in k lye node proper node find ker k la ker kube api server ko update kery , so kube api server is info ko etcd ma update ker dye ga.

- abi b 3 service(schedular , kubapi server , etcd) bt ker rhy hn, so y communication ko secure or encrypt rakhty k lye apny apny certificate use kery gye or apny apny client certificate ko exchange kerty hn apni validation k lhye(ap in ki service file ma b rakh sakhty hn aik dosary ki certificate details.)

same ab kube api server found node ma kubelet(http expose endpoint k through) k ps jye ga or isko instruct kery ga k wo pod ko create kery is node ma...  so y communication ko secure or encrypt rakhty k lye apny apny certificate use kery gye or apny apny client certificate ko exchange kerty hn apni validation k lhye(ap in ki service file ma b rakh sakhty hn aik dosary ki certificate details.)

mean hr kubernetes cluster component na agr kisi or cluster component k sath communication keri ha tu wo kubi api server k through kery ga... or in ki communication secure rhy is k lye y client or server certificate use kerty hn or exchange kerty hn..



-------------------------------
How to View Certificate Details
-------------------------------

is lecture ma hum dekhty gye k hum existing cluster ma kis tarha sa certificates ko dekh sakhty hn...

before starting any troubleshoot with certificate. you need to know on what way the cluster was created.. hum different way sa cluster create ker sakhty hn...

- THe hard way    ---> mean agr ap na cluster ko khud scratch sa create kya ha tu apko sab certificates khud create kerna hogye.
- Kubeadm    ----> is sa kery gye tu y apky khud sab create ker dye ga..

2 hardway sa bnanye cluster ma sari native  service nodes ma bnti ha but kubeadm sa bny cluster ma services pod ma bnti ha.. wo trouble shooting kerty time apko pta hona chahye k kisi information k lye kha jana ha

let say k hmra cluster kubeadm sa create howa ha,, or hum na health check ko perform kerna ha..
----------------------------------------------------------------------------------------------

or ap na certificate ki details view ker k information gather kerni ha.. like "certificate path" "CN name" "alt name" "organizaiton" "issuer" " expiration"

1- "cat /etc/kubernetes/manifests/kube-apiserver.yaml"     

  kubeadm k case ma is file ko kube-api server k lye open kery gye tu apko certificate ki details mil jye gye... ab ap one by one ker k certificate ko open kery or information gather kery

certificate ki detail open kery k lye ap y command use kery

2-  "openssl x509 -in /etc/kubernetes/pki/apiserver.crt -text -noout"  ---> ya certificate info ap "cat" ker k yha sa lye rhy hn  /etc/kubernetes/manifests/kube-apiserver.yaml 

  get "CN NAME" , "ALT NAME" "get expiration date under validity('not after')" , "issuer"

  is tarha sa ap sab certificates ki info is command ko use ker k nikal sakhty hn.


Inspect service log
---------------------



  journalctl -u etcd.service -l   --> use when you create native(khud) cluster setup kya ho...

  kubectl logs etcd-master        --> kubeadm sa bnye cluster k case ma, wo pod sa logs dekh rha hota ha
  
"sometimes kube api server or etcd server down hoty hn us time kubectl sa commmand execute ni hoti us case ma apko docker sa kam lena parta ha logs ko fetch kerny k lye" 
 
  docker ps - a ---> get container id 
  
and then use logs command to see logs.

  docker logs container-id


------------------------------------
Certificate Health Check Spreadsheet
------------------------------------

I have uploaded the Kubernetes Certificate Health Check Spreadsheet here:

https://github.com/mmumshad/kubernetes-the-hard-way/tree/master/tools

Feel free to send in a pull request if you improve it.

----------------------------
Certificate Workflow and API
----------------------------

In this lecture we will see how to manage certificate and what the certificate API is in kubernetes.

sir kha rhy hn k let say hum na cluster create kya or us ma sab component k lye certificate create ker dye or admin k lye b certificate create ker dye... tky admin cluster ko access ker sakhty..

abi sirf admin ki owner ha jo(apni .crt .key) files k through cluster ko access ker sakhty ha.. "but aik new admin ata ha jis na b cluster ko access kerna ha. so what he gona do"

1- new admin need to create his own (.crt .key) files...

like this:
----------

     openssl genrsa -out new-admin.key 2048  --> new-admin.key(private key)
     openssl req -new -key new-admin.key -subj \
          "/CN=kube-admin" -out admin.csr   ---> admin.csr   "kube-admin" k jaga koi b name hosakhta ha.. y wo name ha jisko kubectl client authenticate kerta ha jb wo run kerta ha kubectl command ko.. so audit log or else where ma y name humy dekhta ha..
finally generate certificate 
     openssl x509 -req -in admin.csr -CA ca.crt -CAkey ca.key -out admin.crt     --> admin.crt          (ya per hum ca.crt or ca.key ko use ker k apny certificate ker sign CA sa kerwa rhy hn..)

so new admin create a private key and generates a certificate siging request and send it to "old admin". because abi old admin hi actual ma admin ha.. then old admin CA ko certificate siging k lye request kery ga. or CA apni private key sa certificate ker sign kery ga... then old admin certificate ko wapis new admin ko send ker dye ga...

ab new admin k ps apna valid ca.crt or key hogi jis sa woo b cluster ko access ker sakhta ha...

but issue y ha k..
-------------------

Certificate ka apna validity period ha. jis k khtam hony k bd certificate expire hojye ga.. then again new admin same process ko follow kery ga "new CSR" bnye ga or usko signing k lye old admin ko send kery ga or old admin isko CA( CA signing private key ko use kerty howy kerta ha) sa sign ekrwa ker new admin ko wapis send kery ga..

ab sir kh rhy hn k hum br br kh rhy hn k old admin signing k lye CA server per request kerta ha.. CA server khud kya ha. or y kubernetes ma kha located ha
----------------------------------------------------------------------------------------------------------------------------------------------------------

CA server khud kya ha. or y kubernetes ma kha located ha.

it is just a pair of "key and certificate files(ca.crt , ca.key)" we have created" . jis ko in pair ko file ko access leni ha or sign kerwana ha koi certificate in kubernetes enviroment. y jinty users jitni privileges(permission) k sath certificate ko sign kerwana chahye gye kery ga..

"so in files ko protected or safe enviroment ma store kerny k zaroort ha.. jesy k hum inko server ma rakh sakthy hn jo k fully secure b hota ha.. so us server ko hum "CA server" khy gy.  jb ap na koi siging kerwani ap isko access ker or signing kerwa lye.." abi tk hum na master node k component k lye certificate kya tha or hmry root certificate(ca.crt , ca.key) b master node ma hn wo hum is node ko CA server kha sakhty hn.

kubeadm sa bny cluster ma b root certificate master node ma hoty hn... 

"abi tk hm manually signing kerwa rhy thy CA server sa" but jesy jesy users increase hogye apko alternete or better way ki zaroort pary gi is kam k lye...

kubernetes k ps "built-in Certificate API " ha jo ap k lye y kam kerti ha..
---------------------------------------------------------------------------

  With built-in certificate API you can send a Certificate Signing request directly to kubernetes through an API call.

  ab jb new admin certificate signing k lye old admin ko send kery ga ab old admin CA server ko logging ker k sign kerwany k bjye us per aik "kubernetes API object" create ker dye ga jisy hum "Certificate Signing Request" khty hn.
  
  is tarha sa multiple users certificate signing request old admin k ps aye gi tu wo built-in feature certificate API k through aik Certificate signing object or iski request cluster ko keryga...  cluster jb dekhy ga k request cluster k admin ki traf sa i ha tu wo isko review kery ga or Easy approve ker dye ga..

  phir in certificate ko hum extract ker k user ko share ker dye gye...

see how to do this
------------------

-1 create a private key

  openssl genrsa -out jane.key 2048   ---> jane.key

-2 send request to the admin

  openssl req -new -key jane.key -subj "/CN=jane" -out jana.csr    --> jana.csr

  admin key lye ga or certificate signing request object create kery ga is k lye..   
  
  "The certificate siging request is created like any other kubernetes object using a manifest"

jane-crs.yaml
-------------
apiVersion: certificates.k8s.io/v1
kind: CertificateSigningRequest
metadata:
  name: jane
spec:
  expirationSeconds: 600 #seconds
  usages:
  - digital signature
  - key encipherment
  - server auth
  request:           --- > yha per hum specify kery gye, certificate signing request sent by the user.  but apko plan text ma y ni kerna isko "encode" ker k send kerna ha...  so convert your "jane.csr into base64"   ---> cat jane.csr | base64  .. then move the encoded output yaml under the request section..
    

    convert your "jane.csr into base64"   ---> cat jane.csr | base64  or cat jane.csr | base64 -w 0(it will remove the space)   .. then move the encoded output yaml under the request section..   (i think ap yha per multiple uses ki csv file encode ker k rakh sakthy hn, not confirmed)

it will create the object...

like:
-----

apiVersion: certificates.k8s.io/v1
kind: CertificateSigningRequest
metadata:
  name: akshay
spec:
  expirationSeconds: 600 #seconds
  usages:
  - digital signature
  - key encipherment
  - server auth
  request: LS0tLS1CRUdJTiBDRVJUSUZJQ0FURSBSRVFVRVNULS0tLS0KTUlJQ1ZqQ0NBVDRDQVFBd0VURVBNQTBHQTFVRUF3d0dZV3R6YUdGNU1JSUJJakFOQmdrcWhraUc5dzBCQVFFRgpBQU9DQVE4QU1JSUJDZ0tDQVFFQXJyRy9ETUhXOWhKcTlsQkp5a2tLeFhhdVRPQWQ5bTVKelRmWFRscXRockdsCkRpVjZPQ0JOdUpZRjVnK1k3N002OGlTYlplN1QwTFpjZ1JRaVpOMWhmY0JTTmVoTXBsdFpOVG9OT1lOa1ArTEYKbW9QWVF3THpZcGErK2hHWTk1NUpnSjRsc2VoL2xGeDBlSU1jcWxOUUVNT05ENnBQRnFRa2FBdkNMNWlnZU1sNQpBaFBvTDVSb2d6amlmS0pNRXYrM2dtL1VadzhvVXZhdEFUSlpXb1YxS1ZUUEdQb0gzQTVVQzVpblJQVjRIMHM1Ck55cVZZZGExK3g3OWcvR2VCYTYvWS9ya1dUaWpaMUVzUXVQbnpKQ3Urald5WXNLYnRGaEwwd0dkR1Z0blVWWVAKVml6a1V6TUR6SldCazZyS3EvKzk0SEErYnNUZGp6VW5KUGRqWkZFZm5RSURBUUFCb0FBd0RRWUpLb1pJaHZjTgpBUUVMQlFBRGdnRUJBRElwcUc3ZVlGaDN1N0dneVFLTFU5dmRVWGE2dmJ1NjQ0a05VU2tHak55TjM0MGhxNXFiClZveG9hK0hRVTg5K05zcXVodkl5VnlVZHRLU2sxcThvNTZNdTF0WWxEOGYxY29YUnlZanBRR2NFODlyYXBrR0YKOTMzSUI0bndTb0FZam5oS1dCK3VvRkc3QWQrZ2dudnJNbnpHeWpPNnBvNG9xbVJlK2hBWkRsMENFa241SUZYLwpJRDR1ZlA3MWFmTWRWbnRha1hZNXV2NXh1UDJXdzVzazgvWDJJdmRITkRSMW5oZzVKWFhpbW0wME9mQ0N6K2VQCmdMUTFJRGNiSDZKK2U2WDV4VWFxM2hORHlrenBiMlNQYnF0S2FrZHkrUmc5OGFxT3Z0ZmhjTGhFdUhVdWI4czMKZGJkVy82dHN6b1BhSC9RT1FjNmhnN2FMMksvRitrQ1IrV3c9Ci0tLS0tRU5EIENFUlRJRklDQVRFIFJFUVVFU1QtLS0tLQo=
  signerName: kubernetes.io/kube-apiserver-client             -------->signer Name is complusory
  usages:
  - client auth

once done then use command to apply yaml file.
----------------------------------------------

  kubectl apply -f jane-crs.yaml

command to see certificate siging request
-----------------------------------------

  kubectl get csr

approve the request by running 
--------------------------------
  
  kubectl certificate approve jane    

if needs to deny request then use this command

  kubectl certificate deny jane

kubernetes ca.key(private) sa certificate ko sign kery ga...  this certificate can then be extracted and share the users..

command to delete the certificate API
-------------------------------------

  kubectl delete certificatesigningrequest <csr_name>  or kubectl delete csr <csr_name> 

view the running certificate by getting yaml output
---------------------------------------------------

  kubectl get csr jane -o yaml  

then ap file ko open ker k certificate ko extract(copy)  ker sakhty hn jo apko under "status > certificate" k mily ga .. y encode form ma ha. you need to decode this... 

  echo "encode text" | base64 --decode    --> once done share this with users ... how to need to access the cluster(i think)...


now which component is actually responsible for all the certificate related operations..
----------------------------------------------------------------------------------------

All the certificate related operations are carried out by the "kubernetes controller manager".

is ma controllers hn like:

- CSR-APPROVING
- CSR-SIGNING

these are responsible for carring out these task..

hum janty hn k jo certificate ko sign kerta ha usky ps CA server root certificate(ca.crt) or private key(ca.key) honi chahye.. "so controller manager ma y dono hum specify ker rhy hoty hn.."

  cat /etc/kubernetes/manifest/kube-controller-manager.yaml

    spec
      containers:
      - command:
        - kube-controller-manager
        - --cluster-signing-cert-file=/etc/kubernetes/pki/ca.crt
        - --cluster-signing-key-file=/etc/kubernetes/pki/ca.key


-------------------
Security KubeConfig
------------------

In this lecture, we look at kubeconfig in kubernetes.. 

ab tk hum na y dekha ha k hum kis tarha sa certificates create ekr sakhty hn or kis taraha sa user Rest API k through certificate use kerty howy cluster ko access kerta ha.


  curl https://kube-api-end-point-address/api/v1/pods --key admin.key(private key) --cert admin.crt  --cacert ca.crt   isko api-server validate kery ga user ko authenticate kerny k lye...(i think y Rest API ko use ker k yha pod list kerwa rha ha)

how to do the same thing with kubectl command
---------------------------------------------

  kubectl get pods --server kube-api-server-address:server-port --client-key admin.key --client-certificate admin.crt --certificate-authority ca.crt

bar bar is command ko use kerna ka hatic kam ha ap isko "kubeConfig File" ma move ker sakhty hn.. jo k home directory ma located hoti ha --> "$HOME/.kube/config"

agr apki file home directory ma ha tu apko kubectl command ma path deny ki zaroorat ni ha.. wo by default home directory ma pari file ko uthata ha..

$HOME/.kube/config
------------------

        kubeConfig File

--server kube-api-server-address:server-port 
--client-key admin.key 
--client-certificate admin.crt 
--certificate-authority ca.crt

kubeconfig file k specfic format hota:
-------------------------------------

let take a look..

config has 3 section.

- cluster      ----> is section ma sary cluster aye gye jisko apna access kerna ha...
- user         -----> is section ma users aye gye jin na cluster access kerna ha. in user ko different privileges(permissions) hogi different cluster ko access kerny k lye...
- context      ----->is ma user account aty hn. context cluster or user ko jorta ha.. mean kon sa user account na kon sa cluster access kra ha ha..  mean what user going to access what cluster.

remember existing users per y sari privalage lgye gi.. new users per ni lgye gi... 

In that way you don't have to specify the user certificates and server address in each and every kubectl command..."

so how to fit below information in kube config
----------------------------------------------

--server kube-api-server-address:server-port 
--client-key admin.key 
--client-certificate admin.crt 
--certificate-authority ca.crt

"server or root certificate(ca.crt) ki information  will go to clusters section in kubeconfig--> cluster ma jye gi...
"admin user key(.key) or admin certificate (.crt) will go to users section in kubeconfig"

then ap "context" create kero gye kubeconfig context section ma or specfiy kro gye k kon sa user in users section(in kubeconfig file) will access which cluster available in cluster section...


let take a look for kubeconfig.yaml file
----------------------------------------

apiVersion: v1
kind: Config
current-context: my-kube-admin@my-kube     ----> agr ap na multiple entries dali hn context ma, kubeconfig ko kesy pta chaly ga k us na bydefault kis ko chalna ha , wo is section ma dalny sa pta chaly ga... mean by default current dye gye account k through mention cluster access kery ga..
clusters:    --------> array/list

- name: my-kube   -------name of the cluster
  cluster:
    certificate-authority: ca.crt   
    server: api-end-point of server

contexts:    --------> array/list

- name: my-kube-admin@my-kube   ---> account name
  context:
    cluster: my-kube     ---> give name of cluster here.   it should same name as given name under cluster section. 
    user: my-kube-admin   ----> give name of the user   it should same name as given name under cluster section.
users:        --------> array/list

- name: my-kube-admin   ---name of the user
  user: 
    client-certificate: admin.crt
    client-key: admin.key


same process ko use kerty howy ap multiple entries 3no section ma dal sakthy hn...    


There are command line option available with kubectl to view and modity the kubeconfig files....

command to view kubeconfig:
---------------------------

  kubectl config view

  it list the cluster , contexts and users as well as current-context set..

agr ap ni btao gye k kon si kubeconfig file use kerni ha tu wo default file jo "$HOME/.kube/config" ma ha wo view krwye dye ga... jb ap kubectl command sa view dekhny ko khy gye...


alternatingly ap kubectl command ma b config file direct bta sakhty hn

  kubectl config view --kubeconfig=my-custom-config

you can use "h" to see further config help...

  kubectl config -h   ---> will use current , delete , get , set . unset , use , rename , view 

what about namespace:
--------------------

aik cluster ma multiple namespace create ker sakhty hn. we can also set our context for specfic namespace..

like this:
---------
apiVersion: v1
kind: Config
current-context: my-kube-admin@my-kube     ----> agr ap na multiple entries dali hn context ma, kubeconfig ko kesy pta chaly ga k us na bydefault kis ko chalna ha , wo is section ma dalny sa pta chaly ga... mean by default current dye gye account k through mention cluster access kery ga..
clusters:    --------> array/list

- name: my-kube   -------name of the cluster
  cluster:
    certificate-authority: ca.crt   
    server: api-end-point of server

contexts:    --------> array/list

- name: my-kube-admin@my-kube   ---> account name
  context:
    cluster: my-kube     ---> give name of cluster here.   it should same name as given name under cluster section. 
    user: my-kube-admin
    namespace: finance

users:        --------> array/list

- name: my-kube-admin   ---name of the user
  user: 
    client-certificate: admin.crt
    client-key: admin.key


"when you add namespace as we did above, the context will specfically for the that namespace..." (i think sirf us cluster tk ki access dye rhy hn)

finally about certificate path
------------------------------ 

we just given the name of the certificate in yaml file. it's is better to give the full path..

like this
---------
apiVersion: v1
kind: Config
current-context: my-kube-admin@my-kube     ----> agr ap na multiple entries dali hn context ma, kubeconfig ko kesy pta chaly ga k us na bydefault kis ko chalna ha , wo is section ma dalny sa pta chaly ga... mean by default current dye gye account k through mention cluster access kery ga..
clusters:    --------> array/list

- name: my-kube   -------name of the cluster
  cluster:
    certificate-authority: ca.crt      -----> "better to give full path like this /etc/kubernetes/pki/ca.crt"
    server: api-end-point of server

contexts:    --------> array/list

- name: my-kube-admin@my-kube   ---> account name
  context:
    cluster: my-kube     ---> give name of cluster here.   it should same name as given name under cluster section. 
    user: my-kube-admin   --> name of the user that need to access cluster
    namespace: finance

users:        --------> array/list

- name: my-kube-admin   ---name of the user
  user: 
    client-certificate: admin.crt
    client-key: admin.key


you can also put the ca.crt certificate content directly into yaml
----------------------------------------------------------------

like this..
----------- 

first you need to convert content in base64 encoded format and then shift the encoded format directly into yaml file..

cat ca.crt | base64  ----> copied the encoded content and put it on yaml..


like this
---------
apiVersion: v1
kind: Config
current-context: my-kube-admin@my-kube     ----> agr ap na multiple entries dali hn context ma, kubeconfig ko kesy pta chaly ga k us na bydefault kis ko chalna ha , wo is section ma dalny sa pta chaly ga... mean by default current dye gye account k through mention cluster access kery ga..
clusters:    --------> array/list

- name: my-kube   -------name of the cluster
  cluster:
    certificate-authority-data:

        copied the encoded content and put it on yaml(here)..    ---> agr apko chahye ho tu ap yha sa lye ker copy ker k decode ker k 'echo "content" | bas64 --decode ' k use ko dye sakhty hn...

    server: api-end-point of server

contexts:    --------> array/list

- name: my-kube-admin@my-kube   ---> account name
  context:
    cluster: my-kube     ---> give name of cluster here.   it should same name as given name under cluster section. 
    user: my-kube-admin
    namespace: finance

users:        --------> array/list

- name: my-kube-admin   ---name of the user
  user: 
    client-certificate: admin.crt
    client-key: admin.key



LAB SOLUTION:
------------

1- where is the default kubeconfig file is located

  By default it is located in "/HOME/.kube/config"  --> "/root/.kube/config" 


2- I would like to use the "dev-user" to access "test-cluster-1". Set the current context to the right one so i can do that. Once the right context is indentified. use the "kubectl config use-context" command..

  if we have no information then we first need to create ".key" or ".crt" certificate for this dev-user. it will create with the help of root certificate(ca.crt , ca.key) so we can use it in our .kube/config

  then create a "user" section in .kube/config file and add this certificates. also create a context section in kubeconfig and define the username(jis na cluster ko access kerna ha) clustername(jis cluster ko access kerna ha) and context name(kis context name ko use ker k access kern ha)

  also use this to make it default context--->"kubectl config use-context "context-name" "kubeconfig path(/$HOME/.kube/config)""
3- With the current-context set the research, we are trying to access the cluster. However something seems to be wrong. identify and fix the issue . try running the "kubectl get pods" command and look for the error. All users certificates are stored at "/etc/kubernetes/pki/users"

  so self manage cluster ma apko agr certificate k issue ha tu ap cluster ko access ni ker sakye gye..'kubectl get nodes' kerny per apko error mily ga..

solution:

  kubeconfig file  ma > user section ma .crt certificate k lye jo path ap na dya us ma issue hosakhta ha... apky user k lye certificate jis path ma pary hn us path ko check kery or use (pwd) ker k present working directory ko dekhy or us path ko kubeconfig file ma user section ma add ker dye...

-------------------------
API GROUP
-------------------------

before going to Authentication section. it is important to understand the API GROUP....

what is the kubernetes API
--------------------------

hum na abi tk kube api server k bry ma parha ha. or isko access kya ha, chahye wo "kubectl utility sa" y "Rest api" k through. 

let say hum na node version or pod version ko Rest api k through access kya ha... like this...

  curl https://kube-master:6443/version  or curl https://kube-master:6443/api/v1/pods

hmra focus is /version , /api in API path per ha.... 

kubernetes API grouped hojati hn multiple such(un) groups based on their purpose. such as one for /version , /api , /apis, one for /healths , /metrics /logs.

version api ----> is api ko hum cluster k version dekhny k ly use krty hn.
health and monitor api ---> is api ko use kerty hn cluster ki health ko monitor  kerny k lye.
logs  ----> is ko hum use kerty hn third party logging application k lye...

is lecture ma hum un API ko focus kery gye jo responsible ha cluster functionality k lye like 

1- "core group"  ----> is  ma hmry ps "/api"  ata ha
2- "named group" ----> is  ma hmry ps "/apis"  ata ha

core group
------------

core group(/api -->/v1) ma all functionality exist kerti ha... such as..

- namespaces 
- pods
- replication controller
- events
- endpoints 
- nodes 
- bindings
- PV
- PVC
- configmaps 
- secrets
- services

named group
------------

named group (/apis) more organized ha,, agye all newer features are going to be made available to these

1- /apps
2- /extensions
3- /networking.k8s.io
4- /storage.k8s.io
5- /authentication.k8s.io
6- /certificates.k8s.io  ---> autherization certificates..

                          
                          
                            named
                              |
                          -----------
                             /apis
                          -----------
                               |
-------------------------------------------------------------------------------------------------------------------------------------------  
/apps      /extensions     /networking.k8s.io      /storage.k8s.io     /authentication.k8s.io      /certificates.k8s.io(for authorization)   ---> these are the API GROUP  and below are the api group resources jo in api groups ma group hn apny purpose k according..
-------------------------------------------------------------------------------------------------------------------------------------------
  |                                |                                                                         |                     
 ----                            -----                                                                      ----                  
  /v1                             /v1                                                                        /v1             
 ---|-                           --|--                                                                      --|--             
|---|--------------|               |                                                                          |>/certificatessigningrequests(crs)        
|   |>/deployemnts |--|>list       |>/networkpolices                                                                                
|   |>/replicaset  |  |>get 
|   |>/statefulsets|  |>create |
|                  |  |>delete | 
|------------------|  |>update | 
|    Resources     |  |>watch  |
----------------------|--------|--
                      | VERBS  |
                      ----------
each resources has set of action....

like for deployment you can list, get , delete . update and watch  --> these are knows as "verbs"..


ap google per or kubernetes cluster ma n api group ko dekh sakhty hn(like thi curl and see the api groups "curl http://localhost:6443 -k")

see for named apis -->("curl http://localhost:6443 -k | grep "named")

-------------

ab sir khty hn k ap bina certificate k jb kube api server ko authenticate kery gye tu wo apko authenticate ni kerny dye ga.. sawy version v1 k.... baki forbidden k msg dye ga..
 
"alternates option" y ha k ap "kubectl proxy client" ko start kery. mean proxy use ker k ap access ker sakhty hn... 

kubectl proxy command launches a proxy service locally on port  8001 and uses credentials and certificate from your kubeconfig file to access the cluster. is tarha sa apko isko curl command ma mention kerny ki zaroorat ni..

remember
---------

  kube proxy =! kubectl proxy

kube proxy ---> it is use for networking. it is used to enable connectivity b/w pods and services across different nodes in the cluster.
kubectl proxy  -->  whereas kubectl proxy is an HTTP proxy service created by kubectl utility to access the kubeapi service

next "authorization section" ma hum inhi "api groups resources verbs" ko "allow" or "deny" ker k play ker rahy hogye apny use k according.. 

----------------
Authorization
----------------

authentication ma hum na different method ko use kerty howy dekha k kis tarha sa hum cluster ko authenticate ker sakthy hn..

authorization ma hum dekhy gye k jb cluster ko access ker lety hn tb wo kya kery ga cluster ma...

as a admin hum na cluster ma multiple operation perform kerny hoty so hum full access honi chahye... but different log cluster ko access ekrty hn. so unho hum limit rights dye sakthy hn unky use case k according..

is k lye hum user k accounts create kerty hn.... for different authentication methods ko use ker k(static password file, static token file, certificate, LDAP, service account) in ma sa kisi aik way sa hum account create ker sakthy hn... like we saw in our pervious lecture..

but hum sab users ko aik tarha ki access ni dena chahty, hum uunko unky use case k according access dye gye... tky wo resource ko "view" ker sakhy na k "modify"

like same for the "service account" we only want to provide the external application the minimum level of access to perform its required operations.

jb hum apna cluster different people(teams) or organization ko cluster ma different enviroment through namespace bna ker. hum users ki access ko restrict ker sakthy hn unki apni namespaces tk..

Autherization Mechanisms 
----------------------

There are different authorization mechanism, like

- RBAC
- ABAC
- Node autherization
- webhook

- Node autherization
---------------------

hum janty hn k logs kube api server ko access kerty hn tky wo cluster ko manage ker sakhy..

same cluster ma worker node ma kubelet kubeapi server ko access kerta ha tky wo below Read/Write action ko perform ker sakhty.

- Read 
  - services
  - endpoint
  - nodes
  - pods
- Write
  - node status
  - pod status
  - events
These requests are handled by the special authorizer name node authorization..

pervious lecture ma hum na dekha tha k "kubelet system node group k part tha" and having name prefix with system node. 

so koi b request jo user ki traf sa ati ha with the name system node. and part of the system nodes group is "authorized by the node authorizers". and granted these privalage.  

privalage is required for kubelet so that access within the cluster,

----
ABAC
----

ABAC authorization is where you assoicate a user or a group of users with a set of permission.

let say "dev user" ------->can "veiw PODS , Create Pods , delete pods"

you do this by creating a policy file with a set of policies defined in a JSON format this way..

{"kind":"policy","spec":{"user":"dev-user","namespace":"*","resource":"pods", "apiGroup":"*"}}  --> ap is file ko api server ko pass ker sakthy hn.

similarly, we create a policy defination file for each user or group in this file.   


or jb b ap na security ma koi changes kerni ha. you must edit the policy file manually and restart the kube api server... "is lye ABAC ko manage kerna difficult ha" ABAC is difficult to manage..

--------
RBAC
--------

RBAC is make it much easier..  In RBAC instead of directly assoicate a user or a group of users with a of permission. "we define a role."    mean hum role create kerty hn or us role ma set of permission hum lgty hn or phir users ko wo role assign ker dety hn...

for example
-----------

in this case, for developers(mean hum kubernetes components k lye developers ko authorized ker rhy hn) so we create a developer role(developer name k role) with the set of permissions(can veiw pods, can create pods , can delete pods)  and associate the user to that role.

isi tarha sa hum security k lye role create kerty hn with a right set of permission. and associate the user to that role

jb b hum na koi changes kerni ha, hum role ma changes kerty hn or uska effect reflect hojta ha associate user per..

RBAC is a stardard approach to manage the kubernetes cluster.. 

webhook
---------

what if you want to outsource all the authorization mechanism. mean ap authorzation ko externally manage kerwana chaha rhy hn..

- open policy agent is a third party tool to help with admissoin control and autherization.

is ma 3rd party service k through apki authorization horhi hogi..

ab sir khty hn k mention below mechanism k alwa 2 or mode b hn.. 

- RBAC
- ABAC
- Node autherization
- webhook     

like:

- AlwaysAllow   --->> mean always allow all request without performing any authorization checks
- AlwaysDeny    ---->> mean deny all request.

so hum y kha per configure kery gye... which of them are active by default.? can you have more one at a time. how does authorization work if you do have multiple ones configured.

y mode hum "kube api server ki service file" ma configure kerty hn. with name ----> "--authorization-mode=AlwaysAllow"

"if you do not specify this option. it is set to always allow by default."

"if you want to use multiple mode except this.. then ap kube api server ma is tarha sa ker sakhty hn..."

"--authorization-mode=Node,RBAC,Webhook"  

remember jb ap multiple mechanism use kerty hn tu apki request each mode sa pass-through hoti ha phir ap ko authorization milti ha..

let say ap  NODE , RBAC , Webhook modes ko use ker rhy hn..

jb user request send kerta ha... tu apki request node Authorization module k ps jati ha. ab node authorizar module sirf node ki request ko authorized(handle) kerta ha is lye y apki request ko deny ker dye ga.. jb b request deny hogi tu y further forward hojye gi next chain ma jo madule hoga usky ps. ab apki request further RBAC k ps jye gi.. RBAC apny checks ko perform kery ga or grant kery ga user ko permission. so authorization is complete and user is given access to the request object..

How to create Role
-------------------

like for developer:

developer-role.yaml
-------------------

apiVersion: rbac.authorization.k8s.io/v1
kind: Role
metedata:
  name: developer
rules:         ---------> each role have three section..
- apiGroups: [""]       ---> because "pod" resource "core api group" ka under ata ha. so core group k case ma hum "apiGroup" ko "blank" rakhty gye.   other group(like named group) is case ma hum value dye gyee..
  resources: ["pods"]   ----> jis kubernetes component ki access  ap na developers ko dene ha wo resources section ma aye ga.. like we wrote "pod"
  verbs: ["list", "get", "create", "update", "delete"]   --> and what action they can take will place under verbs..

- apiGroups: [""]
  resources: ["ConfigMap"]
  verbs:["create"]           ----> like this is another rule to allow the "developer" to create configmap... 

you can add multiple rule like this,,,

now create with kubectl command

  kubectl create -f developer-role.yaml

next step to link user with that role 
-------------------------------------

  for this we create another object called "RoleBinding".

devuser-developer-binding.yaml
------------------------------

apiVersion: rbac.authorization.k8s.io/v1
kind: RoleBinding
metadata:
  name: devuser-developer-binding
subjects:   ---> under this we specify the user details..
- kind: User
  name: dev-user
  apiGroup: rbac.authorization.k8s.io
roleRef:   ---> under this we provide the details of role created.
  kind: Role
  name: developer
  apiGroup: rbac.authorization.k8s.io

now create with kubectl command

  kubectl create -f devuser-developer-binding.yaml

remember "role and role binding" falls under the scope of namespace.  we in our case we have not define the "namespace" so hmra dev-user pod ko access ker rha ha only in the "default namespace". same agr other namespace ki access deni ha tu uska name apko btana hoga...(i think role file ma under metadata namespace dye gye..)

view:
-----

view role and role binding...

- kubectl get roles
- kubectl describe role "role name"
- kubectl get rolebindings
- kubectl describe rolebindings "rolebinding name"

what if you being a user would like to see if you have access to a particular resource in the cluster...

is command sa ap dekh sakthy ho k ap kubernetes component k lye authorized ho b y ni....

  kubectl auth can-i create deployments  ---> if it return "yes" then mean k apko access ha 

same 

  kubectl auth can-i delete nodes.  ---> if it return "no" then mean k apko autherization access ni ha 

"now: let sa ap admin hn or apna role or rolebinding k through kisi ko authorized kya ha.. or ap check kerna chahey ha us user ko k is user k lye role sahi sa kam ker b rha ha k ni...

so do this,,

  kubectl auth can-i create deployments --as dev-user   ---> if it return "no" then mean k apko access ni ha 

  kubectl auth can-i create pods --as dev-user  ---> if it return "yes" then mean k apko access ha.

"you can also specify the namespace in command to check the namespace.."

  kubectl auth can-i create deployments --as dev-user --namespace test   ---> mean y check ker rha ha k devops user ko authoriztion ha deployment create kerny ki test namespace ma.. -->if it return "yes" then mean k apko access ha.

Quick note
----------


developer-role.yaml
-------------------

apiVersion: rbac.authorization.k8s.io/v1
kind: Role
metadata:
  name: developer
rules:         ---------> each role have three section..
- apiGroups: [""]       ---> because "pod" resource "core api group" ka under ata ha. so core group k case ma hum "apiGroup" ko "blank" rakhty gye.   other group(like named group) is case ma hum value dye gyee..
  resources: ["pods"]   ----> jis kubernetes component ki access  ap na developers ko dene ha wo resources section ma aye ga.. like we wrote "pod"
  verbs: ["list", "get", "create", "update", "delete"]   --> and what action they can take will place under verbs..

- apiGroups: [""]
  resources: ["ConfigMap"]
  verbs:["create"]           ----> like this is another rule to allow the "developer" to create configmap... 


so is sa y lga rha ha k y role jis user ko b milye ga wo defualt namespace ma sab pods ko create , delete or mention action kerny ki access rakhta ha... default namespace is lye kha because hum na yaml file ma namespace ko mention ni kya. is lye wo by default default name space ma operate kery ga... 

now ab ap chahty hn ka y role jis user ko b do wo default namespace ma sabi pods ko access ni kery.. specfic pod ko access kery so use... "resourceNames" for this...

like this:

developer-role.yaml
-------------------

apiVersion: rbac.authorization.k8s.io/v1
kind: Role
metedata:
  name: developer
rules:         ---------> each role have three section..
- apiGroups: [""]       ---> because "pod" resource "core api group" ka under ata ha. so core group k case ma hum "apiGroup" ko "blank" rakhty gye.   other group(like named group) is case ma hum value dye gyee..
  resources: ["pods"]   ----> jis kubernetes component ki access  ap na developers ko dene ha wo resources section ma aye ga.. like we wrote "pod"
  verbs: ["list", "get", "create", "update", "delete"]   --> and what action they can take will place under verbs..

- apiGroups: [""]
  resources: ["ConfigMap"]
  verbs:["create"]           ----> like this is another rule to allow the "developer" to create configmap... 
  resourceNames: ["blue", "orange"] 

ab y role jis user ko b mily ga wo default namespace ma sirf "blue or orange" name ki pod per hi action perform ker sakhta ha..

Cluster role
-------------

In this lecture we will discuss cluster roles and cluster role binding...

hum na last lecture ma dekha tha k Role or Role binding kisi na kisi namespace per implement hoti ha... agr ap namespace role or role binding create kerty howy namespace ka ni btye gye tu wo default namespace ma implement kery ga..

hum na namespace k lecture ma dekha tha k namespace sa hum saparate isolated enviroment create ker sakhty hn. or jis ma hum resources(pod , deployment , service) ko grouped or isolate ker sakhty hn.

so what about other Resources like nodes
----------------------------------------

can you group or isolate nodes within a namespace?.... like can you say node01 is part of the dev namespace. "ni hum  asa ni ker sakhty" because those are cluster wide or cluster scoped resources... hum inko kisi perticular namespace k sath associate ni ker sakhty..

so the resources are categorized as either "namespaced" or "cluster scoped" 

so the resources for the namespace is:
--------------------------------------

- pods
- replicasets
- deployments
- service
- secrets
- configmaps
- rolebindings
- Jobs
- PVC

is resource ko create kerty howy namespace k btaty ho.. tky y in namespace ma jakr create ho.. agr ap namespace ka ni btaty tu wo by default "default" namespace ma create hojaty hn..

so the resources for the clusterscope is:
----------------------------------------

- nodes
- PV
- clusterroles
- clusterrolebindings
- certificatessigningrequests(crs)
- namespaces  ---> object


agr ma resource ki complete list deni ha jo namespace ma provision hoty hn or jo namespace ma ni provision hoty mean wo cluster scope ma aty hn. for this use below command..

  kubectl api-resource --namespaced=true  --> check resources within namespace

  kubectl api-resource --namespaced=false --> check resource within cluster scope.


"so hum na previous lecture ma dekha k hum na namespace ma authorization kerwani ha user ki tky user us namespace ma resources ko access ker saky. tu is k lye "roles" or "role bindings" ko use kerty hn"

"but agr hum na users ko namespace resource ki bjye cluster wide resources(like node or PV etc) k lye access deni ha tu hum "clusterrole" or "clusterrolebindings" ko use kerty hn"

"cluster role" it is same like "role"(which is for the namespace scope resources) but it is for the cluster scope resources.

we can create multiple cluster roles and assign permission to that role tky user un role ko use kerty howy cluster ma multiple function ko perform ker saky...

like:

cluster-admin-role.yaml
-----------------------

apiVersion: rbac.authorization.k8s.io/v1
kind: ClusterRole
metadata:
  name: cluster-administrators
rules:
- apiGroups: [""]
  resources: ["nodes"]
  verbs: ["list", "get", "create", "delete"]   --->ab y jis b user ko assign kery gye us ko y permission mil jye gi k wo nodes ko delete , create, get , list ker sakhta ha...

kubectl apply -f cluster-admin-role.yaml

so next step is to link user to this cluster role. is k lye apko "cluster role bindings" use kerna hoga.. 



cluster-admin-role-binding.yaml
-----------------------

apiVersion: rbac.authorization.k8s.io/v1
kind: ClusterRoleBinding
metadata:
  name: cluster-admin-role-binding
subjects:
- kind: User
  name: cluster-admin  ---> user-name
  apiGroup: rbac.authorization.k8s.io
roleRef:
  kind: ClusterRole
  name: cluster-administrators   --> cluster-role name
  apiGroup: rbac.authorization.k8s.io

kubectl apply -f cluster-admin-role-binding.yaml

sir khty hn one thing to note
-----------------------------

" we said agr hum na users ko namespace resource ki bjye cluster wide resources(like node or PV etc) k lye access deni ha tu hum "clusterrole" or "clusterrolebindings" ko use kerty hn" but y hard and fast rule ni ha....

"ap cluster role ko namespace resources k lye b use ker sakthy hn"

but cluster role k effect all namespaces per implement hoga... for specfic resource k lye...

like ap na cluster role k through namespace ma pod ko access kera ha so ap kisi perticular namespace ma pod ko access ni bilky all namespaces ma pod ko access ker rhy hogye,. 

solution:
--------

command to count the cluster role and clusterrolebindings

  kubectl get cluster role | wc -l

  or 

  kubectl get clusterrolebinding | wc -l


cluster role and cluster role binding for storage
-------------------------------------------------

---
kind: ClusterRole
apiVersion: rbac.authorization.k8s.io/v1
metadata:
  name: storage-admin
rules:
- apiGroups: [""]
  resources: ["persistentvolumes"]
  verbs: ["get", "watch", "list", "create", "delete"]
- apiGroups: ["storage.k8s.io"]
  resources: ["storageclasses"]
  verbs: ["get", "watch", "list", "create", "delete"]

---
kind: ClusterRoleBinding
apiVersion: rbac.authorization.k8s.io/v1
metadata:
  name: michelle-storage-admin
subjects:
- kind: User
  name: michelle
  apiGroup: rbac.authorization.k8s.io
roleRef:
  kind: ClusterRole
  name: storage-admin
  apiGroup: rbac.authorization.k8s.io

---------------
service account
---------------

service account ap detail ma CKAD ma b phary gye..

there are 2 type of account in kubernetes

- user account --> that is used by Humans to access the cluster
- service account --> that is used by machines to access the cluster   

y said machine like automatic build tool like "jenkins" uses service account to deploy applicaition in kubernetes cluster. or "promethoues" to get metric from cluster to monitoring... 

  kubectl create serviceaccount "servicaccountname"

  kubectl get serviceaccount "servicaccountname"

  kubectl describe serviceaccount "servicaccountname"

jb service account bnta ha wo sath hi "automatically token" create kr deta ha. is token ko external application use krti hn kubernetes api ko authenticate krny k lye..

"jb ap service account create kerty hn tu wo service account object create kerta ha. or usky bd service account k lye token create ekrta ha , phir secret object create kerta ha. phir token ko secret object ma store kerta ha. then secret ko service account k sath link ker deta ah..

to view the token use below commands: 


  kubectl describe serviceaccount "servicaccountname"

  get token name by using above command 
  
  kubectl describe secret "token name(got from service account)"

ab ap ki machine is token ki help sa cluster ko access ker sakhti ha...

"mean apna service account bnana ha RBAC k through right permission deni ha service account ko.. ab service account token create ker k secret object ma store kerta ha waha sa token export kerna ha.. or usy apni machine y 3rd party application ko dena ha tky wo kubernetes api ko authenticate ker saky...

what if ka apki 3rd party application cluster ma hi hosted ho... tu phir service account token kesy dye gye application ko... 
-----------------------------------------------------------------------------------------------------------------------------

is k lye apko service account token ko volume mount k through application pod k sath mount kerwa hoga...

ab sir khety hn k jis b namespace ma ap serviceaccount ko list kery gye tu ap dekhy gye k "default" name k service account namespace ma already create hoga..

  kubectl get serviceaccount.... --> ab y default namespace ma service account ko list kery ga. jis ma default name k service account already create hoga.  mean hr namespace k apna default service account hota ha..

"jb b pod namespace ma create hota ha. tu default serviceaccount volume mount k through by default is k sath(pod) mount hojata ha.. ap isko pod ma describe ker k dekh sakhty hn... mounts section ma apko mily ga... 

or jb ap is mount path ko jo pod ko describe kerny sa mount section ma milta ha ko list ekrygy pod ma tu apko 3 file mily gi jin am sa aik "token" name ki hogi. y token ko ap use ker k kubernetes API ko authenticate ker sakhty hn.

like this:

  kubectl exec -it "podname" --ls /var/run/secrets/kubernetes.io/serviceaccount

  - ca.crt
  - namespace
  - token

remember default service account buhat restricted hota ha. is ko sirf basic kubernetes API ko query kerny ki permission hoti ha.

agr ap pod k sath different service account ko use kerna chahty hn tu
---------------------------------------------------------------------

- create the service account
- And mention name of service account in your pod.yaml file

pod.yaml
--------

apiVersion: v1
kind: Pod
metadata:
  name: my-kubernetes-dashboard
spec:
  containers:
  - name:
    image: 
  serviceAccountName: dashboard-sa

remember:

ap "pod ma service account ko edit ni ker sakhty" apko pod delete ker k recreate k time hi new serviceaccount btatna hoga..
 
"but deployment k case ma ap service account ko edit ker sakhty hn..

because deployment ma koi b changes hoti ha tu wo new replicaset bnta ha or us ma new pods create kerta ha. or is traha sa new pod ko new service account mil jata ha.. 

ab jb ap pod ko describe kery gye tu apko "mount" section ma apka new service account mily ga..

what if k hum automatically pod k sath service account ko mount kerwana ni chahty
----------------------------------------------------------------------------------

tu ap pod.yaml file ma "automountServiceAccountToken: false" use kery

pod.yaml
--------

apiVersion: v1
kind: Pod
metadata:
  name: my-kubernetes-dashboard
spec:
  containers:
  - name:
    image: 
  automountServiceAccountToken: false

service accounts 1.22/1.24 update:  (in dono ma basically service account or secret token k kam kerny k way ko change ker dya )
----------------------------------

jesa k hum na dekha k hr namespace ma default service account created hota ha jis ma secret token hota ha or jesy hi pod create hota ha kubernetes default service account ko associate ker deta ha pod sa. tky pod ko service account ka secret token mil saky...

  isko ap pod ko describe ker k "under mount section" ma mount point path ko dekh sakhty hn.. or pod ma us mount point path per exec command ka through ap jye gye tu apko token mily ga... y token pod ma chalny waly process ko kubernetes api authentication k kabil bnata ha...

ab jb ap below command y "website@JWT.io" sa token ko decode kerty hn tu ap dekhty hn k token ma koi "expiry data ni ha" 

  jp -R 'split(".") | select(length > 0 ) | .[0],.[1] | @base64 | fromjson' <<< "token"

version 1.22
------------

so version 1.22 ma is masly k hal nikal ha by introducing "tokenRequestApi". it is more secure and scaleable via an API. 

token request Api:
------------------

  - Audience Bound
  - Time Bound
  - Object Bound   hota ha...

ab jb pod create kerty hn tu ap apna token request APi sa bna token ko pod.yaml k sath mount kerwaty hn.

like this:

apiVersion: v1
kind: pod
metadata:
  name: nginx
  namespace: default
spec:
  containers:
  - image: nginx
    volumeMounts:
    - mountPath: /var/run/secrets/kubernetes.io/serviceaccount   <---
      name: kube-api-access-6mtg8                                <----
      readOnly: true
  volumes:
  - name: kube-api-access-6mtg8                                  <-----      
    projected:                  <-----------
      defaultMode: 420                |  
      sources:                        | 
      - serviceAccountToken:          |
          expirationSeconds: 3607     | 
          path: token           <------------
      - configMap:
          items:
          - key: ca.crt 
            path: ca.crt  

now version v1.24
-----------------

  version 1.24 ma aik or enhancement hoi ha...

  it deal with the reduction of Secret-based service account tokens.

  past ma y hota tha k jb ap below command k through service account create ekrty thy tu kubernetes "service account object" phir  "automatic token" phir "secret object" create kerta tha or phir is "token ko secret object ma store ker k secret ko service account k sath mount ker deta ha.."

    kubectl create serviceaccount "serviceaccountname"

  "but version 1.24 ma asa ni ha... ap jb command k through service account create ekrty hn tu wo sirf service account ko hi create kerta ha.. token creation k lye apko saparate command use kerna hogi..

     kubectl create serviceaccount "serviceaccountname"

     kubectl create token "serviceaccountname" 

   ab jb ap below command y "website@JWT.io" sa token ko decode kerty hn tu ap dekhty hn k token ma ab "expiry date majod ha" 

    jp -R 'split(".") | select(length > 0 ) | .[0],.[1] | @base64 | fromjson' <<< "token"

    i think y "aik hour" ki default expire hoti ha ap. command k through isko increase b ker sakhty hn.. 

ab sir khty hn "if you would still like to create secrets the old way with non-expiring token" or usko service account k sath associate kerna chahty ho. tu do like this..

secret-definition.yaml
----------------------

  apiVersion: v1
  kind: Secret
  type: kubernetes.io/service-account-token
  metedata:
    name: mysecretname
    annotations:
      kubernetes.io/service-account.name: "service account name"   ---> jis k sath ap na is secret token ko mount kerna ha..

  for this you need to create "service account" first and then create secret + annotating this sercret with service account.

  y apko non-expire secret token create ekr k dye ga...


solution:
---------

1- kubectl get sa ---------------> get serviceaccount in default namespace...
2- kubectl describe serviceaccount "servicaccountname"

  get token name by using above command 
  
  kubectl describe secret "token name(got from service account)"          ------> got token... that needs to be given to external application..

3- kubectl create sa dashboard-sa        ----it will creat service account , automatic token , secret object, store token in secret object and map secret object to service account..

you can add additional permission with service account by using RBAC...

4- kubectl create token "serviceaccount name(dashboard-sa)" ---------> hum na dekha tha k version 1.24 ma hum saparately service account ki command k sath token creation k command use kerni hoti ha...

older way ma hum sirf "service account creation command sa hi service account or token create ker rhy hoty thy." but is ma expiration date ni hoti thi... 

so token command used to create token..  (mean token create hoga or screen per display b hoga..)

4- kubectl get deployment web-dashboard -o yaml > dashboard.yaml   ----> get running deployment into yaml and update service account name..

then apply (kubectl apply -f web-dashboard)

Image Security
--------------

In this lecture we will discuss about securing images... 

"mean how to configure your pods to use images from secure repositories..


apiVersion: v1
kind: pod
metadata:
  name: nginx
  namespace: default
spec:
  containers:
  - image: nginx


so when you say "- image: nginx" mean you are asking pod container to "pull image name nginx" from dockerhub... 

sir khty hn apky image name(nginx in my case) k 2 part hoty hn

like this:

  - image: nginx   basically y is tarha hota ha   "- image: useraccount/image-name"

agr ma na "useraccount ni dya sirf image name hi to mention kya ha tu wo useraccount ki jaga by default "library" assume kery ga." or is library ma sari images store hoti hn..

like this:

  - image: library/nginx    ---> is library ma large no of community or dedicated teams verfied images ko store ker rhi hoti hn.

so ap y images kha per store or kha sa pull horhi hoti hn
---------------------------------------------------------

 - image: nginx   ----> because hum na is trha sa sirf image k name btya ha registry or location ko mention ni kya tu by default wo "docker.io" ma images ko store kery ga...

like this:

  image: docker.io/library/nginx   ----> mean {registry}/{UserAccount}/{ImageRepository}

their many other registries. like google has registry "gcr.io"  

sab cloud provider private registry dety hn...

in registries ma ap repository create ker sakthy hn... or repository ma images store ker sakthy hn...   isko ap credentail k through access ker sakthy hn..

dockerhub k case ma ap "docker login" command k through apni repository ko access kerty hn.. 

"so pod container ko image surely deny k lye apko "api private registry k full path dena hoga""

like this:


apiVersion: v1
kind: pod
metadata:
  name: nginx
  namespace: default
spec:
  containers:
  - image: private-registry.io/apps/internal-app ----> mean hmry gcloud registry k case ma asy bn rha hoga...  gcr.io/{project-id}/{image-name}

ab sir khty hn k y question ha hum jis trah sa "dockerhub ko docker login" ki command ko use kerty howy access kerty hn. so hum hmra GKE pod kis trha sa gcp ki gcr registry ko authenticate ker raha hoga..
------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

is k lye ap secret create kro gye by using "docker-registry" or us ma ap apny credentials dye rhy hogye..

like this:

kubectl create secret docker-registry "secretname" \
    --docker-server=private-registry.io     \
    --docker-username=registry-user   \
    --docker-password=registry-password   \
    --docker-email=registry-user@org.c

  docker-registry build in secret type ha. jo k use hoti ha docker credentials ko store krny k lye..

or phir is credentail name ko apni pod.yaml file ma btana hoga, tky apka pod is credential ko use kerty howy private registry ko authenticate ker lye.

apiVersion: v1
kind: pod
metadata:
  name: nginx
  namespace: default
spec:
  containers:
  - image: private-registry.io/apps/internal-app  --->  gcr.io/{project-id}/{image-name}
  imagePullSecrets:
  - name: "docker-registry secretname"     ----apni created docker-registry k name yha per mention kery.. 

solution:
--------

1- kubectl create secret    ------> it will give you the 3 option

- docker-registry
- generic
- tls

in 3no way ko use kerty howy ap secret create ker sakhty hn...  

or docker-registry ko use kerty howy ap secret create krty hn jis ma ap apna private repo ka credentials dety hn tky apka pod is secret ko use kerty howy private repo ko authenticate ker saky...

2- command to create secrets..

  kubectl create secret docker-registry private-reg-cred --docker-server=myprivateregistry.com:5000 --docker-username=dock_user --docker-password=dock_password  --docker-email=dock_user@myprivateregistry.com

3- ask deployment to use this secret..

edited the deployment and add below parameter under spec..

spec:
  imagePullSecrets:
    name: private-reg-cred


Pre-requisite – Security in Docker
----------------------------------

In this lecture we will discuss about security context in kubernetes..  but kubernetes ki security dekhny sa phily humy docker ki security dekhni chahye..



security context
----------------

jesa k hum na dekha jb ap docker container ko run kerty hn, apky ps option hoti ha container creation k doran set of security parmeters ko add kerny ki..

like this..

  docker run --user=1001 ubuntu sleep 3600

isko hum kubernetes ma b configure ker skahty hn... jesa k hum janty hn k pod ma multiple container hoskahty hn... ap set fo security parameters ko pod level or container level dono per set ker sakhty hn...

agr ap pod level per kerty hn tu us pod ma mojod sab containers per y implement hoga..

agr ap same setting ko container or pod dono per implement kery gye tu. setting on container will be override by setting on pod.. (container level pod level per override hojye ga "mean container level apny security context ko zayada priorty dye ga.....)

security context on pod level:
------------------------------

apiVersion: v1
kind: Pod
metadata:
  name: web-pod
spec:


    securityContext:
        runAsUser: 1000      --->security context on pod level

  containers:
    - name: ubuntu
      image: ubuntu
      command: ["sleep","3600"] 


security context on container level:
-----------------------------------

apiVersion: v1
kind: Pod
metadata:
  name: web-pod
spec:
  containers:
    - name: ubuntu
     image: ubuntu
     command: ["sleep","3600"] 
     securityContext:     -----> set security context in container
        runAsUser: 1000   --> this is userid

we can also "add capabilities" it is only support for containerss..

apiVersion: v1
kind: Pod
metadata:
  name: web-pod
spec:
  containers:
    - name: ubuntu
     image: ubuntu
     command: ["sleep","3600"] 
     securityContext:     -----> set security context in container
        runAsUser: 1000
        capabilities:   ----------------> remember capabilities ki jab bt ho tu samj jye k y under container hi lgye gi y pod level per ni lgti 
          add: ["MAC_ADMIN"]

solution:
---------

1- whoami   ---> y apko btye ga k kis user k through ap localhost per kam ker rhy ho..

pod k under k user jaany k lye apko below command use kerni hogi.

  kubectl exec -it "pod-name" -- whoami      y apko btye ga k kis user k through ap pod ma kam ker rhy ho..

2- kubectl get pod/pod-name -o yaml > pod.yaml

open the pod.yaml file and add security context in pod..

securityContext:     -----> 
        runAsUser: 1010
3- pod level or container level dono per security context lga ha tu container level pod level per override hojye ga "mean container level apny security context ko zayada priorty dye ga.....
4- add section in container level.... because capabilities ki jab bt ho tu samj jye k y under container hi lgye gi y pod level per ni lgti 

securityContext:          
          add: ["SYS_TIME"]

5- securityContext:          
          add: ["SYS_TIME" , "Net_ADMIN"]
----------------
Network Policies
----------------

let us first understand the networking basis. or network traffic flow...

network traffic flow:
--------------------

is concept ko sir na example k sath samjaya ha...

like assume k hmry ps 3 pod hn .. 1 is for webapp work as fronted pod.. 1 is for backend pod and 1 is for DB pod.


          user
           | 
           |
           | ingress    
          80     egress      ingress
        web pod   --------------> 5000 API POD(backend)    
                                   |  egress
                                   |
                                   |
                                   |ingress
                                   |
                                  3306
                                  DB POD
mean:

1- first we have ingress rule(incoming traffic) that accept http traffic on port 80 coming from user to the webserver.
2- egress rule(outgoing traffic) to allow traffic from the webserver to 5000 port of API server..
3- then ingress rule(incoming) accept traffic on port 5000 on api server..
4- egress rule(outgoing traffic) to allow traffic from the API server to 3306 port of DB pod
5- then ingress rule(incoming) accept traffic on port 3306 on DB port.. coming from api server...

ab sir na kha ha k by default pod across the cluster aik dosary k sath communicate ker rhy hoty hn.. mean network is tarha sa design kya hota ha k pods aik dosary k sath communicate kr rhy hoty hn... or kubernetes ma by default her pod per "ALL ALLOW" rule set hota ha.  

but ap ni chahty k apka frontend directly DB pod k sath communicate ekry...  so is k lye ap "network policy" ko use ker skahty hn..

matlab ap chahty hn k apki traffic fronted sa backend or backend sa DB pod per jye. frontend directly DB pod per na jye so y kam ap network policy ko use ker k ker sakhty hn..

tky network policy API server sa any wali traffic ko hi DB server per allow kerwye...
 

just like pod , service , deployment . network policy is also an object in kubernetes.. you link network policy to one or more pod... you can define rules within the network policy..

like: 

network policy:  only allow ingress traffic from API pod on DB server port 3306.
-------------

once this policy is created it block all other traffic and only allow traffic coming from api server to DB pod on port 3306. 

y sirf usy pod k lye apply hoga jis per network policy lgi hogi...

how do you apply(link) network policy to pod
--------------------------------------------

y asy hi hoga jesy hum na replicas set ka set pod ko link kya tha... by using "label and selector"

hum pod ko label kery gye or wohi same label hum apny network policy ko bta dye gy...

like this..

apiVersion: v1
kind: Pod
metadata:
  name: web-pod
  labels:
    role: db   ----------> use this label in network policy for linking pod to network policy
spec:
  containers:
    - name: ubuntu
     image: ubuntu
     command: ["sleep","3600"] 

network policy
--------------

policy-definition.yaml
----------------------
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: db-policy
spec:
  podSelector:
    matchLabels:
      role: db       --------> network policy link to the pod(jis pod per y policy chaly gi) --(pod label)
  policyTypes:   
  - Ingress   ----> give the policy type(mean incoming traffic)
  ingress:
  - from:
    - podSelector:
        matchLabels:
          name: api-pod    ---------->  is pod sa traffic arhi hogi
          
    ports:
    - protocal: TCP
      port: 3306    ---------> DB pod port 


mean api-pod sa traffic arhi hogi to DB pod on port 3306. is k apply k bd other traffic on db port would be rejected..

note that we use policy type ingress, only for incoming traffic(ingress) on DB pod... it will not be effecting on egress traffic(outgoing traffic)... mean pod can make any egress call to other pod.. and the call would not be blocked..  outgoing k lye ap ko policy type ma egress k btana hoga other wise outgoing call block ni hoga...

once done apply this...

  kubectl apply -f policy-definition.yaml

Network policy are enforced by network solution in kubernetes cluster..
-----------------------------------------------------------------------

solutions that support network policies:

- kube-router
- Calico
- Romana
- Weave-net

solutions that do not support network policies:

- flannel

sir khty hn cluster ma asa solution jo network policy ko support ni kerta us ma b ap network policy ko create ker skahty hn..


Developing network Policies
---------------------------

is lecture ma hum network policy ko more detail ma dekhy gye..



ab sir khty hn k hum y dekh rhy thy k "API pod" sa traffic db pod ki 3306 per arhi thi... is k lye hum na network policy create ki thi... jis k apply kerny sa all other traffic stop hojati hn except API pod ki on DB pod 3306 per.  

ab sir khty hn k agr "API pod" name k pod apki namespace k sath sath kisi or namespace ma b create hoga.. uski traffic b apky DB pod per asakhti ha.. so unki traffic ko rokny k lye or sirf apky namespace ma mojodd API pod ki traffic ko allow kerwany k alye hum network policy ma namespace selector name k argument use kerna hoga...

like this..

policy-definition.yaml
----------------------
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: db-policy
spec:
  podSelector:
    matchLabels:
      role: db       --------> network policy link to the pod(jis pod per y policy chaly gi) --(pod label)
  policyTypes:   
  - Ingress   ----> give the policy type(mean incoming traffic)
  ingress:
  - from:
    - podSelector:
        matchLabels:
          name: api-pod    ----------> 
      namespaceSelector:
        matchLabels:
          name: prod      ------> is sa sirf prod namespace ma mojood "API pod" ki traffic hi DB pod per arhi hogi..       
    ports:
    - protocal: TCP
      port: 3306    ---------> DB pod port 


what if k ap network policy ma y na btao k specfically traffic kis pod sa arhi hogi... then us case ma DB pod per iski namespace k sary pod sa traffic arhi hogi.. but outside namespaces ka pod sa traffic ni arhi hogi..

like this:

policy-definition.yaml
----------------------
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: db-policy
spec:
  podSelector:
    matchLabels:
      role: db       --------> network policy link to the pod(jis pod per y policy chaly gi) --(pod label)
  policyTypes:   
  - Ingress   ----> give the policy type(mean incoming traffic)
  ingress:
  - from:
    ---------------------------> ap na yha per ni btao k kis pod sa specfically traffic aye gi tu is case ma DB pod per iski namespace k sary pod sa traffic arhi hogi..  but outside namespaces ka pod sa traffic ni arhi hogi..

   
      namespaceSelector:
        matchLabels:
          name: prod      ------> is sa sirf prod namespace ma mojood "API pod" ki traffic hi DB pod per arhi hogi..       
    ports:
    - protocal: TCP
      port: 3306    ---------> DB pod port 

we an add multiple rules in our network policy... 

sir kha rhy hn k hum na abi y dekha k agr hum apni network policy ma y ni btaty k specfically DB pod per kis pod sa traffic arhi hogi tu us pod per ab DB pod ki namespace ma mojood sabhi pod sa traffic arhi hogi...
---
but what if k let say arha DB pod k lye backup server DB pod ki namespace sa bahir ha. or hum na Ab DB ko allow kerna ha tky wo outside the namespace ma pary Backup server ma data backup ker rha ho.

is k lye hum network policy ma "ipBlock" use ker sakhty hn or backup server ka ip bta sakhty hn... tky DB pod k lye wo ip allow hojye or wo DB pod apna backup backup server ma bhaj rha ho..

like this:

policy-definition.yaml
----------------------
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: db-policy
spec:
  podSelector:
    matchLabels:
      role: db       --------> network policy link to the pod(jis pod per y policy chaly gi) --(pod label)
  policyTypes:   
  - Ingress   ----> give the policy type(mean incoming traffic)
  ingress:
  - from:
    - podSelector:       -----> rule#1
        matchLabels:
          name: api-pod    ----------> is pod sa traffic arhi hogi..
      namespaceSelector:
        matchLabels:
          name: prod      ------> is sa sirf prod namespace ma mojood "API pod" ki traffic hi DB pod per arhi hogi..       

    - ipBlock:             -----> rule#2
        cidr: 19.168.5.10/32         allow ip for backup server in DB pod network policy..  
    ports:
    - protocal: TCP
      port: 3306    ---------> DB pod port 


---------------------

- podSelector:       -----> rule#1
      matchLabels:
        name: api-pod    ----------> is pod sa traffic arhi hogi..
  namespaceSelector:
    matchLabels:
        name: prod      ------> is sa sirf prod namespace ma mojood "API pod" ki traffic hi DB pod per arhi hogi..       

- ipBlock:             -----> rule#2
      cidr: 19.168.5.10/32  

remember network policy ma "rule#1 or rule#2"  "OR operation" k tor per kam kr rhy hn.. 

or "rule#1"  ma multiple section like "podSelector" or "namespaceSelector" aps ma "AND operation" k toor per kam ker rhy hn

"-" dash represention no of rules...

other scenario:
---------------

- podSelector:       -----> rule#1
      matchLabels:
        name: api-pod    ----------> is pod sa traffic arhi hogi..
- namespaceSelector:
    matchLabels:
        name: prod      ------> is sa sirf prod namespace ma mojood "API pod" ki traffic hi DB pod per arhi hogi..       

- ipBlock:             -----> rule#2
      cidr: 19.168.5.10/32 


now pod Selector or namespace work as 2 saparate rule and work as "OR operation..." 
ab is ka y matlab bn rha ha k 1 rule k according same namespace sa "api pod" ki traffic aye gi DB pod per aye gi..  or 2nd rule k according "pod namespace" ki sabi pod ki traffic DB pod per arhi hogi...

ab sir khty hn k let say k apky DB pod ma koi "agent" chal rha ha jo k DB pod sa database k backup lye ker backup server ma send kery... is ka lye apko "egress" policy ko DB pod ma allow kerna hoga tky DB pod sa outgoing traffic bahir ja saky toward backup server per. 
-----
like this:


policy-definition.yaml
----------------------
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: db-policy
spec:
  podSelector:
    matchLabels:
      role: db       --------> network policy link to the pod(jis pod per y policy chaly gi) --(pod label)
  policyTypes:   
  - Ingress   ----> give the policy type(mean incoming traffic)
  - Egress
  ingress:
  - from:
    - podSelector:       -----> rule#1
        matchLabels:
          name: api-pod    ----------> is pod sa traffic arhi hogi..
    ports:
    - protocal: TCP
      port: 3306    ---------> DB pod port 

  egress:  ----> rule of outgoing traffic from DB pod 
  - to:
    - ipBlock:
          cidr: 192.168.5.10/32  ---> ip address of backup server
    ports:
    - protocol: TCP
      port: 80    -------> port of backup server..

Solution:
--------

1- kubectl get networkpolices or kubectl get networkpol   or kubectl get netpol----> in this way you can get network polices in you enviroment..

2- which pod is the network policy applied on?

  describe the network policy and check label... under pod selector.. you will get to know about pod having same label..

3- kubectl describe netpol "network policy name"

  you will get to know about traffic policy..

4- apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: internal-policy
  namespace: default
spec:
  podSelector:
    matchLabels:
      name: internal        --------apply network policy tu internal pod
  policyTypes:
  - Egress
  - Ingress
  ingress:
    - {}         ---no ingress rule
  egress:  ----------- adding egress rule
  - to: 
    - podSelector:
        matchLabels:
          name: mysql           --------- traffic will go from internal pod to db pod
    ports:
    - protocol: TCP
      port: 3306

  - to:
    - podSelector:
        matchLabels:
          name: payroll       --------- traffic will go from internal pod to payroll pod
    ports:
    - protocol: TCP
      port: 8080

  - ports:
    - port: 53
      protocol: UDP        ----------- in port per jye gi...
    - port: 53
      protocol: TCP



















Kubectx and Kubens – Command line Utilities
Throughout the course, you have had to work on several different namespaces in the practice lab environments. In some labs, you also had to switch between several contexts.

While this is excellent for hands-on practice, in a real “live” kubernetes cluster implemented for production, there could be a possibility of often switching between a large number of namespaces and clusters.

This can quickly become confusing and overwhelming task if you had to rely on kubectl alone.

This is where command line tools such as kubectx and kubens come in to picture.

Reference: https://github.com/ahmetb/kubectx

Kubectx:

With this tool, you don’t have to make use of lengthy “kubectl config” commands to switch between contexts. This tool is particularly useful to switch context between clusters in a multi-cluster environment.

Installation:

sudo git clone https://github.com/ahmetb/kubectx /opt/kubectx
sudo ln -s /opt/kubectx/kubectx /usr/local/bin/kubectx

Syntax:

To list all contexts:

kubectx

To switch to a new context:

kubectx

To switch back to the previous context:

kubectx –

To see the current context:

kubectx -c

Kubens:

This tool allows users to switch between namespaces quickly with a simple command.

Installation:

sudo git clone https://github.com/ahmetb/kubectx /opt/kubectx
sudo ln -s /opt/kubectx/kubens /usr/local/bin/kubens

Syntax:

To switch to a new namespace:

kubens

To switch back to previous namespace:

kubens –




