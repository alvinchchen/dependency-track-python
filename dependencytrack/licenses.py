# Copyright 2020 Alvin Chen sonoma001@gmail.com
# SPDX-License-Identifier: GPL-2.0+

import logging

from .exceptions import AuthorizationError, DependencyTrackApiError

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

class Licenses:
    """Class dedicated to all "licenses" related endpoints"""

    def list_licenses(self):
        """List all licenses

        API Endpoint: GET /license

        :return: a list of licenses
        :rtype: list()
        :raises DependencyTrackApiError: if the REST call failed
        """
        response = self.session.get(self.api + "/license", params=self.paginated_param_payload)
        if response.status_code == 200:
            return response.json()
        else:
            description = f"Unable to get a list of components"
            raise DependencyTrackApiError(description, response)
            return None
            
    def list_concise_licenses(self):
        """List all concise licenses

        API Endpoint: GET /license/concise

        :return: a list of  concise licenses
        :rtype: list()
        :raises DependencyTrackApiError: if the REST call failed
        """
        response = self.session.get(self.api + "/license/concise", params=self.paginated_param_payload)
        if response.status_code == 200:
            return response.json()
        else:
            description = f"Unable to get a list of components"
            raise DependencyTrackApiError(description, response)
            return None

    def get_license(self, licenseId):
        """Get details of license.
    
        API Endpoint: GET /license/{licenseId}
    
        :param licenseId: the SPDX ID of the license
        :type licenseId: string
        :return: the requested license
        :rtype: license dist
        :raises DependencyTrackApiError: if the REST call failed
        """
        response = self.session.get(self.api + f"/license/{licenseId}")
        if response.status_code == 200:
            return response.json()
        else:
            description = f"Error while getting license {licenseId}"
            raise DependencyTrackApiError(description, response)

