#!/bin/bash
# Script used to run everything from Valgrind traces generation
# to final traces and images uploading to the server at the
# address : 130.104.78.197

cd ~/coding/opt-cpp-backend/tests/miscellaneous
make clean
make
cd ~/coding/opt-cpp-backend/
make
cd ~/coding/opt-cpp-backend/tests/miscellaneous
make clean

