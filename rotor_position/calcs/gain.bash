
#FILE="-"
#if [ "$#" -eq 1 ]; then
#    FILE=$1
#fi

PVName=$1
Gain=$2


all=$(cat ${FILE})
allExceptPV=$(echo "$all " | grep -v "$PVName")

filtered=$(echo "$all " | grep $PVName | awk -v gain=$Gain '{ newValue=($4+0)*gain; { print $1 " " $2 " " $3 " " newValue;}}')
echo "$filtered"
echo "$allExceptPV"
