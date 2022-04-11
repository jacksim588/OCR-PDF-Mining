'''
Library Imports
'''
import cv2
import csv
import os
import pytesseract
from PIL import Image
import numpy as np
import pandas as pd
import shutil
import numpy as np
from pathlib import Path
from pdf2image import convert_from_path
import PDF2Image
import DataMining
import DataToTable
import time
from pathlib import Path
import shutil



'''
Pytesseract and Poppler files must be installed and their paths added to the system PATH variable
Pytesseract is used for OCR
Poppler is used for converting PDFs to images. (pdf2image is a wrapper for this)
'''
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
poppler_path = r"C:\Program Files\poppler-0.68.0\bin"


'''
Defining file Paths
'''
mainFolder = r'C:\Users\jacks\Documents\GitHub\OCR-PDF-Mining\Output'#root folder for file structure
PDFImagesPath = mainFolder+ '\\bin\PDF Images Path'
FilteredPDFImagesPath = mainFolder+ '\\bin\\Filtered PDF Images'#holds temporary image files - TODO delete after each run
LineImagesPath = mainFolder+ '\\bin\\Line Images'
WordImagesPath = mainFolder+ '\\bin\\Word Images'
downloadPath = mainFolder+ '\downloads'#Holds the PDFs that have been downloaded by the bot
filteredPath = mainFolder+ '\Test Filtered Accounts'#Holds the PFDs once they have been filtered
outputfilePath = mainFolder+ 'output.csv' #the output file for combined data


'''
Creates the File Structure if it doesn't already exist
The bin folder will be deleted at the end of each run
'''
print('Formalising file direcotry...')
Path(mainFolder+'\\bin').mkdir(parents=True, exist_ok=True)
Path(PDFImagesPath).mkdir(parents=True, exist_ok=True)
Path(FilteredPDFImagesPath).mkdir(parents=True, exist_ok=True)
Path(LineImagesPath).mkdir(parents=True, exist_ok=True)
Path(WordImagesPath).mkdir(parents=True, exist_ok=True)
Path(downloadPath).mkdir(parents=True, exist_ok=True)
Path(filteredPath).mkdir(parents=True, exist_ok=True)
Path("/my/directory").mkdir(parents=True, exist_ok=True)

'''
Filter Phrases are used to filter the PDF down, so that only a section of pages are scanned for data
The more pages that are scanned, the longer each PDF will take, and higher the chance of noisy data
Too finite filter phrases may miss out on the page containg the correct data
'''
filterPhrases = ['gross profit'
]

'''
Beginning time tracking
'''
avgtimeperPDF,maxtimeperPDF,mintimeperPDF,pdfCount,avgtimeperPage,maxtimeperPage,mintimeperPage,pageCount=[0]*8
pdfStart = time.time()


'''
Begining loop to filter each PDF
'''
print('Begining PDF filtering...')

'''for unfilteredPDFPath in os.listdir(downloadPath):

    PDF2Image.filterPDFs(downloadPath=downloadPath,
                        unfilteredPDFPath=unfilteredPDFPath,
                        PDFImagesPath=PDFImagesPath,
                        FilteredPDFImagesPath=FilteredPDFImagesPath,
                        filterPhrases=filterPhrases,
                        poppler_path=poppler_path)
'''
'''
for filteredPage in os.listdir(FilteredPDFImagesPath):
    textArrays = DataMining.dataMine(imagePath=filteredPage,
                        FilteredPDFImagesPath=FilteredPDFImagesPath,
                        LineImagesPath=LineImagesPath,
                        WordImagesPath=WordImagesPath,)

    #DataToTable.dataToTable(textArrays)
'''
textArrays = [['ARCO', 'LIMITED', 'SUBSIDIARIES'], ['CONSOLIDATED', 'INCOME', 'STATEMENT', 'FOR', 'THE', 'YEAR', 'ENDED', '2021'], ['2021', '2020'], ['Note', "£'000", '£000'], ['Turnover', '390,21', '9,968'], ['Cost', 'Sales', '(309,548)', '(244,536)'], ['Gross', 'Profit', '80,671', '75,432'], ['Distribution', 'costs', '(30,526)', '(32,777)'], ['Administrative', 'expenses', '(31', ',669)', '(31', ',924)'], ['Exceptional', 'income'], ['Operating', 'Profit', '8,887', '10,731'], ['(Loss)', 'profit', 'disposal', 'tangible', 'asset(s)', '(287)', '2,888'], ['Profit', 'Before', 'Interest', 'and', 'Taxation', '8,600', '3,61'], ['Interest', 'receivable', 'and', 'similar', 'income'], ['Interest', 'payable', 'and', 'similar', 'expenses', '(330)', '(582)'], ['Profit', 'Before', 'Taxation', '8,299', '13,095'], ['Tax', 'profit', '9a,9c', '(4,306)', '(1,630)'], ['Profit', 'for', 
'the', 'financial', 'year', '13,993', '11,465'], ['CONSOLIDATED', 'STATEMENT', 'COMPREHENSIVE', 'INCOME'], ['FOR', 'THE', 'YEAR', 'ENDED', 'JUNE', '2021'], ['Note', '2021', '2020'], ['£’000', '£’000'], ['Profit', 'for the financial', 'year', '13,993', '11,465'], ['Other', 'comprehensive', 'income', '(expense)'], ['Remeasurement', 'net', 'defined', 'benefit', 'obligation', '14,274'], ['Deferred', 'tax', 'on-defined', 'benefit', 'obligation', '(3,569)', '224'], ['Tax', 'rate', 'change', 'movement', 'deferred', 'tax'], ['‘relating', 'revaluation', 'pension', 'deficit', '543'], ['rate', 'change', 'movement', 'derivatives'], ['Purchase', 'own', 'shares'], ['Current', 'year', 'deferred', 'tax', 'corporation', 'tax', 
'rate', '(433)'], ['Cash', 'flow', 'hedges', '140'], ['Deferred', 'tax', 'cash', 'flow', 'hedge', '(63)', '(27)'], ['Currency', 'movement', 'overseas', 'investments', '148'], ['Other', 'comprehensive', 'income', '(expense)', 'for'], ['the', 'year,', 'net', 'tax', ',986', '(261'], ['Total', 'comprehensive', 'income', 'for', 'the', 'year', '25,979', '11,204']]
print(textArrays)

DataToTable.dataToTable(textArrays)
'''
Deleting the bin folder, and all its contents
This holds all the images used for OCR and so can be deleted to reclaim space
'''
#shutil.rmtree(mainFolder+'\\bin')