
import sys
import os
import re

def search_file(seq, file, as_string):

	result = -1

	if not as_string:
		
		fh = open(file, "rb")

		stuff = int.from_bytes(fh.read(), "big")

		fh.close()

		sequence_thing = int(seq, 16)
		sequence_thing = bin(sequence_thing)[2:]
		other_stuff = bin(stuff)[2:]

		print(sequence_thing)
		print(other_stuff)

		list_thing = [m.start() for m in re.finditer(sequence_thing, other_stuff)]

		

		
		if list_thing == []:
			return result
		else:
			return list_thing

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

	print("seq_start: "+str(seq_start))
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

	#return seq_start, as_string

	
	# here a single quote (') means a string



if __name__=="__main__":

	# if --files in arguments then search all files (does not search recursively)
	# if --file is passed then search one singular file
	# --sequence flag describes the hex sequence to search for if it starts with the quote character (") then search as string


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


	if all_files:
		directory = files(path)
		for file in directory:
			result = search_file(sequence, path+file, as_string)
			if result != -1:
				print(file+" : "+str(" ".join(hex(x) for x in result)))
	
	else:
		result = search_file(sequence, filename, as_string)

		if result != -1:
			print(filename+" : "+str(" ".join(hex(x) for x in result)))


