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
#echo ">>> copying images to web server..."
#scp -r img/* inginious@130.104.78.197:/var/www/html/execution_images/
#echo ">>> copying trace file to web server..."
#scp ~/coding/opt-cpp-backend/tests/miscellaneous/thesis_LinkedList.trace inginious@130.104.78.197:/var/www/html/

# Generating random number for student feedback dir uniqueness:
id=$RANDOM
dir="stud_feedback_$id"
echo "generating $dir directory..."
mkdir $dir
cd $dir
mkdir "execution_images"
cd ..
cp -r img/* $dir/execution_images/
cp tests/miscellaneous/thesis_LinkedList.trace $dir
cp demo.html demo_$id.html
cp demo_$id.html $dir
echo "done"
echo "Now uploading the new dir to the web server:"
scp -r $dir inginious@130.104.78.197:/var/www/html/
echo "Deleting local files..."
rm -rf $dir
rm -f demo_$id.html
echo "URL : http://localhost:9000/stud_feedback_$id/demo_$id.html"
echo



