
#FILE="-"
#if [ "$#" -eq 1 ]; then
#    FILE=$1
#fi

all=$(cat ${FILE})
pos=$(echo "$all " | grep EL5021)
velo=$(echo "$pos " | awk 'BEGIN{oldPos=-$4+0} {vel=(-$4+0-oldPos+0)/0.1*60.0/360.0;oldPos=-$4+0; if(vel+0<100 && vel+0>-100) { print $1 "Velo " $2 " " $3 " " vel}}')
echo "$velo"
echo "$all"

