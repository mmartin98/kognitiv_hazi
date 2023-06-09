# kognitiv_hazi

Az én házi feladatom részeként egyszerű vonalkövetést próbálok egy ROS Noetic projekt keretében Gazebo környezetben szimulálni egy Turtlebot3 segítségével. A szimuláció során nyomon lehet majd követni a robotkamera képét és hogy hogyan érzékeli és követi a kijelöltútvonalat.

Itt látható egy kép a kameráról:

![image](https://github.com/mmartin98/kognitiv_hazi/assets/62999338/2dd59cf5-d381-467d-bc56-809236496c29)

## Rövid összefoglaló

A vonalkövető modul fő célja, hogy lehetővé tegye a Turtlebot számára, hogy önállóan kövessen egy vonal által meghatározott pályát (a feladatom keretében az egyszerűség kedvéért ez egy piros vonal lesz). A vonalkövető modul olyan érzékelőkből, például kameraérzékelőkből áll, amelyek egy vonal vagy egy határvonal helyzetének érzékelésére használhatók és az érzékelő adatai alapján a modul ezután kiszámítja a megfelelő vezérlési műveletet, például a robot mozgásának sebességét és irányát, hogy a robot az adott pályán maradjon.

Hasonló, bonyolultabb vonalkövető modulokat gyakran használnak robotikai alkalmazásokban, például automatizált irányított járművekben (AGV), ipari robotokban és pilóta nélküli földi járművekben (UGV). Különösen hasznosak olyan helyzetekben, amikor a robotnak egy előre meghatározott útvonalon kell navigálnia, például gyártási vagy raktári környezetben.

## Világ

A szimulációhoz létrehoztam a Blender-ben egy labirintust, ami világként fog szolgálni. Ezzen része néhány fal, amelyek között egy piros színnel megjelölt útvonal található, melyet a Turtlebot-nak követnie kell majd elejétől a végéig.

A világ felülnézetből, ahogyan a Blender-ben elkészült, bal oldalt alul a robot indulási pozíciója, jobb oldalt pedig a célpozíció.
![image](https://github.com/mmartin98/kognitiv_hazi/assets/62999338/230c487a-6a60-4c59-a80e-a03619977fdb)

Így pedig ahogy Gazebo szimuláció közben (kikapcsolt árnyékokkal):
![image](https://github.com/mmartin98/kognitiv_hazi/assets/62999338/e8fac889-47e6-4304-8db7-c24cb47a4570)

Ahhoz, hogy az alábbi projekt sikeresen futtatható legyen, szükségünk lesz a következőkre:

`opencv-python
numpy`

Szükség lesz természetesen a Turtlebot3 alap csomag anyagaira a MOGI-s módosításokkal, melyeket az órán is használtunk, ezeket az alábbi GIT repokról lehet letölteni:

```
git clone https://github.com/ROBOTIS-GIT/turtlebot3_simulations

git clone https://github.com/ROBOTIS-GIT/turtlebot3_msgs

git clone https://github.com/MOGI-ROS/turtlebot3
```
Ezen felül csupán erre a saját repomra van még szükség, amiben a turtlebot3_line_follower mappa található.

## Program felépítése

A `turtlebot3_line_follower` alapból 3 fő részre osztható, ezekből a launch és a world az indítéskori kezdeti paraméterekért és azok betöltéséért és magáért a világért felelnek, de a lényegi rész a scripts alatt található. Az itt található 3 python program felelős az egész vonalkövetés működéséért. A `detector.py` felelős a vonal érzékeléséért a kamerán keresztül és egy értéked ad vissza ezek alapján attól függően, hogy melyik irányba kell mennie a robotnak. A `follower.py` felelős a tényleges vonalkövetésért, amit a rosrun paranccsal majd meg kell hívni hogy a szimuláció ténylegesen elinduljon. Továbbá ez iratkozik fel a kamera képére és ez adja át a képet a detectornak. A `motion.py` tartalmazza a mozgást kezelő kódokat, itt lehet beállítani a sebesség értékeket, amit a kód a Twist class-on keresztül publishol.

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





