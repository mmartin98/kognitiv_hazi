# kognitiv_hazi

Az én házi feladatom részeként egyszerű vonalkövetést próbálok egy ROS Noetic projekt keretében Gazebo környezetben szimulálni egy Turtlebot3 segítségével. A szimuláció során nyomon lehet majd követni a robotkamera képét és hogy hogyan érzékeli és követi a kijelöltútvonalat.
(KÉP a kameráról)

Rövid összefoglaló

A vonalkövető modul fő célja, hogy lehetővé tegye a Turtlebot számára, hogy önállóan kövessen egy vonal által meghatározott pályát (a feladatom keretében az egyszerűség kedvéért ez egy piros vonal lesz). A vonalkövető modul olyan érzékelőkből, például kameraérzékelőkből áll, amelyek egy vonal vagy egy határvonal helyzetének érzékelésére használhatók és az érzékelő adatai alapján a modul ezután kiszámítja a megfelelő vezérlési műveletet, például a robot mozgásának sebességét és irányát, hogy a robot az adott pályán maradjon.

Hasonló, bonyolultabb vonalkövető modulokat gyakran használnak robotikai alkalmazásokban, például automatizált irányított járművekben (AGV), ipari robotokban és pilóta nélküli földi járművekben (UGV). Különösen hasznosak olyan helyzetekben, amikor a robotnak egy előre meghatározott útvonalon kell navigálnia, például gyártási vagy raktári környezetben.

Világ
A szimulációhoz létrehoztam a Blender-ben egy labirintust, ami világként fog szolgálni. Ezzen része néhány fal, amelyek között egy piros színnel megjelölt útvonal található, melyet a Turtlebot-nak követnie kell majd elejétől a végéig.

Ahhoz, hogy az alábbi projekt sikeresen futtatható legyen, szükségünk lesz a következőkre:

opencv-python
numpy


