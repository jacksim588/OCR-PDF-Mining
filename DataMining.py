import os
import cv2
import numpy as np
import pytesseract
from PIL import Image
import shutil

'''
Function to delete the whole contents of any folder
'''

def deleteFolderContents(folder):
    for filename in os.listdir(folder):
        file_path = os.path.join(folder, filename)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
        except Exception as e:
            print('Failed to delete %s. Reason: %s' % (file_path, e))

'''
Function which, when given a list of numbers, 
returns a list of number pairs representing concurrent numbers
'''
def ranges(data):
    data = sorted(set(data))
    gaps = [[s, e] for s, e in zip(data, data[1:]) if s+1 < e]
    edges = iter(data[:1] + sum(gaps, []) + data[-1:])
    return list(zip(edges, edges))

'''
Function to get a list of pairs of numbers. 
Each pair represents a set of concurrent rows where data is found
this used to extract each line data from the image
'''
def getDataRangesFromImage(imageArray):
    datainrow = []
    #print(len(imageArray))
    i=0
    for line in imageArray:
        #print(line)
        if all(i >= 200 for i in line):
            #print('empty')
            pass
        else:
            #print('found')
            datainrow.append(i)
        i=i+1
    dataRanges = (ranges(datainrow))
    return dataRanges



def dataMine(imagePath,FilteredPDFImagesPath,LineImagesPath,WordImagesPath,wordSpaceLimit=10,wordBuffer=10):

    
        textArrays=[]

        print('Data Mining: ',imagePath)

        image = cv2.imread(FilteredPDFImagesPath+'\\'+imagePath) 
        #create a blank image of the same dimensions as the current image
        blankrow = [255]*len(image[:, :, 0][0]) 

        '''
        Goes through each pixel for each line in the image.
        A line is appended to 'datainrow' if any of its pixels have a value of less than 200
        Values range from 0-255, with 0 being complete black, and 255 being complete white
        This creates a list of pixel rows from the image which contain text
        '''
        dataRanges = getDataRangesFromImage(image[:, :, 0])

        '''
        Cycles through each data range, and so through each line / object found in the page
        '''
        for foundData in dataRanges:
                #print(foundData)
                currentImage = []
                rangeList = list(foundData)

                if rangeList[1] - rangeList[0] > 1: #if there is more than 1 consecutive row with data
                    #print('checking data ranges:')
                    #print(rangeList[0])
                    #print(rangeList[1])
                    #print('image length',len(image[:, :, 0]))
                    '''
                    Adds a buffer to the top and bottom of the data range (If there's space in the page)
                    This improves the OCR text extraction
                    '''
                    if rangeList[0] >=2:
                        lowerBound = (rangeList[0])-2
                    else:
                        lowerBound = 0
                    if rangeList[1] < (len(image[:, :, 0]))-3:
                        upperBound = (rangeList[1])+3
                    else:
                        upperBound = len(image[:, :, 0])

                    

                    '''
                    Exports current data row as image
                    Need to do this as, the function to create a cv2 image object, needed to use OCR,
                    requires a filepath, rather than passing a variable
                    '''
                    for i in range(lowerBound,upperBound): #uses bounds to create image of current data range
                        currentImage.append(image[:, :, 0][i])

                    if currentImage:
                        currentImage = np.asarray(currentImage)
                        #inefficient but needed with OCR package
                        cv2.imwrite(LineImagesPath+'/dataRange'+str(foundData)+".jpeg", currentImage)#saves line as image
                        dataRowImage = cv2.imread(LineImagesPath+'/dataRange'+str(foundData)+".jpeg")#imports image back in
                        '''
                        Transposes the line from horizontal to vertical
                        This allows us to reuse functions to get a list of ranges, defining each word in the row
                        wordSpaceLimit is the variable which controls how many pixels there can be between letters in words
                        wordSpaceLimit has the default value of 10
                        '''
                        imageArray = np.array(dataRowImage[:, :, 0]).T
                        charRanges = getDataRangesFromImage(imageArray)
                        #print(charRanges)

                        consData = []
                        dataRowRanges = []
                        while charRanges:
                            #print('Begining While Loop')
                            #print('charRanges')
                            #print(charRanges)
                            outputList=[]
                            outputList.append(charRanges[0])
                            maxVal = 0
                            '''
                            Checks all Tuples, and if the range of the next tuple starts less than 'wordSpaceLimit' (default 10)
                            pixels away, then the two are combined.
                            Effectively combines all the individual letters in the row into words
                            '''
                            if len(charRanges) > 1:
                                #print('Multiple Tuples Left')
                                for i in range(len(charRanges)):
                                    #print(len(charRanges))
                                    if (i+1 != len(charRanges)) and (charRanges[i+1][0] - charRanges[i][1] <=wordSpaceLimit):
                                        #print(charRanges[i+1][0] - charRanges[i][1] <=10)
                                        outputList.append(charRanges[i+1])
                                        maxVal = i+1
                                    else:
                                        break
                            

                            #print('outputList')
                            #print(outputList)
                            consData.append([outputList])
                            charRanges = charRanges[maxVal+1:]
                        #print(consData)

                        '''
                        dataRowRanges is a list of ranges, each associated to a single word in the line
                        '''
                        for i in consData:
                            dataRowRanges.append((i[0][0][0],i[0][-1][1]))

                        #print(dataRowRanges)

                        j=0
                        '''
                        wordBuffer is the amount of pixels added around the word, so that OCR can read the image more consistantly
                        '''
                        
                        textArray = []
                        for i in dataRowRanges: #for each word in the row

                            currentImage = ((imageArray[i[0]:i[1]].T))#transposes it from vertical, back to horizontal
                            #adds a buffer to the word of 'wordBuffer' pixels. wordBuffer is 10 by default
                            currentImage = np.c_[np.full((len(currentImage), wordBuffer), 255), currentImage, np.full((len(currentImage), wordBuffer), 255) ] 
                            currentImage = np.r_[[currentImage[0]]*wordBuffer,currentImage,[currentImage[-1]]*wordBuffer]
                            
                            im = Image.fromarray(currentImage)#converts the array of the word back to an image
                            if im.mode != 'RGB':
                                im = im.convert('RGB')
                            im.save(WordImagesPath+'\\DataColumnRanges'+str(j)+".jpeg")
                            imageWord = cv2.imread(WordImagesPath+'\\DataColumnRanges'+str(j)+".jpeg")
                            #print('OCR on Image')
                            text = str(pytesseract.image_to_string(imageWord)).rstrip()
                            #print(text)
                            if text !='':
                                textArray.append(text)
                            j+=1
                        
                        print(textArray)
                        if textArray !=[]:
                            textArrays.append(textArray)
                        deleteFolderContents(WordImagesPath)
        deleteFolderContents(LineImagesPath)            
        print(textArrays)
        return textArray

