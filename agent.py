###################################
########### AUTHORSHIP ############
## Created by: Ushini Attanayake ##
######### Date: 31.05.2019 ########
###################################



import numpy as np 
import random
import argparse
import math
import socket 
import msvcrt

from _thread import *

UDP_IN_IP = '127.0.0.1' 
UDP_PORT = 5005
num_queued_msgs = 5
address = (UDP_IN_IP, UDP_PORT)

####################################
######## Markov Chain Agent ########
####################################

class MCAgent():
    ''' States in Markov Chain: 
            Thin melody: removes pitches randomly [0]
            rotate list [1] 
            Invert list [2]
            Retrograde: reverse [3]
            Repetition: repeats segments within the melody [4]

    '''
    transition_matrix = np.array([[0.05, 0.22, 0.26, 0.27, 0.20], 
                                  [0.22, 0.12, 0.16, 0.20, 0.30],
                                  [0.12, 0.32, 0.18, 0.41, 0.21],
                                  [0.21, 0.25, 0.17, 0.12, 0.25],
                                  [0.18, 0.29, 0.19, 0.26, 0.08]])

    def __init__(self):
        self.previous_state = None
        self.current_state = None
        self.current_list = None
        self.pattern_prefix = None
        self.pattern_str = None
        self.p_tree = None
        self.error = None

    def __repr__(self):
        return str(self.transition_matrix)
    
    # determines the next operation which will be applied to the pattern based on the transition probabilities.
    # updates the self.current_state to the resulting state of this transition.
    def transition(self):        
        # if a valid previous state exists, transition to a new state
        if(self.previous_state is not None):
            self.current_state = np.random.choice([0, 1, 2, 3, 4], 1, p=self.transition_matrix[self.previous_state])
            return None
        else:
            return "invalid pattern format"

    # updates pattern in agent's memory
    def update_root_pattern(self, pattern):
        parser = PatternParser() 
        self.pattern_str = pattern
        self.previous_state, self.pattern_str, self.pattern_prefix = parser.extract_current_op_ind(pattern)
        if(self.previous_state == self.pattern_str == self.pattern_prefix == None):
            self.error = "Error: invalid pattern"
        else: 
            self.p_tree = PatternTree()
            print("list string before tree: "+str(self.pattern_str))
            self.p_tree.build_tree(self.pattern_str[1:len(self.pattern_str)], 0)
            print("tree: "+str(self.p_tree))
            print("merged tree: "+str(self.p_tree.merge()))
            pattern_string = self.pattern_str.replace('(', '( ')
            pattern_string = pattern_string.replace(')', ' )')
            self.current_list = pattern_string.split(" ")

    # modifies pattern by applying operations determined by the markov chain
    def get_new_pattern(self):
        if(not self.transition()):
            # Thin state. create tree and add rests
            if (self.current_state == 0):
                self.p_tree = PatternTree()
                self.p_tree.build_tree(self.pattern_str[1:len(self.pattern_str)], 0)
                self.p_tree.add_rests1() 
                new_pattern_str = self.p_tree.merge()
                return self.pattern_prefix+"'"+new_pattern_str+")"
            # Rotate state
            elif (self.current_state == 1):
                new_pattern_str = " ".join(self.current_list) 
                new_pattern_str = new_pattern_str.replace("( ", "(")
                new_pattern_str = new_pattern_str.replace(" )", ")")
                return self.pattern_prefix+"(rotate '"+self.pattern_str+" (random '(-3 -1))))" 
            # Invert state
            elif (self.current_state == 2):
                last_old_pitch = None
                last_new_pitch = None
                for i in range(len(self.current_list)):
                    if(not (self.current_list[i] == '#(' or self.current_list[i] == '(' or self.current_list[i] == ')' or self.current_list[i] == '_' or self.current_list[i] == ' ')):
                        if(last_old_pitch == None and last_new_pitch == None): 
                            try:
                                last_old_pitch = int(self.current_list[i])
                                last_new_pitch = int(self.current_list[i])
                            except ValueError:
                                self.error = "Error: pitch list contains non-numeric values"
                                return self.error
                        else:
                            try:
                                current_pitch = int(self.current_list[i])
                            except ValueError: 
                                self.error = "Error: pitch list contains non-numeric values"
                                return self.error
                            p = last_new_pitch + last_old_pitch - current_pitch
                            last_new_pitch = p
                            last_old_pitch = current_pitch
                            self.current_list[i] = str(p)
                new_pattern_str = " ".join(self.current_list)
                new_pattern_str = new_pattern_str.replace('( ', '(')
                new_pattern_str = new_pattern_str.replace(' )', ')')
                return self.pattern_prefix+"'"+new_pattern_str+")"
            elif (self.current_state == 3):
                new_pattern_str = " ".join(self.current_list)
                new_pattern_str = new_pattern_str.replace('( ', '(')
                new_pattern_str = new_pattern_str.replace(' )', ')')
                return self.pattern_prefix+"(reverse '"+new_pattern_str+"))"
            elif (self.current_state == 4):
                ind1 = random.randint(0, len(self.p_tree.children))
                ind2 = random.randint(0, len(self.p_tree.children))
                repeat_sect = [self.p_tree.children[i] for i in range(min(ind1, ind2), max(ind1, ind2))]
                self.p_tree.children[min(ind1, ind2):min(ind1, ind2)] = repeat_sect
                new_pattern_str = self.p_tree.merge()
                return self.pattern_prefix+"'"+new_pattern_str+")"
            else: 
                pass
        else: 
            return "Error: invalid pattern format"


