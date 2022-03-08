
#FILE="-"
#if [ "$#" -eq 1 ]; then
#    FILE=$1
#fi

PVName=$1
Samples=$2

all=$(cat ${FILE})
allExceptPV=$(echo "$all " | grep -v "$PVName")

filtered=$(echo "$all " | grep $PVName | awk -v samples=$Samples 'BEGIN{max=$4;min=$4;counter=0} { if(counter==0) {min=$4;max=$4;} counter=counter+1; if($4+0>max) { max=$4;}; if($4+0<min) {min=$4;}; if(counter==samples) {print $1 "Max " $2 " " $3 " " max; print $1 "Min " $2 " " $3 " " min; counter=0;} }')
echo "$filtered"
echo "$allExceptPV"
