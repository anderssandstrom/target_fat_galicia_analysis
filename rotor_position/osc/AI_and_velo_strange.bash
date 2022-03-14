AI1=$(cat ~/target_analysis/wednesday/morning/0_23_2_strange.rawdataY.csv | awk '{print( "AI1 2022-02-16 13:38:46.201068 "  $1);}' | bash ../calcs/gain.bash AI1 0.7379332696892712)
AI2=$(cat ~/target_analysis/wednesday/morning/120_23_2_strange.rawdataY.csv | awk '{print( "AI2 2022-02-16 13:38:46.201068 "  $1);}' | bash ../calcs/gain.bash AI2 0.7379332696892712)
AI3=$(cat ~/target_analysis/wednesday/morning/240_23_2_strange.rawdataY.csv | awk '{print( "AI3 2022-02-16 13:38:46.201068 "  $1);}' | bash ../calcs/gain.bash AI3 0.7379332696892712)
Velo=$(python ../../calcVelo.py ~/target_analysis/wednesday/morning/pos_23_2_strange.npz 71 | awk '{print "Velo 2022-02-16 13:38:46.201068 " $1 }' | bash ../calcs/gain.bash Velo -1)
echo "$AI1 "
echo "$AI2 "
echo "$AI3 "
echo "$Velo "
