#!/bin/bash

#COMPILER=gcc # Please adapt this line to your favorite compiler.
#COMPILER=patmos-clang
COMPILER=/Users/dan/t-crest/llvm-project/build_release/bin/clang


OPTIONS=" -g -O2 -Wall -Wno-unknown-pragmas -Werror -mllvm --mpatmos-disable-function-splitter" 
OPTIMIZATION=" -mllvm --mpatmos-enable-stack-cache-promotion"
ARRAY_OPTIMIZATION=" -mllvm --mpatmos-enable-array-stack-cache-promotion"

#EXEC= # Adapt if the executable is to be executed via another program
#EXEC=valgrind\ -q
EXEC="pasim -g 64m -m 32k -l 8k -s 1k --print-stats "

PASS=0
FAIL_COMP=0
FAIL_EXEC=0

for dir in */; do

    cd "$dir"

    printf "Entering ${dir} \n"

    for BENCH in */; do
        cd "$BENCH"
                
        printf "Checking ${BENCH} ..."
        if [ -f a1.out ]; then
            rm a1.out
        fi
        
        if [ -f *.o ]; then
            rm *.o
        fi
        
        
        # Please remove '&>/dev/null' to identify the warnings (if any)
        $COMPILER $OPTIONS *.c -mllvm --mpatmos-serialize=a1.out.pml -o a1.out &> /dev/null
        
        if [ -f a1.out ]; then
            $EXEC "${BENCH%/}"_main a1.out 2> noOpt_"${BENCH%/}".txt
            RETURNVALUE=$(echo $?)
            if [ $RETURNVALUE -eq 0 ]; then
                printf "passed. \n"
                ((PASS++))
            else
                printf "failed (wrong return value $RETURNVALUE). \n"
		rm noOpt_"${BENCH%/}".txt
                ((FAIL_EXEC++))
            fi
        else
            printf "failed (compiled with errors/warnings). \n"
            ((FAIL_COMP++))
        fi 
        # second pass with optimizations 
        if [ -f a2.out ]; then
            rm a2.out
        fi
        
        if [ -f *.o ]; then
            rm *.o
        fi
       $COMPILER $OPTIONS $OPTIMIZATION *.c -mllvm --mpatmos-serialize=a2.out.pml -o a2.out &> /dev/null
       
       if [ -f a2.out ]; then
           $EXEC "${BENCH%/}"_main a2.out 2> opt_"${BENCH%/}".txt
           RETURNVALUE=$(echo $?)
           if [ $RETURNVALUE -eq 0 ]; then
               printf "passed. \n"
               ((PASS++))
           else
               printf "failed (wrong return value $RETURNVALUE). \n"
  	rm opt_"${BENCH%/}".txt
               ((FAIL_EXEC++))
           fi
       else
           printf "failed (compiled with errors/warnings). \n"
           ((FAIL_COMP++))
       fi 

        # third pass with array optimizations 
        if [ -f a3.out ]; then
            rm a3.out
        fi
        
        if [ -f *.o ]; then
            rm *.o
        fi
        $COMPILER $OPTIONS $OPTIMIZATION $ARRAY_OPTIMIZATION *.c -mllvm --mpatmos-serialize=a3.out.pml -o a3.out &> /dev/null
        
        if [ -f a3.out ]; then
            $EXEC "${BENCH%/}"_main a3.out 2> arrayOpt_"${BENCH%/}".txt
            RETURNVALUE=$(echo $?)
            if [ $RETURNVALUE -eq 0 ]; then
                printf "passed. \n"
                ((PASS++))
            else
                printf "failed (wrong return value $RETURNVALUE). \n"
		rm arrayOpt_"${BENCH%/}".txt
                ((FAIL_EXEC++))
            fi
        else
            printf "failed (compiled with errors/warnings). \n"
            ((FAIL_COMP++))
        fi 
        cd ..
    done

    printf "Leaving ${dir} \n\n"
    
    cd ..
done

echo "PASS: $PASS, FAIL_COMP: $FAIL_COMP, FAIL_EXEC: $FAIL_EXEC"
