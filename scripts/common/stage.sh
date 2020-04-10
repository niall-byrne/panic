#!/bin/bash

set -e

deploy_stage() {

  pushd "${PROJECT_HOME}" > /dev/null

    # shellcheck disable=SC1091
    source environments/stage_secret.env

    pushd "${PROJECT_NAME}" >/dev/null

        ./manage.py collectstatic
        cp ../assets/requirements.txt requirements.txt
        cat ../assets/requirements-stage.txt >> requirements.txt
        cp ../environments/stage.yaml app.yaml
        while read -r line; do
          [[ -z "${line}" ]] && continue
          key="$(echo "${line}" | cut -d'=' -f1)"
          value=''
          value="${line/$key=/$value}"
          echo "  ${key}: ${value}" >> app.yaml
        done < "../environments/stage.env"
        gcloud beta app deploy --version v1
        rm app.yaml
        rm requirements.txt

    popd >/dev/null
  popd >/dev/null

}
