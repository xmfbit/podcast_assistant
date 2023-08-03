""" download audio from xiaoyuzhou """
from typing import Tuple, Optional
import requests
from bs4 import BeautifulSoup

__all__ = ['get_episode_info', 'download_audio_file']

def get_episode_info(url: str) -> Tuple[str, str, Optional[str]]:
    """ get episode info from the url """
    try:
        response = requests.get(url)
        response.raise_for_status()
    except requests.exceptions.RequestException as err:
        raise RuntimeError("Failed to download episode info: {}".format(err))
    
    soup = BeautifulSoup(response.text, 'html.parser')

    audio_tag = soup.find('meta', property="og:audio")
    title_tag = soup.find('meta', property="og:title")

    audio_url = audio_tag.get('content').strip() if audio_tag else None
    episode_title = title_tag.get('content').strip() if title_tag else None

    podcast_name = None
    if episode_title and audio_url:
        podcast_title_tags = soup.select('.podcast-title')
        if podcast_title_tags:
            podcast_name = podcast_title_tags[0].text.strip()
        if not podcast_name:
            podcast_name = None

        return audio_url, episode_title, podcast_name
    
    raise RuntimeError("Cannot get episode info from {}".format(url))


def download_audio_file(url: str, local_path: str):
    """ download audio file from url to given local file with stream """
    with requests.get(url, stream=True) as response:
        response.raise_for_status()
        with open(local_path, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)
        