cat 12hdata/12h_test_*.log ../../doc/torque_time.log | grep "EL5021\|Torque" | awk '{print $1 " " $2 " " $3 " " $4}'| bash calcVeloCa.bash | grep "Velo\|Torque" | bash downSampleMaxMin.bash Velo 100 | bash filterOutliers.bash Velo 0.2 | bash gain.bash Torque 5.8 |python plot12HTorqueVelo.py

