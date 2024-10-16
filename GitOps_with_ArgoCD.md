**Content**

1- GitOps Introduction
2-  ArgoCD Basic
3-  ArgoCD Intermediate
4-  ArgoCD Advanced
5-  ArgoCD with Jenkins CI Pipeline

**Problems**

jb ki waja sa gitops with argocd ki zaroorat pari..

Let say team need to implement solution from scratch teams has followed the process.

-   Infrastructure as code
-   Policy as code
-   Configuration as code
-   Network as code

basically team avaid manually setting up infrastructure... for **Infrastructure as code**, it uses **terraform for infra and ansible for configuration**

For central access version control. it uses **git&github**

To overcome the manual process it uses CI/CD pipeline for automation... it automatic the build , test and containerization process for applications. 

And for **deployment the CD pipeline follows the traditional push-based approach** using **kubectl commands** to push changes to the kubernetes cluster..

for agr infrastructure or kubernetes cluster ma koi changes krni ha tu team console sa through commands kr rhi hogi..


**but This approach has a few problems** like using the CI Push-based model making manual changes through a CLI processes security issues as **it requires exposing credentails outside of your cluster**.

There are ways to secure credentails in CI/CD and CLI. **but it is generally not recommeded as it is a very well-known attack vector for the CI/CD systems..**


Since the users are making manual changes to cluster through CLI and other means, it leads to configuration drifts. Lets also not forget about the cloud computing disasters.

During disaster the team should have disaster recovery plan to recover the infrastructure and the application state.

**the configuration can be referenced from the desired state in GIT.** but the problem is the configuration in GIT is not the latest one as manual changes were done directly on the cluster or infrasturture by the team using CLI and other means.. which were not part of git.

**once the infrasturcture and kubernetes are back running, the team has to go through a painstaking process to figure out what changes we made manually and repeat them to get the desired state.**

**This problems could be overcome using the GitOps methodology**

What is GitOps
----------------

Gitops is a framework where the entire code delivery process is controlled via Git. it also includes infrastructure and application definition as code and automation to deploy changes and rollbacks. 


Gitops can be considered as an extension of infrastructrue as code that uses Git as the VCS.


**Developers commit to a shared repository using a version control system such as GIT. Usually, a feature branch is created, which is a copy of the main code base.** 

**where in a team of developers can work on a new feature unitl it is completed. A CI service automatically builds and run unit test on the new code and merge the code into a central repository. Before merging, the changes are reviewed and approved by the concerned team. A continuose deployment is the final stage in the pipeline that refers to the automatic releasing of any developer changes from the repository to the clusters. the core idea here is to have the infrastructure application and all related components declaratively defined in one or more Git repositories.** 

In the GitOps scenario, an automated process ensures that the desired state inthe repository and actual state in the production enviroment always matches. 

**A gitops operator runs within one of the kubernetes cluster. it continuously monitors and pull chnages from Git repository and applies them within the cluster it is running. it can also apply them in a different cluster as well. MeanWhile, if a developer merges new code to the application Git repo an automated CI process kicks in and does a round fo unit testing, whilst the application reads the Docker image and push it to the container repository.**

**Finally, it also updates the kubernetes manifrest within another Git repo. the git operatore identifies the difference b/w the desired state in the Git repo versus the actual state in the cluster. It pull the changes and makes sure that the desired state always matches the actual state.** Gitops also **eases the rollbaceprocess** Since all the code is version controlled in git, **a team memeber can issue a simple Git revert command** to go undo any changes which are made earlier.

Since the repo is continuously monitored by a gitops operator, it picks up the changes and rolls back to the previous state.

GItops principle
----------------

it has four principles.

The first principle is about declarative vs imperative approach.

Gitops demands the entire system, including infrasturcture and application manifest to be declared in a declarative state. 

like:
deployment.yaml
---------------

apiVersion: apps/v1
kind: Deployment
metadata:
    name:   nginx-deployment
spec:
    replicas: 3
    template:
        metadata:
            labels:
                app: nginx
        spec:
            containers:
            -   name: nginx

it **discourages** the use fo the imperative approach as it uses a series of explicit commands to change the desire state.

**it imperative approach also make reconciliation difficult because it does not store any state.**


**2ND principle is to make use of GIT**. All the declarative files. also known as the desired state is stored in a Git repo. it provides VCS and also enforces immutability.

since the desired state is stored and versioned, it is essentially known as the **source of truth state.** Once we store the desired state in Git, We must allow any changes to the state to be applied autmatically. 

**This brings us to the 3rd principle. GitOPs operators, also knowns as Software agents,**


**It automatically pull the desired state from git and apply them in one or more enviroment or clusters. The Gitops operator can run in one of the cluster and can make or oush changes to other cluster as well. **


**the final principle talks about reconciliation. The gitops operator also make sure that the entire system is sefl-healing** to reduce the risk of human errors. **the operator continuously loops through three steps, observe, diff and act**

In **observe step** it checks the git repo for any changes to the disered state. 

In **diff step** it compares the resources received from the previous step to the sctual state of the cluster. 

In **act step** it uses a reconciliation function and tries to match the actual state to the desired state..

What/Why/How ArgoCD
-------------------------

Why use ArgoCD
--------------

It extends the benefits of declarative specfications and Git-based configuration management..

It is the first step in continuous operations based on monitoring, analytics, and automated remediation..

It can deploy to multiple clusters and is Enterprise-friendly(auditability, compliance, security, RBAC, SSO and lot more)

What is ArgoCD
---------------

Argo CD is a declarative, GitOps continuous delivery tool for kubernetes resources defined in a Git repository..

Continuously monitors running  applications and comparing their live state to the desired state..

It reports the deviaitons and provides visualizations to help developers manually or automatically sync the live state with the desired state.

DevOps vs GitOPs
----------------

Gitops typically use ki jati ha containers technologies like **kubernetes and openshift** but devops can be use with any applications.

for example devops pipeline CICD...
-----------------------------------
Devops pipeline 
---------------

In devops pipeline the changes will push to the cluster...

