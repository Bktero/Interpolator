# -*- coding: utf-8 -*-
'''
INTERPOLATOR - A serie interpolator using Python
Copyright (2) 2012  Pierre Gradot

This program is free software; you can redistribute it and/or
modify it under the terms of the GNU General Public License
as published by the Free Software Foundation; either version 2
of the License, or (at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program; if not, write to the Free Software
Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA.
'''

'''
Cette application fait des interpolations de series pour obtenir des valeurs intermediaires.
'''

import classes
import sys
import os
from PyQt4 import QtGui, QtCore
from interpolation_ui import Ui_Interpolation


class Interpolation(QtGui.QMainWindow, Ui_Interpolation):
    def __init__(self, parent=None):
        super(Interpolation, self).__init__(parent)
        self.setupUi(self)
        self.connectSignals()
        self.scriptpath = os.path.dirname( sys.argv[0] )
  
        # Chargement des series
        if os.path.exists( self.scriptpath + r"\\data.file" ) == True :
            # Utilisation du fichier par defaut
            f = open(  self.scriptpath + r'\\data.file', 'r')
            filename = f.read()
            f.close()
            
            # Recuperation de series
            self.createSeriesLoader(filename)
            
            # Interpolateur par defaut et MAJ de la valeur interpolee affichee
            self.createInterpolator(self.seriesloader.listeSeries[0], "linear")
            self.interpolate()
            
        else :
            ok = self.selectAndUseFile()    
            if ok==False:
                # Demander un fichier a l'utilisateur
                self.doubleSpinBoxValeur.setEnabled(False)
                '''
                msgBox = QtGui.QMessageBox()
                print msgBox, type(msgBox)
                msgbox.setText("Aucun fichier s�lectionn� !")
                msgBox.setInformativeText("Il faut s�lectionner un fichier pour utiliser le programme.")
                msgBox.setStandardButtons(QMessageBox.Ok)
                ret = msgBox.exec_()
                '''
                QtGui.QMessageBox.information (self, "Aucun fichier s�lectionn� !", "Il faut s�lectionner un fichier pour utiliser le programme.")
    
    
    def main(self):
        self.show()
        
        
    def connectSignals(self):
        '''
        Connecte les signaux et les slots associes.
        '''
        # Barre de menu
        self.actionQuitter.triggered.connect(QtGui.qApp.quit)
        self.actionSelectionner_fichier.triggered.connect(self.selectAndUseFile)
        self.actionM_moriser_fichier.triggered.connect(self.memorizeFileName)
        
        # Menu deroulant
        self.comboBoxSeries.currentIndexChanged.connect(self.serieWasSelected)
        
        # Calcul d'interpolation
        self.doubleSpinBoxValeur.valueChanged.connect(self.interpolate)
        
           
    def createSeriesLoader(self, filename):
        '''
        Retourne le SeriesLoader obtenu a partir du nom de fichier donne en parametre. Elle suppose ce nom valide.
        Il ne peut y avoir qu'un seul Interpolator a la fois, donc le precedent est supprime s'il existe.
        Enfin, elle met a jour l'affichage
        '''
        # Creation du nouveau SeriesLoader
        try :
            del self.seriesloader
        except AttributeError :
            pass  # Pas d'objet existant, sans doute car c'est la 1ere execution de la methode
    
        self.seriesloader = classes.SeriesLoader(filename) 

        # Mise a jour de l'affichage
        self.comboBoxSeries.clear()
        
        for s in self.seriesloader.listeSeries:
            self.comboBoxSeries.addItem( s.noms["serie"] )
                           
            
    def createInterpolator(self, serie, type):
        '''
        Retourne un Interpolator du type demande pour la serie passee en parametre.
        Il ne peut y avoir qu'un seul Interpolator a la fois, donc le precedent est supprime s'il existe.
        '''
        try :
            del(self.interpol)
        except AttributeError :
            pass  # Pas d'objet existant, sans doute car c'est la 1ere execution de la methode
            
        if (type == "linear") & (isinstance(serie, classes.Serie)) :
            self.interpol = classes.LinearInterpolator(serie)

        else :
            print "Type d'interpolateur non implement�"
            self.interpol = None
     
        
    def selectAndUseFile(self):
        '''
        Slot en reponse au clic sur l'item "Selectionner fichier" dans le menu. 
        Elle recupere un nouveau de fichier a l'aide de la boite a outils dedie.
        - Si aucun fichier n'est selectionne, elle renvoie False.
        - Si non, elle appelle les methodes createSeriesLoader et createInterpolator() pour utiliser ce nouveau fichier.
          Enfin, elle renvoie True.  
        '''
        # Recuperation du nom de fichier
        if hasattr(self, 'dirname') == False:
            self.dirname = self.scriptpath
            
        filename = QtGui.QFileDialog.getOpenFileName(self, "Choisir classeur...", self.dirname, "Excel (*.xls)")
         
        # Action appropriee      
        if filename.isEmpty() == True :
            return False
        
        else :
            #  Memorisation du dossier pour la prochaine fois
            self.dirname = QtCore.QString( os.path.dirname( str(filename.toUtf8())) )
            print self.dirname
            
            # Recuperation de series
            self.createSeriesLoader(filename)
            
            # Interpolateur par defaut et MAJ de la valeur interpolee affichee
            self.createInterpolator(self.seriesloader.listeSeries[0], "linear")
            self.interpolate()
            self.doubleSpinBoxValeur.setEnabled(True) # au cas ou l'utilisateur a clique sur Annuler lors de la premiere selection de fichier (voir __init__())
            
            return True
        

    def memorizeFileName(self):
        '''
        Slot en reponse au clic sur "Memoriser fichier" dans le menu.
        Il enregistre le chemin du fichier Excel actuellement en cours d'utilisation dans le fichier "./data.file"
        '''
        currentfilename = self.seriesloader.filename
        f = open(  self.scriptpath + r'\\data.file', 'w')
        f.write(currentfilename)
        f.close()
        text = "Le fichier suivant sera automatiquement ouvert au prochain d�marrage:\n\n"
        text += self.scriptpath + r"\data.file"
        QtGui.QMessageBox.information (self, "Fichier memorise", text)
        
        
    def serieWasSelected(self, index):
        '''
        Slot en reponse a la selection d'une serie dans le menu deroulant (combo box).
        Il faut cree un nouvel Interpolateur sur cette serie et mettre a jour l'affichage.      
        'index' est l'index de l'entree selectionnee, il est transmis par le signal 'currentIndexChanged'.
        '''
        # Modification de l'interpolateur de la classe
        self.createInterpolator(self.seriesloader[index], "linear")
        
        # MAJ de l'affichage
        self.labelUniteValeurs.setText( self.seriesloader[index].unites["valeurs"] )
        self.labelUniteImages.setText( self.seriesloader[index].unites["images"] )
        self.interpolate()
  
  
    def interpolate(self):
        '''
        Utilise l'interpolateur disponible pour calculer l'image de la valeur entree dans le champ dedie.
        Affiche ensuite cette valeur.
        '''
        x = self.doubleSpinBoxValeur.value()
        y = self.interpol.getImageOf(x)    
        if y is None :
            self.doubleSpinBoxImage.setSpecialValueText("Hors limite")
            self.doubleSpinBoxImage.setValue( self.doubleSpinBoxImage.minimum() )
        else :
            self.doubleSpinBoxImage.setValue(y)

        
#if __name__ == "__main__" :
if __name__=='__main__':
    app = QtGui.QApplication(sys.argv)
    interpolator = Interpolation()
    interpolator.main()
    app.exec_()