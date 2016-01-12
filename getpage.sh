
#!/bin/bash

COUNTER=0

while true; do
wget SW-my-lb-875412444.eu-west-1.elb.amazonaws.com/$COUNTER -O /dev/null
let COUNTER=COUNTER+1 

done



