This is designed for Unity Cloud Build but can be run locally too. Hell, without a lot of work it could be used for non Unity projects.

To run in UCB, all you need to do is get the API key and pass it to the upload script.\
Keep reading to find out how.

TODO:
* Nicer logging: Colours!
* Document environment variables (the ones UCB gives automatically)
* Add some way to set env locally
* Bash wrapper for python script
# Quick Start 
Simply call
```
$ python ...jonathonoh.unitybuildtools.ios/UploadToTestflight/upload_to_testflight.py
```
# Required Environment Variables
Put these all in a .env file in your project root but DON'T COMMIT IT to version control. It's going to contain sensitive information.\
See [example.env](example.env)

(For Unity Cloud Build, go to your configuration > Advanced Settings and scroll down)

## API Key
The following variables all relate to your App Store Connect API Key.\
[See the following section on creating it](#creating-your-api-key)

* `APP_STORE_CONNECT_API_KEY_ISSUER_ID`\
Look for "*Issuer ID*" on [the page you made the API key on](https://appstoreconnect.apple.com/access/integrations/api).

* `APP_STORE_CONNECT_API_KEY_KEY_ID`\
Look for "*Key ID*" on your key in [the page you made the API key on](https://appstoreconnect.apple.com/access/integrations/api).

* `APP_STORE_CONNECT_API_KEY_ALL_CONTENT`\
The raw text contents of your API key. Downloaded from [the page you made the API key on](https://appstoreconnect.apple.com/access/integrations/api).\
Just open the p8 file in any old text editor to get it.

## Other
The following environment variables are set automatically by Unity Cloud Build.

# Creating Your API Key 
This is how the upload script is able authenticate with App Store Connect.

Create here: https://appstoreconnect.apple.com/access/integrations/api\
Bonus points if you check out the docs: https://developer.apple.com/documentation/appstoreconnectapi/creating-api-keys-for-app-store-connect-api

Once you've created and downloaded it (it's a .p8). Save it somewhere secure. This is sensitive.\
If you open it in a text editor, it should look like this.
```
-----BEGIN PRIVATE KEY-----
Accordingtoallknownlawsofaviationthereisnowayabeeshouldbeabletof
lyItswingsaretoosmalltogetitsfatlittlebodyoffthegroundThebeeofco
ursefliesanywaybecausebeesdontcarewhathumansthinkisimpossibleYel
lowblack
-----END PRIVATE KEY-----