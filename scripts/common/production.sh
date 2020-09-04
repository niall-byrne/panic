#!/bin/bash

set -e

deploy_prod() {

  PROXY_FLAG=/tmp/PROXY

  pushd "${PROJECT_HOME}" > /dev/null
    pushd "${PROJECT_NAME}" >/dev/null

        set -a
        # shellcheck disable=SC1091
        source ../environments/prod.env
        # shellcheck disable=SC1091
        source ../environments/admin.env
        set +a

        [[ -f "${PROXY_FLAG}" ]] && echo "Cloud Proxy is already running, halting deploy..." && exit 0

        GOOGLE_APPLICATION_CREDENTIALS=/app/service-account.json cloud_sql_proxy --instances="${CLOUDSQLINSTANCE}=tcp:5432" &
        touch "${PROXY_FLAG}"

        ./manage.py wait_for_db
        ./manage.py migrate

        set -a
        # shellcheck disable=SC1091
        source ../environments/prod.env
        set +a

        ./manage.py collectstatic --no-input

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
        gcloud auth activate-service-account --key-file=../service-account.json
        gcloud config set project "${GCP_PROJECT}"
        gcloud app deploy --version v1 --quiet
        rm app.yaml
        rm requirements.txt

    popd >/dev/null
  popd >/dev/null

}
