import os
import requests
import time
import jwt
from dateutil import parser


class Main():
  def list_self_hosted_runner_groups_for_an_organization(self, organization, application_id, installation_id, private_key):
    try:
      ## create jwt token
      current_time = int(time.time())
      print(f"current_time: {current_time}")
      payload = {
        # issued at time
        "iat": current_time,
        # JWT expiration time (10 minutes maximum)
        "exp": current_time + (10 * 60),
        # GitHub Apps identifier - you can't get it from the GitHub App Dashboard
        "iss": application_id
      }
      jwt_token = jwt.encode(payload, private_key, algorithm="RS256")

      ## create an installation access token for an app
      headers = {
        "Accept": "application/vnd.github+json",
        "X-GitHub-Api-Version": "2022-11-28",
        "Authorization": f"Bearer {jwt_token}"
      }
      url = f"https://api.github.com/app/installations/{installation_id}/access_token"
      response = requests.post(url, headers=headers)
      if response.status_code != 201:
        raise Exception("Falha ao gerar o access_token!")
      
      response_body = response.json()

      ## get access token
      token = response_body["token"]

      ## get expires access token
      expires_at = parser.parse(response_body["expires_at"]).astimezone(tz=None)
      print(f"expires_at: {expires_at}")

      url = f"https://api.github.com/orgs/{organization}/actions/runner-groups"

      payload = ""
      headers = {
        "Accept": "application/vnd.github+json",
        "X-GitHub-Api-Version": "2022-11-28",
        "Authorization": f"Bearer {token}"
      }

      response = requests.get(url, data=payload, headers=headers)

      print(f"Status Code: {response.status_code}")
      print(f"Response Body: {response.json()}")
    except Exception as error:
      print(f"Erro ao executar o método List self-hosted runner groups for an organization: {error}")

if __name__ == '__main__':
  application_id = os.getenv("GITHUB_APP_ID")
  installation_id = os.getenv("GITHUB_APP_INSTALLATION_ID")
  private_key = os.getenv("GITHUB_APP_PRIVATE_KEY")
  organization = os.getenv("GITHUB_APP_ORGANIZATION")
  TIME_SLEEP = os.getenv("TIME_SLEEP")
  main = Main()
  main.list_self_hosted_runner_groups_for_an_organization(organization, application_id, installation_id, private_key)
  time.sleep(int(TIME_SLEEP))
