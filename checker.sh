#!/bin/bash

cd "$(dirname "$0")" || exit 1
cd ..
cp src/* .
cp -R $CHECKER_DATA_DIRECTORY/in $CHECKER_DATA_DIRECTORY/ref $CHECKER_DATA_DIRECTORY/cadical-rel-1.5.3 .

nr_tests=30
points_per_test=3

mkdir -p "out/"
make_output=$(make)
if [ $? != 0 ]; then
    echo "make error, exit code: " $? >&2
    echo "$make_output" >&2
    exit 1
fi

run_test() {
    i=$1
    printf "Test %2d ................................ " $i
    infile="in/data${i}.in"
    if [ ! -f "$infile" ]; then
        echo "SKIP"
        return
    fi

    outfile="out/data${i}.out"
    reffile="ref/data${i}.ref"
    timeout 3 ./main "$infile" "$outfile" &> /dev/null
    if [ $? = 124 ]; then
        echo "TLE"
        return
    fi

    cadical_out=$(./cadical-rel-1.5.3/bin/cadical "$outfile")

    verdict=$(echo "$cadical_out" | grep "^s " | cut -d' ' -f 2)
    if [ "$verdict" = "SATISFIABLE" ]; then
        result=1
    elif [ "$verdict" = "UNSATISFIABLE" ]; then
        result=0
    else
        echo "Something went wrong!" $? >&2
        echo "$cadical_out" >&2
        exit 1
    fi
    ref_result=$(cat "$reffile")
    if [ "$result" = "$ref_result" ]; then
        echo "PASS"
        : $((score+=$points_per_test))
    else
        echo "FAIL"
    fi
}

score=0
if [[ $# = 0 || $1 = "" ]]; then
    nr_tests=30
    tests=$(seq 0 $(($nr_tests - 1)))
    for i in ; do
        run_test "$i"
    done
else
    nr_tests=$#
    tests=$@
fi

max_score=$(($points_per_test * $nr_tests))
for i in $tests; do
    run_test "$i"
done

printf "\nTOTAL SCORE: %d/%d\n" $score $max_score
