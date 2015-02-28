# Program to extract and arrange the required data from the XML and arrange it into a space delimited format

import xml.etree.ElementTree as ET

##===============================================

def removePunctuations(strList):
    punctuation = [".",")","(","","-"]
    newList = [item for item in strList if item not in punctuation]
    return newList

##===============================================


def extractFeatures(context):
    # Split the string based $$head$$ as it differentiates the word we are looking for from the rest of the string
    context = context.split("$$head$$")

    ## We split the first and the last part to get the relevant features (words)
    part1 = context[0].split(" ")
    part2 = context[2].split(" ")

    #clean the lists to represent what we want. Removing empty strings, punctuations
    # We keep commas as suggested by Professor
    newpart1 = removePunctuations(part1)
    newpart2 = removePunctuations(part2)


    # Create a new dictionary and enter the features
    featureSet = {}

    featureSet["w-2"] = newpart1[-2]
    featureSet["w-1"] = newpart1[-1]
    featureSet["w+1"] = newpart2[0]
    featureSet["w+2"] = newpart1[1]
    featureSet["w-2w-1"] = newpart1[-2]+newpart1[-1]
    featureSet["w-1w+1"] = newpart1[-1]+newpart2[0]
    featureSet["w+1w+2"] = newpart2[0]+newpart2[1]
    
    return featureSet
    

##===============================================


if __name__ == "__main__":

    document = "ajTrain.train"

    fileOpen = open(document,"r")

    fileData = ""

    flag = False
    
    for line in fileOpen:
        #print line
        if "activate.v" in line:
            #print "activated"
            flag = True
        if flag == True:
            fileData += line.strip("\n")
        if "</lexelt>" in line:
            #print "deactivated"
            flag = False

    
    fileData = "<startDoc>" + fileData + "</startDoc>"

    fileOpen.close()    

    # replace all the <head> --> <<head>> and all the </head> tags to <<head>>
    fileData = fileData.replace("<head>","$$head$$").replace("</head>","$$head$$")
    
    #print fileData

    xmlSlicedData = []
    
    ## Start XML processing now
    root = ET.fromstring(fileData)
    element = root.getiterator()

    for item in element:
        if item.tag == "instance":
            #print item.find('context').text
            #print "\n\n"
            xmlElem = []
            subRoot = item.getiterator()
            for sub in subRoot:
                if sub.tag == "instance":
                    xmlElem.append(sub.attrib["id"])
                elif sub.tag == "answer":
                    xmlElem.append(sub.attrib["senseid"])
                elif sub.tag == "context":
                    xmlElem.append(extractFeatures(sub.text))
                
            xmlSlicedData.append(xmlElem)

    
    print xmlSlicedData[0]
    print xmlSlicedData[1]

    # Extract the features

    writeToNewFile(xmlSlicedData)


##============================

def writeToNewFile(xmlSlicedData):
    outputFile = open("a3.train","w")
     
    
    
    
