cat 12hdata/12h_test_*.log ../../doc/torque_time.log | grep "EL5021" | awk '{print $1 " " $2 " " $3 " " $4}'| bash calcVeloCa.bash | grep "Velo" | bash downSampleMaxMin.bash Velo 50 | bash filterOutliers.bash Velo 0.2 | python ~/sources/ecmccomgui/pyDataManip/plotCaMonitor.py 

