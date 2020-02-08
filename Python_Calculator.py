import re
global workingArray
global workingArray1
global solvingArray
global parenthesisCount
global currentPar
global i
global inputString
global inputArray
global closeParCount

# Declare your functions here
#(1+1(1+2))-((1+3)(1+4))
def start():
    workingArray = []
    workingArray1 = []
    solvingArray = []
    parenthesisCount = 0
    currentPar = 0
    i = 0
    closeParCount = 0
    inputString = input("Enter your equation: ")
    #r"(?<!\d)\d{4,7}(?!\d)"
    inputArray = re.findall(r"[\d\+\-\*\/\(\)\^]", inputString)
    touchUps(inputArray, workingArray1, currentPar, parenthesisCount, closeParCount)

def touchUps(inputArray, workingArray1, currentPar, parenthesisCount, closeParCount):
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

    #Check for a negative in the beginning
    if inputArray[0] == "-" :
        trash = inputArray.pop(0)
        inputArray[0] = -int(inputArray[0])

    #Check for negative numbers
    inputArray = twoOperatorsCheck(inputArray, '-')

    inputArray = findParenthesis(inputArray, workingArray1, currentPar, parenthesisCount)          


def multipleDigits(inputArray, a):
    if a >= len(inputArray)-1:
        return
    doubleDigit1 = re.match(r"[\d]", inputArray[a])
    doubleDigit2 = re.match(r"[\d]", inputArray[a+1])
    if doubleDigit1 and doubleDigit2:
        inputArray[a] += inputArray[a+1]
        trash = inputArray.pop(a+1)
        multipleDigits(inputArray, a)

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
            #Puts the result of workingArray1 into inputArray
            if i == 0 or i > 0 and inputArray[i-1] == '(':
                #inputArray.insert(i, '*')
                #!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
                #!!!!!  I F  T H I N G S  D O N T  A D D  U P  R I G H T !!!!!
                #!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
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

def solveAndShow(inputArray, parenthesisCount):

    output = solveEquation(inputArray)
    print(output)
    start()

# Solving time!
#Check for multiple digits

start()