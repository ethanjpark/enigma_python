"""
The main enigma encryption process code.

User will input 3 rotors (I,II,III,IV,V), the reflector (A,B,C),
ring settings (3 numbers between 1~26), rotor start positions (3 letters), 
and plugboard configuration (29, 30, 31)

Once this is done, then user will type in message which will then be encrypted or
decrypted depending on which flag was raised initially.

Or can use preset configuration (from key list #649), 29th, 30th, or 31st,
by specifying either 29, 30, or 31 after the flag. User still needs to specify
rotor starting positions.
"""

from rotors import *
from plugboard import *
import sys

#holds the appropriate rotor dictionary (from rotors.py) and the notch locations
left_rotor = None
left_notch = None
mid_rotor = None
mid_notch = None
right_rotor = None
right_notch = None

reflector = None #holds appropriate reflector dictionary (from rotors.py)
plugboard = None #holds appropriate plugboard dictionary (from plugboard.py)

#keeps track of rotor's current wiring state (which contact to which contact)
curr_left_rotor = {}
curr_mid_rotor = {}
curr_right_rotor = {}

#reflector pin dict
reflector_mapping = {}

#alphabet-number matching
alphabet_mapping = { 'A':1,'B':2,'C':3,'D':4,'E':5,'F':6,'G':7,'H':8,'I':9,'J':10,'K':11,'L':12,'M':13,'N':14,'O':15,'P':16,'Q':17,'R':18,'S':19,'T':20,'U':21,'V':22,'W':23,'X':24,'Y':25,'Z':26 }
alphabet = ['','A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z']

#helper function for creating the wiring mapping dictionary
def create_curr_rotor_wiring_dict(rotor,ringstellung,starting_pos):
	global alphabet, alphabet_mapping
	wiring_dict = {}
	#create mapping between contacts for each connection.
	#calculationg is based on the ringstellung and the rotor starting position
	if(ringstellung<1 or ringstellung>26):
		sys.exit("Invalid ringstellung, please select a number between 1 and 26")
	for i in range(1,27):
		contact_out = alphabet_mapping[rotor[alphabet[i]]]
		contact_in = i
		#apply ringstellung offset
		contact_in += ringstellung-1
		contact_out += ringstellung-1
		#keep contacts in range 1-26
		if(contact_in > 26):
			contact_in -= 26
		if(contact_out > 26):
			contact_out -= 26
		#apply rotor starting position offset
		contact_in -= alphabet_mapping[starting_pos]-1
		contact_out -= alphabet_mapping[starting_pos]-1
		#keep contacts in range 1-26
		if(contact_in < 1):
			contact_in += 26
		if(contact_out < 1):
			contact_out += 26
		wiring_dict[contact_in] = contact_out
	return wiring_dict

#check for correct # of args depending on custom config (9) or preset (2)
if(len(sys.argv)!=12 and len(sys.argv)!=5):

	print("Incorrect usage. Please see below for examples.\n")
	print("Custom configuration: input.py I II III A 1 2 3 A B C 29\n")
	print("Preset: input.py 29 A B C")
	sys.exit()

else:
	#assign correct dictionaries and values to the global variables based on inputs
	if(len(sys.argv)==12): #custom configuration
		#left rotor
		if(sys.argv[1]=='I'):
			left_rotor = rotorI
			left_notch = notchI
		elif(sys.argv[1]=='II'):
			left_rotor = rotorII
			left_notch = notchII
		elif(sys.argv[1]=='III'):
			left_rotor = rotorIII
			left_notch = notchIII
		elif(sys.argv[1]=='IV'):
			left_rotor = rotorIV
			left_notch = notchIV
		elif(sys.argv[1]=='V'):
			left_rotor = rotorV
			left_notch = notchV
		else:
			sys.exit("Invalid rotor, exiting")
		curr_left_rotor = create_curr_rotor_wiring_dict(left_rotor,sys.argv[5],sys.argv[8])

		#middle rotor
		if(sys.argv[2]=='I'):
			mid_rotor = rotorI
			mid_notch = notchI
		elif(sys.argv[2]=='II'):
			mid_rotor = rotorII
			mid_notch = notchII
		elif(sys.argv[2]=='III'):
			mid_rotor = rotorIII
			mid_notch = notchIII
		elif(sys.argv[2]=='IV'):
			mid_rotor = rotorIV
			mid_notch = notchIV
		elif(sys.argv[2]=='V'):
			mid_rotor = rotorV
			mid_notch = notchV
		else:
			sys.exit("Invalid rotor, exiting")
		curr_mid_rotor = create_curr_rotor_wiring_dict(mid_rotor,sys.argv[6],sys.argv[9])

		#right rotor
		if(sys.argv[3]=='I'):
			right_rotor = rotorI
			right_notch = notchI
		elif(sys.argv[3]=='II'):
			right_rotor = rotorII
			right_notch = notchII
		elif(sys.argv[3]=='III'):
			right_rotor = rotorIII
			right_notch = notchIII
		elif(sys.argv[3]=='IV'):
			right_rotor = rotorIV
			right_notch = notchIV
		elif(sys.argv[3]=='V'):
			right_rotor = rotorV
			right_notch = notchV
		else:
			sys.exit("Invalid rotor, exiting")
		curr_right_rotor = create_curr_rotor_wiring_dict(right_rotor,sys.argv[7],sys.argv[10])

		#reflector
		if(sys.argv[4]=='A'):
			reflector = reflectorA
		elif(sys.argv[4]=='B'):
			reflector = reflectorB
		elif(sys.argv[4]=='C'):
			reflector = reflectorC
		else:
			sys.exit("Invalid reflector, exiting")
		for i in range(1,27):
			

		#plugboard pairs
		if(sys.argv[11]==29):
			plugboard = plugboard29
		elif(sys.argv[11]==30):
			plugboard = plugboard30
		elif(sys.argv[11]==31):
			plugboard = plugboard31
		else:
			sys.exit("Invalid plugboard, exiting")

	#preset
	else:

		if(sys.argv[1]==29):
			left_rotor = rotorIII
			left_notch = notchIII
			mid_rotor = rotorII
			mid_notch = notchII
			right_rotor = rotorI
			right_notch = notchI
		elif(sys.argv[1]==30):
			left_rotor = rotorIV
			left_notch = notchIV
			mid_rotor = rotorIII
			mid_notch = notchIII
			right_rotor = rotorII
			right_notch = notchII
		elif(sys.argv[1]==31):
			left_rotor = rotorI
			left_notch = notchI
			mid_rotor = rotorV
			mid_notch = notchV
			right_rotor = rotorIII
			right_notch = notchIII
		else:
			sys.exit("Invalid preset, exiting")