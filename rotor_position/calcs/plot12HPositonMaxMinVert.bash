cat 12hdata/12h_test_*.log | awk '{print $1 " " $2 " " $3 " " $4}'| grep AI4  | bash filterOutliers.bash AI4 0.05 |bash downSampleMaxMin.bash AI4 100 | python plot12HPositonMaxMinVert.py 0.7379332696892712

