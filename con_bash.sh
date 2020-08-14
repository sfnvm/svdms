#!/bin/bash

clean_migrations() {
  result=`find . -path "*migrations/*.py" -not -path "./.*" -not -name "__init__.py"`
  echo $result
}

echo "hello motherf*cker"