########################################################
######## Class For Extracting List From Pattern ########
########################################################

class PatternParser():
    def __init__(self):
        pass
        self.pattern_prefix = None

    def isValid(self, pattern):
        #checks for balanced parentheses
        p_count = 0
        for i in range(len(pattern)):
            if(pattern[i] == '('):
                p_count += 1
            if(pattern[i] == ')'):
                p_count -= 1
        return ('play' in pattern and pattern[len(pattern) - 1] == ')' and ':' in pattern and '@' in pattern and p_count == 0 and (('list' in pattern) or ("`" in pattern) or ("'" in pattern)))
        
    # given a pattern, extracts the substring which identifies the operation applied to the list/pattern
    # assumes pattern is in the form start-name-rep-offset-playfunc-list) where the list is some array
    def extract_current_op_ind(self, pattern):
        #removes all text from the pattern except the list
        #Check balanced parentheses
        if(self.isValid(pattern)):
            pattern = pattern.strip()
            play_end_ind = pattern.index('y')
            while(pattern[play_end_ind] is not ')'):
                play_end_ind += 1
            play_end_ind += 2
            # separates pitch list from rest of pattern
            self.pattern_prefix = pattern[0:play_end_ind]
            extracted_list = pattern[play_end_ind:len(pattern)-1]
            extracted_list =  extracted_list.replace('list ', '')
            extracted_list =  extracted_list.replace("`", '')
            extracted_list =  extracted_list.replace("'", '')
            extracted_list =  extracted_list.replace(",", '')
        else: 
            return (None, None, None)
        if('reverse' in extracted_list):
            extracted_list = extracted_list.replace('reverse ', '')
            extracted_list = extracted_list[1:len(extracted_list)-1]
            return (3, extracted_list, self.pattern_prefix)
        elif('rotate' in extracted_list):
            list_start = extracted_list.index("rotate")+7
            list_end = list_start
            while(extracted_list[list_end] is not ')'):
                list_end += 1
            extracted_list = extracted_list[list_start:list_end + 1]
            return (1, extracted_list, self.pattern_prefix)    
        #assumes the first pattern which is sent is a simple list (no nesting or added functions)
        #no function keywords found in list. Could go to invert, thin or repeat.
        else: 
            current_state = np.random.choice([0,2,4])
            return (current_state, extracted_list, self.pattern_prefix)

