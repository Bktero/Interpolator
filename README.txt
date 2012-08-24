INTERPOLATOR - A serie interpolator using Python
Copyright (C) 2012  Pierre Gradot


Présentation :

Ce programme sert à obtenir des valeurs intermédiaires de séries grâce à des méthodes d'interpolation. Ces séries sont contenues dans un fichier Excel répondant à un formatage précis.


Utilisation :

Le programme utilise Python 2.7 et  PyQt4. Il se lance grâce au script main.pyw, après avoir généré le fichier interpolation_ui.py à l'aide pyuic et du fichier interpolation.ui. Le fichier pyuic_call.bat permet de générer ce fichier.

Pour l'instant, seul Windows XP a été testé.


Formatage du fichier Excel :

Le fichier "exemple.xls donne un exemple de fichier formaté correctement. Chaque feuille contient une série, composée d'une plage des valeurs (colonne A) et d'une plage des images de ces valeurs (colonne B). Les deux premières lignes donnent les noms des plages ainsi que les unités utilisées.



Licence :

Le code est placé sous Licence GPLv2. Les termes de la licence sont disponibles dans le fichier LICENCE.txt ou à l'adresse : http://www.gnu.org/licenses/gpl-2.0.html