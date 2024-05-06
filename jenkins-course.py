jenkins buhat simple ha.. is k through ap apni jobs ko automate ker sakhty hn...

what you gonna do... 

- you need to simply perform action/commands on local terminal first
- jb apko apki desire output k according result milna start hojye tu apko. 
- then apna commands ko jenkinsfile ma "sh" use kerty howy dena ha... y apky process ko automate ker deta ha..

jenkins background
------------------
jenkins ma jitni b jobs ap create ekrty hn, background ma in jobs k against folder create hota ha. isi folder ma commands chal rhi hoti ha, agr ap na kuch create kerna ha tu wo b yha hi horha hota ha... or agr ap na koi sa kuch "checkout kerwana ha mean files pull kerwani ha tu wo b yha per hi pull hokr arhi hoti hn" folder location "/var/lib/jenkins/workspace/"targeted folder(y jenkins job k name sa hoga)"

jenkins searchbar
------------------
- ab "search bar" ma "job search" kerny sa ap sedha us job per chaly jye gye... 

or agr "build no" ba ap search bar ma job k sath dye gye tu ap sedha us job ki build per chaly jye gye.. like "demo-first:13" is tarha sa ap "demo-first" jo ki "13" build per chaly jye gye.. 

or agr ma job ki console output per sedha search bar sa jana ha tu. you can write this "demo-first:13 console"

or agr job ki last failed build per jana ha tu ap asy ja sakhty hn "demo-first last failded build"

jenkins configuration
---------------------

jenkins sa related all adminstrative task ap "manage jenkins" ma perform ker rhy hoty hn.

Sections
---------

1- System configuration

    - Configure System  --- is ma hota y ha k ap jenkins ma jitny b plugins install kro gye. unki configuration ma koi changes kerni ha tu wo ap yha sa kr rhy hogye.
    - Global Tool configuration  --- is ma hota y ha k agr apna. let say ka koi b plugin like maven install kya ha. iska path(location) kya ha. wo maven tool kha rakha ha. is sa related jo b kam krna hoga wo yha kerna ha. 
    - Manage plugin   --- ap na jenkins ma koi b plug add , remove y delete kerna ha tu wo ap yha sa kry gay..
    - Manage Node and cloud ---- yha sa ap jenkins ki worker nodes ko manage ker sakhty hn..    

2- Security

    -   Configure Global Security   --- yha per btaty hn k kisi b new users ko jenkins signup ka permission dena ha y ni dena. y phir kisi na URL dala tu directly jenkins access hojye. 
    -   Manage Credentials   ----  yha per ap Credentials create ker sakhty hn or un Credentials ko ap jobs ma use ker sakhty hn.
    -   Manage user  ---- is ma ap na koi b user "delete" kerna ho, "create" kerna ho, wo ap sa ker sakhty hn. 

baki zayada tar yha jenkins information sa related cheezy hn.


Configure System
----------------

ab "manage jenkins" ma sab sa phily jo option ati ha wo configure system ha.(jenkins ma jitny b plugins install kro gye. unki configuration ma koi changes kerni ha tu wo ap yha sa kr rhy hogye.)

ap search bar ma "configure" enter ker k sedha configuration section ma askhty hn.

under configure system ma sab sa phily:

    "system message" -- yha per ap jo b message likhy gye wo apki jobs dashboard k upper show horha hoga. is tarha sa admistrator jenkins user ko jenkins k hawly sa information dye sakhta ha.
    "no of executor"  -- mean aik sath kitni job ap k jenkins server per run hosakhti hn.. (is k lye apko system server ki apni capacity ko dekh ker set kerna hoga.) capacity sa zayada job run ker gye tu jobs chuck hojye gi,
    "labels"   -- we will learn it on further vedios.

    ab sir kha rhy hn k jitny b section ha un k sath read me option ha, ap sab ki details waha sa read ker sakhty hn.

Install First Plugin ( How to Change Jenkins Theme)
---------------------------------------------------

sir kha rhy hn "plugin" aik facility ki tarha ha, mean let say k apka aik mobile ha or ap na us per whatsapp k through messages kerny hn tu ap whatsapp ko install ekrnty hn or is k through message kerty hn. 

same isi tarha sa jis b tarha k apka project ha ap na us sa related plugin ko jenkins ma install kerna ha or is plugin ki facility ko use k apny project ma use kerna ha.

ab "manage plugin" ma apko below section mily gye:
    -   update
    -   available   --- it will give you the list of available plugins
    -   installed   --- it will give you the list of already install plugins in jenkins
    -   advanced

