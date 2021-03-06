#!/usr/bin/env python

import os, time, sys, shutil, copy



from optparse import OptionParser
import textwrap

import multif
from multif import SU2



# -------------------------------------------------------------------
#  Main 
# -------------------------------------------------------------------

def main():
	 
	sys.stdout.write('-' * 90);
	sys.stdout.write('\n');
	sys.stdout.write('\t __  __ _   _ _  _____ ___         ___ \t\n') ;
	sys.stdout.write('\t|  \/  | | | | ||_   _|_ _|  ___  | __|\t\n');
	sys.stdout.write('\t| |\/| | |_| | |__| |  | |  |___| | _| \t\t Dev. : R. Fenrich & V. Menier\n');
	sys.stdout.write('\t|_|  |_|\___/|____|_| |___|       |_|  \t\t        Stanford University\n\n');
	sys.stdout.write('-' * 90);
	sys.stdout.write('\n\n');
	
	# Command Line Options
	parser = OptionParser()
	parser.add_option("-f", "--file", dest="filename",
	                  help="read config from FILE", metavar="FILE")
	parser.add_option("-n", "--partitions", dest="partitions", default=0,
	                  help="number of PARTITIONS", metavar="PARTITIONS")
	
	parser.add_option("-l", "--flevel", dest="flevel", default=-1,
	                  help="fidelity level to run", metavar="FLEVEL")	
	
	(options, args)=parser.parse_args()
	
	options.partitions = int( options.partitions )
	options.flevel     = int( options.flevel )
	
	if options.flevel < 0 :
		sys.stderr.write("  ## ERROR : Please choose a fidelity level to run (option -l or --flevel)");
		sys.exit(0);
	
	nozzle = multif.nozzle.NozzleSetup( options.filename, options.flevel );
	
	### HACK
	#multif.MEDIUMF.AEROSPostProcessing(nozzle);
	#sys.exit(1);
	
	if nozzle.method == 'NONIDEALNOZZLE' :
		multif.LOWF.Run(nozzle);
	elif nozzle.method == 'EULER' or nozzle.method == 'RANS':
		multif.MEDIUMF.Run(nozzle);
		
	# --- Output functions 
	
	#nozzle.WriteOutputFunctions_Plain ();
	nozzle.WriteOutputFunctions_Dakota ();
	
	sys.stdout.write('\n');
	
	# --- Print warning in case the wrong SU2 version was run
	if nozzle.method != 'NONIDEALNOZZLE' and nozzle.SU2Version != 'OK':
		sys.stdout.write('\n');
		sys.stdout.write('#' * 90);
		sys.stdout.write('\n  ## WARNING : You are not using the right version of SU2. This may have caused robustness issues.\n');
		sys.stdout.write('#' * 90);
		sys.stdout.write('\n\n');
	
# -------------------------------------------------------------------
#  Run Main Program
# -------------------------------------------------------------------

if __name__ == '__main__':
    main()
