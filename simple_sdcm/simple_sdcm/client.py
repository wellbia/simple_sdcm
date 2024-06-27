# https://github.com/microsoft/SDCM

import http.client, json, requests
from urllib.parse import quote


class Client:
    def __init__(self, tenant_id, client_id, client_secret):
        self.tenantId = tenant_id
        self.clientId = client_id
        self.clientSecret = client_secret
        self.tokenResource = ""
        self.accessToken = ""

        self.version = "1.0"
        self.tenant = "my"

        self.tokenEndpointTemplate = "/{0}/oauth2/token"
        self.getProductsUrlTemplate = "/v{0}/{1}/hardware/products"
        self.getSubmissionUrlTemplate = (
            "/v{0}/{1}/hardware/products/{2}/submissions/{3}"
        )
        self.commitSubmissionUrlTemplate = (
            "/v{0}/{1}/hardware/products/{2}/submissions/{3}/commit"
        )
        self.updateUrlTemplate = "/v{0}/{1}/hardware/products/{2}/submissions/{3}/"
        self.productUrlTemplate = "/v{0}/{1}/hardware/products"
        self.productUrlWithContinuationTemplate = "/v{0}/{1}/{2}"
        self.getProductUrlTemplate = "/v{0}/{1}/hardware/products/{2}"
        self.createSubmissionUrlTemplate = "/v{0}/{1}/hardware/products/{2}/submissions"
        self.productSubmissionStatusUrlTemplate = (
            "/v{0}/{1}/hardware/products/{2}/submissions/{3}"
        )

    def SetTokenResource(self, tokenResource):
        self.tokenResource = tokenResource

    def GetClientCredentialAccessToken(self):
        tokenRequestBody = "grant_type=client_credentials&client_id={0}&client_secret={1}&resource={2}".format(
            self.clientId, self.clientSecret, self.tokenResource
        )
        headers = {"Content-Type": "application/x-www-form-urlencoded; charset=utf-8"}
        tokenConnection = http.client.HTTPSConnection("login.microsoftonline.com")
        tokenConnection.request(
            "POST",
            self.tokenEndpointTemplate.format(self.tenantId),
            tokenRequestBody,
            headers=headers,
        )

        tokenResponse = tokenConnection.getresponse()
        # print(tokenResponse.status)
        tokenJson = json.loads(tokenResponse.read().decode())
        # print(tokenJson["access_token"])

        tokenConnection.close()

        return tokenJson["access_token"]

    def SetClientCredentialAccessToken(self, accessToken):
        self.accessToken = accessToken

    def GetProducts(self):
        headers = {
            "Authorization": "Bearer " + self.accessToken,
            "Content-type": "application/json",
            "User-Agent": "Python",
        }
        ingestionConnection = http.client.HTTPSConnection(
            "manage.devcenter.microsoft.com"
        )

        ingestionConnection.request(
            "GET",
            self.getProductsUrlTemplate.format(self.version, self.tenant),
            headers=headers,
        )
        res = ingestionConnection.getresponse()
        # print(res.status)
        resJsonObject = json.loads(res.read().decode())
        return resJsonObject

    def GetProduct(self, productId):
        headers = {
            "Authorization": "Bearer " + self.accessToken,
            "Content-type": "application/json",
            "User-Agent": "Python",
        }
        ingestionConnection = http.client.HTTPSConnection(
            "manage.devcenter.microsoft.com"
        )

        ingestionConnection.request(
            "GET",
            self.getProductUrlTemplate.format(self.version, self.tenant, productId),
            headers=headers,
        )
        res = ingestionConnection.getresponse()
        # print(res.status)
        resJsonObject = json.loads(res.read().decode())
        return resJsonObject

    def GetSubmission(self, productId, submissionId):
        headers = {
            "Authorization": "Bearer " + self.accessToken,
            "Content-type": "application/json",
            "User-Agent": "Python",
        }
        ingestionConnection = http.client.HTTPSConnection(
            "manage.devcenter.microsoft.com"
        )

        ingestionConnection.request(
            "GET",
            self.getSubmissionUrlTemplate.format(
                self.version, self.tenant, productId, submissionId
            ),
            headers=headers,
        )
        res = ingestionConnection.getresponse()
        # print(res.status)
        resJsonObject = json.loads(res.read().decode())
        return resJsonObject

    def CreateProduct(self, productBody):
        headers = {
            "Authorization": "Bearer " + self.accessToken,
            "Content-type": "application/json",
            "User-Agent": "Python",
        }
        ingestionConnection = http.client.HTTPSConnection(
            "manage.devcenter.microsoft.com"
        )

        ingestionConnection.request(
            "POST",
            self.productUrlTemplate.format(self.version, self.tenant),
            productBody,
            headers=headers,
        )
        res = ingestionConnection.getresponse()
        # print(res.status)
        resJsonObject = json.loads(res.read().decode())
        return resJsonObject

    def CreateSubmission(self, productId, submissionBody):
        headers = {
            "Authorization": "Bearer " + self.accessToken,
            "Content-type": "application/json",
            "User-Agent": "Python",
        }
        ingestionConnection = http.client.HTTPSConnection(
            "manage.devcenter.microsoft.com"
        )

        ingestionConnection.request(
            "POST",
            self.createSubmissionUrlTemplate.format(
                self.version, self.tenant, productId
            ),
            submissionBody,
            headers=headers,
        )
        res = ingestionConnection.getresponse()
        # print(res.status)
        resJsonObject = json.loads(res.read().decode())
        return resJsonObject

    def CommitSubmission(self, productId, submissionId):
        headers = {
            "Authorization": "Bearer " + self.accessToken,
            "Content-type": "application/json",
            "User-Agent": "Python",
        }
        ingestionConnection = http.client.HTTPSConnection(
            "manage.devcenter.microsoft.com"
        )

        ingestionConnection.request(
            "POST",
            self.commitSubmissionUrlTemplate.format(
                self.version, self.tenant, productId, submissionId
            ),
            headers=headers,
        )
        res = ingestionConnection.getresponse()
        print(res.status)

    def GetProductSubmissionStatus(self, productId, submissionId):
        headers = {
            "Authorization": "Bearer " + self.accessToken,
            "Content-type": "application/json",
            "User-Agent": "Python",
        }
        ingestionConnection = http.client.HTTPSConnection(
            "manage.devcenter.microsoft.com"
        )

        ingestionConnection.request(
            "GET",
            self.productSubmissionStatusUrlTemplate.format(
                self.version, self.tenant, productId, submissionId
            ),
            headers=headers,
        )
        res = ingestionConnection.getresponse()
        # print(res.status)
        resJsonObject = json.loads(res.read().decode())
        return resJsonObject

    def UploadFile(self, filePath, fileUploadUrl):
        f = open(filePath, "rb")
        encoded_uri = quote(fileUploadUrl, safe=":/?&=")
        uploadResponse = requests.put(
            encoded_uri,
            f,
            headers={"x-ms-blob-type": "BlockBlob"},
        )
        f.close()
        print(uploadResponse.status_code)
