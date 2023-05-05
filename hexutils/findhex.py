#!/bin/python3


import sys
import os

# debug mode. enable with --debug
DEBUG = False


def files(path):
	for file in os.listdir(path):
		if os.path.isfile(os.path.join(path, file)):
			 yield file



def search(what, where):
	where = list(where)
	what = list(what)
	if len(what) > len(where):
		return -1
	idx = [i for i, x in enumerate(where) if what[0] == x]
	results = []
	for item in idx:
		if where[item:item+len(what)] == what:
			#print("idx: "+str(idx))
			#print("what:" +str(what))
			#print("where[item:item+len(what)] == "+str(where[item:item+len(what)]))
			#print("item: "+str(item))
			results.append(item)
	if results == []:

		return -1

	else:
		return results

def to_bin(hex_seq):
	# converts hex sequence to bytes
	return bytearray.fromhex(hex_seq)


def shiftbytesleft(seq, count):
	if isinstance(seq, str):
		seq = int(seq, base=16)
	if isinstance(seq, bytearray):
		seq = bytearray(seq).hex()
		seq = int(seq, base=16)
	seq << count
	#print("Returning this: "+str(hex(seq)[2:]))

	return_val = hex(seq)[2:]

	if len(return_val) % 2:
		return_val = "0"+return_val
	return return_val # truncate out the "0x..."


def shiftbytesright(seq, count):
	if isinstance(seq, str):
		seq = int(seq, base=16)
	if isinstance(seq, bytearray):
		seq = bytearray(seq).hex()
		seq = int(seq, base=16)
	seq >> count
	#print("Returning this: "+str(hex(seq)[2:]))

	return_val = hex(seq)[2:]

	if len(return_val) % 2:
		return_val = "0"+return_val
	return return_val # truncate out the "0x..."


def search_file(sequence, filename, as_string, start_index=0, end_index=2**64, shifts=False):
	
	fh = open(filename, "rb")
	stuff = fh.read()
	fh.close()
	#as_string = False

	#if sequence[0] == "\"":
	#	if sequence[-1] != "\"":
	#		print("Close your quote.")
	#		exit(1)
	#	else:
	#		as_string = True
	#		sequence = sequence[1:-1]

	# this is because the message may not always be byte aligned so we need to search for a specific sequence of bytes which are either left or right shifted.

	stuff = stuff[start_index:end_index+1]
	if DEBUG:
		print("Stuff: "+str(stuff))
	results = []
	if not as_string:
		if shifts:

			for i in range(8):


				
				thing = shiftbytesleft(sequence, i)
				#print("Thing: "+str(thing))
				thing = to_bin(thing)
				#print("Stuff"+str(stuff))
				index = search(thing, stuff)
				#if index != -1:
				#	print(filename+" : "+str(hex(index)))

				if index != -1:
					results += index


				thing = shiftbytesright(sequence, i)
				thing = to_bin(thing)
				#print("Stuff"+str(stuff))
				index = search(thing, stuff)
				#if index != -1:
				#	print(filename+" : "+str(hex(index)))

				if index != -1:
					results += index
		else:
			thing = sequence
			thing = to_bin(thing)
			results = [search(thing, stuff)]



	else:
		results = [search(sequence, stuff)]

	if results == []:
		results = -1
	results = [x+int(start_index) for x in results]
	results = list(set(results))
	return results



