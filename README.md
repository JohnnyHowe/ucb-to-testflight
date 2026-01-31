This is designed for Unity Cloud Build but can be run locally too. Hell, without a lot of work it could be used for non Unity projects.

To run in UCB, all you need to do is get the API key and pass it to the upload script.\
Keep reading to find out how.

TODO:
* Nicer logging: Colours!
* Document environment variables (the ones UCB gives automatically)
* Add some way to set env locally

# API Key
## Creating
This is how the upload script is able authenticate with App Store Connect.

Create here: https://appstoreconnect.apple.com/access/integrations/api\
Bonus points if you check out the docs: https://developer.apple.com/documentation/appstoreconnectapi/creating-api-keys-for-app-store-connect-api

To tell the uploader about it, we can either specify environment variables or pass a file path directly.
## Passing API Key with Environment Variables
(recommended for remote build system)

(For Unity Cloud Build, go to your configuration > Advanced Settings and scroll down)

* `APP_STORE_CONNECT_API_KEY_ISSUER_ID`\
Look for "*Issuer ID*" on [the page you made the API key on](https://appstoreconnect.apple.com/access/integrations/api).

* `APP_STORE_CONNECT_API_KEY_KEY_ID`\
Look for "*Key ID*" on your key in [the page you made the API key on](https://appstoreconnect.apple.com/access/integrations/api).

* `APP_STORE_CONNECT_API_KEY_ALL_CONTENT`\
The raw text contents of your API key. Downloaded from [the page you made the API key on](https://appstoreconnect.apple.com/access/integrations/api).\
Just open the p8 file in any old text editor to get it.

## Passing API Key with Argument
(recommended for local use/testing)\
Create your `AppStoreConnectKey.json` file.
```
{
    "key_id": APP_STORE_CONNECT_API_KEY_ISSUER_ID
    "issuer_id": APP_STORE_CONNECT_API_KEY_KEY_ID
    "key": APP_STORE_CONNECT_API_KEY_ALL_CONTENT    # <- Replace newlines with "\n"
} 
```
[See AppStoreConnectKeyExample.json](AppStoreConnectKeyExample.json)
# Running
Using environment variables
```
$ python Editor/UploadToTestflight/upload_to_testflight.py
```
Using key file
```
$ python Editor/UploadToTestflight/upload_to_testflight.py --api-key-path path/to/AppStoreConnectKey.json
```