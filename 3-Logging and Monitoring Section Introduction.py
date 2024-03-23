is ma wo btaty hn k hum nodes metric or pod metrics like cpu , memory , disk space, network k metric ko collect , store or visualized(monitor)ker k nodes or podes ki health ko check ekr sakhty hn..kubernetes k ps iska full pack solution ni ha, but open source tool. like

- metricserver  ---> it collect node and pod metrics , aggregate them and store them in-memory. y in-momery monitoring solution and does not store metric of the disk, so as result you can not see historical performance of data... mean old data.. because memory ko erase hojati ha.. disk ma data log time tk store rhta ha.. older k lye apko advance solution ko use kerna hoga.
- promethoues
- elk
- datadog
- dynatrace


pods k metric nodes sa kesy collect hoty hn

-------------------------------------------

y kam node ma mojod kubernetes k component "kubelet" ka subcomponent "cAdvisor" ker rha hota ha.. cAdvisor is responsible for retriving proformance component from pod and exposing it to kubeapi server to make the metric available for metric server... and metric server in metrics ko in-momery ma save kerta ha... 

-kubeadm sa bny cluster ma metric server ap is command sa enable kerty hn..

    minikube addons enable metrics-server

for other

    git clone https://github.com/kubernetes-incubator/metrics-server.git

    kubectl create -f deploy/1.8//

once done, give some time to metric server to collect data.. 

you can see node metric with command..........

    kubectl top node

for pod metric

       kubectl top pods

Managing Application logs
-------------------------

in this we will discuss various logging mechanisem..

docker container create kerty time without using "-d" sa container k logs terminal per bn rhy hoty thy.. with using -d logs background ma bnty hn.. or docker ma logs dekhny k lye "docker logs container-id" dena hoti ha..

same you can see the application logs in kubernetes with "kubectl logs -f pod/podname" -f is for the realtime logs on screen..

y logs pod ma chal rhy contianer k hoty hn........ and we know that k aik pod ma multiple containers hosakhty hn... is case ma command ko kesy pta chaly ga k us na pod ma kis container k logs dekhny hn... agr aik container pod ma chal rha ha tu then you can simply use this command "kubectl logs -f pod/podname" . but agr pod ma multiple container chal rhy hn tu apko command ma pod k under jis container k logs dekhyny hn uska name b btana hoga.. "kubectl logs -f pod/podname container-name"  other wise logs show ni kery ga..