jenkins ki plugin sa related website ha "plugins.jenkins.io". ab let say k ap na jenkins k theme change kerna ha. so apko is k lye theme ki facility jenkins server ma kerni hogi. ap jenkins ki plugin website per jaty theme brows kerty hn or jo b results aty hn unky "name" ko jenkins ma > manage plugin > available ma search kerty hn. apko wo plugin mil jata ha ap isko apny jenkins server ma insatll ker lety hn.(select plugin .. then click on install without restart. then client on restart jenkis) is tarha sa plugin jenkins ma install hojye ga.

ab sir khty hn k ap na plugin ko jenkins ma install tu ker lya but iski facility ko jenkins server ma add kerny k lye apko "configure system" ma is plugin ko configure kerna hoga.    
or tool ki configuration k lye ap "global tool configuration" section ma jaty hn.

so plugins k effect ko jenkins server ma add kerny k lye apko "configure system" ma "theme" ko apko search kerna ha(because apna theme ka plugin install kya ha), because jesy hi plugins ko ap jenkins server ma add kerty ho, wasy hi "configure system" ma us sa related information ajati ha.. tu waha sa ap installed plugin ki configuration ker k iski facility ko jenkins ma add ker sakthy hn..

"jasye hi ap configure system ma configuration ker k save kro gye tu plugins sa related facility jenkins server ma add hojye gi..


how to uninstalled installed plugin
-----------------------------------

is k lye go to manage jenkins > manage plugins > installed(because ap plugin ko install ker chuky hn)> then select the plugin and select on uninstalled.


Create First User
-----------------

is k lye go to manage jenkins > manage user > create user 

then give information of user.... like

username, password, full-name, gmailaddress.

ab sir khty hn k jesy hi user create hoga ap is user ki detail apny new user ko share kery.. tky wo jenkins server ko login ker sakhy.. 

ab sir khty hn k hum dekhy gye k new user older user ki created jobs/configuration ma changes na ker sakht. y kam hum RBAC ki tarha kr rhy hogye..  

"y ap na kisi devopler ko jenkins ki access deni ha.. k wo sirf job ko build ker pye or kuch na kry...

is kam k lye apko manage jenkins ma koi section ni mily ga. but ap plugin k through y kam ker sakhty hn... 

for this go to "plugins.jenkins.io" > search "role base"  (y apko role base authorization strategy dyea ga ) > is name ko manage plugins ma under "available section" ma search ker k plugin ko jenkins ma install ker lye.

so ab y plugins apko "manage jenkins" ma ni dekhy ga.. or na hi "configure system" ma dekhy ga... Security sa related plugin apko "under security section> configure global security(yha per btaty hn k kisi b new users ko jenkins signup ka permission dena ha y ni dena. y phir kisi na URL dala tu directly jenkins access hojye.)"

so go to "configure global security" >under "authorization" >enable "role-based strategy" > apply and save..  save kerny k bd apko "manage jenkins ma "manage and access role" k option dekhy ga.

then go to manage and access role> yha per ap 
-   manage role -----sa role create ker sakthy ho
-   assign role -----sa role ko assign ker sakthy ho
-   role strategy macros  

so select "manage role", apna admin role ko touch ni krna because admin k ps sary rights hoty hn. 

you need to add "new role":

-   give role name(like developer) under "role to add" and then click on "add".. is tarha sa hum developer na k role ko create ker ker isko "read ki permission(y koi or permission according ko situation dye sakhty hn)"

-   then we need to go to "assign role section under manage and access role "  yha per humy "user or group to add" section ma user add kerna hoga jis ko permission deni ha. jesy hi user bn ker list hojye ga then hum is user ko apna developer role(having read permission) dye dye gye...

then jb b wo user login kery ga jenkins ko then wo assign permission k according hi jenkins ko use ker rha hoga.

"mean agr hum chahty hn k devopler sirf job ko build ker saky.. then hum "manage role" section ma "created developer role" k lye "job build" ko enable ker lye gye.. or y role user ko assign ker dye gye(assign role section ma)... ab user job ko sirf build ker sakhy ga.

manage role ma created roles per ap below mention permission set ker sakhty hn: 
--------------------------------------------------------------------------------

-   overall
-   Credentials
-   agent
-   job
-   run
-   veiw
-   SCM

Use of git plugin and clean workspace(delete workspace befor build starts).
--------------------------------------------------------------------------

ab free style ki pipeline create ker k jb sir na pipeline aik br execute kerny k bd again execute ki tu pipeline na error dya... because pipeline jo code github sa checkout ker k la rhi thi us name ki directory already jenkins workspace ma pipeline k name k bnye target folder ma mojood tha. mean same name ki directory targeted folder ma phily sa mojood thi... 

is k solution k lye apko "jenkins pipeline ki configure section" ma under "Build Enviroment" ka "delete workspace befor build starts" box ko enable kerna hoga.


Build triggers
------------------

ab sir btatye hn k jenkins pipeline configure kerty howy "build trigger" k option ata ha. is ma multiple options ko hum study kery gye k wo kya kerty hn

