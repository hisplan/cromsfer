#!/usr/bin/env python
import requests
from requests.exceptions import HTTPError
from requests.auth import HTTPBasicAuth

from cromsfer.constant import TransferStatus


def prep_api_call(secrets):

    api_version = "v1"
    url = secrets["url"]
    url = f"{url}/api/workflows/{api_version}"

    auth = HTTPBasicAuth(secrets["username"], secrets["password"])

    return url, auth


def get_all_workflows(secrets):

    base_url, auth = prep_api_call(secrets)

    try:
        response = requests.get(
            url=f"{base_url}/query", headers={"Accept": "application/json"}, auth=auth
        )

        if response.status_code == 401:
            raise Exception("Unauthorized access!")

        data = response.json()

        return data

    except HTTPError as err:
        print(err)


def get_succeeded_workflows_not_transferred(secrets):

    base_url, auth = prep_api_call(secrets)

    try:
        # fixme: doesn't work. maybe cromwell bug?
        # response = requests.get(
        #     url=f"{base_url}/query",
        #     headers={"Accept": "application/json"},
        #     params={
        #         "status": "Succeeded",
        #         "excludeLabelOr": "transfer:done",
        #         "excludeLabelOr": "transfer:initiated",
        #         "excludeLabelOr": "transfer:failed"
        #     },
        #     auth=auth
        # )

        # 1. only successful runs
        # 2. only those with no value set for the `transfer` label
        response = requests.get(
            url=f"{base_url}/query",
            headers={"Accept": "application/json"},
            params={
                "status": "Succeeded",
                "label": "transfer:" + TransferStatus.NONE,
            },
            auth=auth,
        )

        if response.status_code == 401:
            raise Exception("Unauthorized access!")

        data = response.json()

        return data

    except HTTPError as err:
        print(err)


def set_label(secrets, workflow_id, key, value):

    base_url, auth = prep_api_call(secrets)

    try:
        response = requests.patch(
            url=f"{base_url}/{workflow_id}/labels",
            headers={"Content-Type": "application/json", "Accept": "application/json"},
            json={key: value},
            auth=auth,
        )

        if response.status_code == 401:
            raise Exception("Unauthorized access!")

        data = response.json()

        return data

    except HTTPError as err:
        print(err)


def get_metadata(secrets, workflow_id):

    base_url, auth = prep_api_call(secrets)

    try:
        response = requests.patch(
            url=f"{base_url}/{workflow_id}/metadata",
            headers={"Content-Type": "application/json", "Accept": "application/json"},
            auth=auth,
        )

        if response.status_code == 401:
            raise Exception("Unauthorized access!")

        data = response.json()

        return data

    except HTTPError as err:
        print(err)
