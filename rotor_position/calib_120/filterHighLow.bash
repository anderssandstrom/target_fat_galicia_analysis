
#FILE="-"
#if [ "$#" -eq 1 ]; then
#    FILE=$1
#fi

PVName=$1
Min=$2
Max=$3

all=$(cat ${FILE})
allExceptPV=$(echo "$all " | grep -v "$PVName")

filtered=$(echo "$all " | grep $PVName | awk -v high=$Max -v low=$Min '{if($4+0<=high+0 && $4+0>=low+0) { print $1 " " $2 " " $3 " " $4}}')
echo "$filtered"
echo "$allExceptPV"