Trigger build remotely
---------------------

is ma hota y ha k let say ap na jenkins jobs ko remotely trigger krna ha. let sa "browser y local terminal" k through..

tu ap "trigger build remotely section" ma koi random "token" set kerty how... wo apko yhi per token deta ha... apna isko apny jenkins k url k sath browser ma use kerna ha... tu apki pipeline trigger hojye gi..

remember agr ap us browser per jis per jenkin login ha kro gye tu pipeline triggeer hojye gi.. agr coginito per kro gye tu wo jenkins login page pr lye jye ga.. 

or agr local terminal sa chalo gye tu wo "authentication mag rha hoga.."

solution:

is k lye apko "plugins.jenkins.io" sa "build authorization token root" name k plugin ka name ko copy krna ha or jenkins ma manage plugins k through plugin ko jenkins ma install krna ha. 

ab "plugins.jenkins.io" ma is plugin k bary ma btya hoga k y Kis traha k url k sath work kerta ha.. so apko jenkins URL k sath isi tarha ka url add kr k browser or local terminal sa run kery gye tu apki job remotly dono sa run hojye gi.

like:

browser:  http://jenkins.local:8080/buildByToken/build?job={job-name}\&token={set-token}    --->     http://jenkins.local:8080/buildByToken/build?job=demo-4th\&token=mysecrettoken

local terminal: curl http://jenkins.local:8080/buildByToken/build?job=demo-4th\&token=mysecrettoken

you will see the job will be running successfully..

Build after other projects are build
------------------------------------

is ma hota y ha k is section ma jis b job k name ap do gye wo job jb successfully run hogi tb sath hi y job b run hojye gi..

mean k ap is trha is job ko bta rhy ho k current job , is section ma mention job per depend kr rhi ha, jesy hi y mention job successfully run hogi tb sath hi y job b run hojye gi.. is traha sa hum parent job sa child job ko trigger krwa sakhty hn.

is use case ko ap kha use ker sakthy hn. let say k aik pipeline apna create ki ha job dockerhub sa image ko pull kr rhi ha. ab jesy hi y pipeline khtm hoti ha. other pipeline jis per y pipeline depend ker rhi thi. run hogi or apko asy configure kr sakthy hn k ya koi test case run kr rhi hogi.. is tarha sa ap multiple pipeline ko aik sath run ker sakthy hn.

"is ma multiple options hn jis ko ap apny use case k according use ker sakthy hn. like 

- trigger build is stable
- trigger build is unstable
- trigger even if the build is fails

agr kisi waja sa main job ko apko unsable kerna ha tu use "exit 10"

Build periodically
------------------------  ---> y hum tb use kerty hn jb hum chahty hn k hmri job aik specfic time per automatically run hojye.

Build periodically k section ma job dye gye schedule time k upper automatically run hojye gi.. is ko hum tb use krty hn jb hum chahty hn k hmri jb dye gye schedule time per khud hi run hojye... alike "cronjob or crontab"

for this you need to give schedule time: "00 03 * * *" mean hr zor job 3AM ko run hogi. hum koi b time job running k set ker sakhty hn..

poll SCM(source code manager)
-----------------------------

is section ko ap tab use krty hn jb ap chahty hn k dye gye time k according jenkins br br SCM Like github per code changes ko check kry agr usy koi changes milti ha tu wo pipeline trigger ker dye. 

like if you set time "02 00 * * *" mean ab jenkins br 2min k bd SCM ma changes ko check kry ga. or agr usko koi changes mily gi tu wo pipeline ko trigger ker dye ga..

Github hook trigger for GITScm polling 
--------------------------------------

is ma hota ya ha k devopler jesy hi SCM like github per new code changes push kerta ha, github jenkins ko btye k is repository ma new code push howa ha so jenkins is information k according pipeline ko trigger ker dye...


is k lye apko (webhook or jenkins ip)  through SCM github ko jenkins or jenkins ko github k btana hota ha..


Environment Variable
--------------------

but sa varibale hum jenkins ma apny use case k according khud dye rhy hoty hn. but kuch variable jenkins khud inject kerwa rha hota ha jin ko hum use ker sakhty hn. jo apko is path sa mily gye. "(jenkins-ipaddress:port/env-vars.html)" like in my case it would be "https://jenkins.dataimagineers.ai/env-vars.html/"

use it to print.....

sh 'echo "Build Id is ${BUILD_ID}"'
sh 'echo "Job name is ${JOB_NAME}"'


iska use case y ha ka ap na jenkins k through build bna ker agr koi artifact ma send kerni ha tu ap image k sath build id lga ker send ker sakthy hn.. tky repository ma older builds ka b record rhy...  