class PatternTree():
    def __init__(self):
        self.Node = None
        self.children = []

    def insert(self, data):
        pass

    def extract_nested_list(self, index):
        pass

    def __repr__(self):
        return str(self.Node)+" : "+str(self.children)

    def build_tree(self, pattern_str, ind):
        child_string = ''
        i = ind
        while i < len(pattern_str):
            if (pattern_str[i] == "("):
                if(not child_string == ''):
                    p_list = child_string.strip().split(" ")
                    for p in p_list:
                        leaf_node = PatternTree()
                        leaf_node.Node = p
                        self.children.append(leaf_node)
                    child_string = ''
                if (i + 1 <= len(pattern_str)):
                    # returns the new index
                    subtree = PatternTree()
                    i = subtree.build_tree(pattern_str, i + 1)
                    self.children.append(subtree)
                    continue
            elif(pattern_str[i] == "#"):
                if(not child_string == ''):
                    p_list = child_string.strip().split(" ")
                    for p in p_list:
                        leaf_node = PatternTree()
                        leaf_node.Node = p
                        self.children.append(leaf_node)
                    child_string = ''
                if (i + 1 <= len(pattern_str)):
                    # returns the new index
                    subtree = PatternTree()
                    subtree.Node = "#"
                    i = subtree.build_tree(pattern_str, i + 2)
                    self.children.append(subtree)
                    continue
            elif (pattern_str[i] == ")"):
                if(not child_string == ''):
                    p_list = child_string.strip().split(" ")
                    for p in p_list:
                        leaf_node = PatternTree()
                        leaf_node.Node = p
                        self.children.append(leaf_node)
                    child_string = ''
                return i+1
            else:
                child_string = child_string + pattern_str[i]
            i += 1
        return len(pattern_str)

    def merge(self):
        list_string = ''
        if(self.Node == None):
            list_string = list_string + '('
        elif(self.Node == "#"):
            list_string = list_string + "#("
        else: 
            list_string = self.Node+" "
        if(not self.children == []):
            for i in range(len(self.children)):
                child_string = self.children[i].merge()
                if(not child_string[0] == ')' and list_string[len(list_string)-1] == ')'):
                    list_string = list_string+" "+child_string
                else: 
                    list_string = list_string+child_string
                if(i == len(self.children)-1):
                    if(list_string[len(list_string)-1] == " "):
                        list_string = list_string[0:len(list_string)-1]+')' 
                    else:
                        list_string = list_string + ')'
        return list_string

    def add_rests(self):
        num_rests = random.randint(1,len(self.children) - 1)
        for i in range(num_rests):
            p = PatternTree()
            p.Node = "_"
            self.children[i] = p
        return None

    def add_rests1(self):
        num_rests = 0
        if(len(self.children) > 2):
            num_rests = max(1, int(len(self.children)*random.choice([0.25, 0.5])))
        elif(len(self.children) == 2): 
            num_rests = 1
        else: 
            pass
        for i in range(num_rests):
            j = random.randint(0, max(len(self.children)-1, 1))
            if(not self.children == []):
                if(self.children[j].Node == None):
                    self.children[j].add_rests1()
                if(self.children[j].Node == '#'):
                    print("found chord")
                    self.children[j].Node = "_"
                    self.children[j].children = []
                else:
                    self.children[j].Node = "_"
        return None

def editor_client(client, address, agent):
    print("in new editor client thread: "+str(addr))
    while True:
        print(".")
        data = client.recv(1024)
        print("received pattern: "+data.decode('utf-8'))
        if(data.decode('utf-8') is not ''):
            if(not data.decode('utf-8') == 'change'):
                agent.update_root_pattern(data.decode('utf-8'))
            new_pattern = agent.get_new_pattern()
            print("new pattern: "+new_pattern)
            reply = new_pattern 
            client.send(str.encode(reply))
        if not data: 
            break
        if msvcrt.kbhit():
	        if ord(msvcrt.getch()) == 27:
	             break
    client.close()
    return None

# creates a new socket.   
extemp_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
try:
    extemp_sock.bind(address)
except socket.error as e: 
    print(str(e))

extemp_sock.listen(num_queued_msgs)
print("listening for messages...")

# whenever a message is received from the client, create a new thread on 
# which the agent can serve (return a new pattern string)
while True: 
    client, addr = extemp_sock.accept()
    print('connected to: '+addr[0]+':'+str(addr[1]))
    agent = MCAgent()
    start_new_thread(editor_client, (client, addr, agent))