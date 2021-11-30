#!/bin/bash

#Variables del script Bash
deploy_path=$PWD
test_path=$PWD/../test/

run_test(){
	test_name=$1
	if [ -d "$test_path/$1" ]; then
	  output_file=$deploy_path/result_$test_name.xml
	  rm -f $1 $output_file
	  cd $test_path/$test_name
	  python3 -m unittest
	  py.test --junitxml=$output_file
	 else
	  echo "test directory not found: $1"
    exit 1
  fi
}

#Instalando los requerimientos
echo "* Installing requirements *"
pip3 install  -r requirements.txt

#Si solo se va a ejecutar un test
test_to_run="$1"

#Validando se se envio como parametro un test a ejecutar
if [ -z $test_to_run ]; then
echo "Running all test"

run_test "unit"

else
if [ -d "$test_path/$test_to_run" ]; then
 echo "Runnig one test: $test_to_run"
run_test $test_to_run
else
  echo "test directory not found: $test_to_run"
  exit 1
fi
fi

