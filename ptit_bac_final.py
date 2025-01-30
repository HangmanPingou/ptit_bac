from PySide6.QtWidgets import QApplication, QWidget, QMainWindow, QPushButton, QLabel
from PySide6 import QtCore, QtWidgets
from PySide6.QtCore import QTimer
from random import randint
from winsound import Beep
from time import sleep
import sys

lettres = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", "P", "Q","R", "S", "T", "U", "V", "W", "X","Y", "Z"]
list_themes = ["Aliment", "Animal", "Arbre", "Boisson", "Couleur", "Dans la pièce", "Fleur", "Fruit", "Marque", "Meuble", "Monnaie", "Pays", "Personnage", "Personnalité", "Prénom féminin", "Prénom masculin", "Ville"]
theme_choisi ="THEMES"
# temps_choisi = self.spn_chrono.value()

class ma_fenetre(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Le Petit Bac") # Nom de la fenêtre
        self.setFixedSize(800,600) # Taille de la fenêtre non modifiable
        self.setToolTip("Bonne partie et amusez-vous bien!!") # Ce qui apparait quand on laisse la souris immobile

        self.bar_du_bas = self.statusBar() # Juste pour mon copyright ;))
        self.bar_du_bas.setStyleSheet("background: #9d00d8; font-size: 12px")
        self.bar_du_bas.showMessage("Fait par l'aimable PINGOU")
        self.bar_du_bas.setToolTip("Et oui Marguerite, je suis AIMABLE ;)")

        self.central = QWidget(self) # Pour gérer ma zone de travail
        self.central.setStyleSheet("background: #dbffff")
        self.setCentralWidget(self.central)

        self.lb_central = QLabel("Bienvenue", self.central) # Mon label principal
        self.lb_central.setGeometry(150, 40, 500, 500)
        self.lb_central.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.lb_central.setStyleSheet("font-size: 80px ; font-weight: bold ; color: red")

        self.lb_lettres_restantes = QLabel(f"Il reste 26 lettres", self.central) # Label en haut à droite donnant le nombre de lettres restantes
        self.lb_lettres_restantes.setGeometry(680, 10, 100, 30)
        self.lb_lettres_restantes.setStyleSheet("font-size: 12px ; font-weight: bold")
        self.lb_lettres_restantes.setToolTip("Nombre de lettres restantes")

        self.lb_temps = QLabel("", self.central)
        self.lb_temps.setStyleSheet("font-weight: bold")
        self.lb_temps.setGeometry(350, 60, 150, 30)

        self.spn_chrono = QtWidgets.QSpinBox(self.central)
        self.spn_chrono.setGeometry(350, 10, 60, 30)
        self.spn_chrono.setToolTip("Choisir le nombre de minutes")

        self.activ_chrono = QtWidgets.QCheckBox(self.central) # Case à cocher pour activer le chronomètre
        self.activ_chrono.setGeometry(460, 10, 30, 30)
        self.activ_chrono.setToolTip("Activer / Désactiver le chronomètre")

        self.bouton1 = QPushButton("Fin de la partie", self.central) # Met fin à la partie.
        self.bouton1.setGeometry(10, 540, 100, 30)
        self.bouton1.setStyleSheet("font-size: 12px")
        self.bouton1.setToolTip("Au revoir")
        self.bouton1.clicked.connect(self.fin)

        self.bouton2 = QPushButton("Commencer", self.central) # Mon bouton commencer puis suivant
        self.bouton2.setGeometry(690, 540, 100, 30)
        self.bouton2.setStyleSheet("font-size: 12px")
        self.bouton2.clicked.connect(self.jeu)

        self.cbb_themes = QtWidgets.QComboBox(self.central) # Ma liste de thèmes et si pas de thème choisi donne un thème aléatoire
        self.cbb_themes.setGeometry(10, 10, 200, 40)
        self.cbb_themes.setStyleSheet("font-size: 20px ; font-weight: bold ; border: 0px")
        self.cbb_themes.setEditable(True) # Permet d'utiliser le setAlignment ainsi que le setCurretText
        self.cbb_themes.lineEdit().setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.cbb_themes.setToolTip("Choisir une thème")
        self.cbb_themes.addItems(list_themes)
        self.cbb_themes.setCurrentText(theme_choisi)
        self.cbb_themes.activated.connect(self.choix_theme)

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.fin_chrono)

        self.affiche_timer = QTimer(self)
        self.affiche_timer.timeout.connect(self.maj_chrono)

    def jeu(self): # Tirage au sort de la lettre
        global lettres
        if theme_choisi == "THEMES":
            self.themes_aleatoirs()
        else:
            self.cbb_themes.setCurrentText(theme_choisi)
        if len(lettres) > 0:
            a = randint(0, len(lettres)-1)
            self.lb_central.setText(lettres[a])
            self.lb_central.setStyleSheet("font-size: 400px")
            lettres.remove(lettres[a])
            self.bouton1.setText("Fin de la partie")
            self.bouton2.setText("Lettre suivante")
            self.lb_lettres_restantes.setText(f"Il reste {len(lettres)} lettre{'s' if len(lettres) > 1 else ''}")
        else:
            lettres = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", "P", "Q","R", "S", "T", "U", "V", "W", "X","Y", "Z"]
            self.partie_suivante()
        if self.activ_chrono.isChecked():
            self.temps = self.spn_chrono.value()  # Récupère la valeur de mon spinbox
            self.timer.start(self.temps * 60000)
            global temps_restant
            temps_restant = self.spn_chrono.value() * 60
            self.affiche_timer.start(1000)
        else:
            self.lb_temps.setText("")
        # else:
        #     self.timer.stop()

    def partie_suivante(self): # Je change juste le nom des boutons, quand je changeais le signal ça faisait des trucs bizard ;))) car il gardait aussi le signal du même bouton comme si 2 boutons étaient superposés
        global theme_choisi
        theme_choisi = "THEMES"
        self.cbb_themes.setCurrentText(theme_choisi)
        self.lb_central.setText("Veux-tu continuer?")
        self.lb_central.setGeometry(150, 40, 500, 500)
        self.lb_central.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.lb_central.setStyleSheet("font-size: 55px ; font-weight: bold")
        self.bouton1.setText("non")
        self.bouton2.setText("oui")

    def themes_aleatoirs(self): # Donne un thème aléatoire de la liste
        a = randint(0, len(list_themes)-1)
        self.cbb_themes.setCurrentText(list_themes[a])

    def choix_theme(self): # Si un thème est choisi par le joueur
        global theme_choisi
        theme_choisi = self.cbb_themes.currentText()

    def maj_chrono(self):
        global temps_restant
        self.lb_temps.setText(f"Il reste {temps_restant//60} min et {temps_restant%60} sec")
        temps_restant -= 1
        if temps_restant == -1:
            self.affiche_timer.stop()

    def fin_chrono(self):
        self.lb_central.setText("FIN DU TEMPS")
        self.lb_central.setGeometry(150, 40, 500, 500)
        self.lb_central.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.lb_central.setStyleSheet("font-size: 72px ; font-weight: bold ; color: red")
        Beep(1000, 700) # A travailler pour une belle musique
        self.timer.stop()

    def fin(self): # Avec exit "output1" et quit "output2" ne fonctionne pas en exe, d'où je passe par la bibliothèque SYS
        sys.exit()  

app = QApplication()  # Crée l'application
fenetre = ma_fenetre()
fenetre.show()
app.exec()


