import zipfile as z
import requests
import xml.etree.ElementTree as etree
import json
from io import BytesIO
import re


class RegisterDataset(object):
    """Gets the dataset titles and gets the datasets of type 'occurrence' only"""
    def __init__(self, url_list):
        self.res = []
        try:
            for url in url_list:
                self.res.append(requests.get(url))
        except requests.exceptions.MissingSchema as e:
            print('\n !!!', e)


    def gettitle(self, res):
        pattern = re.compile("eml\.xml$")
        title = []
        for j in res:
            with z.ZipFile(BytesIO(j.content)) as zipper:
                #print(zipper.namelist())
                nl = zipper.namelist()
                for name in nl:
                    if pattern.search(name):
                        with zipper.open(name) as eml:
                            myeml = eml.read().decode('utf-8-sig')
                            root = etree.fromstring(myeml)
                            #print(root.tag, '-- this should be it.')
                            for j in root.findall('dataset'):
                                title.append(j.find('title').text)
        return title

    def gettype(self, res):
        '''
        :param res: A list of URL objects
        :return: The type of dataset either OCCURRENCE or SAMPLING EVENT
        '''
        pattern = re.compile("meta\.xml$")
        dwc_type = []
        for j in res:
            with z.ZipFile(BytesIO(j.content)) as zipper:
                nl = zipper.namelist()
                for name in nl:
                    if pattern.search(name):
                        with zipper.open(name) as meta:
                            mymeta = meta.read().decode('utf-8-sig')
                            root = etree.fromstring(mymeta)
                            for j in root:
                                print(j.tag)
                                if j.tag == "{http://rs.tdwg.org/dwc/text/}core":
                                    rt = j.get('rowType')
                                    if rt == "http://rs.tdwg.org/dwc/terms/Occurrence":
                                        dwc_type.append('OCCURRENCE')
                                    if rt == "http://rs.tdwg.org/dwc/terms/Event":
                                        dwc_type.append('SAMPLING_EVENT')
        return dwc_type

    def getendpoint(self, endpoint_uuid, res):
        '''
        Search for dataset endpoints. DEVELOPMENT ON HOLD.
        :param endpoint_uuid: For the installation/{UUID}/dataset API that returns a dataset list
        :param res:
        :return:
        '''
        pass


class CreateDataset(object):
    """Creates  datasets in the GBIF registry and crawls them"""
    def __init__(self, header, payload, title, type, user, pw, api_url='http://api.gbif.org/v1/dataset'):
        '''
        :param header: Metadata for the API call. JSON expected.
        :param payload: Parameters going into the API call (installation key and publisher key)
        :param title: Dataset title
        :param type: Dataset type
        :param user: GBIF user name
        :param pw: Password to the GBIF account
        :param api_url: The key word arg
        '''
        self.api_url = api_url
        self.header = header
        payload['title'] = title
        payload['type'] = type
        print(payload)
        self.payload = payload
        self.credentials = (user, pw)


    def create_dataset(self):
        #Creates the global res var that contains the dataset UUID
        self.res = requests.post(self.api_url, auth=self.credentials, data=json.dumps(self.payload), headers=self.header).text
        self.res = self.res.strip('"')
        print(self.res)


    def create_endpoint(self, dataset_uuid, endpoint):
        '''
        :param dataset_uuid: Dataset key (GBIF UUID)
        :param endpoint: Dataset DwC archive endpoint
        :return: Endpoint ID
        '''
        create_endpoint_url = '{}/{}/endpoint'.format(self.api_url, dataset_uuid)
        print(create_endpoint_url)
        jsn = {"type": "DWC_ARCHIVE", "url": endpoint}
        r = requests.post(create_endpoint_url, auth=self.credentials, data=json.dumps(jsn), headers=self.header)
        print(r.text)
        return r.text


    def crawl_dataset(self, uuid):
        '''
        :param uuid: Dataset to be crawled
        '''
        crawlurl = '{}/{}/crawl'.format(self.api_url, uuid)
        print(crawlurl)
        print(self.credentials)
        requests.post(crawlurl, auth=self.credentials)
