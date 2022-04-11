'''
Library Imports
'''
import cv2
import os
import pytesseract
from pdf2image import convert_from_path
import time


def filterPDFs(downloadPath,unfilteredPDFPath,PDFImagesPath,FilteredPDFImagesPath,filterPhrases,poppler_path):

    print('filtering PDF: ',unfilteredPDFPath)
    filteredPages = [] #list to hold pages with relevant key words
    print(downloadPath+'\\'+unfilteredPDFPath)
    print('converting PDF pages to images')
    pages = convert_from_path(downloadPath+'\\'+unfilteredPDFPath, 350,poppler_path=poppler_path) #converts a PDF to a list of images
    print(pages)
    #Useful for bug testing, can be commented out
    print('Searching Pages for Data')
    print('Number of pages being searched: ', len(pages))

    imageCount = 0 #cv2 requires an image path, so the image is stored locally using image count as name
    cumulateArray = [] #Stores the extracted Data from the filtered PDF Pages
    i=0
    for page in pages:
        imageCount+=1
        print('Filtering Page: ',imageCount)
        pageStart = time.time()
        imagePath = PDFImagesPath+'\\page'+str(imageCount)+'.jpg'
        print('Page Saved')
        page.save(imagePath,'JPEG') #saves image as jpeg to temp storage
        image = cv2.imread(imagePath) #imports image as cv2 image object
        text = str(pytesseract.image_to_string(image)).lower() #Uses OCR to extract text (as lower case) from the page as a string
        print('Checking for filter phrases')
        if any(word in text for word in filterPhrases): #if any of the filtered phrases are in the page
            page.save(FilteredPDFImagesPath+'\\page'+str(imageCount)+'.jpg','JPEG')
        