like in cheetay hum build bnany k bd us per 2 tag lgty hn... aik build id ka sath or dosra "latest" k sath... build id tag sa hum builds ka record rakh rhy hoty thy... or latest tag ko hum agye deployment ma use ker rhy hoty thy...

Global Environment Variable
---------------------------

we will see how to create a globle Enviroment variable. jo hr job k lye available rhy ga..

go to manage jenkin > configure system > in global properites select "Environmental variable" then under "list of variable" give "name and value" for global variable.. ab y global variable hr pipeline k lye available rhy gye..

use case let say apko aik variable asa chahye jo apna sab job ma define kerna ha. usko ap is tarha sa kr rhy hogye.. agr future ma hum na koi changes krni b ha tu hum is variable ma aik hi br changes kry gye jo k un sab pipeline jin ma y variable define hoga ma changes implement hojye gi...

Parameterized jobs in Jenkins
-------------------------------

is ma hum dekhy gye k agr kisi build ma specfic parameter user ka dena ha.

user base perameter agr kisi job k lye hn tu wo kesy define kery gye, "mean job run kerty time user specfic peremeter variable dye rha ha jo job use ma use hona ha.. 

"y user sa input job job k lye jani ha wo multiple format ma mil sakhti ha..."  like "string , boolean , choice b hosakhta ha

how to do this,

"go to job configuration > under "general" select "the project is parameterized"(yha per multiple option hogi like "string , boolean , choice parameterd)  select and then set the information accordingly.." like in "string" case  set "name and default value". and call "name variable" in your script..."

ab jb ap job build kery gye tu "apka default dena howa name b waha per ajye ga.." ap again next kery gye tu wo name apki job ma as variable pass worha hoga.. or is ma ko change ker k koi or name as variable pas ker sakhty hn

"parmetrized choice k case ma ap multiple option dye sakhty hn" like deployment , stage , production. or y apko build k time per show hogi or jis ko ap select ker k next kro gye wo as user variable job ma jye ga..

Parameterized job - part 2
--------------------------

same you can use.

