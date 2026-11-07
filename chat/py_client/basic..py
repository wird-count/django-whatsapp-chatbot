import requests
endpoint = 'https:///www.github.com' 
endpoint = 'https://httpbin.org/cookies'
endpoint = 'https://httpbin.org/status/200'
endpoint = 'https://httpbin.org/anything'


def lancee_une_requette(endpoint):
    get_response = requests.get(endpoint) #HTTP requests
    print(get_response.text)



lancee_une_requette(endpoint)




