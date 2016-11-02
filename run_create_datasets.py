import obtain_datasets as od


def register_datasets(api_url, url, installation_key, publisher_key, user, password, base_url=None, header={'Content-Type': 'application/json'},
                 payload={"installationKey":None,"publishingOrganizationKey":None,"title":None,"type":None}):
        scr = od.ScrapeLinks(url, base_url)
        zip_urls = scr.get_page_content()
        print(zip_urls)
        url_objects = od.RegisterDataset(zip_urls)
        titles = url_objects.gettitle(url_objects.res)
        titles_for_pop = titles[:]
        types = url_objects.gettype(url_objects.res)
        payload['installationKey'] = installation_key
        payload['publishingOrganizationKey'] = publisher_key
        for j in titles:
            mydataset = od.CreateDataset(header, payload, titles_for_pop.pop(), types.pop(), user, password, api_url)
            mydataset.create_dataset()
            mydataset.create_endpoint(mydataset.res, zip_urls.pop())
            mydataset.crawl_dataset(mydataset.res)
