#!/usr/bin/env bash

lint_check() {

  set -e

  pushd "${PROJECT_HOME}"  > /dev/null
    isort -c
    pushd "${PROJECT_NAME}" > /dev/null
      pylint --rcfile ../.pylint.rc -j 2 ./*
    popd > /dev/null
    shellcheck -x scripts/*.sh
    shellcheck -x scripts/common/*.sh
  popd  > /dev/null

}
