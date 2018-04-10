import hvac

class vaultClient():
    def __init__(self,url,user,pwd):
        self.client = hvac.Client(url)

        try:
            self.client.auth_userpass(user, pwd)
            print("Vault logged in.")
        except Exception:
            print("Something went wrong,probably username/password related")



    def get(self, secret):
        return self.client.read('secret/jenkins/%s' % secret)["data"]
