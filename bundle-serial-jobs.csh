#!/bin/tcsh 

# Set up Python 3 environment
module load python3

# Set array of input files
set inFiles = ()

# Get number of files
set numInFiles = $#inFiles

# Create the subdirectory for holding LSF output and error files
mkdir -p lsfOutFiles

# Submit jobs. Bubdle 2 serial jobs in one LSF job 
@ n = 0
while ($n < $numInFiles)
    @ leftOver = $numInFiles - $n
    if ($leftOver >= 2) then
	# Normal actions of handling a full block
	@ n1 = $n + 1
	@ n2 = $n + 2

	bsub -n 2 -W 10080 -R "span[hosts=1]" -o ./lsfOutFiles/$inFiles[$n1]-$inFiles[$n2].out.%J -e ./lsfOutFiles/$inFiles[$n1]-$inFiles[$n2].err.%J "python3 ./scripts/SMT/$inFiles[$n1] \&; python3 ./scripts/SMT/$inFiles[$n2] \&; wait"
    else
	# Actions of handling left over not enough for a full block
	switch ($leftOver)
	    case 1:
		@ n1 = $n + 1

		bsub -n 1 -W 10080 -R "span[hosts=1]" -o ./lsfOutFiles/$inFiles[$n1].out.%J -e ./lsfOutFiles/$inFiles[$n1].err.%J "python3 ./scripts/SMT/$inFiles[$n1] \&; wait"
		breaksw
	    case 2:
		@ n1 = $n + 1 
		@ n2 = $n + 2

		bsub -n 2 -W 10080 -R "span[hosts=1]" -o ./lsfOutFiles/$inFiles[$n1]-$inFiles[$n2].out.%J -e ./lsfOutFiles/$inFiles[$n1]-$inFiles[$n2].err.%J "python3 ./scripts/SMT/$inFiles[$n1] \&; python3 ./scripts/SMT/$inFiles[$n2] \&; wait"
		breaksw
	endsw
    endif

    @ n = $n + 2
end