def handle_sequence(args):

	final_sequence = None
	as_string = False
	seq_start = args[args.index("--sequence")+1]
	#print("args: " + str(args))
	#print("seq_start: " + str(seq_start))
	#if "\"" not in seq_start or "\'" not in seq_start:
	#if "\"" not in seq_start:
	#	final_sequence = seq_start
	#	print("poopoo")
	#	return final_sequence, as_string
	if "\"" in seq_start:
		# as_string = true
		as_string = True
		seq_start = seq_start[1:] # get rid of the quote
		if "\"" in seq_start: # the quote is in the same thing

			seq_start = seq_start[:-1]
			final_sequence = seq_start
			return final_sequence, as_string


		final_sequence = seq_start
		counter = args.index("--sequence")+2

		while "\"" not in args[counter]:
			final_sequence+= str(args[counter])
			counter += 1
			if counter == len(args):
				print("Close your quote")
				exit(1)
		return final_sequence, as_string



	if " " in seq_start:
		sequence_thing = ''.join(seq_start.split(" "))
		as_string = False
		#print("sequence_thing: " + str(sequence_thing))
		print("sequence_thing: "+str(sequence_thing))
		return sequence_thing, as_string


	# We can not do this because of the way python handles the sequences internally.
	if "\'" in seq_start:
		# as_string = False
		as_string = False
		seq_start = seq_start[1:] # get rid of the quote
		if "\'" in seq_start: # the quote is in the same thing

			seq_start = seq_start[:-1]
			final_sequence = seq_start
			return final_sequence, as_string


		final_sequence = seq_start
		counter = args.index("--sequence")+2

		while "\'" not in args[counter]:
			final_sequence+= str(args[counter])
			counter += 1
			if counter == len(args):
				print("Close your quote")
				exit(1)
		#print("final_sequence: " + str(final_sequence))
		return final_sequence, as_string

	print("seq_start : "+str(seq_start))
	return seq_start, as_string
	
	# here a single quote (') means a string



if __name__=="__main__":

	# if --files in arguments then search all files (does not search recursively)
	# if --file is passed then search one singular file
	# --sequence flag describes the hex sequence to search for if it starts with the quote character (") then search as string

	if "--debug" in sys.argv:
		DEBUG = True


	if "--sequence" not in sys.argv:
		print("Please specify a sequence with --sequence .")
		exit(1)


	sequence, as_string = handle_sequence(sys.argv) # this line gets the search sequence and handles stuff like starting the sequence with a quote character (") and stuff

	# sequence = sys.argv[sys.argv.index("--sequence")+1]



	if "--files" not in sys.argv and "--file" not in sys.argv:
		print("Please specify to search all files not recursively (--files) or one singular file with (--file) .")
		exit(1)



	all_files = False
	
	if "--files" in sys.argv:
		all_files = True

	path = "./"
	if "--path" in sys.argv:

		if sys.argv.index("--path")+1 >= len(sys.argv):
			print("No path specified even though --path flag used.")
			exit(1)

		path = sys.argv[sys.argv.index("--path")+1]
		if path[-1] != "/":
			path += "/"
	filename = False
	if "--file" in sys.argv:
		if sys.argv.index("--file")+1 >= len(sys.argv):
			print("No file specified.")
			exit(1)

		filename = sys.argv[sys.argv.index("--file")+1]

	start_index = 0

	end_index = 2**64

	if "--start" in sys.argv:

		start_index = str(sys.argv[sys.argv.index("--start")+1])
		if "0x" in start_index:
			# accept hex as start index.
			start_index = int(start_index[2:], base=16)
		else:
			start_index = int(start_index)

	if "--end" in sys.argv:


		end_index = str(sys.argv[sys.argv.index("--end")+1])
		if "0x" in end_index:
			# accept hex as start index.
			end_index = int(end_index[2:], base=16)
		else:
			end_index = int(end_index)

	print("end_index == "+str(hex(end_index)))
	print("start_index == "+str(hex(start_index)))

	if all_files:
		directory = files(path)
		for file in directory:
			result = search_file(sequence, path+file, as_string, start_index=start_index, end_index=end_index)
			if result != -1:
				print(file+" : "+str(" ".join(hex(x) for x in result)))
	
	else:
		result = search_file(sequence, filename, as_string, start_index=start_index, end_index=end_index)

		if result != -1:
			print(filename+" : "+str(" ".join(hex(x) for x in result)))





