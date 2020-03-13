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
        self.session.headers.update({"X-Api-Key": f"{self.api_key}"})

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
        response = self.session.get(self.api + f"/search/{query}")
        if response.status_code == 200:
            return response.json()['results']
        else:
            description = f"Error while searching"
            raise DependencyTrackApiError(description, response)

