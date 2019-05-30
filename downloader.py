import requests
from urllib3 import PoolManager


class Downloader:

    def __init__(self):
        self.content_length = None
        self.current_chunk = None
        self.local_filename = None
        self.headers = None

    def is_downloadable(self, url):
        h = requests.head(url, allow_redirects=True)
        header = h.headers
        content_type = header.get('content-type')
        if 'text' in content_type.lower():
            return False
        if 'html' in content_type.lower():
            return False
        return True

    def download(self, url):
        if self.is_downloadable(url):
            self.local_filename = url.split('/')[-1]
        else:
            print("Unable to download")
            return
        with requests.get(url, stream="True") as response:
            response.raise_for_status()
            with open(self.local_filename, "wb") as file:
                self.current_chunk = 1
                self.content_length = self.get_headers(url)['Content-Length']
                for chunk in response.iter_content():
                    if self.current_chunk >= int(self.content_length)/2:
                        break
                    self.current_chunk+=1
                    if chunk:
                        print(self.current_chunk)
                        file.write(chunk)
                        #file.flush()

                file.close()


    #def pause

    def resume(self, url):
        if self.is_resumable(url):
            resume_header = {'Accept-Encoding': 'gzip', 'Range': 'bytes={}-'.format(self.current_chunk)}
            with requests.get(url, headers=resume_header, stream=True) as response:
                response.raise_for_status()
                with open(self.local_filename, 'a') as file:
                    for chunk in response.iter_content():
                        if chunk:
                            print("r{}".format(self.current_chunk))
                            file.write(str(chunk))
                        self.current_chunk += 1
                    file.close()

    def is_resumable(self, url):
        headers = self.get_headers(url)
        if headers['Accept-Ranges'] == 'bytes':
            return True
        else:
            return False

    def get_headers(self, url):
        pool = PoolManager()
        response = pool.request('GET', url, preload_content=False)
        return response.headers



    #def stop

url = 'http://cdn2.discovertuscany.com/img/livorno/livorno-terrazza-mascagni-6.jpg'
downloader = Downloader()
downloader.download(url)
downloader.resume(url)