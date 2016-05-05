#!/bin/bash

cd ~/coding/opt-cpp-backend/tests/miscellaneous
make clean
make
cd ~/coding/opt-cpp-backend/
make
cd ~/coding/opt-cpp-backend/tests/miscellaneous
make clean

