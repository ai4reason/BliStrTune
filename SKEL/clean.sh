#!/bin/sh

(cd allprobs; ls | grep "\.protocol_" | xargs rm -f)
rm -fr prots/*
rm -fr strats/*
rm -fr epymils/epymils-*
rm -fr bests nohup.out

