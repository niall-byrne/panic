#!/bin/bash

set -e

deploy_stage() {

  pushd "${PROJECT_HOME}" > /dev/null

    set -a
    # shellcheck disable=SC1091
    source environments/stage.env
    set +a

    pushd "${PROJECT_NAME}" >/dev/null

        ./manage.py collectstatic --no-input
        cp ../assets/requirements.txt requirements.txt
        cat ../assets/requirements-stage.txt >> requirements.txt
        cp ../environments/stage.yaml app.yaml
        while read -r line; do
          [[ -z "${line}" ]] && continue
          key="$(echo "${line}" | cut -d'=' -f1)"
          value=''
          value="${line/$key=/$value}"
          echo "  ${key}: \"${value}\"" >> app.yaml
        done < "../environments/stage.env"
        gcloud auth activate-service-account --key-file=../service-account.json
        gcloud config set project "${GCP_PROJECT}"
        gcloud app deploy --version v1 --quiet
        rm app.yaml
        rm requirements.txt

    popd >/dev/null
  popd >/dev/null

}
