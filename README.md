# kognitiv_hazi

Az én házi feladatom részeként egyszerű vonalkövetést próbálok egy ROS Noetic projekt keretében Gazebo környezetben szimulálni egy Turtlebot3 segítségével. A szimuláció során nyomon lehet majd követni a robotkamera képét és hogy hogyan érzékeli és követi a kijelöltútvonalat.

Itt látható egy kép a kameráról:

![utvonal](https://github.com/mmartin98/kognitiv_hazi/assets/62999338/8c80aaa9-51bd-4db9-9bce-a9e8eb82fe0e)


## Rövid összefoglaló

A vonalkövető modul fő célja, hogy lehetővé tegye a Turtlebot számára, hogy önállóan kövessen egy vonal által meghatározott pályát (a feladatom keretében az egyszerűség kedvéért ez egy piros vonal lesz). A vonalkövető modul olyan érzékelőkből, például kameraérzékelőkből áll, amelyek egy vonal vagy egy határvonal helyzetének érzékelésére használhatók és az érzékelő adatai alapján a modul ezután kiszámítja a megfelelő vezérlési műveletet, például a robot mozgásának sebességét és irányát, hogy a robot az adott pályán maradjon.

Hasonló, bonyolultabb vonalkövető modulokat gyakran használnak robotikai alkalmazásokban, például automatizált irányított járművekben (AGV), ipari robotokban és pilóta nélküli földi járművekben (UGV). Különösen hasznosak olyan helyzetekben, amikor a robotnak egy előre meghatározott útvonalon kell navigálnia, például gyártási vagy raktári környezetben.

## Világ

A szimulációhoz létrehoztam a Blender-ben egy labirintust, ami világként fog szolgálni. Ezzen része néhány fal, amelyek között egy piros színnel megjelölt útvonal található, melyet a Turtlebot-nak követnie kell majd elejétől a végéig.

A világ felülnézetből, ahogyan a Blender-ben elkészült, bal oldalt alul a robot indulási pozíciója, jobb oldalt pedig a célpozíció.
![image](https://github.com/mmartin98/kognitiv_hazi/assets/62999338/e4247a06-6f49-4f4f-b05b-19cc78db7241)

Így pedig ahogy Gazebo szimuláció közben (kikapcsolt árnyékokkal):
![palya](https://github.com/mmartin98/kognitiv_hazi/assets/62999338/c09386e5-c85b-4814-b11b-c2cd43a2b0cd)

Ahhoz, hogy az alábbi projekt sikeresen futtatható legyen, szükségünk lesz a következőkre:

`opencv-python
numpy`

Szükség lesz természetesen a Turtlebot3 alap csomag anyagaira a MOGI-s módosításokkal, melyeket az órán is használtunk, ezeket az alábbi GIT repokról lehet letölteni:

git clone https://github.com/ROBOTIS-GIT/turtlebot3_simulations

git clone https://github.com/ROBOTIS-GIT/turtlebot3_msgs

git clone https://github.com/MOGI-ROS/turtlebot3

## Program felépítése

A `turtlebot3_line_follower` alapból 3 fő részre osztható, ezekből a launch és a world az indítéskori kezdeti paraméterekért és azok betöltéséért és magáért a világért felelnek, de a lényegi rész a scripts alatt található. Az itt található 3 python program felelős az egész vonalkövetés működéséért. A `detector.py` felelős a vonal érzékeléséért a kamerán keresztül és egy értéked ad vissza ezek alapján attól függően, hogy melyik irányba kell mennie a robotnak. A `follower.py` felelős a tényleges vonalkövetésért, amit a rosrun paranccsal majd meg kell hívni hogy a szimuláció ténylegesen elinduljon. A `motion.py` tartalmazza a mozgást kezelő kódokat, itt lehet beállítani a sebesség értékeket, amivel a robot mozogni fog a szimuláció során.

## Változtatások, megjegyzések, elkészítés lépései és futtatás

Az eredeti MOGI-s verzióhoz képest annyi változtatást eszközöltem, hogy a kamerának a pitch szögének értékét átállítottam 0.4-re, ugyanis a tesztfuttatások során ez megfelelőnek bizonyult a kamera állását tekintve.

A source parancsokat és a Turtlebot verzióját beleírtam a `.bashrc`-be, ezzel is könnyítve a futtatásokat.

A Blender-ből betöltött fájlt a Gazebo segítségével .world fájllá alakítottam, amiben annyi további változtatást eszközöltem, hogy 40-ed részére csökkentettem a méretét, ugyanis későn vettem észre, hogy a Blender-ben készített munkám túl nagy volt, és ez tűnt a legegyszerűbb megoldásnak.

A szimuláció futtatásához két terminálra lesz szükség, egyikben elnavigálunk a megfelelő mappába a 

`cd catkin_workspace`

`cd src`

parancsok segítségével, majd pedig elindítjuk a ROS-t és a Gazebo szimulációt:

`roslaunch turtlebot3_line_follower line_follower.launch`

Ez eltarthat egy darabig, legalábbis az én gépem kevésbé bírja már jól, de amint betöltött, a másik terminálon a follower.py futtatásával elindíthatjuk a robotunkat:

`rosrun turtlebot3_line_follower follower.py`

A szimuláció kicsit lassú, a korábban megemlített nagyméretű pályának következtében, szépen lassan a Turtlebot végighalad a kijelölt pályán a kezdeti ponttól a végpontig.





