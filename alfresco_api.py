import requests

class AlfrescoAPI:
    def __init__(self, base_url, username, password):
        self.base_url = base_url
        self.username = username
        self.password = password

class AlfrescoSearchAPI(AlfrescoAPI):
    def search_by_name(self, document_title: str):
        url = f"{self.base_url}/alfresco/api/-default-/public/search/versions/1/search"
        body = {
            "query": {
                "query": f"cm:name:\"{document_title}\""
            }
        }
        return requests.post(url, json=body, auth=(self.username, self.password)).json()
    
class AlfrescoNodeAPI(AlfrescoAPI):
    def get_node_content(self, node_id: str):
        url = f"{self.base_url}/alfresco/api/-default-/public/alfresco/versions/1/nodes/{node_id}/content?attachment=false"
        return requests.get(url, auth=(self.username, self.password)).content.decode("utf-8")

class AlfrescoDiscoveryAPI(AlfrescoAPI):
    def get_repository_info(self):
        url = f"{self.base_url}/alfresco/api/discovery"
        return requests.get(url, auth=(self.username, self.password)).json()