#!/bin/bash

g++ -c -fPIC kuiper.cpp -o kuiper.o
g++ -shared -Wall -o libkuiper.so  kuiper.o
