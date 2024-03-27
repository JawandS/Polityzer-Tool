import requests

API_KEY = "xXaJt4QsteETBAa8UY4004G4QZeMHRK7upUdf2XrFQZQpN"

url = "https://pribot.org/api/web/analyzeNewPolicy"
json= {
    "url":"https://jawands.github.io/VA-Privacy-Policies/House/CECliffHayesJr.html",
    "key": f"{API_KEY}"
}

response = requests.request("POST", url, json=json)
print(response.json())