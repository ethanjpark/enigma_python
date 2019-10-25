#actual encryption algorithm stuff here
"""
at the very rudimentary level, the algorithm goes like this:

input -> plugboard -> right rotor -> mid rotor -> left rotor -> reflector -> left rotor -> mid rotor -> right rotor -> plugboard -> output
"""

#stepping a rotor, input is the wiring dict for a particular rotor
def step_rotor(rotor):
	new_dict = {}
	#rotor is turning towards the operator, so decrement the pin number
	for contact_in in rotor:
		temp = contact_in-1
		if(temp < 1):
			temp = 26
		new_dict[temp] = rotor[contact_in]-1
	return new_dict

#pass in the wiring dictionaries populated in input.py
def enigma(msg,lr,lnotch,lstart,mr,mnotch,mstart,rr,rnotch,rstart,reflector,plugboard):
	output_str = ''
	upp_msg = msg.upper()
	left_rotor = lr
	mid_rotor = mr
	right_rotor = rr
	for char in upp_msg:
		#don't encrypt any non alphabetic characters
		if(not char.isalpha()):
			output_str = output_str + char

		else:
			alphabet = ['A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z']
			#maps alphabet to the entry wheel pins basically
			entry_mapping = { 'A':1,'B':2,'C':3,'D':4,'E':5,'F':6,'G':7,'H':8,'I':9,'J':10,'K':11,'L':12,'M':13,'N':14,'O':15,
								 'P':16,'Q':17,'R':18,'S':19,'T':20,'U':21,'V':22,'W':23,'X':24,'Y':25,'Z':26 }
			output_char = char
			curr_char_left = alphabet.index(lstart)
			curr_char_mid = alphabet.index(mstart)
			curr_char_right = alphabet.index(rstart) 
			step_mid = False
			step_left = False

			##### 1. PLUGBOARD ######
			#if character needs to be swapped per plugboard
			if(output_char in plugboard): #char in keys
				output_char = plugboard[output_char]
			elif(output_char in plugboard.values()): #char in values
				for key_char in plugboard:
					if(plugboard[key_char] == output_char):
						output_char = key_char
						break

			##### 2. Stepping the rotors #####
			if(alphabet[curr_char_mid] == mnotch):
				step_left = True
			if(alphabet[curr_char_right] == rnotch):
				step_mid = True

			if(step_left):
				left_rotor = step_rotor(left_rotor)
				curr_char_left = (curr_char_left+1) % len(alphabet) #update rotor position (character that would show on top on an actual enigma machine)
				mid_rotor = step_rotor(mid_rotor) #mid rotor also steps because of the double stepping phenomena
				curr_char_mid = (curr_char_mid+1) % len(alphabet) #update rotor position
				step_left = False
				step_mid = False #I haven't encountered this in all of the material that I've read so far about the enigma, but
								 #basically the case where both the mid and right rotors are in their notch positions. If my logic
								 #is correct, this can only happen if the starting positions of the rotors are set to the notch
								 #positions intentionally.
			if(step_mid):
				mid_rotor = step_rotor(mid_rotor)
				curr_char_mid = (curr_char_mid+1) % len(alphabet) #update rotor position
				step_mid = False
			right_rotor = step_rotor(right_rotor) #right rotor steps with every keystroke
			curr_char_right = (curr_char_right+1) % len(alphabet) #update rotor position
 
			##### 3. Rotors #####
			entry_out = entry_mapping[output_char]
			right_out = right_rotor[entry_out] #right rotor substitution
			mid_out = mid_rotor[right_out] #mid rotor substitution
			left_out = left_rotor[mid_out] #left rotor substitution

			##### 4. Reflector #####
			ref_out = reflector[left_out]

			##### 5. Rotors (again) #####
			#going backwards through the rotors, and since the rotor wiring dictionaries are one-directional,
			#have to go through the connections and find the input contact that connects to the output contact
			#that we got from the reflector
			mid_in = 0
			while(mid_in == 0): #finding pin to mid rotor
				for pin_in in left_rotor:
					if(left_rotor[pin_in] == ref_out):
						mid_in = pin_in
						break

			right_in = 0
			while(right_in == 0): #finding pin to right rotor
				for pin_in in mid_rotor:
					if(mid_rotor[pin_in] == mid_in):
						right_in = pin_in
						break

			entry_in = 0
			while(entry_in == 0): #finding pin to entry
				for pin_in in right_rotor:
					if(right_rotor[pin_in] == right_in):
						entry_in = pin_in
						break

			#find what character has been output by all the rotor stuff
			for letter in entry_mapping:
				if(entry_mapping[letter] == entry_in):
					output_char = letter
					break

			##### 6. Plugboard (again) #####
			#if character needs to be swapped per plugboard
			if(output_char in plugboard): #char in keys
				output_char = plugboard[output_char]
			elif(output_char in plugboard.values()): #char in values
				for key_char in plugboard:
					if(plugboard[key_char] == output_char):
						output_char = key_char
						break

			output_str = output_str + output_char
			return output_str
