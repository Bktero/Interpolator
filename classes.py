# -*- coding: utf-8 -*-
'''
INTERPOLATOR - A serie interpolator using Python
Copyright (C) 2012  Pierre Gradot

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
http://www.portailsig.org/content/python-lire-et-ecrire-des-fichiers-microsoft-excel-application-quantum-gis
'''
import xlrd


class Serie(object):
    '''
    Une serie correspond a la recuperation d'une feuille d'un classeur Excel.
    Le parametre est une feuille Excel et non juste son nom litteral.
    '''  
    def __init__(self, feuille):
        # Recuperation des deux plages formant la serie
        self.valeurs = feuille.col_values(0)
        self.images = feuille.col_values(1)
        
        # Extraction des champs indicatifs puis suppression des plages chiffrees
        self.noms =  { "serie" : feuille.name, "valeurs" : self.valeurs[0], "images" : self.images[0] }
        self.unites =  { "valeurs" : self.valeurs[1], "images" : self.images[1] }
        
        del self.valeurs[0]
        del self.images[0]
        del self.valeurs[0]
        del self.images[0]
        
        
        
    def __str__(self):
        return "-" * 50 + "\n" + repr(self.noms) + "\n" + repr(self.unites) + "\n" + repr(self.valeurs) + "\n" + repr(self.images) + "\n" + "-" * 50
        
        
        
    def __repr__(self):
        return self.__str__()

        
        
    def getIndicesOf(self, recherchee):
        '''
        La fonction recherche la valeur 'recherchee' dans les valeurs de la serie.
        Elle retourne un tuple contenant :
            - rien si la valeur 'recherchee' est hors limite
            - un seul indice si la valeur 'recherchee' est presente
            - les deux indices des valeurs encadrant au mieux la valeur 'recherchee' sinon
        '''            
            
        if recherchee in self.valeurs :
            return ( self.valeurs.index( recherchee ), ) # On n'oublie pas la virgule pour creer un tuple !
            
        elif ( recherchee >= self.valeurs[0] ) & ( recherchee <= self.valeurs[-1] ) :
            for i in range(0, len(self.valeurs) - 1):
                if (self.valeurs[i] < recherchee) & (self.valeurs[i+1] > recherchee) :
                    return (i, i+1)
           
        else :
            return () 

       

class SeriesLoader(object):
    '''
    Le SeriesLoader charge toutes les pages qu'il trouve dans le fichier Excel.
    Il suppose que chaque page contient une serie valide.    
    '''
    def __init__(self, filename):
        self.filename = filename
        classeur = xlrd.open_workbook(filename)       
        self.listeSeries = [ Serie( classeur.sheet_by_name(feuille) ) for feuille in classeur.sheet_names() ]
        
    def __str__(self):
        chaine = ""
        for s in self.listeSeries :
            chaine += repr(s) + "\n"
        return chaine

    def __repr___(self):
        return self.__str__()
        
    def __getitem__(self, indice):
        if isinstance(indice, int):
        # Acces indiciel a la liste des series
            return self.listeSeries[indice]
                
        elif isinstance(indice, str):
        # Acces comme un dictionnaire sur le nom des series
            for s in self.listeSeries :
                if s.noms["serie"] == indice:
                    return s
        
        else :
        # Autres cas, non geres
            return None



class Interpolator(object):
    '''
    Cette classe est une classe abstraite
    dont herite les differents interpolateurs.
    '''
    def __init__(self, serie):
        self.serie = serie
    '''
    def getImageOf(self, recherchee):
        
        pass'''
        #''' Methode virtuelle pure '''

        
class LinearInterpolator(Interpolator):
    '''
    Cette classe donne les outils pour realiser des interpolations lineaires sur une serie.
    '''
    def __init__(self, serie):
        super(LinearInterpolator, self).__init__(serie) # http://docs.python.org/library/functions.html?highlight=super#super

    def getImageOf(self, recherchee):
        '''
        Renvoie l'image de la valeur 'recherchee' :
            - soit par image directe si 'recherchee' fait partie de la serie ;
            - soit par interpolation lineaire si elle est entre les bornes de la serie.
        Dans le cas ou 'recherchee' est hors limite, la methode renvoie None.
        '''
        indices = self.serie.getIndicesOf( recherchee )
        
        if indices is () :
            return None
        if len( indices ) == 1 :
            # Image exacte
            return self.serie.images[ indices[0] ]
        else :
            # Calcul de l'image interpolee
            x = recherchee            
            x1 = self.serie.valeurs[indices[0]]
            x2 = self.serie.valeurs[indices[1]]
            y1 = self.serie.images[indices[0]]
            y2 = self.serie.images[indices[1]]
            
            p = (y2 - y1) / (x2 - x1)
            
            return p * ( x-x1 ) + y1
        
                   
'''
Main
'''    
if __name__=='__main__':

    allseries = SeriesLoader(r"d:\Documents and Settings\pgradot\Mes documents\Tools SD\Interpolation\Classeur.xls")
    
    serie = allseries["OutdoorSensor"]
    print serie
    
    az = temperature = 13.31   
    
    cdc = LinearInterpolator( serie ).getImageOf( az )
    
    print "T = {} donc R = {}".format(az, cdc)
    
    print type(cdc)
    print type (az)