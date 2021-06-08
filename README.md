# Genshin Impact Check-In Helper

This repo will summarise all the possible methods for auto check-in. If you found this website from my YouTube (taka gg), that method (Github Actions) is **no longer advisible** as it is against Github Terms of Service (botting) when you are only registering account to use the Github actions.

The auto check-in feature is for [Genshin Impact Web Daily Check-In](https://webstatic-sea.mihoyo.com/ys/event/signin-sea/index.html?act_id=e202102251931481&lang=en-us) introduced by miHoYo few months back.

## ALTERNATIVE METHOD (Much safer)

[Wayscript](https://github.com/am-steph/genshin-impact-helper/wiki/Wayscript)

[Heroku](https://github.com/am-steph/genshin-impact-helper/tree/heroku)

[Run locally on PC/Raspberry PI](https://github.com/napkatti/genshin-impact-helper/)

## Further help

If you need any help or discussion, please find us in [TakaGG Discord](https://discord.gg/takagg) at `#autocheckin-chat channel`.

I will not make any changes to the instructions below, but **please keep in mind that this is against Github ToS and your account might get deactivated. Please use it at your own risk**.

## Usage (Not advisible)

1. Fork this repository to your own account.  
   ![](https://imgur.com/VUH3ZwB.png)
2. Go to the Daily Check-In event website https://webstatic-sea.mihoyo.com/ys/event/signin-sea/index.html?act_id=e202102251931481&lang=en-us
3. Log in with your MiHoYo/Genshin Impact account.  
   *If you have never checked in before, manually check in once to ensure that your cookies are set properly.*
4. Open the developer tools on your web browser (F12 on firefox/chrome)
5. Click on the "Console" tab
6. Type in `document.cookie` in the console
7. Copy the text output from the console  
   ![](https://imgur.com/eWP1OyO.png)
8. Go back to your GitHub repository page, Click "Settings" on the top right
9. Click "Secrets" on the bottom left
10. Click "New Repository Secret" on the top right  
    ![](https://imgur.com/wDKNZeP.png)
11. In the "Name" box type in `OS_COOKIE`
12. In the "Value" box paste the text you copied earlier  
    ![](https://imgur.com/6EcYnEu.png)
    - Remove any quotation marks "" at the front or end of the text 
    - Go back to the MiHoYo event website. You may close the tab but do not click the "Log Out" button because it may cause your cookie to expire.
    - **IF YOU WANT TO CHECK-IN MULTIPLE GENSHIN ACCOUNTS:**
    1. Paste your first cookie into the Value box on GitHub, but do not click "Add Secret" yet.
    2. Open a new private browsing / Incognito window
    3. Go to the MiHoYo event website on your new browser instance, and log in with your second account
    4. Copy the `document.cookie` as before
    5. Go back to the GitHub page, and type a hash `#` at the end of your first cookie
    6. Paste your second cookie immediately after the `#` and remove the quotation marks "" if needed
13. Click "Add Secret"
14. Click the "Actions" tab in the top middle of the page
15. Click "I understand my workflows"  
    ![](https://imgur.com/Za5ej1L.png)
16. Click "Genshin Impact Helper Global"
17. Click "Enable workflows"  
    ![](https://imgur.com/0hVWa9M.png)
18. Click `main-os.yml` to edit your schedule, and pick what time of day the script should check-in for you.  
    ![](https://imgur.com/CL5NnQl.png)
19. Click the edit button  
    ![](https://imgur.com/BnXlcjH.png)
20. Change only the first two numbers.  
    The second number is the hour of day and the first number is minute of hour  
    Note that the time is in UTC, so convert to your timezone whatever time is most convenient.  
    ![](https://imgur.com/L1xlTWx.png)
21. Go back and click Run Workflow.  
    ![](https://imgur.com/CL5NnQl.png)
22. You should see a yellow circle next to the job. Wait for it to become a green check mark.  
    ![](https://imgur.com/NZnhTlc.png)

If you see the green check mark, congratulations, your auto check-in has been successfully set up.  
Your script will now automatically run every day at your scheduled time, without you needing to have your browser open.

**If you no longer want to check in automatically, you must manually disable your workflow or delete your Github repository.**
![](https://i.imgur.com/uw8qwTF.png)

## Discord Webhooks
This is an **OPTIONAL** step to let the script send you a notification on Discord whenever it runs a check-in.

Instructions provided by https://github.com/am-steph/genshin-impact-helper
1. Edit channel settings. (Create your own discord server or private channel for this)
   ![](https://i.imgur.com/Q0KFNzv.png)
2. Go into Integrations and view webhooks.
   ![](https://i.imgur.com/Z4pfACE.png)
3. Create a new webhook and copy the URL.
   ![](https://i.imgur.com/b3ZL3m3.png)
4. Go back to the "Secrets" tab on the repository and add a new secret called DISCORD_WEBHOOK.
   ![](https://i.imgur.com/YusKz6V.png)
5. Run the github action again and check for message in the channel you set the webhook in
   ![](https://i.imgur.com/0FMvJHW.png)
   
To stop receiving Discord notifications, delete your DISCORD_WEBHOOK secret.
