import argparse
import requests
import json
from pprint import pprint
from requests.exceptions import HTTPError
from requests.auth import HTTPBasicAuth


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
            url=f"{base_url}/query",
            headers={"Accept": "application/json"},
            auth=auth
        )

        # if response.status_code == 200:
        data = response.json()

        return data

    except HTTPError as err:
        print(err)


def get_succeeded_workflows_not_transferred(secrets):

    base_url, auth = prep_api_call(secrets)

    try:
        response = requests.get(
            url=f"{base_url}/query",
            headers={"Accept": "application/json"},
            params={
                "status": "Succeeded",
                "excludeLabelAnd": "flag:transferred"
            },
            auth=auth
        )

        # if response.status_code == 200:
        data = response.json()

        return data

    except HTTPError as err:
        print(err)


def set_label(secrets, workflow_id, key, value):

    base_url, auth = prep_api_call(secrets)

    try:
        response = requests.patch(
            url=f"{base_url}/{workflow_id}/labels",
            headers={
                "Content-Type": "application/json",
                "Accept": "application/json"
            },
            json={key: value},
            auth=auth
        )

        # if response.status_code == 200:
        data = response.json()

        return data

    except HTTPError as err:
        print(err)


def get_metadata(secrets, workflow_id):

    base_url, auth = prep_api_call(secrets)

    try:
        response = requests.patch(
            url=f"{base_url}/{workflow_id}/metadata",
            headers={
                "Content-Type": "application/json",
                "Accept": "application/json"
            },
            auth=auth
        )

        # if response.status_code == 200:
        data = response.json()

        return data

    except HTTPError as err:
        print(err)


def get_secrets(path_secrets_file):

    with open(path_secrets_file, "rt") as fin:
        data = json.loads(fin.read())

    return data


def main(path_secrets_file):

    secrets = get_secrets(path_secrets_file)

    get_all_workflows(secrets)

    set_label(
        secrets,
        "9782ec5f-0bb9-42b1-badd-73e2b6faf4e8",
        "flag", "transferred"
    )

    data = get_succeeded_workflows_not_transferred(secrets)

    pprint(data)

    metadata = get_metadata(secrets, "9782ec5f-0bb9-42b1-badd-73e2b6faf4e8")

    pprint(metadata)

    outputs = metadata["outputs"]

    pprint(outputs)


def parse_arguments():

    parser = argparse.ArgumentParser()

    parser.add_argument(
        "--secrets",
        action="store",
        dest="path_secrets_file",
        help="path to secrets file",
        required=True
    )

    # parse arguments
    params = parser.parse_args()

    return params


if __name__ == "__main__":

    params = parse_arguments()

    main(
        params.path_secrets_file
    )
