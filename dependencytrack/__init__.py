# Copyright 2020 Alvin Chen sonoma001@gmail.com
# SPDX-License-Identifier: GPL-2.0+

import logging
import requests

from .projects import Projects
from .components import Components
from .licenses import Licenses
from .exceptions import AuthenticationError, DependencyTrackApiError

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

class DependencyTrack(Projects, Components, Licenses):

    """Main DependencyTrack API class

    Manipulation against a running DependencyTrack instance is performed using an API key.

    :Example:

    >>> from dependencytrack import DependencyTrack
    >>> dt = DependencyTrack(url, api_key)

    .. note::
        
        The class instantiation exits if the session with the DependencyTrack server
        can't be established

    :param url: URL of the DependencyTrack instance
    :param api_key: The API key generated using the DependencyTrack UI
    :type url: str
    :type api_key: str
    :raises AuthenticationError: if the api_key couldn't be found
    """

    def __init__(self, url, api_key):
        self.host = url
        self.api_key = api_key

        self.api = self.host + "/api/v1"
        self.session = requests.Session()
        self.session.headers.update({"X-Api-Key": f"{self.api_key}", "X-Total-Count": '5aa0'})
        """
        Most APIs are paginated so if you have more than 100 results you’ll need to page through them.
        X-Total-Count header seems no use to increase the number of result.
        So using parameter is my workround for now. Guess 10000 will fit for most of situation.
        """
        self.paginated_param_payload = {'pageSize': "10000", 'pageNumber': "1"}

        logger.info(
            f"DependencyTrack instance against {self.host} using {self.api}"
        )
        
    def close(self):
        self.session.close()

    def search(self, query):
        """Search from the server
    
        API endpoint: GET /search/{query}
        
        :Example:
        >>> dt.search('dnsmasq-2.78')['results']['component']
        
        :return: the seatch result
        :rtype: dict {'license': [], 'project': [], 'component': [], 'vulnerability': []}
        :raises DependencyTrackApiError: if the REST call failed
        """
        response = self.session.get(self.api + f"/search/{query}", params=self.paginated_param_payload)
        if response.status_code == 200:
            return response.json()['results']
        else:
            description = f"Error while searching"
            raise DependencyTrackApiError(description, response)
            
    def search_component(self, query):
        """Search component from the server
    
        API endpoint: GET /component/?searchText={query}
        
        :Example:
        >>> dt.search_component('dnsmasq-2.78')
        
        :return: the seatch result
        :rtype: dict
        :raises DependencyTrackApiError: if the REST call failed
        """
        response = self.session.get(self.api + f"/component/?searchText={query}", params=self.paginated_param_payload)
        if response.status_code == 200:
            return response.json()
        else:
            description = f"Error while component searching"
            raise DependencyTrackApiError(description, response)

    def search_project(self, query):
        """Search project from the server
    
        API endpoint: GET /project/?searchText={query}
        
        :Example:
        >>> dt.search_project('my project')['results']['component']
        
        :return: the seatch result
        :rtype: dict
        :raises DependencyTrackApiError: if the REST call failed
        """
        response = self.session.get(self.api + f"/project/?searchText={query}", params=self.paginated_param_payload)
        if response.status_code == 200:
            return response.json()
        else:
            description = f"Error while project searching"
            raise DependencyTrackApiError(description, response)

    def search_vulnerability(self, query):
        """Search vulnerability from the server
    
        API endpoint: GET /vulnerability/?searchText={query}
        
        :Example:
        >>> dt.search_vulnerability('my vulnerability')
        
        :return: the seatch result
        :rtype: dict
        :raises DependencyTrackApiError: if the REST call failed
        """
        response = self.session.get(self.api + f"/vulnerability/?searchText={query}", params=self.paginated_param_payload)
        if response.status_code == 200:
            return response.json()
        else:
            description = f"Error while vulnerability searching"
            raise DependencyTrackApiError(description, response)

    def search_license(self, query):
        """Search license from the server
    
        API endpoint: GET /license/?searchText={query}
        
        :Example:
        >>> dt.search_license('my license')
        
        :return: the seatch result
        :rtype: dict
        :raises DependencyTrackApiError: if the REST call failed
        """
        response = self.session.get(self.api + f"/license/?searchText={query}", params=self.paginated_param_payload)
        if response.status_code == 200:
            return response.json()
        else:
            description = f"Error while license searching"
            raise DependencyTrackApiError(description, response)

