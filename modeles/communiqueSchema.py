# from marshmallow import INCLUDE
# from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
#
# from modeles.communique import Localite, Date, Communique, get_session
#
#
# class LocaliteSchema(SQLAlchemyAutoSchema):
#     class Meta:
#         model = Localite
#         include_fk = True
#         load_instance = True
#
#
# class DateSchema(SQLAlchemyAutoSchema):
#     class Meta:
#         model = Date
#         include_fk = True
#         include_relationships = True
#         load_instance = True
#
#
# class CommuniqueSchema(SQLAlchemyAutoSchema):
#     class Meta:
#         model = Communique
#         unknown = INCLUDE
#         include_relationships = True
#         load_instance = True
#
#
# if __name__ == '__main__':
#     my_json = {
#         "nom": "2021-10",
#         "date_list": [
#             {
#                 "date": "20/10",
#                 "nb_test": 213,
#                 "nb_nouv_ca": 13,
#                 "nb_cas_cont": 11,
#                 "nb_cas_com": 2,
#                 "nb_gueri": 32,
#                 "nb_dece": 1,
#                 "nom_fse": "2021-10",
#                 "dateheure_ext": "26/07/1997 22:59:03",
#                 "localite": [
#                     {
#                         "nom_localite": "Dakar",
#                         "nb_cas": 12
#                     },
#                     {
#                         "nom_localite": "Thies",
#                         "nb_cas": 2
#                     }
#                 ]
#             }
#         ]
#     }
#
#     schema = CommuniqueSchema()
#
#     list_communique = schema.load(my_json, session=get_session())
#     print(list_communique)
