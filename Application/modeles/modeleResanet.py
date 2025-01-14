#!/usr/bin/python
# -*- coding: utf-8 -*-


import mysql.connector
import sys
reload(sys)
sys.setdefaultencoding("utf-8")


connexionBD = None

def getConnexionBD() :
	global connexionBD
	try :
		if connexionBD == None :
			connexionBD = mysql.connector.connect(
					host = 'localhost' ,
					user = 'root' ,
					password = 'azerty' ,
					database = 'resanet'
				)
		return connexionBD
	except :
		return None


def seConnecterGestionnaire( login , mdp ) :
	try :
		curseur = getConnexionBD().cursor()
		requete = '''
					select nom,prenom 
					from Gestionnaire
					inner join Personnel 
					on Gestionnaire.matricule = Personnel.matricule
					where login = %s
					and mdp = %s
				'''

		curseur.execute( requete , ( login , mdp ) )
		
		enregistrement = curseur.fetchone()
		
		gestionnaire = {}
		if enregistrement != None :
			gestionnaire[ 'login' ] = login
			gestionnaire[ 'nom' ] = enregistrement[ 0 ]
			gestionnaire[ 'prenom' ] = enregistrement[ 1 ]
			
		curseur.close()
		return gestionnaire
		
	except :
		return None
		
def seConnecterUsager( numeroCarte , mdpCarte ) :
	try :
		curseur = getConnexionBD().cursor()
		requete = '''
					select solde,activee,nom,prenom 
					from Carte
					inner join Personnel 
					on Carte.matricule = Personnel.matricule
					where numeroCarte = %s
					and mdpCarte = %s
				'''

		curseur.execute( requete , ( numeroCarte , mdpCarte ) )
		
		enregistrement = curseur.fetchone()
		
		usager = {}
		if enregistrement != None :
			usager[ 'numeroCarte' ] = numeroCarte
			usager[ 'solde' ] = enregistrement[ 0 ]
			usager[ 'activee' ] = enregistrement[ 1 ]
			#print type( usager[ 'activee' ] )
			usager[ 'nom' ] = enregistrement[ 2 ]
			usager[ 'prenom' ] = enregistrement[ 3 ]
			
		curseur.close()
		return usager
		
	except :
		return None


def verificationInitMDP(numeroCarte, mdpCarte):
	try:
		curseur = getConnexionBD().cursor()
		requete = '''
					select solde,activee,nom,prenom 
					from Carte
					inner join Personnel 
					on Carte.matricule = Personnel.matricule
					where numeroCarte = %s
					and oldMdpCarte = %s
				'''

		curseur.execute(requete, (numeroCarte, mdpCarte))

		enregistrement = curseur.fetchone()

		verifInitMDP = False
		if enregistrement != None:
			verifInitMDP = True
			curseur.close()
		return verifInitMDP

	except:
		return None

def getMdp( numeroCarte ):
	try:
		curseur = getConnexionBD().cursor()
		requete = '''
					select mdpCarte
					from Carte
					where numeroCarte = %s
				'''

		curseur.execute(requete , ( numeroCarte , ))
		enregistrement = curseur.fetchone()

		mdp = 'inconnu'
		if enregistrement != None :
			mdp = enregistrement[0]
			curseur.close()
		return mdp

	except:
		return None

def getOldMdp( numeroCarte ):
	try:
		curseur = getConnexionBD().cursor()
		requete = '''
					select oldMdpCarte
					from Carte
					where numeroCarte = %s
				'''

		curseur.execute(requete , ( numeroCarte , ))
		enregistrement = curseur.fetchone()

		oldMdp = 'inconnu'
		if enregistrement != None :
			oldMdp = enregistrement[0]
			curseur.close()
		return oldMdp

	except:
		return None

def setOldMdp( numeroCarte ):
	try:
		curseur = getConnexionBD().cursor()
		requete = '''
					update Carte
					set oldMdpCarte = NULL
					where numeroCarte = %s
				'''

		curseur.execute(requete , ( numeroCarte , ))
		connexionBD.commit()
		nbTuplesTraites = curseur.rowcount
		curseur.close()

		return nbTuplesTraites

	except:
		return None


def getYear( numeroCarte ):
	try:
		curseur = getConnexionBD().cursor()
		requete = '''
					select year( dateNaissance )
					from Personnel as p
					inner join Carte as c
					where c.matricule = p.matricule
					and c.numeroCarte = %s
					'''
		curseur.execute(requete , (numeroCarte ,))
		enregistrement = curseur.fetchone()

		year = 'inconnu'
		if enregistrement != None :
			year = enregistrement[0]
			curseur.close()
		return year

	except:
		return None

