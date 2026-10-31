#!/bin/bash
# usage: vm.sh ssh '<cmd>' | vm.sh scp <args...>   (od-l4b, IAP)
A="--tunnel-through-iap --zone us-east4-c --project system-one-509903"
case "$1" in
  ssh) shift; gcloud compute ssh od-l4b $A --command "$1" 2>&1 | grep -v -i "numpy\|increasing_the_tcp\|^$\|^WARNING\|tunnel, consider" ;;
  scp) shift; gcloud compute scp $A "$@" 2>&1 | grep -v -i "numpy\|increasing_the_tcp\|^$\|^WARNING\|tunnel, consider" ;;
esac
