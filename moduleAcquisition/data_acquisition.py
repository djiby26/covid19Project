import glob
import json
import os
import shutil
from datetime import datetime

import pytesseract
from pdf2image import convert_from_path

from pdfminer.pdfparser import PDFParser
from pdfminer.pdfdocument import PDFDocument
from pdfminer.pdftypes import resolve1
from pytesseract import Output
import re
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

tabJson = []
tab_month = []
entries = os.listdir('../files/pdf')
source_file = ''
round = 1

# recuperation du chemin de chaque doc pdf dans le dossier
for pdf_path in entries:
    source_file = pdf_path
    print(round)
    try:
        images = convert_from_path('../files/pdf/' + pdf_path, poppler_path=r'C:\poppler-21.03.0\Library\bin')
        pil_im = images[0]  # assuming that we're interested in the first page only
        ocr_dict = pytesseract.image_to_data(pil_im, lang='eng', output_type=Output.DICT)
        text1 = " ".join(ocr_dict['text'])

        file = open('../files/pdf/' + pdf_path, 'rb')
        parser = PDFParser(file)
        document = PDFDocument(parser)
        # This will give you the count of pages
        if resolve1(document.catalog['Pages'])['Count'] > 1:
            pil_im1 = images[1]
            ocr_dict1 = pytesseract.image_to_data(pil_im1, lang='eng', output_type=Output.DICT)
            text2 = " ".join(ocr_dict1['text'])
        else:
            text2 = ''
        # ocr_dict now holds all the OCR info including text and location on the image
        text = text1 + text2

        day = re.search("(lundi|mardi|Mercredi|mércredi|jeudi|vendredi|samedi|dimanche)", text, re.IGNORECASE)

        word = r"\W*([\w]+)"
        n = 3
        groups = re.search(r'{}\W*{}{}'.format(word * n, str(day.group(0)), word * n), text, re.IGNORECASE).groups()
        date_input = str(groups[n:][0]) + '-' + str(groups[n:][1]).lower() + '-' + str(groups[n:][2])
        if len(str(groups[n:][0])) < 2:
            daily = '0' + str(groups[n:][0])
        else:
            daily = str(groups[n:][0])
        if str(groups[n:][1]).lower() == 'janvier':
            month = '01'
        if str(groups[n:][1]).lower() == 'février':
            month = '02'
        if str(groups[n:][1]).lower() == 'mars':
            month = '03'
        if str(groups[n:][1]).lower() == 'avril':
            month = '04'
        if str(groups[n:][1]).lower() == 'mai':
            month = '05'
        if str(groups[n:][1]).lower() == 'juin':
            month = '06'
        if str(groups[n:][1]).lower() == 'juillet':
            month = '07'
        if str(groups[n:][1]).lower() == 'août':
            month = '08'
        if str(groups[n:][1]).lower() == 'septembre':
            month = '09'
        if str(groups[n:][1]).lower() == 'octobre':
            month = '10'
        if str(groups[n:][1]).lower() == 'novembre':
            month = '11'
        if str(groups[n:][1]).lower() == 'décembre':
            month = '12'
        date = daily + '/' + month + '/' + str(groups[n:][2])

    except Exception as e:
        print(e)

    # COLLECTING DATAS
    cas_positifs = re.search(r'(\w+\s+){0,3}sont revenus positifs(\w+\s+){0,3}', text, re.IGNORECASE)
    if cas_positifs:
        pos_num = str(cas_positifs.group(0))
        cas_positifs_nums = [int(s) for s in pos_num.split() if s.isdigit()]
        if not cas_positifs_nums:
            cas_positifs_nums = [0]
    else:
        cas_positifs_nums = [0]

    cas_importes = re.search(r'(\w+\s+){0,3}cas importés(\w+\s+){0,3}', text, re.IGNORECASE)
    if cas_importes:
        imp_num = str(cas_importes.group(0))
        cas_importes_nums = [int(s) for s in imp_num.split() if s.isdigit()]
        if not cas_importes_nums:
            cas_importes_nums = [0]
    else:
        cas_importes_nums = [0]

    cas_contacts = re.search(r'(\w+\s+){0,3}cas contacts(\w+\s+){0,3}', text, re.IGNORECASE)
    if cas_contacts:
        cont_num = str(cas_contacts.group(0))
        cas_contacts_nums = [int(s) for s in cont_num.split() if s.isdigit()]
        if not cas_contacts_nums:
            cas_contacts_nums = [0]
    else:
        cas_contacts_nums = [0]

    tests_realises = re.search(r'(\w+\s+){0,3}tests réalisés(\w+\s+){0,3}', text, re.IGNORECASE)
    if tests_realises:
        test_num = str(tests_realises.group(0))
        if tests_realises.group(0) is not None:
            cas_test_nums = [int(s) for s in test_num.split() if s.isdigit()]
            if not cas_test_nums:
                cas_test_nums = [0]
    else:
        cas_test_nums = [0]

    sous_traitement = re.search(r'(\w+\s+){0,3}sous traitement(\w+\s+){0,3}', text, re.IGNORECASE)
    if sous_traitement:
        trait_num = str(sous_traitement.group(0))
        cas_sous_traitement_nums = [int(s) for s in trait_num.split() if s.isdigit()]
        if not cas_sous_traitement_nums:
            cas_sous_traitement_nums = [0]
    else:
        cas_sous_traitement_nums = [0]

    contacts_suivis = re.search(r'(\w+\s+){0,3}contacts suivis(\w+\s+){0,3}', text, re.IGNORECASE)
    if contacts_suivis:
        suivi_num = str(contacts_suivis.group(0))
        cas_contacts_suivis_nums = [int(s) for s in suivi_num.split() if s.isdigit()]
        if not cas_contacts_suivis_nums:
            cas_ccontacts_suivis_nums = [0]
    else:
        cas_contacts_suivis_nums = [0]

    cas_communautaires = re.search(r'(\w+\s+){0,12} communautaire(\w+\s+){0,3}', text, re.IGNORECASE)
    if cas_communautaires:
        comm_num = str(cas_communautaires.group(0))
        cas_communautaires_nums = [int(s) for s in comm_num.split() if s.isdigit()]
        if not cas_communautaires_nums:
            cas_communautaires_nums = [0]
    else:
        cas_communautaires_nums = [0]

    cas_gueris = re.search(r'(\w+\s+){0,6}négatifs et déclarés guéris(\w+\s+){0,3}', text, re.IGNORECASE)
    if cas_gueris:
        gueris_num = str(cas_gueris.group(0))
        cas_gueris_nums = [int(s) for s in gueris_num.split() if s.isdigit()]
    else:
        cas_gueris_nums = [0]

    cas_deces = re.search(r'(\w+\s+){0,10}décès(\w+\s+){0,10}', text, re.IGNORECASE)
    if cas_deces:
        deces_num = str(cas_deces.group(0))
        cas_deces_nums = [int(s) for s in deces_num.split() if s.isdigit()]
        if not cas_deces_nums:
            cas_deces_nums = [0]
    else:
        cas_deces_nums = [0]

    # different regions du senegal
    expression = r"(?i)(?:\bDakar\D{0,20})([0-9][0-9,]*)[^.,]|([0-9][0-9,]*)[^.,](?:\D{0,20}Dakar)"
    expression1 = r"(?i)(?:\bThiès\D{0,20})([0-9][0-9,]*)[^.,]|([0-9][0-9,]*)[^.,](?:\D{0,20}Thiès)"
    expression2 = r"(?i)(?:\bTouba\D{0,20})([0-9][0-9,]*)[^.,]|([0-9][0-9,]*)[^.,](?:\D{0,20}Touba)"
    expression3 = r"(?i)(?:\bDiourbel\D{0,20})([0-9][0-9,]*)[^.,]|([0-9][0-9,]*)[^.,](?:\D{0,20}Diourbel)"
    expression4 = r"(?i)(?:\bFatick\D{0,20})([0-9][0-9,]*)[^.,]|([0-9][0-9,]*)[^.,](?:\D{0,20}Fatick)"
    expression5 = r"(?i)(?:\bKaolack\D{0,20})([0-9][0-9,]*)[^.,]|([0-9][0-9,]*)[^.,](?:\D{0,20}Kaolack)"
    expression6 = r"(?i)(?:\bKaffrine\D{0,20})([0-9][0-9,]*)[^.,]|([0-9][0-9,]*)[^.,](?:\D{0,20}Kaffrine)"
    expression7 = r"(?i)(?:\bKolda\D{0,20})([0-9][0-9,]*)[^.,]|([0-9][0-9,]*)[^.,](?:\D{0,20}Kolda)"
    expression8 = r"(?i)(?:\bTamba\D{0,20})([0-9][0-9,]*)[^.,]|([0-9][0-9,]*)[^.,](?:\D{0,20}Tamba)"
    expression9 = r"(?i)(?:\bZiguinchor\D{0,20})([0-9][0-9,]*)[^.,]|([0-9][0-9,]*)[^.,](?:\D{0,20}Ziguinchor)"
    expression10 = r"(?i)(?:\bSaint-Louis\D{0,20})([0-9][0-9,]*)[^.,]|([0-9][0-9,]*)[^.,](?:\D{0,20}Saint-Louis)"
    expression11 = r"(?i)(?:\bMatam\D{0,20})([0-9][0-9,]*)[^.,]|([0-9][0-9,]*)[^.,](?:\D{0,20}Matam)"
    expression12 = r"(?i)(?:\bSédhiou\D{0,20})([0-9][0-9,]*)[^.,]|([0-9][0-9,]*)[^.,](?:\D{0,20}Sédhiou)"
    expression13 = r"(?i)(?:\bKédougou\D{0,20})([0-9][0-9,]*)[^.,]|([0-9][0-9,]*)[^.,](?:\D{0,20}Kédougou)"

    nbCasDkr = re.findall(expression, text)
    if not nbCasDkr:
        nb_cas_dakar = [0]
    else:
        dkr_str = str(nbCasDkr)
        nb_cas_dakar = re.findall(r'\d+', dkr_str)

    nbCasTh = re.findall(expression1, text)
    if not nbCasTh:
        nb_cas_thies = [0]
    else:
        th_str = str(nbCasTh)
        nb_cas_thies == re.findall(r'\d+', th_str)

    nbCasTb = re.findall(expression2, text)
    if not nbCasTb:
        nb_cas_touba = [0]
    else:
        tb_str = str(nbCasTb)
        nb_cas_touba = re.findall(r'\d+', tb_str)

    nbCasDbl = re.findall(expression3, text)
    if not nbCasDbl:
        nb_cas_diourbel = [0]
    else:
        dbl_str = str(nbCasDbl)
        nb_cas_diourbel = re.findall(r'\d+', dbl_str)

    nbCasFtk = re.findall(expression4, text)
    if not nbCasFtk:
        nb_cas_fatick = [0]
    else:
        ftk_str = str(nbCasFtk)
        nb_cas_fatick = re.findall(r'\d+', ftk_str)

    nbCasKlk = re.findall(expression5, text)
    if not nbCasKlk:
        nb_cas_kaolack = [0]
    else:
        klk_str = str(nbCasKlk)
        nb_cas_kaolack = re.findall(r'\d+', klk_str)

    nbCasKfr = re.findall(expression6, text)
    if not nbCasKfr:
        nb_cas_kaffrine = [0]
    else:
        kfr_str = str(nbCasKfr)
        nb_cas_kaffrine = re.findall(r'\d+', kfr_str)

    nbCasKld = re.findall(expression7, text)
    if not nbCasKld:
        nb_cas_kolda = [0]
    else:
        kld_str = str(nbCasKld)
        nb_cas_kolda = re.findall(r'\d+', kld_str)

    nbCasTmb = re.findall(expression8, text)
    if not nbCasTmb:
        nb_cas_tamba = [0]
    else:
        tmb_str = str(nbCasTmb)
        nb_cas_tamba = re.findall(r'\d+', tmb_str)

    nbCasZig = re.findall(expression9, text)
    if not nbCasZig:
        nb_cas_ziguinchor = [0]
    else:
        zig_str = str(nbCasZig)
        nb_cas_ziguinchor = re.findall(r'\d+', zig_str)

    nbCasSl = re.findall(expression10, text)
    if not nbCasSl:
        nb_cas_saintl = [0]
    else:
        sl_str = str(nbCasSl)
        nb_cas_saintl = re.findall(r'\d+', sl_str)

    nbCasMtm = re.findall(expression11, text)
    if not nbCasMtm:
        nb_cas_matam = [0]
    else:
        mtm_str = str(nbCasMtm)
        nb_cas_matam = re.findall(r'\d+', mtm_str)

    nbCasSdh = re.findall(expression12, text)
    if not nbCasSdh:
        nb_cas_sedhiou = [0]
    else:
        sdh_str = str(nbCasSdh)
        nb_cas_sedhiou = re.findall(r'\d+', sdh_str)

    nbCasKdg = re.findall(expression13, text)
    if not nbCasKdg:
        nb_cas_kedougou = [0]
    else:
        kdg_str = str(nbCasKdg)
        nb_cas_kedougou = re.findall(r'\d+', kdg_str)
    annee_mois = ''
    # PUTTING DATA IN JSON OBJECT
    json_data = {
        pdf_path: {
            'date': date,
            'nouveaux_cas': cas_positifs_nums[0],
            'cas_importes': cas_importes_nums[0],
            'cas_contacts': cas_contacts_nums[0],
            'test_realise': cas_test_nums[0],
            'personne_sous_traitement': cas_sous_traitement_nums[0],
            'cas_communautaires': cas_communautaires_nums[0],
            'nombre_gueris': cas_gueris_nums[0],
            'nombre_deces': cas_deces_nums[0],
            'date_heure_extraction': str(datetime.now()),
            'nom_fichier_source': source_file,
            'localites': {
                'Dakar': int(nb_cas_dakar[0]),
                'Thies': int(nb_cas_thies[0]),
                'Diourbel': int(nb_cas_diourbel[0]),
                'Fatick': int(nb_cas_fatick[0]),
                'Kaolack': int(nb_cas_kaolack[0]),
                'Kaffrine': int(nb_cas_kaffrine[0]),
                'Touba': int(nb_cas_touba[0]),
                'Kolda': int(nb_cas_kolda[0]),
                'Tambacounda': int(nb_cas_tamba[0]),
                'Ziguinchor': int(nb_cas_ziguinchor[0]),
                'Saint-Louis': int(nb_cas_saintl[0]),
                'Matam': int(nb_cas_matam[0]),
                'Sedhiou': int(nb_cas_sedhiou[0]),
                'Kedougou': int(nb_cas_kedougou[0])
            }
        }}
    tabJson.append(json_data[pdf_path])
print('FILES CREATED', tabJson)

# GROUP ALL OBJECTS HAVING SAME MONTH
values = set(map(lambda x: x['date'][3:12], tabJson))
newlist = [[y for y in tabJson if y['date'][3:12] == x] for x in values]

# CREATING JSON OBJECTS TO DUMP ON JSON FILE FOR EACH MONTH
for i in newlist:
    doc_name = i[0]['date'][3:12]
    txtFile = doc_name.replace('/', '-')
    annee_mois = doc_name
    if txtFile:
        with open(str(txtFile) + '.json', 'w', encoding='utf-8') as f:
            json.dump(i, f, ensure_ascii=False, indent=4)
        f.close()
# MOVE ALL JSON FILE IN JSON FOLDER
for f in glob.glob('*.json'):
    shutil.move(f, '../files/jsons')
round += 1
print('---------operationn successfull--------')
