import json
import requests
import pandas as pd
import time

def get_profile_data(url, token,profile_id):    
    data={"payload":{"profile_id":profile_id ,"profile_schema_and_version": "cortex/TestAccount"}}
    data=json.dumps(data)
    headers={'Content-Type': 'application/json','Authorization': 'Bearer {}'.format(token)}
    activation_data=requests.post(url,headers=headers,data=data).json()
    time.sleep(4)
    if activation_data['success']:
        activation_id=activation_data['activationId']
        profile_data=requests.get('https://api.cortex.insights.ai/v3/agents/services/activations/'+str(activation_id),headers=headers).json()
    return profile_data

def get_profiles_list():
     file = open("datapreparation/profiles.txt","r") 
     profiles_list = file.read().splitlines()
     return profiles_list


def parse_profile_data(url,token):
    final_list=[]
    profiles_list=get_profiles_list()
    for profile_id in profiles_list:
        profile_data=get_profile_data(url,token,profile_id)

        entities=[]
        contacts=[]
        d={}
        d['profile_id']=profile_id
        #print (profile_id)
        for i in profile_data['activation']['response']['profile']['attributes']:
            if i['attributeKey'] == 'AccountName':
                account_value=i['attributeValue']['value']
                d['account_name']=account_value
            if i['attributeKey'] == 'Competitors':
                competitor_value=i['attributeValue']['value']
                d['competitor_names']=competitor_value
            if i['attributeKey'] == 'Industry':
                industry_value=i['attributeValue']['value']
                d['industry_name']=industry_value
            if i['attributeKey'] == 'Entities':
                for j in i['attributeValue']['value']:
                    for k in j['entities']:
                        entities.append(k['token'])
                        d['entities']=entities
            if i['attributeKey'] == 'Contacts':
                for j in i['attributeValue']['value']:
                    contacts.append(j['ContactName'])
                    d['contacts']=contacts

            if i['attributeKey'] == 'Opportunity':
                for j in  i['attributeValue']['value']:
                     if len(i['attributeValue']['value']) > 0:
                            count=len(i['attributeValue']['value'])+1
                            for z in range(1,count):
                                OpportunityName='OpportunityName'+str(z)
                                OpportunityStatus='OpportunityStatus'+str(z)
                                Amount='Amount'+str(z)
                                ExecSponsor='ExecSponsor'+str(z)
                                d[OpportunityName]=j['OpportunityName']
                                d[OpportunityStatus]=j['OpportunityStatus']
                                d[Amount]=j['Amount']
                                d[ExecSponsor]=j['ExecSponsor']




        final_list.append(d)
    return final_list


def remove_text(x):
    number=x['Amount1']
    if number.isdigit(): 
        return number
    else:
        return 0

def random_competitors(x):
    a= x['account_name']
    b= x['competitor_names_y']
    if len(b) > 1:
        b.remove(a)
        y=b[0]
        b.append(a)
    else:
        y=b[0]
    return y

def get_df_competitors(original_df):
    t = []
    for i in original_df["industry_name"].unique():
        t.append({"industry_name": i, "competitor_names": list(original_df[original_df["industry_name"]==i]["account_name"])})
    competitor_df = pd.DataFrame(t)
    merge_df=pd.merge(original_df,competitor_df, on='industry_name')
    merge_df['competitor_names_x'] = merge_df.apply(random_competitors, axis=1)
    merge_df=merge_df[["Amount1","ExecSponsor1","OpportunityName1","OpportunityStatus1","account_name","competitor_names_x","contacts","industry_name","profile_id"]]
    merge_df = merge_df.rename(columns={'competitor_names_x':'competitor_names'})
    return merge_df



def main():
	token='eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJjb2duaXRpdmVzY2FsZS5jb20iLCJhdWQiOiJjb3J0ZXgiLCJzdWIiOiJzc3dldGFuayIsInRlbmFudCI6ImNvcnRleC1hY2NlbGVyYXRvcnMiLCJiZWFyZXIiOiJwdWJsaWMiLCJrZXkiOiI0dk9zRVRFZFJtazl0T0NFdUV4UnRsdEVuVllnck9VdiIsImV4cCI6MTU5MTY5MzE4OCwiYWNsIjp7Ii4qIjpbIlJFQUQiLCJSVU4iLCJXUklURSIsIkRFTEVURSJdLCIvdjMvYWdlbnRzL2Vudmlyb25tZW50cy8uKiI6WyJERU5ZIl0sIi92Mi90ZW5hbnRzL2N1cnJlbnQtdXNlci1kZXRhaWxzIjpbIlJFQUQiXSwiL3YyL2FkbWluLy4qIjpbIkRFTlkiXSwiL3YyL2FjY291bnRzLy4qIjpbIkRFTlkiXSwiL3YyL3RlbmFudHMvLioiOlsiREVOWSJdLCIvdjIvYWNjb3VudHMvdG9rZW5zLy4qIjpbIlJFQUQiLCJSVU4iLCJXUklURSJdLCIvdjIvdGVuYW50cy9zZWNyZXRzLy4qIjpbIlJFQUQiLCJSVU4iLCJXUklURSJdLCIvdjMvYWdlbnRzL2Vudmlyb25tZW50cy9jb3J0ZXgvZGVmYXVsdCI6WyJSRUFEIiwiUlVOIiwiV1JJVEUiXSwiL3YzL2NhdGFsb2cvLioiOlsiUkVBRCIsIlJVTiIsIldSSVRFIiwiREVMRVRFIl19LCJpYXQiOjE1NjAxNTcxODh9.oqypuJ22neeuzzhJ_0XEG3OYJOhyMcWJU35uIbaZugw'
	url="https://api.cortex.insights.ai/v3/agents/c360/customer-360-toplevel/services/retrieve-profile"
	final_list=parse_profile_data(url,token)
	#print(final_list)
	original_df = pd.DataFrame(final_list)
	original_df['Amount1']=original_df.apply(remove_text, axis=1)
	#original_df.to_csv("1.csv", sep=',', index=False,encoding='utf-8')
	final_df=get_df_competitors(original_df)
	#final_df.to_csv("2.csv", sep=',', index=False,encoding='utf-8')
	final_df_with_dummies = pd.get_dummies( final_df, columns = ['competitor_names','ExecSponsor1','OpportunityName1','OpportunityStatus1','industry_name'] )
	final_df_with_dummies.to_csv("profiledata.csv", sep=',', index=False,encoding='utf-8')


if __name__ == '__main__':
    main()

