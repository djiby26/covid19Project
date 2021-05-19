import json
import sys

from PyQt5.QtCore import QDir, Qt
from PyQt5.QtWidgets import QApplication, QMainWindow, QFileSystemModel, QTreeWidgetItem, QButtonGroup, \
    QAbstractItemView
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from base import Ui_MainWindow
from modeles.communiques import CommuniqueSchema

engine = create_engine('mysql://root:1234@localhost/covid')
session = sessionmaker(bind=engine)


class MainWindow(QMainWindow, Ui_MainWindow):
    checked_item_row = []
    unchecked_item_row = []
    official_checked_row = []
    json_file_content = ''

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.model = QFileSystemModel()
        self.ui = Ui_MainWindow()  # represente la fenetre principale
        self.ui.setupUi(self)
        self.ui.treeView.doubleClicked.connect(self.on_double_click)  # signal sur une ligne du tableau affichant
        # l'ensemble des fichiers json
        self.ui.treeView.setAlternatingRowColors(True)
        self.ui.treeView.setHeaderHidden(True)
        self_radio_group = QButtonGroup(self.ui.groupBox)
        self_radio_group.addButton(self.ui.radioButton)
        self_radio_group.addButton(self.ui.radioButton_2)
        self.ui.radioButton.clicked.connect(self.on_trx_radio)
        self.ui.radioButton_2.clicked.connect(self.on_ac_radio)
        selmodel = self.ui.treeWidget.selectionModel()
        selmodel.selectionChanged.connect(self.check_box_clicked)
        self.ui.pushButton_3.clicked.connect(self.validation)

    def populate_table(self):
        self.model.setRootPath(QDir.currentPath())  # definition de chemin d'acces des fichiers json et xml a afficher
        self.ui.treeView.setModel(self.model)  #
        self.ui.treeView.setRootIndex(self.model.index('./files'))
        self.ui.treeView.hideColumn(1)
        self.ui.treeView.hideColumn(3)
        self.ui.treeView.setColumnWidth(0, 300)

    def on_double_click(self, index):
        # premet d'obtenir le chemin d'acces du fichier selectionne lors d'un double clique
        file_path = self.model.filePath(index)

        # recuperation du nom du fichier selectionne los d'un double clique
        index_ = self.ui.treeView.selectedIndexes()  # on recupere l'ensemble des indexes
        first_index = index_[0].data()  # on recupere la premiere indexe qui correspond a la colonne name du tableau

        # appelle la fonction display_preview en lui donnant le chemin et le nom du fichier
        self.display_preview(file_path, first_index)

    # affiche le contenu d'un fichier sur le panneau a droite
    def display_preview(self, file_path, first_index):

        with open(file_path) as f:
            self.json_file_content = json.load(f)
        # print(type(self.json_file_content))
        print(self.json_file_content['nom'])
        schema = CommuniqueSchema()

        list_communique = schema.load(self.json_file_content)
        view = self.ui.treeWidget
        view.setSelectionMode(QAbstractItemView.MultiSelection)
        view.setHeaderHidden(True)
        item = QTreeWidgetItem(view.invisibleRootItem())
        item.setText(0, list_communique.nom)
        item.setExpanded(True)
        for i in range(len(list_communique.dates)):
            child_item = QTreeWidgetItem()
            child_item.setText(0, list_communique.dates[i]['date'])
            child_item.setCheckState(0, Qt.Unchecked)
            sub_child1 = QTreeWidgetItem()
            sub_child2 = QTreeWidgetItem()
            sub_child3 = QTreeWidgetItem()
            sub_child4 = QTreeWidgetItem()
            sub_child5 = QTreeWidgetItem()
            sub_child6 = QTreeWidgetItem()
            sub_child7 = QTreeWidgetItem()
            sub_child8 = QTreeWidgetItem()
            sub_child9 = QTreeWidgetItem()
            sub_child1.setText(0, "Nombre de Test: " + str(list_communique.dates[i]['nb_test']))
            sub_child2.setText(0, "Nombre nouveaux Cas: " + str(list_communique.dates[i]['nb_nouv_ca']))
            sub_child3.setText(0, "Nombre cas contact: " + str(list_communique.dates[i]['nb_cas_cont']))
            sub_child4.setText(0, "Nombre cas communautaire: " + str(list_communique.dates[i]['nb_cas_com']))
            sub_child5.setText(0, "Nombre gueri: " + str(list_communique.dates[i]['nb_gueri']))
            sub_child6.setText(0, "Nombre deces: " + str(list_communique.dates[i]['nb_dece']))
            sub_child7.setText(0, "Nom du fichier source: " + list_communique.dates[i]['nom_fse'])
            sub_child8.setText(0, "Date et heure d'extraction: " + list_communique.dates[i]['dateheure_ext'])
            sub_child9.setText(0, "Localites")

            for j in range(len(list_communique.dates[i]['localite'])):
                nom_localite = QTreeWidgetItem()
                nb_cas = QTreeWidgetItem()
                nom_localite.setText(0, "Localite: " + list_communique.dates[i]['localite'][j]['nom_localite'])
                nb_cas.setText(0, "Nombre de cas: " + str(list_communique.dates[i]['localite'][j]['nb_cas']))
                sub_child9.addChildren([nom_localite, nb_cas])

            child_item.addChild(sub_child1)
            child_item.addChild(sub_child2)
            child_item.addChild(sub_child3)
            child_item.addChild(sub_child4)
            child_item.addChild(sub_child5)
            child_item.addChild(sub_child6)
            child_item.addChild(sub_child7)
            child_item.addChild(sub_child8)
            child_item.addChild(sub_child9)
            item.addChild(child_item)
        view.addTopLevelItem(item)

    def check_box_clicked(self, selected, deselected):

        for index in selected.indexes():
            self.checked_item_row.append(index.row())
            # print(index.row())
        for index in deselected.indexes():
            self.unchecked_item_row.append(index.row())
            # print(index.row())

    def validation(self):
        schema = CommuniqueSchema()
        json_dates = ''
        for it in self.unchecked_item_row:
            self.checked_item_row.remove(it)
        for it in range(len(self.checked_item_row)-1):
            json_dates += '%s,' % self.json_file_content['dates'][it]
        json_dates += "%s" % self.json_file_content['dates'][len(self.checked_item_row)-1]
        json_string = "{'nom':'%s','dates':[%s]}" % (self.json_file_content['nom'], json_dates)
        # json_dict = dict(json_string)
        json_object = schema.loads(json_string)
        print(json_string)

    def on_trx_radio(self):
        self.ui.pushButton.setEnabled(True)
        self.ui.pushButton_2.setEnabled(True)

    def on_ac_radio(self):
        self.ui.pushButton.setEnabled(False)
        self.ui.pushButton_2.setEnabled(False)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    mW = MainWindow()
    mW.populate_table()
    mW.show()
    app.exec_()
