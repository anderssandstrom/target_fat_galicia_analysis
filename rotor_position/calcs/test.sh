cat ~/target_analysis/thursday/rampdown_28_rpm_1.log | awk '{print $1 " " $2 " " $3 " " $4;}' | bash calcVeloCa.bash | grep "Velo\|Opto" | python ~/sources/ecmccomgui/pyDataManip/plotCaMonitorYY.py Opto Velo