-   password parameter    ----> build krty time ap password dye sakhty hn jo k apki job ma use hoga... ("go to job configuration > under "general" select "the project is parameterized">password> set password variable(jisko ap na job ma use krna ha), and set default password, use password variable in your job) ab jb ap job build kro gye tu ap password jo do gye wo apki job ma variable ki jaga use hoga...
-   multi-line string     ----> multiple line phily sa likh sakhty hn jo k apki job ma use hoga..
-   file parameter    --------> ("go to job configuration > under "general" select "the project is parameterized"> file option > set file path> default path> use file path variable in script(ab jb ap job run kro gye tu wo apko chose file path k option dye ga jis k through ap file ko upload kr sakhty hn job ma or is ma job content ha isko use ker sakhty hn like "cat" or other command ko use ker k)    


use case like java or nodejs k ap project bano tu apko saparate env file upload krni ho.. or ssh key file build k time apko upload kerni ho.. y phir apna kubernetes ki ".kubeconfig" file ko pipeline ma upload krna ho...

abort the build if it stuck
---------------------------

let sa ap na aik job create ki ha jo infinite loop tk chal rhi ha y buhat time leti ha  . or is ma apka aik "executor" occupy b kya howa ha... tu ap kesy job k lye "time set" kr sakthy hn k y job itny time tk chaly gi.. or agr us set time sa zayada time lgye ga tu job automatically abropt hojye gi..

so to do this  "go to job configuration> under build enviroment select "abort the build if it stuck"> set time(default time 3min k hota ha)"

mean agr default time ko lye ker chalo gye tu 3min sa agr koi job zayada time lye gi tu wo job automatically abropt hojye gi.


under this section "abort the build if it stuck". apky ps multiple option hoty hn ap select ker sakhty hn.

- abort  --- mean given set time k bd job abort hojye gi.
- faild  --- mean given set time k bd job fail hojye gi.


TimeStamp
---------

we will see how to add "timestamp" in jenkins pipeline... mean jesy jesy pipeline ki console ma commands execute hogi sath sath apko timestamp b nazar aye ga... 

so to do this  "go to job configuration> under build enviroment> select add timestamp to the console output.

Enable/Disable Job
------------------

we will see how to enable or disable project.  or uska kya use aye ga production enviroment ma...

so to do this "select the pipeline> select disable project option"   apka project disable hojye ga. or "build" ki option chaly jye gi.

for enable the project "click the same button to make it enable"

ap same kam pipeline ki configure sa b ker skahty hn. so "select pipeline> configure > under general select disable the porject. apka project diable hojye ga..


Build a Job Concurrent or Parallels
-----------------------------------

mean aik sath ap multiple job run ker sakhty hn... 

how to do this.. go to manage jenkins > configure system > add no of executor(mean jitni jobs ap aik sath run kerna chahty hn itny executor dye. "aik job k lye aik executor use hoga")

now go the pipeline > configure > under general select "execute concurrent build if neccessary"

is tarha sa multiple jobs aik sath run hosakhti hn..

Retry Count
-----------

is section ma ap jitna b no do gye. itni br jenkins retry kry ga action perform kerny k lye...

like let sa ap SCM sa code pull kerwa rhy ho... kisi issue ki waja sa code pull ni howa tu jenkins again try kery ga code pull kerny ki... as per retry count no...


throttle Build
--------------

is ma hum dekhy gye k ap aik job per kesy limit lga sakhty hn k "given set time ma job 3 sa zayada , y 4 sa zayada.. y kisi b set no sa zayada br run ni hosakhti"

like 1 mint ma job 3 br sa zayada run na ho... so 4 br k lye ap run kro  gye tu job run ni hogi... or wasy b aik job k lye default set time 20s k hota ha.. so 1mint ma 3 job sa zayada run b ni hosakhti.... is tarha sa ap apna use case set ker sakhty hn k given time ma kitni br sa zayada job run na ho.. utni bt k bd job fail hojye gi...


"to do this go to pipeline configuration> under general select throttle build> give on of job executor and time(mean given time ma itni job sa zayada run ni ho)


you can set limit in (min , sec , hours , day , week...)


use custom workspace
--------------------

In which we will learn. how to change workspace default location(var/lib/jenkins/workspace/targetfolder) to other custom workspace location in jenkins.

"to do this go to the jenkins pipeline configuration> under general select "Use custom workspace" option > and give custom workspace directory. > save..

apki sara data pipeline ka is directory ma clone hoga jb ap pipeline ko run kry gye or sari commands b isi directory ma execute hogi..

Change Display Name And Rename Job
----------------------------------

"to do this go to the jenkins pipeline configuration> under general write name in "display-name" section...

you can also change the jenkins project name. "go to the jenkins pipeline configuration>rename..


Block Build when Upstream/Downstream job is building
----------------------------------------------------

Upstream mean parent job.   
Downstream mean child job.

jo job dosari job ko trigger kry gi wo parent job ha... or jis job sa dosari job trigger hogi tu wo dosari job child job hogi.

ap dono ko aik sath jor sakhty hn jenkins configuration ma configuration ker k...

"to do this create parent pipeline and create child pipeline 

now 

"go to jenkins configuration of child pipeline> under build triggers select "build after other projects are build"> select parent pipeline..

ab ap parent pipeline ko trigger kry gye... jesy hi wo successfully execute hogi then child pipeline automatically trigger hojye gi or wo b run hojye gi....

ab jb apki parent pipeline chal rhi hogi or sath hi child pipeline b run ker skahty hn.... but agr ap asa ni krna chahty tu ap child pipeline ma check lga sakty hn k jb parent pipeline chal rhi ho tu child pipeline ko run b kry tu wo run na ho... y kam ap child pipeline ma "block build when upstream project(parent) is building" ko select ker k ker sakthy hn... 

or same for the parent 
---------------------
ap parent ma y check lga sakhty hn.. "block build when downstream project(child) is building"


General Discussion
------------------

is lecture ma sir na btya ha k jb ap fresh jenkins server ko without plugins k run kro gye tu apko buhat kam options mily gye play kerny k lye...

like: pipeline section ma apko sirf "freestyle" pipeline ka option hi mily ga... or freestyle ma apko buhat kam option mily gye...  mean jenkins without plugin kuch b ni ha... or plugins k sath y powerfull ha..

Create first Jenkins Pipeline using Build Pipeline
--------------------------------------------------

jave project
--------------

- have some java code..
- install maven to make it build... "sudo apt-get install maven"
- use "mvn test" command for "unit-test".. if you have any test case...  once done it will create "target folder" 
- now make build by using "mvn install". y command apky springboot project ki "jar y war" file create ker k "target folder" ma provide ker dye gi...

jaha apki springboot application ha waha y commands run hogi..

now deploy is on tomcat server, install tomcat server.. "sudo apt-get install tomcat9" default port for tomcat is 8080..(hum is warfile ki dockerfile k through image create ker k b container ma chala sakhty hn)

ap apni "war-file" ko commandline or GUI dono k through deploy ker sakhty hn...

DEPLOY warfile WITH COMMANDLINE
-----------------------------------

once tomcat9 installation done..

- "go to /var/lib/tomcat9/webapps
- copy springboot war file in webapp directory  "cp warfile ./"

ab apko isko browser sa access kerna ha... for this take ip-address and port with stringboot file name.. and access it from browser...

"like: ipaddress:port/stringbootwarfilename   jesy hi ap isko browser ma kro gye apki jave application access hojye gi..

DEPLOY warfile WITH GUI
-----------------------

Access tomcat server(ipaddress:port). it will give you the information k ap tomcat9 admin ko b install ker sakhty hn.

    "sudo apt-get install tomcat9-admin"

then click on "managerwebapp".  it will show the signup page. agr ap k pass username or password ni ha... ap koi b random username or password dye.. wo apko 401 unauthorized page per lye jye or khy ga k below command ko tomcat file location ma add kry..

<role rolename="manager-gui"/>
<user username="tomcat" password="anypassword" roles="manager-gui"/>

configurationfile location: "/etc/tomcat9/tomcat-users.xml"

"now restart the tomcat server: service tomcat9 restart

now signin again... ap successfully tomcat server ko access ker lo gye through GUI..

now go to  "WAR file to deploy" section. or apni warfile ko select kry or deploy ker dye.. 

agr apna tomcat server kisi instance ma create kya ha or local browser sa ap server ko access kr rhy ho tu. war file b apko instance sa local system ma lani hogi. then ap GUI page k through warfile ko local system sa get ker k deploy ker sakhty ho instance ma..

"GUI sa b warfile tomcat9 server ma /var/lib/tomcat9/webapp locate per hi jarhi hoti ha..

--- > plugin name "copy artifact". artifact ko aik server sa dosary server per move kerny k lye... once install this plugin go to the pipeiline where you need to get the artifact. "go to pipeline configuration> check option under general "permission to copy artifact". or other pipeline k name dye jin na artifact ko copy kerna ha is pipeline sa... is traha sa other pipelines ko is pipeline ka artifact copy krny ki permision mil jye gi..

ab ap us pipeline ki configuration ma jye jaha apna artifact copy kerwana ha.. and select "copy artifact from other project" or name use pipeline k use sa artifact copy kerna ha is pipeline ma...


jenkins master/slaves
----------------------

- jobs run k lye ap hamesha master node ko hi kho gye... master node agye work ko distribute kery ga worker-nodes ma...
- master nodes slave k status ko monitor kery ga k wo running ma b ha k ni...

how to add jenkins slave on master node..
-----------------------------------------

for this go to manage jenkins > manage nodes and cloud > new nodes > give node name(like linux) and click on permanent agent and then click on OK..

now configure agent in master node:
-----------------------------------

Name:  already given
Description: add discription accordingly
No of executor: set accordingly (2 , 3 ,4 ,or 5)
Remote root directory: /var/jenkins  --- y slave node ki root directory hogi... "you need to create this directory in jenkins slave"
label: set label
Usage: use this node as much as possible    -----> mean master slave node ko job run k lye jitna ho sakhy ga itna use kry ga..
Launch Method:  "launch agent via ssh" --- is tarha sa master node java k program jenkins slave ko ssh ki help sa remote machine ma launch ker dye ga..
HOST: give ip address of remote machine..
Credentials: remote machine ka SSH username or password mean credentials.. (username or password ap global credentials ma dal ker yha call kerwa sakhty hn) 
Host key verfication strategy: "Non verifying verfication strategy"
Available: "Keep this agent online as much as possible"

then save.. and launch agent..

ab sir na btya ha k jenkins master node, slave ka status b dekhta ha k on ha k ni..  abi apki master node slave node ko offline dye gi...

because master node ma jarfile ko slave ma launch tu ker dya but slave node ma "jave" ka package ni hony ki waja sa wo file execute hi ni hoi.. is lye master node slave ko offline dekha rha ha...

so you need to add jave package in slave node. tky master node ki jarfile slave node ma execute hojye..

  sudo apt-get install openjdk-8-jre-headless


"now you will see the agent launch successfully in logs.. also see k jenkins na remote k status ko b green ker dya ha.. or ap dekhy gye k ap na slave k lye jo executor btye hn wo master node k sath sath slave k lye b show horhy hogye..

Run job in slave
----------------

ab sir simple job create kerty hn or isko run kerty hn tu wo job slave node ma jaker run hoti ha... 

asa is lye hota ha because slave node ki configuration kerty time hum na btya tha.. "usage section ma use this node as much as possible".  is lye master node na is slave ko job run kerny k lye use kya...

but jenkins master node is job ko khud ko b schedule ker sakhta ha. "use this node as much as possible" mean wo jitna hoga use kery ga. agr ni hoga(mean slave busy hoga) tu wo khud ko b assign ker sakhta ha job ko. 

like sir na btya k let say ka apky ps aik slave ha or slave k ps 1 executor ha.. or 2 jobs run kerty hn aik sath.. master aik job ko slave ko assign ekr dye a or because slave busy ha tu dosrai job khud ko assign ker dye ga...


How jenkins master node can run specfic job tu specfic slave nodes
------------------------------------------------------------------

phily y hota tha k jenkins master node zayada sa zayada slave ko use kerta tha gr wo busy hota tha tu apny ap ko job assign kerta tha..  

hum y b ker sakhty hn k aik specfic job aik specfic slave per hi run ker rhi ho..

yam kam hum "labels" ko use ker k ker skahty hn...

"so apna kerna y ha ka master node ma slave ki configuration(manage jenkins > manage nodes and cloud ) ma label section ma aik label ko set kerna ha.. like "linux" would be your label for 1 slave node. ab apna jenkins master node ma us job per jana ha jisko ap specfically slave1 node ma chalna chaty hn.. 

"wha apko us job ki configuration ma under general > Restrict where the project can be run> label expression(give label here: "linux")

ab jb b y pipeline run hogi tu jenkins master node job ma lgye label ko slave profile k sath match kery ga or isko job ko specfically slave ma run kery ga...

ab apki job specfically isi slave per hi run horhi hogi..

job apki slave ma run ho but wo output job ki apky master node ma record ker k dekhy ga..


Create first Pipeline as code - Create first Jenkin
---------------------------------------------------

- Scriptive
- Declaravtive


pipeline {
    agent any
    stages {
        stage('Example') {
            steps { 
                echo 'Hello World'
            }
        }
    }
}

ab sir na btya ha k agr apka jenkins "windows OS" ma run ker rha ha tu apko, pipeline ma commands ko execute kerny k lye "bat" use kre ha. 

or agr linux ma run ker rha ha tu ap "sh" use kro gye

like for window:
----------------

pipeline {
    agent any
    stages {
        stage('Example') {
            steps { 
               bat "echo 'Hello World'"
            }
        }
    }
}

for linux
---------

pipeline {
    agent any
    stages {
        stage('Example') {
            steps { 
              
                sh "echo 'Hello World'"
            }
        }
    }
}


for mulitple use this(''' '''):   after using this you do not need to add "sh" on every command    
---------------------

pipeline {
    agent any
    stages {
        stage('Example') {
            steps { 
                sh '''
                ls
                pwd
                mkdir

                '''
            }
        }
    }
}


calling enviromental variable:
------------------------------


pipeline {
    agent any
    stages {
        stage('Example') {
            steps { 
                sh "echo  ${BUILD_ID}"     ---> Kuch eniviromental variable jenkins k ps build in hoty hn jo hum apni pipeline ma use ker sakhty hn... baki or enviroment variable hum khud b add ker sakthy hn, apni requirement k according jo hmri pori ki pori pipeline ma available rhy gye.. 
            }
        }
    }
}


adding own eniviromental variables that will be available for whole pipeline:
-----------------------------------------------------------------------------


pipeline {
    agent any
    environment {
      name = 'hassan'
      email = 'muhammadhassanb122@gmail.com'        ---> is tarha sa enviromental variable sari pipeline k lye available rhy gye..
      }


    stages {
        stage('Example') {
            steps { 
                sh 'echo "${name}"'
            }
        }

        stage('email') {
            steps { 
                sh 'echo "${email}"'
            }
        }
    }
}


ab ap chahty hn k enviromental variable whole pipeline k lye ni bikly aik stage tk limit rhy
--------------------------------------------------------------------------------------------

how to do this:

ab ap chahty hn k enviromental variable whole pipeline k lye ni bikly aik stage tk limit rhy. tky us stage ma unko use kya ja sakhy..


pipeline {
    agent any

    stages {
        stage('Example') {
            environment {
                      name = 'hassan'
                      email = 'muhammadhassanb122@gmail.com'        ---> is tarha sa enviromental variable sirf aik stage k lye available rhy gye.. y jin jin stage ma ap btao gye un ma available rhy gye.
            }
            steps { 
                sh 'echo "${name}"'
                sh 'echo "${email}"'
            }
        }

        stage('email') {
            steps { 
                sh 'echo "${email}"'
            }
        }
    }
}

Parameterized
----------------

In this vedio we discuss about parameter jis k through ap users sa input lye sakhty hn.


pipeline {
    agent any
    environment {
           name = 'hassan'
           email = 'muhammadhassanb122@gmail.com'       
            }
    parameters{
          string{name: 'person', defaultValue: 'Hassan', Description: 'who are you'}     --> mean ap user sa string value lye gye... ap isma dye value ko pipeline ma call kerwa ker use b ker sakhty hn.
          booleanParam{name: 'isMale', defaultValue: 'true', Description: ''}
          choice{name: 'City', Choices: ['lahore' , 'karachi' , 'ISB'], Description: ''}
             
            }

    stages {
        stage('Example') {
            
            steps { 
                sh 'echo "${name}"'
                sh 'echo "${email}"'
                sh 'echo "${person}"'

            }
        }

        stage('email') {
            steps { 
                sh 'echo "${email}"'
            }
        }
    }
}

Use of "INPUT" in stage
-----------------------

remember input sirf stage k under hi use hota ha, y hum is lye use kerty hn "tky during running pipeline jenkins user sa input lye or jb user apni input add kery then wo stage execute ho or pipeline ki baki stage b execute ho,,,


pipeline {
    agent any
    environment {
           name = 'hassan'
           email = 'muhammadhassanb122@gmail.com'       
            }
    parameters{
          string{name: 'person', defaultValue: 'Hassan', Description: 'who are you'}     --> mean ap user sa string value lye gye... ap isma dye value ko pipeline ma call kerwa ker use b ker sakhty hn.
          booleanParam{name: 'isMale', defaultValue: 'true', Description: ''}
          choice{name: 'City', Choices: ['lahore' , 'karachi' , 'ISB'], Description: ''}
             
            }

    stages {
        stage('terraform apply') {
            input{
              message "should we continue"              ---> ab is stage per jenkins apki input lye ga, agr ap "yes you should" per click kro gye tu further pipeline execute hogi. or agr "abort" per click kro gye tu pipeline rok jye gi..
              ok "yes you should"  
            }
            
            steps { 
                sh 'echo "${name}"'
                sh 'echo "${email}"'
                sh 'echo "${person}"'

            }
        }

        stage('email') {
            steps { 
                sh 'echo "${email}"'
            }
        }
    }
}

POST ACTION
----------

"Isko ap pipeline ma use ker sakhty hn jis sa y hoga k apka koi asa task ha jo chalna hi chalna ha chahye pipeline fail ho ya successfull ho.. tu wo is sa chaly gi...

y global or stage level dono per define hojata ha...

Conditions
"always": Run the steps in the post section regardless of the completion status of the Pipeline’s or stage’s run.

"changed": Only run the steps in post if the current Pipeline’s run has a different completion status from its previous run.

"fixed": Only run the steps in post if the current Pipeline’s run is successful and the previous run failed or was unstable.

"regression": Only run the steps in post if the current Pipeline’s or status is failure, unstable, or aborted and the previous run was successful.

"aborted": Only run the steps in post if the current Pipeline’s run has an "aborted" status, usually due to the Pipeline being manually aborted. This is typically denoted by gray in the web UI.

"failure": Only run the steps in post if the current Pipeline’s or stage’s run has a "failed" status, typically denoted by red in the web UI.

"success": Only run the steps in post if the current Pipeline’s or stage’s run has a "success" status, typically denoted by blue or green in the web UI.

"unstable": Only run the steps in post if the current Pipeline’s run has an "unstable" status, usually caused by test failures, code violations, etc. This is typically denoted by yellow in the web UI.

"unsuccessful": Only run the steps in post if the current Pipeline’s or stage’s run has not a "success" status. This is typically denoted in the web UI depending on the status previously mentioned (for stages this may fire if the build itself is unstable).

"cleanup": Run the steps in this post condition after every other post condition has been evaluated, regardless of the Pipeline or stage’s status.

Example 3. Post Section, Declarative Pipeline
pipeline {
    agent any   -------> mean job kisi b node per run ho...  or agr ap na job ko kisi specfic node per run kerna ha tu apko label use krna hoga.. agent { label "node"} , mean hmry case ma node per jo label hoga wo "node" hoga...ab jb job run hogi tu wo is label wali node per run hogi..
    stages {
        stage('Example') {
            steps {
                echo 'Hello World'
            }
        }
    }
    post { 
        always { 
            echo 'I will always say Hello again!'
        }
    }
}


trick to write pipeline easily
------------------------------

1- apko vscode ma "jenkinsfile" name ki extension add ker leni ha.. jis sa hoga y k... jenkinsfile ka lye jitny b block hn wo khud hi bna dye ga..
2- yka apko pipeline ki configuratin ma "pipeline syntax" last ma mily ga. jisko use ker k ap pipeline k lye scripts bna sakhty hn..

create pipeline by using plugin
-------------------------------

you can also create pipeline by clicking.. mean it would be easy to make or it can be done by using plugin.

plugin name is "blue ocean" so install plugin in jenkins... ab ap jenkins k dashboard open kery gye tu apko "open blue ocean" ka option mily ga..

"remember: humari agr pipeline kisi stage per fail hoti ha tu hum "scraptive pipeline" k through sirf specfic stage ko hi again ni chala sakhty, but "declarative pipeline" k through hum "blue ocean" plugin ko use kerty howy ker sakhty. 

mean agr meri pipeline kisi specfic stage per fail hogi ha tu hum declarative pipeline ma blue ocean plugin ko use ker k sari pipeline again chalny k bjye sirf us stage ko again run ker sakhty hn... is sa time safe hoga...   

"blue ocean" is plugin ko jenkins ma kerny sa apka jenkins kafi advance hojye ga..