def getJoursFeries():
	try:
		curseur = getConnexionBD().cursor()
		requete = '''
					select dateFeries
					from JoursFeries
				'''

		curseur.execute(requete, ())

		enregistrements = curseur.fetchall()

		jours = []
		for unEnregistrement in enregistrements:
			uneDate = '%02d-%02d' % (unEnregistrement[0].month, unEnregistrement[0].day)

			jours.append(uneDate)

		curseur.close()
		return jours

	except:
		return None

	try :
		curseur = getConnexionBD().cursor()
		requete = '''
					select jour
					from joursFeries
				'''

		curseur.execute( requete , () )

		enregistrements = curseur.fetchall()
		jours = []
		for unJour in enregistrements :
			print int(unJour)
			leJour = {}
			leJour[ 'jour' ] = unJour[ 0 ]
			jours.append( leJour )

		curseur.close()
		return jours

	except :
		return None

def getSolde( numeroCarte ) :
	print '[START] modeleResanet::getSolde()'
	try :
		curseur = getConnexionBD().cursor()
		requete = '''
					select solde
					from Carte
					where numeroCarte = %s
				'''

		curseur.execute( requete , ( numeroCarte , ) )
		
		enregistrement = curseur.fetchone()
		
		solde = 'inconnu'
		if enregistrement != None :
			solde = enregistrement[ 0 ]
			#print type(solde)
			
		curseur.close()
		print '[STOP] modeleResanet::getSolde()'
		return solde
		
	except :
		print '[STOP] modeleResanet::getSolde()'
		return None
		
		
def getTarifRepas( numeroCarte ) :
	print '[START] modeleResanet::getTarifRepas()'
	try :
		curseur = getConnexionBD().cursor()
		requete = '''
					select tarifRepas
					from Fonction
					inner join Personnel
					on Fonction.idFonction = Personnel.idFonction
					inner join Carte
					on Personnel.matricule = Carte.matricule
					where numeroCarte = %s
				'''

		curseur.execute( requete , ( numeroCarte , ) )
		
		enregistrement = curseur.fetchone()
		
		tarif = 'inconnu'
		if enregistrement != None :
			tarif = enregistrement[ 0 ]
			#print type(tarif)
			
		curseur.close()
		print '[STOP] modeleResanet::getTarifRepas()'
		return tarif
		
	except :
		print '[STOP] modeleResanet::getTarifRepas()'
		return None


def getPersonnelsSansCarte() :
	try :
		curseur = getConnexionBD().cursor()
		requete = '''
					select matricule, nom , prenom , nomService
					from Service
					inner join Personnel
					on Service.idService = Personnel.idService
					where matricule not in ( 
												select matricule
												from Carte
											)
				'''

		curseur.execute( requete , () )
		
		enregistrements = curseur.fetchall()
		
		personnels = []
		for unEnregistrement in enregistrements :
			unPersonnel = {}
			unPersonnel[ 'matricule' ] = unEnregistrement[ 0 ]
			unPersonnel[ 'nom' ] = unEnregistrement[ 1 ]
			unPersonnel[ 'prenom' ] = unEnregistrement[ 2 ]
			unPersonnel[ 'nomService' ] = unEnregistrement[ 3 ]
			personnels.append( unPersonnel )
			
		curseur.close()
		return personnels
		
	except :
		return None

def getPersonnelsAvecCarte() :
	try :
		curseur = getConnexionBD().cursor()
		requete = '''
					select Personnel.matricule, solde, activee, nom , prenom , nomService
					from Service
					inner join Personnel
					on Service.idService = Personnel.idService
					inner join Carte
					on Carte.matricule = Personnel.matricule
				'''

		curseur.execute( requete , () )
		
		enregistrements = curseur.fetchall()
		
		personnels = []
		for unEnregistrement in enregistrements :
			unPersonnel = {}
			unPersonnel[ 'matricule' ] = unEnregistrement[ 0 ]
			unPersonnel[ 'solde' ] = unEnregistrement[ 1 ]
			unPersonnel[ 'activee' ] = unEnregistrement[ 2 ]
			unPersonnel[ 'nom' ] = unEnregistrement[ 3 ]
			unPersonnel[ 'prenom' ] = unEnregistrement[ 4 ]
			unPersonnel[ 'nomService' ] = unEnregistrement[ 5 ]
			if unPersonnel[ 'activee' ] == 1:
				unPersonnel[ 'activee' ]='Activée'
			else:
				unPersonnel[ 'activee' ]='Bloquée'

			personnels.append( unPersonnel )
			
		curseur.close()
		return personnels
		
	except :
		return None


