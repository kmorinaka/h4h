### Setup local Polyglot server

1. Download ngrok (follow instructions to download [here](https://ngrok.com/download).
2. Open a tunnel to your local machine.  You'll basically be generating a custom forwarding URL to be used to tell Twilio where to find the Polyglot app.  Run this command `./ngrok http 5000`
3. You should now see a screen that looks something like this: ![ngrok running](https://github.com/kmorinaka/h4h/blob/master/static/img/ngrok_running.png)
4. Log into the Twilio account: `https://www.twilio.com/console/phone-numbers/incoming`
* login info found in Slack channel
5. Click on the one number that should be listed in the Phone Numbers table
6. Scroll down to the *Messaging* section.  
7. Update the Webhook with the custom forwarding URL you generated in Step 2 (The address in the *Forwarding* row.) ![webhook](https://github.com/kmorinaka/h4h/blob/master/static/img/update_message_webhook.png) -- MAKE SURE TO ADD THE `/sms` route the end of the url.  Just follow the example in the picture.
8. Click save.
9. Test out the app -- every http request that comes in will be logged in the ngrok window ![ngrok with http requests logs](https://github.com/kmorinaka/h4h/blob/master/static/img/ngrok_with_http_requests_logs.png)
