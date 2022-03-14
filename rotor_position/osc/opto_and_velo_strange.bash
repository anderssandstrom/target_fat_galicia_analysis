Opto=$(cat ~/target_analysis/wednesday/morning/opt_2_strange.rawdataY.csv | awk '{print( "Opto 2022-02-16 13:38:46.201068 "  $1);}')
Velo=$(python ../../calcVelo.py ~/target_analysis/wednesday/morning/pos_23_2_strange.npz 71 | awk '{print "Velo 2022-02-16 13:38:46.201068 " $1 }' | bash ../calcs/gain.bash Velo -1)

echo "$Opto "
echo "$Velo "
