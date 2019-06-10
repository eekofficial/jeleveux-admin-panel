from admitad import api, items
import re

class AdmitadLinkError(Exception):
    pass

class AdmitadCampaignError(Exception):
    pass

client_id = 'fb41868e5e22594acf4bd4957a870b'
client_secret = '8da1f502b3d5b263c8c501049bdc32'
scope = ' '.join(set([items.Me.SCOPE, items.DeeplinksManage.SCOPE, items.CampaignsForWebsite.SCOPE]))

client = api.get_oauth_client_client(
    client_id,
    client_secret,
    scope
)

def get_admitad_link(website, campaign, net_link, subid):
    try:
        link = client.DeeplinksManage.create(website, campaign, ulp=net_link, subid=subid)
        return link[0]
    except:
        raise AdmitadLinkError

def get_campaign_list(website):
    try:
        response = client.CampaignsForWebsite.get(website)['results']
        campaign_list = list()
        for i in response:
            campaign_list.append((i['id'], re.findall(r'://w{0,3}\.?([a-z]+)',i['site_url'])[0]))
        return campaign_list
    except:
        raise AdmitadCampaignError
