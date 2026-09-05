import json
import logging
import ssl
import urllib.parse
import urllib.request
import urllib.error
from typing import Optional, List, Dict, Any

try:
    import certifi
    SSL_CONTEXT = ssl.create_default_context(cafile=certifi.where())
except ImportError:
    SSL_CONTEXT = ssl.create_default_context()

logger = logging.getLogger(__name__)

class LRCLIBClient:
    """In-process HTTP client for the public LRCLIB API."""
    BASE_URL = "https://lrclib.net/api"
    USER_AGENT = "Flexioke/0.2.6 (https://github.com/reg-almonte/flexioke)"
    TIMEOUT = 5.0

    def __init__(self, base_url: str = BASE_URL, timeout: float = TIMEOUT):
        self.base_url = base_url.rstrip("/")
        self.timeout = timeout

    def _make_request(self, endpoint: str, params: Optional[Dict[str, Any]] = None) -> Optional[Any]:
        """Internal helper to execute GET requests against LRCLIB."""
        url = f"{self.base_url}/{endpoint.lstrip('/')}"
        if params:
            url += "?" + urllib.parse.urlencode({k: v for k, v in params.items() if v is not None})

        req = urllib.request.Request(
            url,
            headers={
                "User-Agent": self.USER_AGENT,
                "Accept": "application/json"
            }
        )

        try:
            with urllib.request.urlopen(req, timeout=self.timeout, context=SSL_CONTEXT) as response:
                status = getattr(response, "status", None)
                if status is not None and isinstance(status, int) and status != 200:
                    return None
                data = response.read()
                if isinstance(data, bytes):
                    data = data.decode("utf-8")
                return json.loads(data)
        except urllib.error.HTTPError as e:
            if e.code == 404:
                logger.debug("LRCLIB endpoint returned 404 Not Found: %s", url)
            else:
                logger.warning("LRCLIB HTTP error %s for URL: %s", e.code, url)
        except Exception as e:
            logger.warning("LRCLIB request error for %s: %s", url, e)

        return None

    def get_lyrics(
        self,
        track_name: str,
        artist_name: Optional[str] = None,
        duration: Optional[float] = None
    ) -> Dict[str, Any]:
        """Fetches lyrics for a track, first trying exact lookup then fuzzy search fallback."""
        if not track_name or not track_name.strip():
            return {
                "found": False,
                "lyrics": "",
                "has_timestamps": False,
                "message": "Track name cannot be empty"
            }

        params: Dict[str, Any] = {"track_name": track_name.strip()}
        if artist_name and artist_name.strip():
            params["artist_name"] = artist_name.strip()
        if duration is not None:
            params["duration"] = round(duration)

        # 1. Try exact lookup
        data = self._make_request("get", params)

        # 2. Fallback to fuzzy search if not found
        if not data:
            query = f"{track_name} {artist_name or ''}".strip()
            results = self.search_lyrics(query)
            if results:
                # Prefer result with synced lyrics
                synced_match = next((r for r in results if r.get("has_synced_lyrics")), None)
                chosen = synced_match or results[0]
                return {
                    "found": True,
                    "id": chosen.get("id"),
                    "track_name": chosen.get("track_name") or track_name,
                    "artist_name": chosen.get("artist_name") or (artist_name or ""),
                    "duration": chosen.get("duration"),
                    "synced_lyrics": chosen.get("synced_lyrics"),
                    "plain_lyrics": chosen.get("plain_lyrics"),
                    "lyrics": chosen.get("lyrics") or "",
                    "has_timestamps": chosen.get("has_synced_lyrics", False),
                }

        if data and isinstance(data, dict):
            synced = data.get("syncedLyrics")
            plain = data.get("plainLyrics")
            lyrics = synced or plain or ""
            return {
                "found": bool(lyrics),
                "id": data.get("id"),
                "track_name": data.get("trackName") or track_name,
                "artist_name": data.get("artistName") or (artist_name or ""),
                "duration": data.get("duration"),
                "synced_lyrics": synced,
                "plain_lyrics": plain,
                "lyrics": lyrics,
                "has_timestamps": bool(synced),
            }

        return {
            "found": False,
            "lyrics": "",
            "has_timestamps": False,
            "message": "No matching lyrics found on LRCLIB"
        }

    def search_lyrics(self, query: str) -> List[Dict[str, Any]]:
        """Searches LRCLIB for candidate tracks matching a query string."""
        if not query or not query.strip():
            return []

        data = self._make_request("search", {"q": query.strip()})
        if not data or not isinstance(data, list):
            return []

        results = []
        for item in data:
            synced = item.get("syncedLyrics")
            plain = item.get("plainLyrics")
            results.append({
                "id": item.get("id"),
                "track_name": item.get("trackName") or "",
                "artist_name": item.get("artistName") or "",
                "album_name": item.get("albumName") or "",
                "duration": item.get("duration"),
                "has_synced_lyrics": bool(synced),
                "synced_lyrics": synced,
                "plain_lyrics": plain,
                "lyrics": synced or plain or ""
            })
        return results

lrclib_client = LRCLIBClient()
