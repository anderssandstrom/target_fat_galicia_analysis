cat ~/target_analysis/wednesday/12h_test_20.log | head -n 10000 | awk '{print $1 " " $2 " " $3 " " $4;}' | bash calcVeloCa.bash | grep "Velo\|AI2" | bash filterHighLow.bash Velo 23.9 24.1 | python ~/sources/ecmccomgui/pyDataManip/plotCaMonitorYY.py AI2 Velo