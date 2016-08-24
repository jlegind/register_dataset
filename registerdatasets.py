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
        for url in url_list:
            self.res.append(requests.get(url))


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
        self.api_url = api_url
        self.header = header
        payload['title'] = title
        payload['type'] = type
        print(payload)
        self.credentials = (user, pw)
        self.res = requests.post(api_url, auth=self.credentials, data=json.dumps(payload), headers=header).text
        self.res = self.res.strip('"')
        print(self.res)


    def create_endpoint(self, dataset_uuid, endpoint):
        create_endpoint_url = '{}/{}/endpoint'.format(self.api_url, dataset_uuid)
        print(create_endpoint_url)
        print(endpoint, "TEST")
        jsn = {"type": "DWC_ARCHIVE", "url": endpoint}
        r = requests.post(create_endpoint_url, auth=self.credentials, data=json.dumps(jsn), headers=self.header)
        print(r.text)
        return r.text


    def crawl_dataset(self, uuid):
        crawlurl = '{}/v1/dataset/{}/crawl'.format(self.api_url, uuid)
        print(crawlurl)
        requests.post(crawlurl, auth=self.credentials)

##TEST CODE##
# myurl = 'http://asnhc.angelo.edu/archives/'
# archive = ['http://asnhc.angelo.edu/archives/dwca-angelo-reptiles.zip', 'http://asnhc.angelo.edu/archives/dwca-angelo-plants.zip']
# chk = CheckDataset(archive)
# titles = chk.gettitle(chk.res)
# titles_pop = titles[:]
# #essentially makes a copy
# print(titles)
# types = chk.gettype(chk.res)
# print(types)
#
# header = {'Content-Type': 'application/json'}
# payload = {"installationKey":"afafe88e-4b8e-4e62-8f38-3eaa24f71532","publishingOrganizationKey":"9c0a8aa8-4ce7-49ba-aac7-21a97234f886","title":None,
#              "type":None}
# uat_api = 'http://api.gbif-uat.org/v1/dataset'
#
# for j in titles:
#     mydataset = CreateDataset(header, payload, titles_pop.pop(), types.pop(), 'jlegind', 'mussimus', api_url=uat_api)
#     mydataset.create_endpoint(mydataset.res, archive.pop())
#     mydataset.crawl_dataset(mydataset.res)
## ##
