import requests

class AlfrescoAPI:
    def __init__(self, base_url, username, password):
        self.base_url = base_url
        self.auth = (username, password)

class AlfrescoSearchAPI(AlfrescoAPI):
    def search_by_name(self, document_title: str):
        url = f"{self.base_url}/alfresco/api/-default-/public/search/versions/1/search"
        body = {
            "query": {
                "query": f"cm:name:\"{document_title}\""
            }
        }
        return requests.post(url, json=body, auth=self.auth).json()

    def search_folders_by_name(self, folder_name: str):
        url = f"{self.base_url}/alfresco/api/-default-/public/search/versions/1/search"
        body = {
            "query": {
                "query": f"cm:name:\"{folder_name}\" and TYPE:folder",
                "language": "afts"
            }
        }
        return requests.post(url, json=body, auth=self.auth).json()

    def search_recent_docs_snippets(self, search_term: str):
        url = f"{self.base_url}/alfresco/api/-default-/public/search/versions/1/search"
        body = {
            "query": {
                "query": f"TEXT:\"{search_term}\" and TYPE:content and @cm:modified:[NOW-1DAY TO NOW]"
                },
                "highlight": {
                    "snippetCount": 10,
                    "fragmentSize": 256,
                    "mergeContiguous": True,
                    "fields": [
                        {
                            "field": "cm:content",
                            "prefix": "**",
                            "postfix": "**"
                        }
                    ]
                }
            }
        return requests.post(url, json=body, auth=self.auth).json()
    
class AlfrescoNodeAPI(AlfrescoAPI):
    def get_node_content(self, node_id: str):
        url = f"{self.base_url}/alfresco/api/-default-/public/alfresco/versions/1/nodes/{node_id}/content?attachment=false"
        return requests.get(url, auth=self.auth).content.decode("utf-8")

    def upload_file(self, file_path: str, parent_id: str):
        url = f"{self.base_url}/alfresco/api/-default-/public/alfresco/versions/1/nodes/{parent_id}/children"
        files = {"filedata": open(file_path, "rb")}
        return requests.post(url, files=files, auth=self.auth).json()

    def copy_to_folder(self, node_id: str, folder_id: str):
        url = f"{self.base_url}/alfresco/api/-default-/public/alfresco/versions/1/nodes/{node_id}/copy"
        body = {
            "targetParentId": f"{folder_id}"
        }
        return requests.post(url, json=body, auth=self.auth).json()


class AlfrescoDiscoveryAPI(AlfrescoAPI):
    def get_repository_info(self):
        url = f"{self.base_url}/alfresco/api/discovery"
        return requests.get(url, auth=self.auth).json()