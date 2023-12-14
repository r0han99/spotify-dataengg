#### Authentication and Redirect URI

This dashboard has somefeatures that requires the app to access your playlist information,listening records and some other necessary details. It is imperative to access and visualise all these features. 

#### What happens when you click Authenticate!

You will be redirected to a separate tab, the spotify landing page, you have to login to your account, so that the app gets the token back as a resposne. Ideally, you only authenticate once, because we store the authentication token for the transitory period. 

#### Important Information

Once you are redirected to the authenticated URL, you are required to stay there and ditch the initially opened link because now, you can notice that the url is extended with a token. That's how you know that you are authenticated and good to go. 

---