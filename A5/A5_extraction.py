# Program to extract and arrange the required data from the XML and arrange it into a space delimited format

import xml.etree.ElementTree as ET

#global hash tables to store the word counts and occurrences and the mapping of the ids to the numbers
bag_of_words = {}
cntr_words = 0
id_mapping = {}
cntr_id = 0


##===============================================

def writeToNewFile(slicedData):
    outputFile = open("a3.train","w")

    print bag_of_words

    for element in slicedData:
        length = len(element)
        print element
        line = element[1]
        for item in element[len(element)-1]:
            line += " "+str(bag_of_words[item])+":1"
        
        print line
        outputFile.write(line)
        outputFile.write("\n")

    outputFile.close()

##===============================================

def removePunctuations(strList):
    punctuation = [".",")","(","","-"]
    # convert each string to lowercase, for better matching
    newList = [item.lower() for item in strList if item not in punctuation]
    return newList

##===============================================


def extractFeatures(context):
    global bag_of_words, cntr_words, id_mapping, cntr_id

    # Split the string based $$head$$ as it differentiates the word we are looking for from the rest of the string
    context = context.split("$$head$$")

    ## We split the first and the last part to get the relevant features (words)
    part1 = context[0].split(" ")
    part2 = context[2].split(" ")

    #clean the lists to represent what we want. Removing empty strings, punctuations
    # We keep commas as suggested by Professor
    newpart1 = removePunctuations(part1)
    newpart2 = removePunctuations(part2)

    # Enter into the appropriate dictionaries
    if bag_of_words.get(newpart1[-2],"NA") == "NA":
        bag_of_words[newpart1[-2]] = cntr_words + 1
        cntr_words +=1
        

    if bag_of_words.get(newpart1[-1],"NA") == "NA":
        bag_of_words[newpart1[-1]] = cntr_words + 1
        cntr_words +=1

    if bag_of_words.get(newpart2[0],"NA") == "NA":
        bag_of_words[newpart2[0]] = cntr_words + 1
        cntr_words +=1

    if bag_of_words.get(newpart2[1],"NA") == "NA":
        bag_of_words[newpart2[1]] = cntr_words + 1
        cntr_words +=1

    return [newpart1[-2],newpart1[-1],newpart2[0],newpart2[1]]
    
    

##===============================================


if __name__ == "__main__":

    document = "ajTrain.train"

    fileOpen = open(document,"r")

    fileData = ""

    flag = False
    
    for line in fileOpen:
        #print line
        if ("activate.v" in line): #or ("difficulty.n" in line) or ("interest.n" in line) :
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
                    if sub.text.count("$$head$$") > 2:
                        index1 = sub.text.index("$$head$$")
                        index2 = sub.text.replace('$$head$$', 'XXX', 1).find('$$head$$')
                        context = sub.text[0:index1-1] + sub.text[index+8:index2] + sub.text[index2+8:]
                        xmlElem.append(extractFeatures(sub.text))
                    else:
                        xmlElem.append(extractFeatures(sub.text))
                
            xmlSlicedData.append(xmlElem)

    
    print xmlSlicedData,"\n\n\n"

    # Extract the features

    writeToNewFile(xmlSlicedData)



    
    
    
