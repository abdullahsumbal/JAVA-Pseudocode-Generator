#!/usr/bin/python

import re
import random
import sys
import copy

# - variables
round_brackets_stack = []
curly_brackets_stack = []
comments = ""

# - data types
dataTypes = ['int', 'char' , 'boolean', 'String','long','void']

# - read java code
input = open('java','r')
allJavaCode = input.read()

# - remove comments
for i in range(0,len(allJavaCode)):
    if i <len(allJavaCode)-1   and allJavaCode[i] == "/" and allJavaCode[i+1] == "/":
        while allJavaCode[i] != "\n":
            comments =  comments + allJavaCode[i] 
            i = i +1

        allJavaCode =  allJavaCode.replace(comments,'')
    comments = ""

print allJavaCode

# - check for the opening and closing brackets
for i in range(0,len(allJavaCode)):
    if allJavaCode[i] == '(':
        round_brackets_stack.append("(")
    if allJavaCode[i] == ')':
        try: 
            round_brackets_stack.pop()
        except:
            print "missing a round bracket "
            sys.exit()

    if allJavaCode[i] == '{':
        curly_brackets_stack.append("{")
    if allJavaCode[i] == '}':
        try:
            curly_brackets_stack.pop()
        except:
            print "curly bracket missing"
            sys.exit()


if len(round_brackets_stack) == 0 and len(curly_brackets_stack) == 0:
    print "your brackets are good"
else:
    print "check your brackets"
    sys.exit()


# - find the name of method
methodDecalration = re.findall(r'.*[public,private]?\s*[static]?\s*\w+\s*[\[]?\s*[\]]?\s+[a-zA-Z,\_,\$]{1}\w*\s*\(.*\)',allJavaCode)
if len(methodDecalration) > 1:
    print "please make sure there is only one method"
    sys.exit()
elif len (methodDecalration)==1:
    open_round_bracket_index = methodDecalration[0].index("(")
    for i in range(0,len(methodDecalration[0])):
        if methodDecalration[0][i] == " " and i < open_round_bracket_index-1:
            if " " not in methodDecalration[0][i:open_round_bracket_index].strip() :
                space_index = i
    method_name = methodDecalration[0][space_index:open_round_bracket_index].strip()

# - find the input of the method
if len (methodDecalration)==1:
    close_round_bracket_index = methodDecalration[0].index(")")
    inputs = methodDecalration[0][open_round_bracket_index+1 :close_round_bracket_index].strip() 
    raw_input_list = inputs.split(',')
    input_list = []
   
    for input in raw_input_list:
        input = input.strip()
        for i in range(0,len(input)):
            if input[i] == " ":
                if " " not in input[i+1:len(input)]:
                    space_index = i
        input_list.append(input[space_index:len(input)].strip())

# - the convert everything inside the method

def convert(allJavaCode, spaces,method_content):
    method_start = allJavaCode.index("{")
    index = 1
    while allJavaCode[len(allJavaCode)-index] != "}":
        index = index + 1
        method_end = len(allJavaCode) - index
         
    raw_method_content = allJavaCode[method_start+1:method_end].strip()
    inst_list = raw_method_content.split(";")

    # - for condition helper vaiables
    forinit = 0
    forterm = 0
    forincr = 0
    fornum1 =0 
    fornum2 =0
    collecting_condition = 0
    code_collecting = ""

    for inst in inst_list:
        inst =  inst.strip()

        # colelcting code
        if collecting_condition == 1:
            code_collecting = code_collecting + inst
            if "}" in inst:
                collecting_condition = 0
                print code_collecting
                
              

        # - for loop condition
        if re.split(r'\s\(',inst)[0] == "for" or forinit == 1 or forterm == 1 or forincr == 1 and collecting_condition == 0:
            forinit = 1
            
            if forincr == 1:
                forint = 0
                forincr = 0
                forterm = 0
                collecting_condition = 0
                method_content.append("Repeat "+ str(fornum2 - fornum1)+" times")
                
                # -  int statment for 
                if re.split(r'\{',inst):
                    print re.split(r'\{',inst)[1]

                
            if forterm == 1:
                forincr = 1
                forterm = 0
                forinit = 0
                if re.match(r'.*\<\s*\d+',inst):
                    fornum2 = int(re.split(r'\<',inst)[len(re.split(r'\<',inst))-1])
                if re.match(r'.*\<\=.*',inst):
                    fornum2 = int(re.split(r'\<\=',inst)[len(re.split(r'\<\=',inst))-1])+1


            if forinit == 1 :
                forterm = 1
                forinit = 0
                forincr = 0
                if re.match(r'.*\=.*',inst):
                    fornum1 = int(re.split(r'\=',inst)[len(re.split(r'\=',inst))-1])
                

        # - system.out.print statments
        if "System.out.print" in inst and collecting_condition == 0:
            print_to_screen = re.findall(r'\".*\"',inst)
            
            print_to_screen[0] = "Print "+ print_to_screen[0]
            method_content.append(print_to_screen[0])




        # - int statments
        if re.split(r'[\s]',inst)[0] == "int" and "[]" not in inst and collecting_condition == 0:
            int_variable_name = re.split(r'\s',inst)[1]
            if "=" in inst:
                int_value = re.split(r'=',inst)[1].strip()
                method_content.append(int_variable_name+u" \u2190 "+int_value)
                
        # - char statement
        if re.split(r'\s',inst)[0] == "char" and "[]" not in inst and collecting_condition == 0:
            char_variable_name = re.split(r'\s',inst)[1]
            if "=" in inst:
                char_value = re.split(r'=',inst)[1].strip()
                method_content.append(char_variable_name+u" \u2190 "+char_value)




method_content = []
convert(allJavaCode,0,method_content)


        

print "----------------------------------------------------"
print "Algothrim:" + method_name
print "----------------------------------------------------"
print "INPUT: " + ", ".join(input_list)
print "OUPUT: "

print "----------------------------------------------------\n"
for inst in method_content:
    print inst

