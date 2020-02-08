import re
#Honestly, I'm not sure if these declarations are even necessary...
global workingArray
global workingArray1
global solvingArray
global parenthesisCount
global currentPar
global i
global inputString
global inputArray
global closeParCount

# Start
def start():
    workingArray = []
    workingArray1 = []
    solvingArray = []
    parenthesisCount = 0
    currentPar = 0
    i = 0
    closeParCount = 0
    
    inputString = input("Enter your equation: ")
    inputArray = re.findall(r"[\d\+\-\*\/\(\)\^]", inputString)
    
    touchUps(inputArray, workingArray1, currentPar, parenthesisCount, closeParCount)

def touchUps(inputArray, workingArray1, currentPar, parenthesisCount, closeParCount):
    
    #Look for multiple number digits and count up the amount of parenthesis. Give parenthesis error if number of open and closed parenthesis are uneven
    #Will most likely be changed to ignore that and still give correct answers   
    for b in range (len(inputArray)):
        if b >= len(inputArray)-1 :
            for a in range (len(inputArray)):
                if inputArray[a] == '(':
                    parenthesisCount += 1
                if inputArray[a] == ')':
                    closeParCount += 1
                if a >= len(inputArray)-1:
                    if parenthesisCount != closeParCount:
                        print('Parenthesis Error')
                        start()
                    break
            break
        multipleDigits(inputArray, b)

    #Check for a negative in the beginning of the string
    if inputArray[0] == "-" :
        trash = inputArray.pop(0)
        inputArray[0] = -int(inputArray[0])

    #Check for negative numbers
    inputArray = twoOperatorsCheck(inputArray, '-')
    #Check for parenthesis and solve them.
    inputArray = findParenthesis(inputArray, workingArray1, currentPar, parenthesisCount)          

#Puts multiple digit numbers that have been split up in the array together again
def multipleDigits(inputArray, a):
    if a >= len(inputArray)-1:
        return
    doubleDigit1 = re.match(r"[\d]", inputArray[a])
    doubleDigit2 = re.match(r"[\d]", inputArray[a+1])
    if doubleDigit1 and doubleDigit2:
        inputArray[a] += inputArray[a+1]
        trash = inputArray.pop(a+1)
        multipleDigits(inputArray, a)
        
#Function to check for double negatives or weird combinations like *- or +*
def twoOperatorsCheck(workingArray, badOperator):
    for f in range (len(workingArray)) :
         if f == len(workingArray):
            break
         if str(workingArray[f]) in ['+', '-', '*', '/', '('] and str(workingArray[f+1]) == badOperator :
            del workingArray[f+1]
            if badOperator == '-':
                workingArray[f+1] = -int(workingArray[f+1])
    return workingArray


# Search for '(' put the equation inside that into a workingArray until ')'. Solve that equation. Put it back in with a * in front. It may look like 1+*3 so look for doubleNegatives except look
# for * after all parenthesis have been found and solved.
def findParenthesis(inputArray, workingArray1, currentPar, parenthesisCount):
    i = 0
    currentPar = 0
    
    for i in range (len(inputArray)-1):
        if parenthesisCount > 0:
            if parenthesisCount > 0 and inputArray[i] == '(':
                workingArray1 = []
                currentPar += 1
                if currentPar == parenthesisCount :

                    inputArray = solveParenthesis(inputArray, i, workingArray1, currentPar, parenthesisCount)
                    parenthesisCount = parenthesisCount - 1
                    findParenthesis(inputArray, workingArray1, currentPar, parenthesisCount)
        else:
            break
    solveAndShow(inputArray, parenthesisCount)


def solveParenthesis(inputArray, i, workingArray1, currentPar, parenthesisCount):

    for y in range (len(inputArray)-i-1):
        if str(inputArray[i+y+1]) != ')' :
            workingArray1.append(inputArray[i+y+1])
        else:     
            #Deletes the parenthesis and its contents and replaces it with the result of workingArray1
            for z in range (len(workingArray1)+2):           
                if z == len(workingArray1)+2:
                    break
                trash = inputArray.pop(i)
            #SOLVE THE EQUATION INTO workingArray1!!!!
            workingArray1 = solveEquation(workingArray1)
            #Puts the result of workingArray1 back into inputArray
            if i == 0 or i > 0 and inputArray[i-1] == '(':
                #Fills inputArray if it is empty to prevent errors. It will times by 1 to prevent wrong answers. In all my testing, it doesn't screw something up so far.
                if inputArray == [] :
                    inputArray = [1]
                if inputArray[i] :
                    if str(inputArray[i]) not in ['+', '-', '*', '/', ')']:
                        inputArray.insert(i, '*')
                inputArray.insert(i, workingArray1)
               # trash = inputArray.pop(i)
            elif len(inputArray) == i:
                inputArray.insert(i, workingArray1)
                inputArray.insert(i, '*')             
            else:
                inputArray.insert(i, '*')
                if inputArray[i+1] :
                    if str(inputArray[i+1]) not in ['+', '-', '*', '/', ')']:
                        inputArray.insert(i+1, '*')
                inputArray.insert(i+1, workingArray1)
            inputArray = twoOperatorsCheck(inputArray, '*')
            return inputArray
            
def solveEquation(solvingArray):
    
    #This loop solves exponents
    k = 0
    while k < len(solvingArray):
        
        if k >= len(solvingArray):
            break

        if solvingArray[k] == '^':
            input1 = float(solvingArray.pop(k-1))
            operator = solvingArray.pop(k-1)
            input2 = float(solvingArray.pop(k-1))
            input1 = float(input1)**float(input2)
            solvingArray.insert(k-1, input1)
            if k == len(solvingArray) :
                break
            k -= 1
        k += 1
    #This loop solves both multiplication and division
    g = 0
    while g < len(solvingArray):
        if solvingArray[g] == '*':

            input1 = float(solvingArray.pop(g-1))
            operator = solvingArray.pop(g-1)
            input2 = float(solvingArray.pop(g-1))
            input1 = float(input1) * float(input2)
            solvingArray.insert(g-1, input1)

            if g == len(solvingArray) :
                break
            g -= 1


        if solvingArray[g] == '/': 
            input1 = float(solvingArray.pop(g-1))
            operator = solvingArray.pop(g-1)
            input2 = float(solvingArray.pop(g-1))
            input1 = float(input1) / float(input2)
            solvingArray.insert(g-1, input1)

            if g == len(solvingArray) :
                break
            g -= 1
            
        g += 1

    #This loop finishes it off by doing the addition and subtraction.
    numOfOperators = int((len(solvingArray) - 1) / 2)
    input1 = float(solvingArray.pop(0))
    for c in range (numOfOperators) :

        operator = solvingArray.pop(0)
        input2 = float(solvingArray.pop(0))
        if operator == "+" :
            input1 = float(input1) + float(input2)
        if operator == "-" :
            input1 = float(input1) - float(input2)

    
    return(input1)
#This takes the full array after parenthesis are taken care of and runs it through the solveEquation function and then goes back to the prompt.
def solveAndShow(inputArray, parenthesisCount):

    output = solveEquation(inputArray)
    print(output)
    start()

#This starts it all off
start()