developer code ---> push source code(commit) --->CI-portion[unit test--->build-artifacts ----> build-imagesv2.4 ----> push registryv2.4]-->CD-portion[---> an applies a kubectl imperative command to push the changes to the cluster "kubectl applyv2.4] 

GitOps pipeline
---------------

In gitops pipeline the changes were pulled by the operator..

developer code ---> push source code(commit) --->CI-portion[unit test--->build-artifacts ----> build-imagesv2.4 ----> push registryv2.4] ----> clone the manifest configuration repo --->update the manifest---> push to the feature branch with the new images name, commit and push to branch---> and finally pipeline raise pull request to the manifest repo--> team member or sernior review it and approve the changes.. and merges the changes...


now git operatior running in the kubernetes cluster will pull the changes from the repo and sync them with the cluster.

Push vs PUll base deployment
----------------------------

developer code ---> push source code(commit) --->CI-portion[unit test--->build-artifacts ----> build-imagesv2.4 ----> push registryv2.4]-->CD-portion[---> an applies a kubectl imperative command to push the changes to the cluster "kubectl applyv2.4] 


this is a push base deployment where we are basically push the changes to the cluster through jenkins as CICD tool... is case ma jenkins k ps cluster ki red/write access honi chahye jis sa wo cluster ma changes push kry ga.. jis k lye cluster k credentail expose kr k outside the cluster jenkins ma store krny hogi..

this raises potential issue and is not recommended. 

Apart from this the CI system(jenkins) also has read-only access to the git repo and read write access to the container register(gcr/ecr/dockerhub). and kubernetes cluster has read only access to container register(gcr/ecr/dockerhub)

benefits 
--------
-   In a push base approach the deployment is not restricted to  a perticular plugin..
-   Deploying Helm charts can be done easier
-   Secret Management is easier

Problems
------
-   Cluster config are embedded inside the CI system.
-   CI system has Read-Write access to the cluster.
-   Deployment approach coupled to the CD system..

Pull based Deployment
---------------------

-   In pull based approach the Gitops operator argocd agent deploys new images from inside of kubernetes cluster.

-   The operator can either check a container repo(container registery) for new images or can get check github repositary for manifest files updates...

-   in pull base approach CICD jenkins system has Readonly access for github and readwrite access for container repo(registry). and it does not have access to the kubernetes cluster..


- PUll base has some challenges like managing secret is big tricky as compare to push base model..

As devops engineer. it is important to encrypt the secret. so in pull base model we can do this by using **HashiCorp Vault** or **Bitnami sealed secrets**

As per gitops principles, even secrets could be declaratively published to Git repo. While deploy a Helm Chart, managing secrets is harder because the secrets must first be encrypted using a tool like HashiCort Vault or Bitnami Sealed secrets, and the decrypted before passing on to the GITOPS operator. this approach remains the same for generic secrets deployments as well.

benefits
---------
-   nO external user/client has the right to modify the cluster
-   Scan container registry for new versions.
-   Secrets in the Git repositary via Hashicorp vault
-   Deployment appraoch is not coupled to CD pipeline
-   Gitops operators support multi-tenant model. mean multiple namespace and contianer registry at the same time..

GitOps Feature Set & Usecases
-----------------------------

-   Everything must be decleravtively stored in git repositary.. contains the desired state and its knows as signal source of truth.. 

-   Since everything is stored at git. the application roll back can achevied using a simple **GIT revert command**, which reverts to the previous Git state.

ap commit history ko dekh ker check ker sakhty hn k issue kha per ha...

**one of the key distinction b/w gitops and other deployment techniques is its ability to detect configuration drifts earlier.**

**With with GItops you can also make deployment on multiple clusters**

The single gitops operator can deploy application on multiple cluster without the need to be installed or set up on all the cluster.

GitOps Benefits & DrawBacks
---------------------------

Benefits
--------

-    it is light weight and vendor-neutral. it's because the underline protocal is open source and usable on a wide variety of platforms and setups.
-   it is faster, safer, immutable, and reproducible deployments.
-   Eliminating configuration drift. let assume even after taking  precautions, someone from the team manually changed or updated a configuration directly on the cluster. Here the gitops operator will fix that for you based on the desire state which is stored in the Git.
-   Uses familiar tools and processes.
-   Revisions with history   , we take advantage of history tracking capabilities of git.. in order to identify difference b/w two 2 declarative files, we may compare them, and they can typically be linked to a specific change request.

Drawbacks
-------------

-   it does not help with secret managment. the OPs teams needs additional tools to secure and use secrets with git operators.
-   Number of Git repositories , we need to decide whether to have source code and manifest in the same or saparate repositories..    buhat zayada repo sa code pic krny m ay masla krta ha.

and for multiple enviroment we need to decide to use either saparate repo or multiple git branches... when it comes for organizing your git repositories there is not at one size at all.. we should go with what is good to work best for our applicaitons..

- We also have challenges with programmatic updatess. CI or CD k br br chalny sa update repo ma conflict ker sakhti hn, so for resolving the conflict on repo we need to have a manual solution to avoid this issue.

-  Governance other than **PR approval**...., Here GitOps relies on PR, which is a poll-based approval model. Where a PR approval is responsible for the review.

-   Malformed YAML/ config Manifests  --> so users must rely on other tools to validate the manifest files.

GitOps Project Tools
--------------------

we will apply gitops practices to kubernetes applicaitons.. And gitops controller, we will make use of the ArgoCD project.

Argocd is declarative continuous deployment tools for kubernetes.. 

Other tools which provides the gitops capabilites...
-----------------------------------------------------

-   FluxCD        
-   Altantis
-   Autoapply   autoapply change from git to kubernetes- cluster
-   CloudBees
-   jenkinX   - it provide pipeline automation with built in gitops.
-   Flagger
-   Ignite
-   Faros
-   Helm Operator
-   Weave GitOps Core
-   KubeStack         gitops frameworks using terraform for cloud kubernetes distributions like AKS, EKE, EKS with CI/CD for common tool
-   Weave Cloud    which is automation and management platform form development and devops teams..
-   GitKube
-   PipeCD   it is continous delivery tool for declarative kubernetes , serverless and infrastructure applications..
-   Werf


How ArgoCD works
-------------------

It follows the GitOps pattern by using Git repositaries as the source of truth for the desired state of app and the target deployment envs.

    kustomize applications
    Helm charts
    Ksonnet applications
    Jsonnet files
    YAML/JSON manifests

It automates the synchroznization of the desired application state with each of the specified target enviroments..

Concepts Terminology
--------------------

argocd k concept ko samjny k lye apko git, docker, kubernetes , CICD  k concept any chahye..


hum argocd ma **argocd application** bna b rhy hogye or kam b kr rhy hogye...

**application aik custom resource defination ha. jb ap argocd ko install krty hn tu y create hoti ha...**

**or argo cd application ma source or destination kubernetes resources define hoty hn..**

**the tool that is used to build the application is** ,**Helm** , **Kustomize**, **ksonnet**.

**it provides a logical grouping of application, which is useful when argo cd is used by multiple teams...**

Applications: A group of kubernetes resources as defined by a manifest.
------------

Applicaition source type: A tool is used to build the application. E.g Helm, kustomize or ksonnet.
------------------------

Project: 
-------
it provides a logical grouping of application, which is useful when argo cd is used by multiple teams...

Target state
-----------------

The desired state of an applicaiton manifest, as represented by files in a git repository..

Live state
-------------

The live state of that application, What pods, configmap, secrets, etc are created/deployed in a kubernetes cluster.


**when an argo cd applications created. it tries to synchronize the desired state in GIT to the live state in cluster**

this is called as **sync**. it reconcile the current state of cluster to the target state(desired) in git

**it is an example of applying changes to the kubernetes cluster...**

**Sync status** is know, whether or not the live state matches the target state. Is the deployed application the same as GIT says it should be?

**Sync operation status** let us know whether or not sync succeeded.

**Refresh** Compare the latest code in Git with the live state, figure out what is different.

**Health** The health of the application, is it running correctly? can it serve requests?

it provide overall health application status as a whole..


Argo CD features
-----------------

-   it has an option to automatically deploy applications to specfied target enviroment in multiple clusters.
-   it also support multiple config management and templating tools (kustomize, helm , ksonnet, jsonnet, plain-YAML)
-   it also provides audit trails for applications events and API calls..
-   it can also intregrate with varies 3rd party product. **Github** **Gitlab** **Microsoft** **Linkedin, OIDC, OAuth2, LDAP, SAML 2.0 for SSO intregrations** 
-   Webhook integration (GITHUB , BITBUCKET , GITLAB)
-   It also has an option to Rollback/Roll-anywhere to any applcaiton configuration which is committed in Git repository..
-   It also provide web UI for real-time view of application activity..
-   It can also automatically detect any configuration drift, and it can also give you visualizations to pinpoint the differences. 
- It also provide out-of-the-box prometheus metrics. so we can set promethoues and we can visualized the data using grafana.
-   it also has alot of option like preSync, Sync, postSync hooks to support complex applications rollouts(e.g blue/green & canary upgrades)
- It also supports Multi-tenancy and you can also create custom RBAC policies for different authorization
- It also provides a CLI and supports access tokens for automation through CI integrations.
- It also provides health status analysis of all the applicaiton resources..and we can also create our own custom health checks as well..
- It also provides an option to automatically and manually synchronzie an application to its desired state.

ArgoCD architecture
----------------------

Let assume k hmry pass kubernetes ka enviroment ha or argocd install howa ha kubernetes enviroment ma as kubernetes controller..

Users can access argocd and make changes within argocd either using CLI or through a user interface.

some of the operations like creating argo cd applicaitons and managing existing projects, setting up single sign-on with external providers, and more synchronizing options.

Argocd continuously monitors running applications and compairs the current state(in cluster) against the desired state in the Git repository,

**so any changes made to the desired state in the Git repo can be automatically pulled and applied in the specified target envrionments**

**we can also configure a webhook on Git repository which is going to notify ArgoCD based on Git events..**

The argocd API server is a gRPC REST server, which exposes the api... This API is consumed by the web UI, CLI and can also be used with CICD systems.

**Argocd install in one kubernetes enviroment can attach with multiple other kubernetes enviroment from this enviroment..** This is known as multi-cluster deployment.

**Argocd also exposes different set of prometheus metrics, which can be visualized through Grafana, and it also has out of the box notifications service with various triggers, message templates and can notify multiple 3rd party service like Slack, email, Github**

Argo CD install option
----------------------

Argo CD has 2 installation options, 

-   Multi-tenant
-   Core      A Core installation is best suited for users who use the argoCD alone and do not require multi-tanent.

it install minimul non HA version of each component and exclude the API Server and user interface..

**Multi tanent is the most popular method for installing the argocd in the multi-tanent installation model.**

In multi-tanent we have 2 different installation method available

-   High Availability
-   Non High Availability   --- it is not suggested for using productions..  it can be used in evaluation phase , for testing , for proof of concept.. it has 2 manifest....

    -   Install.yaml   it provide a standard installation with cluster-admin access to argocd. If you intend to use ArgoCD to deploy application in the same cluster. where argocd is running. use this manifest site, with provided credentials. it will still be able to deploy applications to remote cluster as well.
    -   namespace-install.yaml   This provides installation which only requires namespace-level access.  We need to use the manifest if we want argocd to rely on provided cluster credentials and don't need argocd to deploy application in the same cluster that it is running in.

    And of course, with provided credentials, it will still be possible to deploy applications within the same cluster.  

    For production use, we use the high-availability installation option and the components in this are identical but have enhanced per high availability and resilience. it again provide 2 manifests, 

        -   ha/install.yaml
        -   ha/namespace-install.yaml


    In this course, we will be using the **install.yaml** manifest form the non-HA available version and install it within the argocd namespace... like

        kubectl apply -n argocd -f https://raw.githubusercontent.com/argoproj/argo-cd/stable/manifests/install.yaml

**Argo CD can also be installed using helm. This is a community-managed or maintained chart, And by default, installs the non-HA version of ArgoCD.**

    helm repo add argo https://argoproj.github.io/argo-helm
    helm install my-argo-cd argo/argo-cd --version 4.8.0

**After installing argoCD, to interact with argoCD API server, we need to download the CLI from its GITHUB repository and move it to our user local bin directory** we will set this up, and log in and interact with server using CLI commands..

    curl -sSL -o /usr/local/bin/argocd https://github.com/argoproj/argo-cd/releases/latest/download/argocd-linux-amd64

    chmod +x /usr/local/bin/argocd

ArgoCD Installation
--------------------

let install argo cd and argocd CLI.

**https://argo-cd.readthedocs.io/en/stable/getting_started/**

or 

**https://github.com/argoproj/argo-cd/releases**

commands.. for NON HA-Version

kubectl create namespace argocd
kubectl apply -n argocd -f https://raw.githubusercontent.com/argoproj/argo-cd/v2.11.7/manifests/install.yaml

after this check resources in **argocd-namespace name**, **argocd** and to access the argocd server service from browser, changed argocd server service from clusterip to nodeport. and user ip and port in browser for accessing the argocd page.

for login:
----------

username: admin
password: you can get it from cluster secret where argocd installed.

    kubectl get secret -n argocd
    kubectl get secrets argocd-initial-admin-secret -o json -n argocd

    get password from it. it would be in the base64 format. so first decode the password and use it for login..

     kubectl get secrets argocd-initial-admin-secret -o json -n argocd | jq .data.password -r | base64 -d

     get and use password in login


with argocd repository section. you can connect with you github repository...

with argocd cluster section. you can connect with multiple clusters.

go to account section and update the password for security and set your own password and login again..

Now install the argocd CLI
--------------------------

So the argocd server can also be access using argocd CLI.


go to the argocd github releases section and take (copy url)**argocd-linux-amd64**

**https://github.com/argoproj/argo-cd/releases**

now go to cluster cli and download the package from internet by using **wget** commnad like

**wget + argocd-linux-amd64 copied url**

once you download it successfully, rename the package and make it executable and move it to the **bin** directory..

mv argocd-linux-amd64 argocd    --> rename it
chmod +x argocd                 --> make it executable
mv argocd /usr/local/bin/       --> mv it to the bin directory

verify it 
---------

argocd --version

once done

now connect argocd from CLI
---------------------------

use below command for this
    
    argocd login ipaddress_of_argocd_server

kubectl get service argocd-server ---> take ip and use it login command again...


in a way you can successfully login in argocd from terminal..

the use **app list** command for list the deployed app.. it will give you nothing. because nothing was deployed..

    argocd app list 

    argocd cluster list  --> when you install argocd in kubernetes cluster it is going to also make the cluster(target) where we installed it as the target, so it should be able to deploy applications to this cluster.

next we will see how argocd will create application on multiple cluster..

ArgoCD App & project
--------------------

let talk about argocd application...

we need to understand 2 thing,

-   Application
-   Project

An application is a CRD(Custom resource defination) which represents a deployed application instance in a cluster.

An application in argocd is defined by 2 key pieces of information.

-   source and destination for your kubernetes resources..

the source is mapped with git repository where the desire state of our kubernetes manifest live. and destination is the target where resource deployed.

apart from source and destination, CRD have 

-   Source
-   Destination
-   Project
-   Sync Policy
-   Ingore Diff
-   Helm
-   Jsonnet as a source 
-   Customize

**Application CRDs can be create in different ways** like

-   YAML specfication
-   User Interface
-   CLI

Doing with CLI
--------------

    argocd app create color-app \
    --repo https://github.com/sid/app-1.git \
    --path team-a/color-app \
    --dest-namespace    color \
    --dest-server   https://kubernetes.default.svc

once the application created. it pulls the manifest from the github source and send it to the target..


YAML Specfication for generic Argocd application
------------------------------------------------

apiVersion: argoproj.io/v1alpha1
kind:   Application
metadata:
    name: color-app
    namespace: argocd
spec:
    project:    default
    source: 
        repoURL:    https://github.com/sid/app-1.git
        targetRevision: HEAD
        path:   team-a/color
    destination:
        server: https://kubernetes.default.svc
        namespace: color
    syncPolicy:
        automated:
            selfHeal:   true
        syncOptions:
        -   CreateNamespace=true

Demo Argocd Application using UI
--------------------------------

Let see how to create argocd application using UI..

open argo cd on browser then

> go to application section
> click New App
> give argo applicaiton name
> select project to which argo cd project will be mapped to or the will be mapped to.. **bydefault one default project named default will be create to select it**
> select sync policy **Manual** or **Automatic**, in our case we select manual. you can also set a sync options..
> now give the source(where your yaml file have been placed). in our case it would be in github.. 

you can copy paste the link. or you can git argocd with github from **argocd repository section**

if you connect argocd to repo as source then below are the steps..
-----------------------------------------------------
>In argocd go to Manage your repositories > repositories > connect repo using HTTPS >

then give 

type: git
project: default
Repository link: github repo https link
username:  
password:
give username/password here if your repo is private...

then click on **connect**. it will connect argocd to github repo as source.....

this info you just gave, argocd stores it in cluster as secret... 

when you will go and see the secrets where argocd have installed. you will see a new secret just came up. and when you open it using get command you will get your given information in base64 format..

    kubectl get secrets "secret-name" -o json -n argocd

verify it by decoding the secret..
----------------------------------

    kubectl get secrets "secret-name" -o json -n argocd | jq .data.url -r | base64 -d


ab jb again ap UI sa app create kro gye.. as i have mentioned in my pervious step.. tu source section ma apko apki created source repository hover horhi hogi... select it..

also select **repository path**

> once source repo selected. Now you can select destination path...

destination would be the same cluster. it will hover you the same cluster where argocd deployed.. because you have not added any other cluster in argocd...

and **give cluster namespace** as well where target resource should be deployed..

then click to create it..

> now go inside the applicaition. and you will see that application connected to github and get yamls for deployment inside the cluster. but it is not deployed yet. because some resource like mentioned namespace(it was mentioned while create the CRD applicaition using UI) was not created in cluster. for resolving this create a name space in cluster. 

and you can manually sync target to live by clicking on **sync** in argocd under applications.

let say you have not create namespace in cluster and manually sync using argocd UI. it will give you the **SYNCOUT** Error. **Click on it and it will give you the exact reason. why it is not creating a resource**.

In a way you can see the error.

so for resolving this. you can manully create a namespace in cluster. using kubectl command 

**but you can also do the same thing using argocd UI. click on Sync > then click on auto-create namespace in a cluster > and click on synchronized, and it will pull resources from github and deploy resource in that namespace. it will create a require namespace. because the during the CRD application created you have mentioned the name of the namespace.

now the same detail. you usually get from kubernetes after deployment like pod, service etc. will also get from argocd as well.. you just click on the component and see want you want to see.

ab ap jo b changes github yaml manifest ma kro gye argocd operatore isko automatically sync kr lye ga agr apna CRD krty time automatic per click kya tha..other wise apki manually argocd k through sync per click kr k sync krwana hoga.

you can also click on the argocd **Refresh**. it will poll the repository and check the upload if found it will deploy to destination cluster.

How to rolled back using argocd
-------------------------------

you can also rolled back to pervious updates using argocd, if any thing in new update get promblematic..

so for this go to argocd under applicaiton CRD and click on **History and Rollback**(it will show you previous commit) > and on previous commit just click on **RollBack**. argocd will take it to the previous state.. and it going to use previous git configuraiton..

Delete application
------------------

once you delete the argocd application. your all resource in kubernetes cluster that were created by the applicaition will be deleting as well. 

but namespace will not be deleting

Creating Argocd application using CLI
-------------------------------------

how to create argocd application using CLI...

first connect to your argocd server using CLI.. 

    argocd login **argocd-serverip**

then 

using command to create applicaiton CRD using cli..

    argocd app create ----> with this you can use source like git, helm app, helm repo, jsonnet app, kustomize, custom tool..

command:
-------

    argocd app create solar-system-app-2 \
    --repo https://github-repo-link \
    --path "path to the github repo(name of the folder where yaml are available)" \
    --dest-namespace  "namespace name where resource will be deploying" \
    --dest-server   https://kubernetes.default.svc --> destination server..


    argocd app list --------> for listing the app

    argocd app sync "name-of-the-application"    -----> it will manually sync the target(source yaml) to the destination(cluster resources)      --> y ap tb use kr rhy hoty hn jb apna application  CRD create krty time **automatic** ki bjye **manual** sync ko select kya ho.. automatic k case ma wo automatically sync kr leta ha..

    argocd app list --> status HEALTHY will give you the confirmation that everything(resource) is running fine.. 

Argocd PROJECT
---------------------

Creating a custom argocd Project...

list the existing project...

    argocd proj list

with this we have seen a default project with name default... it has

Destination: * => mean all
Sources:    * => mean All
Cluster resource:   */*  --> it can deploy any cluster level..


we are creating a custom project that have some restrictions...


> so go to argocd under projects section and create a new project >

default project ma by default sab **allow** hota ha but for restrict, you need to create new project jis ma ap apny accordingly cheezy set kr sakhty hn...

like sir did this.. he is basically creating a project and add some restriction on it. so it can use in application CRD. so application work accordingly... 

under project y removed the * and add source github repo url. will * the project will get source from any github repo. but without this it will only get source from mention repo..

same do with the destination.


**and under cluster resources section under created project.. we can control what resources need to add or what do not need to add to the cluster...**

**mean wo sab ko source sa lye ga but jb ko ap na deny list ma dala ha wo resource destination cluster ma create ni hoga..**

you can also enable monitoring from this....

apart from this you can adjust or set **Roles**, **synchronized Windown**, **event** in project..

once the project create, you can also see through UI and CLI...

    argocd proj "project-name" ----> CLi command to see the project.. 

now use this project in your CRD's applications..


Argocd intermediate
-----------------------

Reconcilation loop(is ma argocd sync kb kry ga wo time define krty hn.. )
-----------------

Reconciliation function tries to match the actual state of a kubernetes cluster to the desired state defined in GIT. 

**but a reconciliation loop is how often your argocd application synchronize from the git repository.** 

In a Devops or GitOps world, software teams have multiple releases per day to production. the teams commit the application to git repo multiple times throughout the day. If multiple commits are done to the git, how often does argocd synchronized the desired state from git to the actual state in kubernetes environment. 


**In generic Argocd configuration, the default timeout period is set to 3**, or agr ap bulkul ma wait kerna ni chahty tu ap **argocd UI per REFRESH ko click kery** y set time k khtam hony k wait ni kry ga or instancly changes get kerny k lye sync start kry dye ga github sa..... This is a one way to sync and check if any update commit happened in git repo...

This value is configurable and is used within the argocd repo server. As discussed earlier, the argocd repo server is responsible to retrive the desired straight from GIT repo server, and it has a timeout option called as the application reconciliation timeout.

if we check the enviroment variable of argocd repo server pod, it says that the key timeout reconciliation can be configured on argocd config map. the argocd config map is created when we install argocd and is empty by default. we can patch this config map with timeout reconciliation key and a custom value for example 300sec. 

After patching the config map, the argocd repo server deployment should be restarted for it to pick up the value from the config map. once it done the argocd will check the changes in git repo every five(300sec) minutes.


    kubectl -n argocd describe pod argocd-repo-server | grep -i "ARGOCD_RECONCILIATION_TIMEOUT:" -81

    kubectl -n argocd patch configmap cargocd-cm --patch='{"data":{"timeout.reconciliation":"300s}}'

    kubectl -n argocd rollout restart deploy argocd-repo-server

    kubectl -n argocd describe pod argocd-repo-server | grep -i "ARGOCD_RECONCILIATION_TIMEOUT:" -81

webhook
-------

In the previous slide, we saw how the repo server depends on the reconciliation timeout parameter for argocd config map. with or without the timeout, the argocd repo server pulls git repo every 3 to 5 mint to see if any manifest have changed. 

**The API server can be set up to receive webhook events in order to remove the polling delay within our git provider **

we can create the webhook by defining the argocd server instance endpoint appended with **/api/webhook**

Once the webhook is created for every push event to the git repo, the webhook is going to send the events to the argocd server, and argocd repo server will in turn pull the committed changes. By using a webhook we can remove the polling delay which we have seen in the earlier slide.

Git WEBHOOK CONFIGURATION
-------------------------

when ever a change is pushed to the repo, it is going to send an event to the argocd server, and argocd will pull that commit and deployed into destination cluster.

create and argocd CRD application using UI
------------------------------------------

> go to application section
> click New App
> give argo applicaiton name
> select project to which argo cd project will be mapped to or the will be mapped to.. **bydefault one default project named default will be create to select it**. mean it is allow to sync from all source and send to all destination... default has no restriction set...
> select sync policy **Manual** or **Automatic**, in our case we select manual. you can also set a sync options..
> now give the source(where your yaml file have been placed). in our case it would be in github.. 

you can copy paste the link. or you can git argocd with github from **argocd repository section**

copy paste the github link , **Set Revision HEAD** , **Set path to the path in github where is your manifest available**
> Now you can select destination path...

destination would be the same cluster. it will hover you the same cluster where argocd deployed.. because you have not added any other cluster in argocd...

and **give cluster namespace** as well where target resource should be deployed..

then click to create it..

> now go inside the applicaition. and you will see that application connected to github and get yamls for deployment inside the cluster.

now click on **sync** button to sync manifest manually.. during this you can also check box the **automatically create namespace**. it will auto create namespace you mentioned while creating the application CRDs. now click on **synchronized** button... it will start synchronizing manifest from github and deploy this into destination cluster.


HOw to set the polling delay
----------------------------

For this you need to go to cluster where argocd deployed...

**when you describe the argocd service in cluster(the service is responsible for connecting to the git repo and fetching the data ). you will get to know there will be argocd reconciliation timeout which is basically getting timeout values from argocd configmap.... **

if you want to set a time out, like five minutes or 10 min instead of the default three min, you can go ahead and edit this argocd Configmap and add the timeout reconciliation in a parameter within the data field.

**This is one way of setting up**


**The other way of setting up the time out. the other option is if you want to get the synchronization status as soon as a puh event was made to the repo, then we can make use of webhooks.**

Configure webhook
-----------------

> go to the github repo settings > webhooks > add webhooks > and in webhook and target URL. so when the change on repo commited. webhook will send the event to argocd and argocd starts pulling changes from github...

target url
----------

http://argocdipaddress:port/api/webhook

Http method: POST
Post content type:  application/json
Trigger On: Push Events 

and save it

you might be facing some certificate requirement issue. while saving the webhook..

mean github needs some certificate to communicate with argocd server... but we do not have any certificate so for this we will make changes in argocd server deployment and add **--insecure** in deployment..

so edit the argocd server deployment using kubectl command.. and add **--insecure** under spec under container under commands,

mean you are asking your deployment to run insecure by using command...

by doing this. your webhook will successfully connect to your argocd server..

again access your argocd from browser with http url like http://argocdipaddress:port/api/webhook

because it is making connect on plain text. basically we are trying to connect server with insecure way. for secure communicate we need a valid TLS certificate as we have seen before...


ab ap jesy hi git repo ma koi changes update kry gye webhook event trigger kry ga argocd ko or argocd changes pull kr lye ga github sa or apko argocd UI per **OUTOFSYNCE** mil rha hoga, mean us na sync lye lya ha but or synce apni cluster ma implement ni howa, disire or live state mean same ni ha...

ab because of ma synce trigger manual set ki thi application CRD create krty time is lye apko Argocd UI sa isko manually trigger krna hoga.... agr ap automatic set krty tu wo automatically implement b kr denta

Application Heathcheck
----------------------

Let's talk about argocd application health checks...

As seen earlier, argo cd continuously pulling git repo for any new changes, and at the same time. 

argocd will continuously check the status of kubernetes resources. 

let assume argocd pull the changes and applied it on a kubernetes cluster.

argocd will monitor this deployment and designate it as unhealthy if it is unable to scale up to the neccessary number of replicas. 

similarly, there are various resource health check, which are already includes in argocd. like

-   Healthy: which is used when all the resources are 100% healthy, 
-   Progressing: The progressing status is used if a resource is unhealthy but could still be healthy given time..
-   Degraded:   The degraded status is used if the resource status indicates a failure or an inability to reach a healthy state in a timely manner.
-   Missing: the missing status is used if resource is not present in the cluster. 
-   Suspended: The suspended status is used if a resource is suspended or paused.
-   Unknown:    If a health assessment failded and actual health status is not known an unknown status is used..

The following checks are made for specfic types of kubernetes resources. For **kubernetes secrets.** it will determine whether the service is of type load balancer and verifies that the laodbalancer.ingress list is not empty and that the hostnam or ip has at least one value. 

**for ingress resources** it is similar to the service object. it will check if the status.loadBalancer.ingress is not empty and validate thet therer is at least one value for hotsname or ip.

**for PVC**, it checks the PVC,s status.phase field if checks the PVC is actually bounded to a persist volume. 

For deployment , replicaSets, StatefulSets, and DaemonSets the observerd generation must be equal to the desired generation and the updated number of relicas should be equal to the number of desired replicas..


In some cases, we want or we might use policy rules for an open policy agent, these rules are stored in configmaps. As of now  argocd just checks if a configMap map exist and does not check any conditions. Not only a configMap.


**if you cannot find a health chck or your resources, you can also create a custom argocd health check,  argocd supports custom health checks written in Lua scripting..**

which is a lightweight scripting language. custom health check can be defined in argocd configmap. 

Let's assume-- ab is ma sir na btya k aik fronted ki applicaiton deploy krni ha jis ka backgroud white or us per triangle b white hoga jo k nazar ni aye ga.. so hum healthcheck ma y define kr sakhty hn k wo check kry gye triangle ka color white ha tu wo **degarded** k error dye. tky isko change kr k sahi show krwana ja sakhy.. 

similary..


we can create custom health check for any kubernetes resource.

for example: cronjobs. runtimeclase, roles, secrets, namespace, pods, PVCs etc...

A health check makes troubleshooting simpler and provides quicker feedback...

it is much easier to identify an argocd application that is in an unhealthy state rather than going through all the associate configmap to find the error or the misconfiguration.


Application custom healthcheck
-------------------------------

creating custom health check.. we can create custom healthcheck using lua scripting.... it is available on argocd officail website..

define this lau script in configmap.. like this and config map will definitly attach with the deployment.. 

configmap:
---------
apiVersion: v1
kind: ConfigMap
data:
    resource.customization.health.ConfigMap: |
        hs = {}
        hs.status = "Health"
            if obj.data.TRIANGLE_COLOR == "white" then
                hs.status = "Degraded"
                hs.message = "Usa a different color"
            end
        return hs
metadata:
    annotations: ....

once save the change and refresh argocd from UI.. it will give **degraded** health status... you can open a component  by clicking on it which are creating problematic error. it will give you the exact error information..


**ap argocd k through b kubernetes deployed component ko delete or restart kr sakhty hn...**

for resolving problem. update the github repo triangle section on configmap accordingly and sync it again from argocd and it will show you the healthy status..

Type of Sync Strategies
--------------------------

let see the various argocd syncronization strategies..

Argo cd allows customizaition to some aspects of how it synchronizes the desired state from Git to the target kubernetes cluster. When Argo CD discovers a new version of your application in Git, 

it either performs a **manual sync or an automated sync**. if set to **automatic**, argo CD will apply the changes then update or create new resources in the target kubernetes cluster.

if it is set to **manual**, argo cd will detect the changes, but it won't make any changes to the cluster unit and unless a user manually clicks on the synchronized button within the UI or use the sysc application CLI command.

**Argocd auto-pruning** feature describes what happens when files are deteted or removed from Git. Argocd will also remove the corresponding resource from the cluster if it is enabled, and argoCD would delete anything from the cluster if this feature is disable. 

**Self-Healing** of cluster defines the argo cd ability to self-heal when kubectl edits are made directly to the cluster. Note that if you want to adhere to the Gitops standards, performinng manual modifications in the cluster is not advised. if enabled the argocd will remove the changes and return the cluster to the desired state specified in git. 


sir na btya ha y 3(**manual/automatic sync, auto-pruning, Self-Healing)** option ko use krna zaroori ha.. other wise issue askhty hn...

if you have enable automatic sync while creating application CRDs. so when any changes commits in github argocd will pull the change and deploy it in the destination server. 

and at the same time, if the developer/user delete or uses a git revert command to remove any resource manifest from github resource manifest locaiton(mean koi resource delete kr dya ha github sa) let say service.yaml manifest delete ki ha github sa.

Then the service.yaml file will be removed from the git repository but no changes will be done on the destination kubernetes cluster because as of now the application CRD is not enabled for **auto-pruning** the resource.. 

and if any user tries to make any manual changes directly on the cluster using the kubectl CLI command line, for example deleting the configmap directly from cluster using commandline then the configmap resource will be deleted and would not be restore from github(mean manually delete krny sa delete hojy ga but self-healing enable na krny ki waja github ma available configmap ko is ki jaga deploy ni kry ga..) because **self-healing** option is not yet enabled for the application. **if the argocd application has the self-healing option enabled the deleted configmap will be replaced by the configmap which is there in the git repository...**

Demo sync strategies
--------------------

how to enable these 3 component.. 

> open argocd UI on browser.. then go to under application CRDs and **click on App Details** > under app details under **Sync Policy** enable 3 options(manual/automatic sync, auto-pruning, self-healing) 

Declaravtive setup
------------------

**Argocd resource which has an application CRD,s repository, or argocd projects can also be declaratively written as a manifest and created using kubectl.**  matlab y ha k argocd ma ap application CRDs jo argocd UI  k through created krty hn wohi kam ap iski mestifest file create kr k b ker sakhty hn jo k **kubectl apply command sa run hogi...**

In our earlier sessions, we made use of the argocd CLI and the ArgoCD UI to create new applicaitons by inputting the source and the destination data. **The same can be created using declaratively manifest.** Let's assume this is the tree structure of our git repository which has a directory name declaravtive with two sub-directories named manifest and mono app. within the mano app. we have an argocd application CRD YAML file.

This YAML file has the project name, the source field referencing to the desired state in GIT by passing the repo URL revision and the path.

This path is referring to the declarative manifest which contains 2 kubernetes resources within the git repository the 2 resource are deployment and service yaml files..

the application has a destination field refering to the cluster and namespace


argocd declarative manifest template:
-------------------------------------

    apiversion: argoproj.io/alpha1
    kind:  Application
    metadata:
        name:   geocentric-model-app
        namespace: argocd
    spec:
        project: default
        source:
            repoURL:    
            targetRevision: repo url --> source in github
            path: ./declartive/manifests/geocentric-model   --> file path...
        destination:    
            server: https://kubernetes.default.svc     -->serveraddress
            namespace:  geocentric-model
        syncPolicy:
            syncOptions:
                -   CreateNamespace=true
            automated:
                selfHeal: true

    
    it can be created buy using kubectl apply command

        kubectl apply -f mono-app/geocentric-app.yaml

    once it is created and once your synchronize it manually/automatically. it is going to pull the deployment and the service manifest from the git repository, and it is going to create them on the cluster.

    this is what we can declaravitively define an applicaiton  and maintain it within the same git repository as well.

Demo ArgoCD application Declarative Setup
--------------------------


RBAC - Role based access control
--------------------------------

We will see how argocd manages role base access control...

    kubectl -n argocd patch configmap argocd-rbac-cm \
    --patch='{"data":{"policy.csv":"p, role:create-cluster, clusters, create, *, allow\ng, jai, role:create-cluster"}}'

    according to the role, it is giving the cluster creation role to "jai" user

Role verfication
----------------

    argocd account can-i create clusters '*'

it will return you "yes".. meaning jai has role for cluster creation...

    argocd account can-i delete clusters '*'

it will return you "no".. meaning jai does not have role for cluster deletion...

giving role for specfic project
-------------------------------
    
    kubectl -n argocd patch configmap argocd-rbac-cm \
    --patch='{"data":{"policy.csv":"p, role:kia-admins, applications, *, kia-project/*, allow\ng, ali, role:kia-admins"}}'

according to the role ali has permissions to access kia-project

Argocd user management
----------------------


The default argocd installation has one build in admin user that has full access to the system and is a super user.


it is advised to only utilize the admin user for initial settings, and then disable it after adding all required users. New users can be created and used for various roles.

ArgoCD supports 2 type of users, local users, and through SSO by intefrating ArgoCD with OKTA , or similar SSO products. In this slide, we will talk about local user management.


    argocd account list    ---> this is you will see the argcd users...

New users can be defined using argocd ConfigMap. We edit the argocd configmap and add account username record. Each user can be assoicated with 2 capabilities, 

-   API key
-   login

    kubectl -a argocd patch configmap argocd-cm --patch='{"data":{"accounts.jai": "apikey,login"}}' 

    
    kubectl -a argocd patch configmap argocd-cm --patch='{"data":{"accounts.ali": "apikey,login"}}' 

after creating user list user to see 


      argocd account list 

    
API key allows generating JSON web token authentication for API access and whereas the login capability allows the user to login using user interface.

The argocd CLA provides commands to set up or to update a user password in a couple of ways. if you are managing users as the admin user,

like:

    argocd account update-password --account jai

    or 

    argocd account update-password \
    --account jai \
    --new-password <enter-password-here> \

    with this way you can update users password using admin account..

The admin password needs to be in putted to set the user password. By default, all the new users have no access. Argocd has 2 predefined default roles, **read only and admin**

The read-only provides read-only access to all the resourcs, whereas the admin role provides unrestrictred access to all resources. By default, the admin user is assigned to the admin role.

we can modify this and can also assign custom role to users by editing argocd RBAC configmap,

    kubectl -n argocd patch configmap argocd-rbac-cm --patch='{"data":{"policy.default": "role:readyonly"}}'

in this example, we are patching the argocd RBAC configmap by assigning a default read-only to any user who is not mapped to a specfic role..

Dex Okta Connector
------------------

Let's understand how ArgoCD uses the dex connector. To allow for the delegation of authentication to a third-party [?] service,

ArgoCD embeds and bundles Dex as part of its installation. Dex is an identity service that powers authentication for other applications

by using Open ID Connect. When a user logs in through Dex, the user's identity is usually stored and authenticated by an external IDP.

Dex acts as a shim between a client application and the identity provider. In this example, the client application is ArgoCD,

and the external IDP is Okta. Dex supports multiple types of identity providers like Okta, Google, GitLab, GitHub, OpenShift, and other protocols like SAML,

OIDC, LDAP, and et cetera. If we go with Okta, we can create a SAML application by providing few basic details within Okta.

For a single sign-on URL, we use the ArgoCD server URL, with /API/desk/callback as its endpoint. Then we assign the SAML application

to individual user or to multiple groups. In this example, we assigned the application to a user named Kia-team. These users and user groups

are completely managed by Okta. Once the Okta app is created, it also provides a single sign-on URL and an X509 certificate.

The single sign-on URL and the X509 certificate needs to be added to ArgoCD configmap. After adding the Dex configuration

to the ArgoCD configmap, we can refresh the Argo UI, and you can see a new login via Okta button

is enabled on the login page. By default, users logged in via Okta will not be able to make any changes

within ArgoCD. We can edit the ArgoCD RBAC configmap and add a new policy to allow all operations for applications

within ArgoCD kia project. Please notice that we have used kia-team within the group section in the policy. This is the name of the group,

which is defined and maintained in Okta. This policy applies to all people who are part of the group kia-team which is maintained within Okta.  Thank you.

check secreen shots...


Demo User Management with OKTA
------------------------------

[music] -Let's talk about how Argo CD can be connected with an external IdP, such as Okta for user management. Let me quickly go to the documentation.

This is how the Argo CD user
interface login page looks like. By default, it only allows you
to use the basic username

and password authentication. Let's configure it
to use an external IdP such as Okta. Within the documentation,
if you go under the User Management,

you have a lot of third-party IdPs. We will be making use of the Okta product. Within Okta, we have a couple of options. 

We can enable single sign-on
either using SAML or OIDC. We will be using SAML with the Dex option. It gives you
the step by step instructions

on how you can create an Okta application and how to configure it within Argo CD,
right? You can go through these steps,
and you can enable it.

Let's do this. First, we need to create
an application in Okta UI. I have created a trial version of Okta.

If you see here, it's valid for 27 days. Within this trial version, we are going to create an application

and assign the application
with certain users who will be able to log in
to our Argo CD server. First things first,

we have to add people
and associate with them with groups. You can manually create a set of people. You can add persons

and you can basically use any dummy data
or mock data for the demo purpose. I just have two users, Alice and John.



**is ma sir y hi bta rhy hn k argocd server ko login krny k lye users/group ki management 3rd party tools sa b ker sakhty hn**

different 3rd party tool avaialble hn is k lye but sir na **okta** k through configuration ker k dekhya ha...

argocd ki official website k follow ker k ap isko easily ker sakhty hn..


sir na phily okta ka free verision install kya.. us ma kuch user or groups create kye... phir okta ma application section ma ja kr configuration ki, matlab okta ko argocd k sath configure kerny ka steps kye. tky okta ma created users argocd server ko access ker sakhy.. or SLAM certificate ko argocd k configmap ma add kya...

verfication k lye argocd k home page ko refresh kya tu okta login agya...

ab okta ma created users argocd ko access ker sakhy hn...

y step ap argocd ki official documentation ko follow ker ka ker sakhty hn..

bari team k lye y authentication method sahi ha...

------------------------------------------------------------------------------------------------------
Bitnami Sealed Secrets with argocd(y wohi kube sealed secret ha jo hum na kodekloud sa study kya tha)
------------------------------------------------------------------------------------------------------

kubectl create secret generic mysql-password --from-literal=password=<> --dry-run=client -o yaml > mysql-password.yaml


argocd app create sealed-secrets --repo https://bitnami-labs.github.io/sealed-secrets --helm-chart sealed-secrets --revision 2.2.0 --dest-namespace kube-system --dest-server https://1.2.3.4

you can also install operator with **helm** directly...

client side utility called kube sealed
======================================

you can download and install with this.

wget https://github.com/bitnami-labs/sealed-secrets/release3/download/v.0.18.0/kubeseal-0.18.0-linux-amd64.tar.gz -O kubeseal && sudo install -m 755 kubeseal /usr/local/bin/kubeseal

Command to create kubesealed
----------------------------

kubeseal -o yaml --scope cluster-wide --cert sealedSecret.crt < k8-secret.yaml> sealed-secret.yaml

it will convert k8's secret to sealed secrets...

agr kubeseal cluster ma operator sa certificate or public key ni lye rha hoga tu hum isko khud --cert sa pass kry gye...

or this you can also pass this encrypted sealed.yaml on github.

**ap cluster ma deployment ko argocd sa deploy kr sakhty hn y hum pta ha.. or argocd github k sath sync hota ha or waha per manifest ma hoi changes ko sync krta ha or deploy krta ha cluster ma**

**ap is k lye repo create krty hn argocd ma, repo ko **HTTP,SSH,GITHUBAPP** or other option ko select ker k create kya ja sakhta **

most commonly we uses **connection repo using HTTP** is ma ap apny github ki repo jis ma paki manifest pari hn bta sakhty hn... so argocd wha sa manifest ki changes sync kry ga or cluster ma deploy kry ga...

**ap repo ma URL option ko use krty hn github k link deny k lye tky argocd github sa changes get kry... or ap repo ma URL option ma public url b dye sakhty hn** like helm k url.. so argocd public internet sa info lye ker cluster ma resources deploy kry... jesy hum helm repo ko cluster ma directory helm k through add krty hn..

for this we need to select **type** in repo... **type (git or helm)** hn, helm resource deployment k lye helm or git sa sync kry k lye git select kry gye.. and you can select multiple project 


**then hum argocd ma applicaitons create krty waqt is repo ko use kry gye**

Steps for setting up applicaiton
---------------------------------

1- Name:   applicaiton name like sealed secrets
2- Project Name: default or other create project
3- SYNC POLICY: Manual or automatic
4- Source: Repository url(ap yha argocd sa create repo jis ma github ka url(mean argo isko use kr k manifest github sa lye ga) as source set ha wo b dye sakhty hn) or manually url github k b set kernsakhty hn..

also give chart in case of helm type ****

5- Destination: give cluster url here 

you can also give namespace here.. 

remainings option left same and click on create 

or manual sync k same ma apko manually sync per click krna hoga.. sync start krny k lye...

**Healthy status** mean everything is running perfectly..

**note: sir na cluster operator, argocd k through deploy krya ha.. ap argocd sa b or manully cluster sa dono tarha sa deploy kr sakhty hn..**


**ab sir na kubeseal cli ko linux system ma kubeseal cli ki gitrepo ko follow krty howy kya ha..**

**phir sir na kubeseal cli ki cluster ka operator k sath communication set up ki**


**how do we get cert manually from cluster operator installed in cluster**
--------------------

ab hum cluster ma operator sa manually certificate ko lye gye or isko kubeseal ko --cert use krty howy dye gye... jis sa kubeseal or cluster operator ki communication stablish hojye gi..

use this to get sealed secrets from cluster...

    kubectl get secrets -n kube-system

    kubectl get secrets <give sealed secret name> -n kube-system -o yaml

    and get **tls.crt**

    kubectl get secrets <give sealed secret name> -n kube-system -o json | jq .data'."tls.crt"'

    or getting tls.crt out of the double "" use this.. and also decode into base64

    kubectl get secrets <give sealed secret name> -n kube-system -o json | jq .data'."tls.crt"' -r | base64 -d 

    and save it to the file..

    kubectl get secrets <give sealed secret name> -n kube-system -o json | jq .data'."tls.crt"' -r | base64 -d > sealed-secret.crt


Now passing it to kubeseal cli using --cert
------------------

    kubeseal -o yaml --cert sealed-secret.crt --scope cluster-wide < pass k8 .yaml secret-temple here for conversion> <outputsealedfile.yaml>  ---> it will encrypt the secret 

    here --scope is for mentioning the namespace where this resource going to installed.. for cluster-wide mean any where..

    ab sir bty hn.. aik issue open ha argocd ka github k sath jis ki waja sa is parameter sa error. arha ha 

    kubeseal -o yaml --cert sealed-secret.crt --scope cluster-wide < pass k8 .yaml secret-temple here for conversion> <outputsealedfile.yaml>  ---> it will encrypt the secret 

**so by replacing --cert with --scope option it works fine**

    kubeseal -o yaml --scope cluster-wide --cert sealed-secret.crt  < pass k8 .yaml secret-temple here for conversion> <outputsealedfile.yaml>  ---> it will encrypt the secret 

**then kubectl dry-run wali command ko use krty howy secret k template create kya**

or phir kubeseal ki command ko use krty howy is secret ko encrypt kr dya...

ab is encrpyted template ko ap github ma safely rakh sakhty hn.. or cluste ma kubectl apply -f command sa iska object create ker sakhty hn...

cluster ma operator isko decrypt ker dye ga.. or y simple secret k tarha behave kry ga,

ArgoCD will fetch secrets from hashicorp vault
-----------------

Let's have a look at how Argo CD Vault Plugin 
will fetch secrets from HashiCorp vault. Argo CD Vault Plugin
is a custom Argo CD plugin that can inject secrets 

into Kubernetes resources after retrieving them from various
secret management technologies such as HashiCorp vault,
IBM Cloud Secrets Manager,

AWS secret manager, and et cetera. HashiCorp vault is a secret management tool
that was created specifically to control access to sensitive credentials
in a public environment.

We will be using HashiCorp vault
to securely store the secrets and Argo CD plugin will retrieve 
and inject them in Kubernetes YAML files.

**Storing secrets in Vault is possible by using secret engines. A secret engine is a vault component which stores, generates, or encrypts secrets.**

**In this example, 
we enable Key/Value secrets engine, which simply stores and reads data. The /path or the -path is where we are going to put all our key-value pair secrets.**

command to enable the secret engine:
-----------------------------
**like: vault secrets enable -path=crds kv-v2**   -path or /path is for mentioning the path where you are going to store secrets..

The KV put command  writes the data to a given path. Here, **we write a key MYSQL-PASSWORD with value 1234567 to crds/mysql path.**

**like: vault kv put crds/mysql MYSQL-PASSWORD=1234567

**In Vault, we are storing the password in plain text, and hence within the Kubernetes secret YAML manifest, we use string data field.**

**The string data field is used because it accepts plain strings as values. If we use data field, then the values for all keys should be base 64 encoded strings.**

like:
mysql-secret.yaml
-----------------
apiVersion: v1
kind:   Secret
metadata:   
    name:   mysql-secret
    annotations:
        avp.kubernetes.io/path: "crds/data/mysql"  ---->>is annotation ki waja sa kubernetes vault k is path "crds/data/ mysql" sa value lye ga..   or nichy hum **stringData feild use ker rhy hn** jo k y kerti ha... **The string data field is used because it accepts plain strings as values. If we use data field, then the values for all keys should be base 64 encoded strings.**
type: Opaque
stringData:
    password: <MYSQL-PASSWORD>   ---> y same wohi **key** ha jo hum na hashicorp vault ma secret create kerty howy di thi... kubernetes is key ko use krty howy vault sa is key k against secret lye aye ga... remember key ko hum na kubernetes manifest ma <> greater or lesser sign k under likhna ha..

**Within the password field, we use the actual key, which is mentioned in the HashiCorp vault. It has to be mentioned within the "greater than" and "less than" template markers, and we can download the Argo CD Vault Plugin binary and move it to our user local bin directory.**

**like: curl -Lo argocd-vault-plugin https://github.com/argoproj-labs/argocd-vault-plugin/releases/download/v1.10.0/argocd-vault-plugin_v1.10.0_linux_amd64**

chmod +x argocd-vault-plugin && mv argocd-vault-plugin /usr/local/bins

Argo CD Vault Plugin uses a generate command, which will generate the manifest from templates with vault values. The plugin uses the **avp.kubernetes.io/path** annotation


to look for MYSQL-PASSWORD key value within the crds/data/mysql 
path of Vault, **but before that, the plugin needs to connect 
and authenticate with Vault.**

**We can use the -c option, which is used to refer a file containing the vault configuration data either in JSON, YAML, or environment file format.**

**like: argocd-vault-plugin generate -c vault.env - < mysql-secret.yaml**

vault.env --> file
VAULT_ADDR=http://vault:8200  --> vault address 
VAULT_TOKEN= <token-paste-here>
AVP_TYPE=vault
AVP_AUTH_TYPE=token          

**argocd k vault plugin  vault.env ma mention information ko use kerty howy vault ka sath authentication kery ga or kuberntes manifest ma annotation path sa secret lye gi or stringdata ma rhy gi...  **

This configuration has vault address, 
authentication type, vault type, and the vault token. Here, we are using
the vault token authentication.

It also supports other authentication modes
such as app roll, GitHub, Kubernetes authentication 
are also supported. Once the plugin gets authenticated,
it reads the path from the annotation,

which is the secret from Vault 
and injects it into the placeholder. This is how the Argo CD Vault Plugin 
works manually.

In the next video, we'll see 
how to use this Argo CD Vault Plugin within the Argo CD applications. Thank you.

let understand how argo vault plugin can intregrate with ArgoCD
---------------------------------

example manifest
----------------

containers:
    - name: argocd-repo-server
      volumeMounts:
        -   name: custom-tools
            mountsPath: /usr/localbin/argocd-vault-plugin           --> main argocd container
volumes:
    -   name: custom-tools
        emptyDir: {}
initContainers:                       ----> argocd vault plugin running as init container , will go to main container with pod local emptyDir volume. for vault authentication, create kubernets secret having vault creds information and refer it to main argocd continare..
    -   name: download-tools
        image: 'alphine:3.8'
        command: [-sh, -c]
        args:
            - wget -O argocd-vault-plugin
            https://github.com/../argocd-vault-plugin/v1.10.1 && chmod +x argocd-vault-plugin && mv argocd-vault-plugin /custom-tools/
        volumeMounts"
        -   mountPath: /custom-tools
            name: custom-tools


argocd configmap.. 
-----------------

data:
    configManagementPlugins: |-
        - name: argocd-vault-plugin
          generate:
            command: ["argocd-vault-plugin"]
            args: ["generate", "./"]

once the plugin been available, next step isto register the plugin with argocd. and next step is to configure the point and authenticate with vault..


- One way is with kubernetes secret. and refer the secret within the repo server container.
- other is to embed the vault config directly in each and every argocd application configuration. This can be done through argocd UI and CLI. 

once done use the **argocd plugin generate command** it will fetch secrets from vault. and update the manifest.

**flow---> argocd will first get kubernetes secret manifest from github, and because we have already set argocd operator in kubernets cluster running as pod container havig vault plugin running as init container and vault authntication refer as secert to main container  as discuss above** so argocd take this manifest and use command like this **argocd-vault-plugin generate -c vault.env - < mysql-secret.yaml** mean use generate command and authenticate vault and fetch and place secrets in given manifest..

and then apply the secret manifest...

demo(agrocd vault plugin with cli)
--------

**In this demo, we are going to see, how the argocd vault plugin can connect with vault and fetch the secrets...**

sir na vault ko helm k through install kya ha cluster... but by using argocd

remember jo installation manually kubernets ma kerty hn, chahye wo kubectl sa ho y helm k through wohi ap argo k through b ker sakhty hn...

- once vault installation done on cluster. access vault from outside the cluster by changing service from cluster-ip to loadbalancer. 

**- after that access it from browser and initailized the vault and save the initial root token, key1 and key2. so you can use it somewhere else also, like using during vault authentication from other services.** 

**- now give the same key1 and key2 during the vault unsealed step...**

**- now select the sign method name "token" and give "vault initial root token" here.**

by default you have one secret engine enabled in vault. You can also create other one in vault.. so for this you can click on **Enable new engine** > select KV(mean key values) in it > give path(where you credentail store) name like(credentails) and leave defaults values.. 

now its time to store secrets within the credential path in vault... during creating secret you can create multiple path in credentail for saving different secrets values, like secret for app , for database and etc... 

now give secrets name an values under **secret data** while creating secrets in vault in credentail path by specfic secret path in credentails(like for app)... 


**---> ab agr hum simple kubernetes ko use kerty howy secret vault sa lena chahty hn tu humy apni kubernetes secret ma below annotations ko use kerna ha.** 

annotations:
         vault.hashicorp.com/agent-inject: 'true'
         vault.hashicorp.com/role: 'internal-app'       ---> service account name(# Vault role with necessary permissions)
         vault.hashicorp.com/agent-inject-secret-database-config.txt: 'internal/data/database/config'  --> # Path in Vault for secret..


**arg ap agrocd k through secret vault sa get krna chahty hn tu add below annation on kubernetes secrets**     

annotations:
        avp.kubernetes.io/path: "crds/data/mysql" --->  avp means argocd vault plugin( this is "crds/data/mysqlPath" in Vault for secret, remember to append /data in path here..)..
type: Opaque
stringData:
    password: <MYSQL-PASSWORD>  --> vault secret key...


now, secret manifest

mysql-secret.yaml
-----------------
apiVersion: v1
kind:   Secret
metadata:   
    name:   mysql-secret
    annotations:
        avp.kubernetes.io/path: "crds/data/mysql"  ---->>is annotation ki waja sa kubernetes vault k is path "crds/data/mysql" sa value lye ga..   or nichy hum **stringData feild use ker rhy hn** jo k y kerti ha... **The string data field is used because it accepts plain strings as values. If we use data field, then the values for all keys should be base 64 encoded strings.**
type: Opaque
stringData:
    password: <MYSQL-PASSWORD>   ---> y same wohi **key** ha jo hum na hashicorp vault ma secret create kerty howy di thi... kubernetes is key ko use krty howy vault sa is key k against secret lye aye ga... remember key ko hum na kubernetes manifest ma <> greater or lesser sign k under likhna ha..

**ab sir na argocd vault k plugin ko install kya using "wget". isky bd vault ki generate command ko use kya. jis ma -c flage ma vault.env ma vault ki authentication information ki jis ma** 

- vault addr: vault address
- vault token:  vault initial root token
- avp type: vault
- avp host type: token

command:
-------

    argocd-vault-plugin generate -c vault.env - < mysql-secret.yaml   
    
    ---> plugin vault.env ko use krty howy vault ko authenticate kry ga, phir secret manifest(mysql-secret.yaml) ma annotation ma jo path ha, is same path sa vault sa wo secret fetch/place kry ga by seeing stringdata key name.. 

This is for the agrocd vault plugin with cli way....

demo(agrocd vault plugin with argocd)
------

In this demo, we are going to install vault plugin within argocd.


let understand how argo vault plugin can intregrate with ArgoCD
---------------------------------

example manifest
----------------

containers:
    - name: argocd-repo-server
      volumeMounts:
        -   name: custom-tools
            mountsPath: /usr/localbin/argocd-vault-plugin           --> main argocd container
volumes:
    -   name: custom-tools
        emptyDir: {}
initContainers:                       ----> argocd vault plugin running as init container , will go to main container with pod local emptyDir volume. for vault authentication, create kubernets secret having vault creds information and refer it to main argocd continare..
    -   name: download-tools
        image: 'alphine:3.8'
        command: [-sh, -c]
        args:
            - wget -O argocd-vault-plugin
            https://github.com/../argocd-vault-plugin/v1.10.1 && chmod +x argocd-vault-plugin && mv argocd-vault-plugin /custom-tools/
        volumeMounts"
        -   mountPath: /custom-tools
            name: custom-tools


argocd configmap.. 
-----------------

data:
    configManagementPlugins: |-
        - name: argocd-vault-plugin
          generate:
            command: ["argocd-vault-plugin"]
            args: ["generate", "./"]

once the plugin been available, next step isto register the plugin with argocd. and next step is to configure the point and authenticate with vault..


- One way is with kubernetes secret. and refer the secret within the repo server container.
- other is to embed the vault config directly in each and every argocd application configuration. This can be done through argocd UI and CLI. 

once done use the **argocd plugin generate command** it will fetch secrets from vault. and update the manifest.

**flow---> argocd will first get kubernetes secret manifest from github, and because we have already set argocd operator in kubernets cluster running as pod container havig vault plugin running as init container and vault authntication refer as secert to main container  as discuss above** so argocd take this manifest and use command like this **argocd-vault-plugin generate -c vault.env - < mysql-secret.yaml** mean use generate command and authenticate vault and fetch and place secrets in given manifest..

and then apply the secret manifest...

**follow the documenatation** , 

remerber ap vault ki authentication jo secret create ker k argocd operator main application ko refer ker k krwaty thy wo kam ap argocd ki GUI sa argocd plugin section sa vault ki authention info dye kr b kr sakhty hn. argocd plugin install krny sa plugin option GUI ma ajti ha..

vault authenticatiob info
-------------------------

- vault addr: vault address
- vault token:  vault initial root token
- avp type: vault
- avp host type: token


ArgoCD Metrics & Monitoring
---------------------------

Let's understand how ArgoCD metrics can be visualized
through Prometheus and Grafana. Argo CD exposes different sets
of Prometheus metrics. In this slide, we will understand
how Argo CD

and Prometheus can be configured
to scrape metrics. In this example,
we make use of the Prometheus operator. The operator uses
Kubernetes custom resources

to simplify the deployment
and configuration of Prometheus, AlertManager Grafana,
and other related monitoring components. We can execute inside
the config hyphen reloader container

of the Prometheus port
and read the Prometheus environment YAML file
to see the scrap interval, rules file, and scrape configuration. By default, it is going to scrape metrics

from Kubernetes components
such as Cube, APS Server, and others. How do we configure Prometheus
to scrape ArgoCD metrics? The Prometheus operator uses service
or part monitoring CRD

to perform auto-discovery
and auto-configuration of scraping targets. For service monitoring,
the following steps are required. In the first step,
we need to have actual services,

which expose metrics
at a defined endpoint port and identified with an appropriate label. Argo CD, out of the box, exposes several services
exposing Prometheus metrics.

We have a service for repo server,
ArgoCD metrics, service server metrics,
and application site controller metrics. This is how a sample service looks like.

In the second step,
we need to have service monitor, which is a custom resource to discover
the services based on matching labels.

Argo CD also provides
sample service monitor manifest, which can be applied
on the Kubernetes server. In the third step,
the operator uses the Prometheus CRD

to match the service monitors
based on labels and generates the configuration
for Prometheus. In the fourth step,
the Prometheus operator calls the config loader component
to automatically update

the configuration YAML
with Argo CD scraping target details. This is how ArgoCD metrics
are scraped by Prometheus and by configuring Grafana,

we can visualize these metrics using a grafana dashboard.


ArgoCD Metrics & Monitoring-2
-----------------------------

Lets have a look at how Argocd metrics can be used by prometheus to raise alerts using alerts manager. AlertManager handles alerts sent

by client applications such as the Prometheus server. In this session, we will understand how to raise alerts based on ArgoCD metrics

within the Prometheus server. In the previous session, we have seen how to scrape ArgoCD metrics with Prometheus. In this slide,

we make use of those metrics to create rules and raise alerts. As part of the Prometheus operator, we also get Alertmanager conflicts

and Prometheus rules CRD. Prometheus rules ease a custom resource that defines recording and alerting of rules for a Prometheus instance.

In this example, we create a Prometheus rule with one alerting rule. Each rule has a name, trigger, duration, annotation, and label.

For example, the alert name is 'Argo app out of sync'. It will be triggered when  the application synchronization status

is out of sync. It's going to be there for a duration of five minutes, and it's going to add a warning level severity

to the triggered alert. Finally, it also uses annotation to define a summary. Once the Prometheus rule is created, the Prometheus operator uses

the Prometheus rule CRD and generates the configuration for Prometheus. Prometheus operator calls the config reloader component to automatically update the rules file.

The alerting rules added as part of the rules file should be available when we go to the rules tab

in the prometheus UI. An alert should be triggered and visible in the alertmanager UI if any ArgoCD applications sync status is out of sync. Thank you..

Monitoring through Prometheus + Grafana
-------------------------------

In this demo, we are going to use prometheus and grafana to visualize the argocd metrics, within the argocd metrics documentation,

it says that Argo CD
exposes different sets of Prometheus metrics per server. These are the different Prometheus metrics which are generated
by the application controller, the server,

and the repo servers,
so you have a lot of options over here. We can quickly check
this within the cluster. I can do a quick argocd get svc.

If I do a quick curl on one of,
let's say, the Argo CD server-- If I do a server
like 10.98.110.228:80/metrics--

-----> 

Is ma sir bta rhy hn k kesy hum argocd ka metrics ko promethoues sa collect krwa ker grafana per show krwa sakhty hn..

Step:
----

helm repo add prometheus-community https://prometheus-community.github.io/helm-charts

helm repo update

helm install [RELEASE_NAME] prometheus-community/prometheus


sir ma phily helm k through cluster ma promethous to install kya.. phir service ko change ker k browser sa promethouse ko access kya.. phir **targets** ma jakr dekha k promethous kin kin metrics ko abi target ker rha ha... abi promethouse sirf apny hi metrics mostly target ker rha hoga,,,

- phir sir na kha k ab hum na promethoues k target ma argocd ka metrics deny hn... jis k ly sir na argocd ki documentation dekhi jis ma argocd k lye promenthouse operators define thye... belows are the links... is ma sir na kha ap na link ma dye same templetes ko use krna ha but promethous operator k templates ma release name ap na wo use krna ha jo ap helm chart sa promethouse to cluster ma install krty howy use kya tha..

https://argo-cd.readthedocs.io/en/stable/operator-manual/metrics/

https://argo-cd.readthedocs.io/en/stable/operator-manual/metrics/#prometheus-operator

IN most of the scenarios, 
-------------------------

we will be joining 2 different projects where the promethous stacks already exists, if you are given a task for creating service monitors.You need to know this release name. How do we get this release name.

there are multiple way.. one of is given below...

    kubectl get prometheuses.monitoring.coreos.com -o yaml -n monitoring | grep -i servicemonitorselector -A5

    it will give you the release name, you can use it for your servicemonitors templatess.. like below 

    https://argo-cd.readthedocs.io/en/stable/operator-manual/metrics/#prometheus-operator

    so that the prometheus operator can read those services or the service monitores..

---> now again refresh the promethouse target page and you could see the more argocd targets..

After collecting the metrics with promethouse the next part is how to visualize these metrics in grafana...
------------------------------------------------------------------------------------------------

kuo k hum na promethoues operator kya ha cluster ma, y apny sath grafana instance ko b lye ker aya ha mean iska deployment or service b bani ha. ...

see

    kubectl get svc -n monitoring ---> see the grafana service and edit the service to change it to nodeport or loadbalancer...





