from requests import Session

class LoggedInException(Exception):

    def __init__(self, *args, **kwargs):
        super(LoggedInException, self).__init__(*args, **kwargs)

class UnifiVideoApi(object):
    _verify_ssl=None
    _baseurl = "/api/2.0/"
    _host = None
    _apikey = None

    def __init__(self, host="https://unifivideo:7443", apikey: str=None, verify_ssl: bool=False):
        self._session = Session()
        self._host = host
        self._apikey = apikey
        self._verify_ssl = verify_ssl

    def _apigetrequest(self, path, params=None):
        return self._session.get(self._host + self._baseurl + path + "?apiKey=" + self._apikey, verify=self._verify_ssl)

    def _apiputrequest(self, path, data):
        return self._session.put(self._host + self._baseurl + path + "?apiKey=" + self._apikey, verify=self._verify_ssl, json=data)

    def getcamera(self, id=None):
        path = "camera"

        if id != None:
            path += "/" + id
        r = self._apigetrequest(path)

        if r.status_code == 401:
            raise LoggedInException("Invalid login, or apikey")

        if r.status_code != 200:
            raise Exception("Received status code " + str(r.status_code) + " from the api.")

        return r.json()['data']

    def postcamera(self, id, data):
        path = "camera/" + id

        r = self._apiputrequest(path, data)

        if r.status_code == 401:
            raise LoggedInException("Invalid login, or apikey")

        if r.status_code != 200:
            raise Exception("Received status code " + str(r.status_code) + " from the api.")

        return r.json()['data']