def getInformationsCarte(numeroCarte):
		curseur = getConnexionBD().cursor()
		requete = '''
					select matricule, nom , prenom , nomService
					from Service
					inner join Personnel
					on Service.idService = Personnel.idService
					where matricule = %s
				'''

		curseur.execute(requete, (numeroCarte))

		informations = curseur.fetchall()

		personnel = []
		for uneInformation in informations:
			unPersonnel = {}
			unPersonnel['matricule'] = uneInformation[0]
			unPersonnel['nom'] = uneInformation[1]
			unPersonnel['prenom'] = uneInformation[2]
			unPersonnel['nomService'] = uneInformation[3]
			personnel.append(unPersonnel)

		curseur.close()
		return personnel



def activerCarte( numeroCarte ) :
	try :
		curseur = getConnexionBD().cursor()
		
		requete = '''
			update Carte
			set activee = 1
			where numeroCarte = %s
			'''
			
		curseur.execute( requete , ( numeroCarte , ) )
		connexionBD.commit()
		nbTuplesTraites = curseur.rowcount
		curseur.close()
		
		return nbTuplesTraites
	
	except :
		return None
	
def bloquerCarte( numeroCarte ) :
	try :
		curseur = getConnexionBD().cursor()
		
		requete = '''
			update Carte
			set activee = 0
			where numeroCarte = %s
			'''
			
		curseur.execute( requete , ( numeroCarte , ) )
		connexionBD.commit()
		nbTuplesTraites = curseur.rowcount
		curseur.close()
		
		return nbTuplesTraites
		
	except :
		return None
		

def crediterCarte( numeroCarte , somme ) :
	try :
		curseur = getConnexionBD().cursor()
		
		requete = '''
			update Carte
			set solde = solde + %s
			where numeroCarte = %s
			'''
			
		curseur.execute( requete , ( somme , numeroCarte ) )
		connexionBD.commit()
		nbTuplesTraites = curseur.rowcount
		curseur.close()
		
		return nbTuplesTraites
		
	except :
		return None


def reinitialiserMdp( numeroCarte ) :
	try :
		curseur = getConnexionBD().cursor()

		requete2 = '''
			update Carte as c
			set oldMdpCarte = (
				select mdpCarte
				from Personnel
				where c.matricule = Personnel.matricule
				and c.numeroCarte = %s
			)
			where numeroCarte = %s
			'''

		requete = '''
			update Carte as c
			set mdpCarte = (
				select year( dateNaissance )
				from Personnel
				where c.matricule = Personnel.matricule
				and c.numeroCarte = %s
			)
			where numeroCarte = %s
			'''

		curseur.execute( requete2, (numeroCarte, numeroCarte ) )
		curseur.execute( requete , ( numeroCarte , numeroCarte ) )
		connexionBD.commit()
		nbTuplesTraites = curseur.rowcount
		curseur.close()
		
		return nbTuplesTraites

	except :
		return None


def modifierMdpUsager( numeroCarte , nouveauMdp) :
	try :
		curseur = getConnexionBD().cursor()
		
		requete = '''
			update Carte as c
			set mdpCarte = %s
			where numeroCarte = %s
			'''
			
		curseur.execute( requete , ( nouveauMdp , numeroCarte ) )
		connexionBD.commit()
		nbTuplesTraites = curseur.rowcount
		curseur.close()
		
		return nbTuplesTraites
		
	except :
		return None


def creerCarte( matricule) :
	try :
		curseur = getConnexionBD().cursor()
		
		requete = '''
			insert into Carte 
			values(%s,(select year(datenaissance) from Personnel where matricule = %s ),NULL,0.0,CURRENT_DATE,0,%s);
			'''
			
		curseur.execute( requete , ( matricule, matricule, matricule ) )
		connexionBD.commit()
		nbTuplesTraites = curseur.rowcount
		curseur.close()
		
		return nbTuplesTraites
		
	except :
		return None


def enregistrerReservation( numeroCarte , dateReservation ):
	try:
		curseur = getConnexionBD().cursor()

		requete = '''
			insert into Reservation( dateResa , numeroCarte )
			values( %s , %s )
			'''

		curseur.execute(requete, ( dateReservation , numeroCarte ) )
		connexionBD.commit()
		nbTuplesTraites = curseur.rowcount
		curseur.close()

		return nbTuplesTraites

	except:
		return None


