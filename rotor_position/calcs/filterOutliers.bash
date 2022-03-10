
#FILE="-"
#if [ "$#" -eq 1 ]; then
#    FILE=$1
#fi

PV=$1
TOL=$2
all=$(cat ${FILE})
allExceptPV=$(echo "$all " | grep -v "$PV")
filteredvals=$(echo "$all " | grep $PV |awk -v tol=$TOL 'BEGIN{oldVal=$4+0} {  diff=$4+0-oldVal+0; if( (diff*diff)<(tol*tol)){ print $1 " " $2 " " $3 " " $4;}; oldVal=$4+0;}')
echo "$filteredvals"
echo "$allExceptPV"
