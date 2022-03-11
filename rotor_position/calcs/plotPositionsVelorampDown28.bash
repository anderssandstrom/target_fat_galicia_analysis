cat ~/target_analysis/tuesday/rot/data_rampdown.log | awk '{print $1 " " $2 " " $3 " " $4}' | tail -n 10000 |bash calcVeloCa.bash | grep "Velo\|Opto\|AI"| bash gain.bash AI 0.7379332696892712 | bash filterOutliers.bash AI4 0.05 | bash filterOutliers.bash AI4 0.05 | python plotPositionsVelo.py 

