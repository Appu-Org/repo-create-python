# import argparse
import os, json
import logging
# import urllib3
import requests
from requests.auth import HTTPBasicAuth
# import system

class GitHubConnect():
    def __init__(self, github_url, organisation_name, github_user, github_pat, repo_name):
        self.github_url = github_url
        self.github_organisation_name = organisation_name
        self.github_user = github_user
        self.github_pat = github_pat
        self.repo_name = repo_name
#         self.branch_name = branch_name
        
    def create_repository(self):
        # https://docs.github.com/en/rest/reference/repos#create-a-repository-using-a-template
        data = {'name':self.repo_name, "owner": self.github_organisation_name, "private": True }
        URL = self.github_url + "/orgs/" + self.github_organisation_name + "/repos"
        response_data, response_code = self.post_api_call(URL, json.dumps(data))
        logging.debug(response_data)
        if (response_code == 201):
            self.patch_repository_to_internal()
            print("Repository has been created at ",self.github_organisation_name)
            
        else:
            logging.error("Unable to create the repository: " + self.repo_name)
            exit(1)

    
    def post_api_call(self, url, data):      
        logging.info("post_api_call URL: " + url)
        response = requests.post(url, data=data, auth=(self.github_user, self.github_pat))
        logging.info("POST call response: " + str(response))
        print("--+post_api_call",response)
        return response.text, response.status_code
    
    def patch_repository_to_internal(self):
        data = {"visibility": "internal"}
        URL = self.github_url + "/repos/" + self.github_organisation_name + "/" + self.repo_name
        response_data, response_code = self.post_api_call(URL, json.dumps(data))
        print("--+patch_repository_to_internal",URL,response_code)
        logging.debug(response_data)
        if response_code  == 200:
            logging.error("Unable to update repository to internal group")
            exit(1)
def main():
    
#     parser = argparse.ArgumentParser(description='Single Click Utility')
#     parser.add_argument('pat', help='Please provide the GitHub PAT (Persional Access Token)', required=True)
#     args = vars(parser.parse_args())
   
    github_url = os.environ['github_url']
    github_pat = os.environ['token']
    github_user = os.environ['git_user']
    # print("repo_owner--",repo_owner)
    # print("github_user--",github_user)
    # print("github_pat--",github_pat)
    # print("github_url--",github_url)
   
    organisation_name = "philips-test-org"
    # organisation_name = "Appu-Test-org"
    repo_name = "testrepo7"
    # github_url = "https://api.github.com"
    # github_user = "appuraj-philips"
    # github_pat ="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" 

    # try:
    #      github_pat = os.environ['pat']
    # except KeyError: 
    #         print ("Please set the environment variable pat")

    print("----------------++++++++----main.py-----+++++++++-----------------")
    github = GitHubConnect(github_url, organisation_name, github_user, github_pat, repo_name)
    if True:
        github.create_repository()
    else:
        print("Fail to create Repository")
    
if __name__ == '__main__':
    main()
