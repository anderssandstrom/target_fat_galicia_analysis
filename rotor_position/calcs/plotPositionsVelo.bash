 cat ~/target_analysis/wednesday/12h_test_1.log | awk '{print $1 " " $2 " " $3 " " $4}' | head -n 22000 |bash calcVeloCa.bash | grep "Velo\|Opto\|AI"| bash gain.bash AI 0.7379332696892712 | bash filterOutliers.bash AI4 0.1 | bash filterOutliers.bash AI4 0.1 | python plotPositionsVelo.py