"""
FB Manager Pro - Hidemium API Service
Handle communication with Hidemium Browser API
"""

import requests
import json
from typing import List, Dict, Optional, Any
from config import API_CONFIG


class HidemiumAPI:
    """Hidemium Browser API Client"""
    
    def __init__(self, base_url: str = None):
        self.base_url = base_url or API_CONFIG["hidemium_base_url"]
        self.timeout = API_CONFIG["timeout"]
    
    def _request(self, method: str, endpoint: str, data: Dict = None) -> Dict:
        """Make HTTP request to Hidemium API"""
        url = f"{self.base_url}{endpoint}"
        
        try:
            if method == "GET":
                response = requests.get(url, timeout=self.timeout)
            elif method == "POST":
                response = requests.post(url, json=data, timeout=self.timeout)
            elif method == "PUT":
                response = requests.put(url, json=data, timeout=self.timeout)
            elif method == "DELETE":
                response = requests.delete(url, timeout=self.timeout)
            else:
                return {"success": False, "error": f"Unknown method: {method}"}
            
            response.raise_for_status()
            return {"success": True, "data": response.json()}
        
        except requests.exceptions.ConnectionError:
            return {"success": False, "error": "Cannot connect to Hidemium. Is it running?"}
        except requests.exceptions.Timeout:
            return {"success": False, "error": "Request timeout"}
        except requests.exceptions.HTTPError as e:
            return {"success": False, "error": f"HTTP Error: {e}"}
        except json.JSONDecodeError:
            return {"success": True, "data": response.text}
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    # ========== PROFILE OPERATIONS ==========
    
    def get_profiles(self, folder_id: str = None, page: int = 1, limit: int = 100) -> Dict:
        """Get list of profiles from Hidemium"""
        endpoint = f"/api/v2/profiles?page={page}&limit={limit}"
        if folder_id:
            endpoint += f"&folder_id={folder_id}"
        return self._request("GET", endpoint)
    
    def get_profile(self, uuid: str) -> Dict:
        """Get single profile by UUID"""
        return self._request("GET", f"/api/v2/profiles/{uuid}")
    
    def create_profile(self, profile_data: Dict) -> Dict:
        """Create a new profile"""
        return self._request("POST", "/api/v2/profiles", profile_data)
    
    def update_profile(self, uuid: str, profile_data: Dict) -> Dict:
        """Update an existing profile"""
        return self._request("PUT", f"/api/v2/profiles/{uuid}", profile_data)
    
    def delete_profile(self, uuid: str) -> Dict:
        """Delete a profile"""
        return self._request("DELETE", f"/api/v2/profiles/{uuid}")
    
    # ========== BROWSER OPERATIONS ==========
    
    def start_browser(self, uuid: str, headless: bool = False) -> Dict:
        """Start browser for a profile"""
        data = {"headless": headless}
        return self._request("POST", f"/api/v2/profiles/{uuid}/start", data)
    
    def stop_browser(self, uuid: str) -> Dict:
        """Stop browser for a profile"""
        return self._request("POST", f"/api/v2/profiles/{uuid}/stop")
    
    def get_browser_status(self, uuid: str) -> Dict:
        """Get browser running status"""
        return self._request("GET", f"/api/v2/profiles/{uuid}/status")
    
    def get_active_browsers(self) -> Dict:
        """Get list of running browsers"""
        return self._request("GET", "/api/v2/profiles/active")
    
    # ========== FOLDER OPERATIONS ==========
    
    def get_folders(self) -> Dict:
        """Get list of folders"""
        return self._request("GET", "/api/v2/folders")
    
    def create_folder(self, name: str) -> Dict:
        """Create a new folder"""
        return self._request("POST", "/api/v2/folders", {"name": name})
    
    # ========== UTILITY ==========
    
    def health_check(self) -> bool:
        """Check if Hidemium API is reachable"""
        result = self._request("GET", "/api/v2/health")
        return result.get("success", False)
    
    def get_version(self) -> str:
        """Get Hidemium version"""
        result = self._request("GET", "/api/v2/version")
        if result.get("success"):
            return result.get("data", {}).get("version", "Unknown")
        return "Unknown"


# Global API instance
hidemium_api = HidemiumAPI()


def test_connection() -> Dict:
    """Test connection to Hidemium"""
    api = HidemiumAPI()
    is_healthy = api.health_check()
    version = api.get_version() if is_healthy else "N/A"
    
    return {
        "connected": is_healthy,
        "version": version,
        "base_url": api.base_url
    }
