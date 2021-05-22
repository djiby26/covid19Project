import json
from typing import List

from sqlalchemy import Column, Integer, String, PickleType

from marshmallow import Schema, fields, post_load
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import scoped_session, sessionmaker, relationship, backref

Base = declarative_base()


class Localite(Base):
    __tablename__ = "localite"

    id = Column(Integer, primary_key=True, autoincrement=True)
    nom_localite = Column(String(30), nullable=False)
    nb_cas = Column(Integer, nullable=False)

    # date_id = Column(Integer, ForeignKey('date.id'))

    def __init__(self, nom_localite, nb_cas):
        self.nom_localite = nom_localite
        self.nb_cas = nb_cas


# class Date(Base):
#     __tablename__ = 'date'
#     id = Column(Integer, primary_key=True, autoincrement=True)
#     date = Column(String(30), nullable=False)
#     nb_test = Column(Integer, nullable=False)
#     nb_nouv_ca = Column(Integer, nullable=False)
#     nb_cas_cont = Column(Integer, nullable=False)
#     nb_cas_com = Column(Integer, nullable=False)
#     nb_gueri = Column(Integer, nullable=False)
#     nb_dece = Column(Integer, nullable=False)
#     nom_fse = Column(String(30), nullable=False)
#     dateheure_ext = Column(String(30), nullable=False)
#     localites = relationship("Localite")
#     communique_id = Column(Integer, ForeignKey('communique.id'))
#
#     def __init__(self, date, nb_test, nb_nouv_ca, nb_cas_cont, nb_cas_com, nb_gueri, nb_dece,
#                  nom_fse, dateheure_ext, localite: List[Localite]):
#         self.date = date
#         self.nb_test = nb_test
#         self.nb_nouv_ca = nb_nouv_ca
#         self.nb_cas_cont = nb_cas_cont
#         self.nb_cas_com = nb_cas_com
#         self.nb_gueri = nb_gueri
#         self.nb_dece = nb_dece
#         self.nom_fse = nom_fse
#         self.dateheure_ext = dateheure_ext
#         self.localite = localite


class Communiques(Base):
    __tablename__ = 'communique'

    id = Column(Integer, primary_key=True, autoincrement=True)
    date = Column(String(30), nullable=False)
    test_realise = Column(Integer, nullable=False)
    nouveaux_cas = Column(Integer, nullable=False)
    cas_contacts = Column(Integer, nullable=False)
    cas_communautaires = Column(Integer, nullable=False)
    cas_importes = Column(Integer, nullable=False)
    personne_sous_traitement = Column(Integer, nullable=False)
    nombre_gueris = Column(Integer, nullable=False)
    nombre_deces = Column(Integer, nullable=False)
    nom_fichier_source = Column(String(30), nullable=False)
    date_heure_extraction = Column(String(30), nullable=False)
    localites = Column(PickleType)

    # communique_id = Column(Integer, ForeignKey('communique.id'))

    def __init__(self, date, test_realise, nouveaux_cas, cas_contacts, cas_communautaires, cas_importes,
                 personne_sous_traitement, nombre_gueris, nombre_deces,
                 nom_fichier_source, date_heure_extraction, localite=dict):
        self.date = date
        self.test_realise = test_realise
        self.nouveaux_cas = nouveaux_cas
        self.cas_contacts = cas_contacts
        self.cas_communautaires = cas_communautaires
        self.cas_importes = cas_importes
        self.personne_sous_traitement = personne_sous_traitement
        self.nombre_gueris = nombre_gueris
        self.nombre_deces = nombre_deces
        self.nom_fichier_source = nom_fichier_source
        self.date_heure_extraction = date_heure_extraction
        self.localite = localite


# class LocaliteSchema(Schema):
#     nom_localite = fields.Str()
#     nb_cas = fields.Int()


class CommuniqueSchema(Schema):
    date = fields.Str()
    test_realise = fields.Int()
    nouveaux_cas = fields.Int()
    cas_contacts = fields.Int()
    cas_communautaires = fields.Int()
    cas_importes = fields.Int()
    personne_sous_traitement = fields.Int()
    nombre_gueris = fields.Int()
    nombre_deces = fields.Int()
    nom_fichier_source = fields.Str()
    date_heure_extraction = fields.Str()
    localite = fields.Dict()

    @post_load()
    def make_user(self, data, **__):
        return Communiques(**data)


# class CommuniqueSchema(Schema):
#     nom = fields.Str()
#     dates = fields.Nested(DateSchema, many=True)
#
#     @post_load()
#     def make_user(self, data, **__):
#         return Communiques(**data)


if __name__ == '__main__':
    my_json = {
        'nom': '2021-10',
        'dates': [
            {
                'date': '20/10',
                'nb_test': 213,
                'nb_nouv_ca': 13,
                'nb_cas_cont': 11,
                'nb_cas_com': 2,
                'nb_gueri': 32,
                'nb_dece': 1,
                'nom_fse': '2021-10',
                'dateheure_ext': '26/07/1997 22:59:03',
                'localite': [
                    {
                        'nom_localite': 'Dakar', 'nb_cas': 12
                    },
                    {
                        'nom_localite': 'Thies', 'nb_cas': 2
                    }
                ]
            },
            {'date': '21/10', 'nb_test': 213, 'nb_nouv_ca': 13, 'nb_cas_cont': 11, 'nb_cas_com': 2, 'nb_gueri': 32,
             'nb_dece': 1, 'nom_fse': '2021-10', 'dateheure_ext': '26/07/1997 22: 59: 03', 'localite': [
                {'nom_localite': 'Dakar', 'nb_cas': 12
                 },
                {'nom_localite': 'Thies', 'nb_cas': 2
                 }
            ]
             }
        ]
    }

    print(my_json)

    #  avec marshmallow
    schema = CommuniqueSchema()
    # result = schema.load(my_json)
    # for j in my_json:
    # result = json.load(my_json)
    list_com = schema.load(my_json)
    # print(list_com)