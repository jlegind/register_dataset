import obtain_datasets as od

url = "http://asnhc.angelo.edu/archives/"
scr = od.ScrapeLinks(url, "http://asnhc.angelo.edu/archives/")
zip_urls = scr.get_page_content()

print(zip_urls)


chk = od.RegisterDataset(zip_urls)
titles = chk.gettitle(chk.res)
titles_pop = titles[:]
#essentially makes a copy
print(titles)
types = chk.gettype(chk.res)
print(types)

header = {'Content-Type': 'application/json'}
payload = {"installationKey":"afafe88e-4b8e-4e62-8f38-3eaa24f71532","publishingOrganizationKey":"9c0a8aa8-4ce7-49ba-aac7-21a97234f886","title":None,
             "type":None}
uat_api = 'http://api.gbif-uat.org/v1/dataset'

for j in titles:
    mydataset = od.CreateDataset(header, payload, titles_pop.pop(), types.pop(), 'jlegind', 'mussimus', api_url=uat_api)
    mydataset.create_endpoint(mydataset.res, zip_urls.pop())
    mydataset.crawl_dataset(mydataset.res)