def annulerReservation( numeroCarte , dateReservation ):
	try:
		curseur = getConnexionBD().cursor()

		requete = '''
			delete from Reservation
			where numeroCarte = %s
			and dateResa = %s
			'''

		curseur.execute(requete, ( numeroCarte , dateReservation ) )
		connexionBD.commit()
		nbTuplesTraites = curseur.rowcount
		curseur.close()

		return nbTuplesTraites

	except:
		return None


def getReservationsCarte( numeroCarte , dateDebut , dateFin ):
	print '[START] modeleResanet::getReservationsCarte()'
	try:
		curseur = getConnexionBD().cursor()
		requete = '''
					select dateResa
					from Reservation
					where numeroCarte = %s
					and dateResa >= %s
					and dateResa <= %s 
				'''

		curseur.execute(requete, ( numeroCarte , dateDebut , dateFin ) )

		enregistrements = curseur.fetchall()

		dates = []
		for unEnregistrement in enregistrements:
			
			uneDate = '%04d-%02d-%02d' % ( unEnregistrement[0].year , unEnregistrement[0].month , unEnregistrement[0].day )
			
			dates.append( uneDate )

		curseur.close()
		print '[STOP] modeleResanet::getReservationsCarte()'
		return dates

	except:
		print '[STOP] modeleResanet::getReservationsCarte()'
		return None


def getHistoriqueReservationsCarte( numeroCarte ) :
	try:
		curseur = getConnexionBD().cursor()
		requete = '''
					select dateResa
					from Reservation
					where numeroCarte = %s
					order by dateResa DESC
				'''

		curseur.execute(requete, ( numeroCarte , ) )

		enregistrements = curseur.fetchall()

		dates = []
		for unEnregistrement in enregistrements:
			
			uneDate = '%04d-%02d-%02d' % ( unEnregistrement[0].year , unEnregistrement[0].month , unEnregistrement[0].day )
			
			dates.append( uneDate )

		curseur.close()
		return dates

	except:
		return None


	
def getReservationsDate( dateResa ) :
	try :
		curseur = getConnexionBD().cursor()
		requete = '''
					select Carte.numeroCarte , Personnel.nom , Personnel.prenom , Service.nomService
					from Reservation
					inner join Carte
					on Carte.numeroCarte = Reservation.numeroCarte
					inner join Personnel
					on Personnel.matricule = Carte.matricule
					inner join Service
					on Service.idService = Personnel.idService
					where Reservation.dateResa = %s
				'''

		curseur.execute( requete , ( dateResa , ) )
		
		enregistrements = curseur.fetchall()
		
		reservations = []
		for unEnregistrement in enregistrements :
			uneReservation = {}
			uneReservation[ 'numeroCarte' ] = unEnregistrement[ 0 ]
			uneReservation[ 'nom' ] = unEnregistrement[ 1 ]
			uneReservation[ 'prenom' ] = unEnregistrement[ 2 ]
			uneReservation[ 'nomService' ] = unEnregistrement[ 3 ]
			reservations.append( uneReservation )
			
		curseur.close()
		return reservations
		
	except :
		return None


	
def debiterSolde( numeroCarte ) :
	try :
		curseur = getConnexionBD().cursor()
		
		requete = '''
			update Carte as c
			set solde = solde - (
				select tarifRepas
				from Fonction
				inner join Personnel
				on Personnel.idFonction = Fonction.idFonction
				where c.matricule = Personnel.matricule
				and c.numeroCarte = %s
			)
			where numeroCarte = %s
			'''
			
		curseur.execute( requete , ( numeroCarte , numeroCarte ) )
		connexionBD.commit()
		nbTuplesTraites = curseur.rowcount
		curseur.close()
		
		return nbTuplesTraites

	except :
		return None
		
	
def crediterSolde( numeroCarte ) :
	try :
		curseur = getConnexionBD().cursor()
		
		requete = '''
			update Carte as c
			set solde = solde + (
				select tarifRepas
				from Fonction
				inner join Personnel
				on Personnel.idFonction = Fonction.idFonction
				where c.matricule = Personnel.matricule
				and c.numeroCarte = %s
			)
			where numeroCarte = %s
			'''
			
		curseur.execute( requete , ( numeroCarte , numeroCarte ) )
		connexionBD.commit()
		nbTuplesTraites = curseur.rowcount
		curseur.close()
		
		return nbTuplesTraites

	except :
		return None
