# Program to extract and arrange the required data from the XML and arrange it into a space delimited format

import xml.etree.ElementTree as ET

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

    xmlSlicedData = []
    
    ## Start XML processing now
    root = ET.fromstring(fileData)
    element = root.getiterator()

    for item in element:
        if item.tag == "instance":
            xmlElem = []
            subRoot = item.getiterator()
            for sub in subRoot:
                if sub.tag == "instance":
                    xmlElem.append(sub.attrib["id"])
                elif sub.tag == "answer":
                    xmlElem.append(sub.attrib["senseid"])
                elif sub.tag == "context":
                    xmlElem.append(sub.text)
            xmlSlicedData.append(xmlElem)


    print xmlSlicedData[0]
    print xmlSlicedData[1]
    
    
    
