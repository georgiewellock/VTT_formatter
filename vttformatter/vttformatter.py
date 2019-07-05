__version__ = '1.0'
import numpy as np
import os
import re


class VttFormatter:
    """ 
    The Vtt Formatter class takes an .vtt file as the input and converts it to a reformatted .txt file with the timestamps and identifiers removed 

    Args:
        filename (str): The name of the .vtt file to be reformatted. Include full path if file not in working directory

    """

    def __init__( self, filename ):
        self.filename = filename

    def import_file( self ):
        """ Opens the .vtt file and creates a list of lines """
        #open the file
        try:
            with open(self.filename) as file:
            #create a list containing each line in the file
                 self.data = [line for line in file]
        except FileNotFoundError:
            raise FileNotFoundError
        if not self.data[0].startswith('WEBVTT'):
            raise NameError('Incorrect file type, file does not start with WEBVTT') 

    def create_dictionary( self ):
        """ Assigns each item in the list of lines from the .vtt file to a relevant dictionary element. """
        #create data list
        self.import_file()
        #initialise an empty dictionary
        data_dict = {}
        #initialise an empty dictionary element for messages as it will be a nested dictionary
        data_dict['messages'] = []
        #loop over each line in the list and assign the value to a relevent dictionary element 
        for i, line in enumerate(self.data):
            if line.startswith( 'NOTE duration' ):
                data_dict['duration'] = line.split(':"')[1].strip()
                pattern = re.compile(r'[0-9]{2}:[0-9]{2}:[0-9]{2}.[0-9]{7}')
                if not pattern.match(data_dict['duration']):
                    raise ValueError('duration not in correct format')
            if line.startswith( 'NOTE language' ):
                data_dict['language'] = line.split(':')[1].strip()
            if line.startswith('NOTE Confidence'):
                data_dict['messages'].append(self.read_message(i))
        self.data_dict = data_dict
#        with open( 'data/test_data_dict.yml', 'w', encoding='utf8') as fp:
#            yaml.dump(self.data_dict, fp, default_flow_style=False, allow_unicode=True)
        return self.data_dict
        print(my_message['start'])

    def read_message( self, i ):
        """
        Loops through the list of file lines starting at a given index until the is a line break. Taken as a message item, containing a confidence level, uuid, timestamp and content and creates a dictionary.
        Args:
            i (int): Index for the start of the message item
        Returns:
            my_message (dict): dictionary containing the elements of each message item
        """

        #initialise an empty dictionary
        my_message={}
        #loop over specific lines in the list based on a given index and assign the value to a relevent dictionary element
        my_message['confidence']= self.data[i].split(':')[1].strip()
        pattern1 = re.compile(r'[0-1]{1}.[0-9]{14}')
        pattern2 = re.compile(r'[0-1]{1}.[0-9]{13}')
        if not pattern1.match(my_message['confidence']):
            if not pattern2.match(my_message['confidence']):
                raise ValueError('Confidence value not in correct format')
        i+=2
        my_message['marker'] = self.data[i].strip()
        pattern = re.compile(r'[0-9a-f]{8}(?:-[0-9a-f]{4}){3}-[0-9a-f]{12}', re.I)
        if not pattern.match(my_message['marker']):
                raise ValueError('Marker not in UUID format')
        i+=1
        my_message['start'] = self.data[i].split(' ')[0].strip()
        my_message['stop'] = self.data[i].split(' ')[-1].strip()
        pattern = re.compile(r'[0-9]{2}:[0-9]{2}:[0-9]{2}.[0-9]{3}')
        if not pattern.match(my_message['start']):
            raise ValueError('Start time not in correct format')
        if not pattern.match(my_message['stop']):
                raise ValueError('Stop time not in correct format')
        #initialise an empty list to append message content if multiple lines
        my_message['content'] = []
        #append lines to list until there is a line break
        while self.data[i] != '\n':
            i+=1 
            if self.data[i] != '\n':
                my_message['content'].append(self.data[i].strip())
        return my_message

    def format_text(self):
        """
        Creates the dictionary from the .vtt file and creates a new list of message content based on the timestamps. If the start and stop times for two subsequent messages are the same, the messages get combined to form coherent sentences.
        Returns:
         
   full_messages (list): list of structures sentences.
        """

        #create the dictionary from the .vtt file
        data_dict = self.create_dictionary()
        #initialise an empty list for partially combined message content
        part_messages = []
        #loop over the message items and combine the message content for each item
        for item in data_dict['messages']:   
            part_messages.append(' '.join(item['content']))
        #initialise an empty list for fully combined message content
        full_messages = []
        #create lists for the start and stop time for each partially combine message content
        start = [item['start'] for item in data_dict['messages']]
        stop  = [item['stop'] for item in data_dict['messages']]
        #join the start times, stop times and partially combined messages into an array.
        x=np.array([start, stop, part_messages])
        #initialise a counter to run while it remains less than the length of the message list
        i=0
        while i < len(part_messages)-2:
            #check to see if the start and stop times for subsequent messages are the same, if not append the message to full_messages and increase the counter to check the next line
            if x[0,i+1] != x[1,i]:
                full_messages.append(x[2,i])
                i+=1
            #if the start and stop times are the same initialise an empty string and loop over messages from that point and append them to the string until the start and stop times are no longer consistent
            else:
                sentence = ''
                while x[0,i+1] == x[1,i]:
                    sentence = sentence + x[2,i] + ' '
                    i+=1
                sentence = sentence + x[2,i]
                i+=1
                #append the full message string to full_messages
                full_messages.append(sentence)
        #check the last 2 elements of the partial message list and append them to full_messages
        if x[0,-1] == x[1,-2]:
            end = x[2,-2] + ' ' + x[2,-1]
            full_messages.append(end)
        else:
            full_messages.append(x[2,-2])
            full_messages.append(x[2,-1])
        #return the list with all the fully combined messages
        return part_messages, full_messages

    def reformat_vtt(self):
        """create a new .txt file with the same nane as the original .vtt and write each line in the list containing full messages to the file separated by a blank line. """

        text = self.format_text()[1]
        newfile = open(os.path.join(self.filename.replace(".vtt", ".txt")),'w')
        for line in text:
            newfile.write("%s" % line)
            newfile.write("\n \n")

