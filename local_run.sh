#!/bin/bash
# Script used to run everything from Valgrind traces generation
# to final traces and images uploading to the server at the
# address : 130.104.78.197

cd ~/coding/opt-cpp-backend/tests/miscellaneous
echo ">>> generating trace file...";
make clean
make
cd ~/coding/opt-cpp-backend/
echo ">>> generating images...";
make clean
make
echo ">>> copying images to web server..."
scp -r img/* inginious@130.104.78.197:/var/www/html/execution_images/
echo ">>> copying trace file to web server..."
scp ~/coding/opt-cpp-backend/tests/miscellaneous/thesis_LinkedList.trace inginious@130.104.78.197:/var/www/html/
echo "done";
