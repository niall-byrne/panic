#!/bin/bash

set -e

deploy_prod() {

  pushd "${PROJECT_HOME}" > /dev/null

    set -a
    # shellcheck disable=SC1091
    source environments/prod.env
    set +a

    pushd "${PROJECT_NAME}" >/dev/null

        ./manage.py collectstatic
        cp ../assets/requirements.txt requirements.txt
        cat ../assets/requirements-prod.txt >> requirements.txt
        cp ../environments/prod.yaml app.yaml
        while read -r line; do
          [[ -z "${line}" ]] && continue
          key="$(echo "${line}" | cut -d'=' -f1)"
          value=''
          value="${line/$key=/$value}"
          echo "  ${key}: \"${value}\"" >> app.yaml
        done < "../environments/prod.env"
        gcloud app deploy --version v1
        rm app.yaml
        rm requirements.txt

    popd >/dev/null
  popd >/dev/null

}
