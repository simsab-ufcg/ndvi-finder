def throwError(step, code):
	'''
	Takes a code of error and print its message (in case of a known error).
	In case of a unknown error, halts program execution.
	'''

	exit_code = (code >> 8)
	signal_code = (511 & code)

	switch = {
		1: 'Could not open TIFF file.',
		2: 'Could not read from TIFF file.',
		3: 'Unsupported band in TIFF file.',
		4: 'Could not write in TIFF file.',
		5: 'Could not read MTL file.',
		6: 'Could not read Coordinate of TIFF file.'
	}

	if switch.has_key(exit_code):
		print 'Error while in ' + step + ' step. ' + switch[exit_code]
	else:
		print 'Unexpected error: signal error was ' + str(signal_code) + '. Step: ' + step
		raise SystemExit
	