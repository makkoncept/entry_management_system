## Table of Contents

- [Video Demo](#video_demo)
- [Introduction](#introduction)
- [Checkout the application on heroku](#heroku)
- [Screenshots](#screenshots)
- [Application Stack](#app_stack)
- [Run the app locally](#local)
- [Important Note](#imp_note)



## [Video demo](https://www.youtube.com/watch?v=WhA7RoPlmko)<a name = "video_demo"></a>
## Entry Management Application<a name = "introduction"></a>

This is my submission for Innovaccer SDE Intern assignment.
This is a simple Entry Management Application which you can use to keep track of the entries of the guest in your office.

There are two types of users. **Host**(someone who is hosting a meeting) and **Guest**(someone who goes to the meeting).

### Host

-   You have to register yourself in the application.
-   After you register, guests would be able to see you as one of the registered host and can select you while checking in.
-   You can see all the guests that have checked in and out after logging into account.
-   Email and message notification is also triggered when a guest checks in, therefore please enter valid email and phone number.

### Guest

-   Unlike host, you don't have to register in the application.
-   For checking in, just fill a simple form and select from the dropdown the host that you are visiting. Keeping in mind the real world scenario where you can checkin with more that one hosts at once(when you
    will have 3 meetings in the same company, for example), the application will not stop you to checkin with other host also.
-   For checkout out, you have enter your email and select the host that you checked in with.
-   Just like in the real world as long as you don't checkout with a host, you cannot checkin again.
-   When you will checkout, a message and mail will be sent to you with the details of your visit, therefore please enter a valid email and phone number.

### Deployed application<a name = "heroku"></a>
The application is deployed on heroku (https://entry-management-app.herokuapp.com/).
Please also read the [important note](#imp_note) below regarding the message and mail sending feature of the application.

## Screenshots<a name = "screenshots"></a>

<p align="center">
	<img src="https://user-images.githubusercontent.com/34679965/69772816-ff1c8280-11b6-11ea-8b49-f629cd8e09ab.png" alt="homepage"> 
    <span align="center"> The homepage of the application. The design is minimal and intuitive and thanks to bootstrap4 and custom css, it is mobile responsive.</span>
</p>

<p align="center">
	<img src="https://user-images.githubusercontent.com/34679965/69772821-ffb51900-11b6-11ea-9d50-640a81026bfe.png" alt="host-register"> 
    <span align="center"> A host can register in the application using this form.</span>
</p>

<p align="center">
	<img src="https://user-images.githubusercontent.com/34679965/69772820-ffb51900-11b6-11ea-8a90-a01599f55a0d.png" alt="host-login"> 
    <span align="center"> After registering, the host can login to their account using the login form.</span>
</p>

<p align="center">
	<img src="https://user-images.githubusercontent.com/34679965/69772812-fe83ec00-11b6-11ea-8b8d-eb6c096aa70f.png" alt="guest-checkin"> 
    <span align="center">A guest don't need to create an account. They can just use this form to checkin. They don't have to provide the checkin time as it the timestamp of checking in is registered at the backend itself.</span>
</p>

<p align="center">
	<img src="https://user-images.githubusercontent.com/34679965/69772813-fe83ec00-11b6-11ea-91a3-72641de2d045.png" alt="guest-checkin-multiple"> 
    <span align="center">The application can have multiple hosts and the guest can select the host from the dropdown.</span>
</p>

<p align="center">
	<img src="https://user-images.githubusercontent.com/34679965/69772814-fe83ec00-11b6-11ea-8a22-f5e204e4cccb.png" alt="guest-checkout"> 
    <span align="center">The process of checking out is very simple. A guest just needs to enter their email and select the host from the dropdown. Just like the checkin, they don't need to manually enter the checkout time.</span>
</p>

<p align="center">
	<img src="https://user-images.githubusercontent.com/34679965/69772815-ff1c8280-11b6-11ea-8520-4025b27bdcc1.png" alt="guest-checkout-notification"> 
    <span align="center">The process of checking in and checking out triggers the necessary mail and sms notifications.</span>
</p>

<p align="center">
	<img src="https://user-images.githubusercontent.com/34679965/69772818-ff1c8280-11b6-11ea-9c1b-55034380ccd8.png" alt="host-account"> 
    <span align="center">The host account dashboard shows their information and has a link which they can use to update the information they want.</span>
</p>

<p align="center">
	<img src="https://user-images.githubusercontent.com/34679965/69772810-fdeb5580-11b6-11ea-95f8-97c2c08cdd44.png" alt="host-view-guest"> 
    <span align="center">The host can also view all the guests that have checked in and out.</span>
</p>

<p align="center">
	<img src="https://user-images.githubusercontent.com/34679965/69772823-004daf80-11b7-11ea-9a6e-4b85c02062e1.png" alt="account-update"> 
    <span align="center">The account update form is prefilled with the host details and they can update it from this form.</span>
</p>

<p align="center">
	<img src="https://user-images.githubusercontent.com/34679965/69772819-ffb51900-11b6-11ea-8a58-26334edd207a.png" alt="change-password"> 
    <span align="center">The host can also change the password from the change password form.</span>
</p>

## Application Stack<a name = "app_stack"></a>

-   The backend of the application will be in Flask (Python) with some extensions like Flask-sqlalchemy, Flask-wtforms, Flask-migrate, Flask-login etc.
-   Sqlite database is used for the development.
-   Jinja for templating reusable html code.
-   Web app is hosted on the hobby plan of Heroku with Postgres database.
-   Flask-bcrypt for password hashing.
-   Bootstrap4 and custom css a responsive and modern UI.
-   Flask-Mail to send the mail notifications.
-   Twilio API to send message notifications. (trial account)
-   Version control: git and source code is hosted on github.

## Run it locally<a name = "local"></a>

-   clone the repository. `git clone <url>`
-   Create a python virtual environment `python3 -m venv venv` and activate it `source venv/bin/activate`.
-   Install the dependencies `python -r requirements.txt`.
-   Create a .env file in the root directory with the required environment variables.

```
SID=Twilio_account_sid
AUTH=twilio_account_token
MAIL_USERNAME=your_gmail_username
MAIL_PASSWORD=your_gmail_password
```

-   Run `python databasereset.py` to create the database. You can enter your own credentials instead of the defaut host.
-   Run `python run.py` to start the development server.
-   Visit http://localhost.com:5000 in your faviourite browser to view the application.

## Important note<a name="imp_note"></a>
- The application that is deployed or that you will run locally can face some issues while sending the mails and messages. 

- **Mails**
- _local deployement:_ After entering your email and password in the `.env` file, you must also toggle on [this gmail setting](https://myaccount.google.com/lesssecureapps) for your account.
- _heroku deployed app:_ I have made a gmail account for exactly the above necessary step. Therefore the mails can be sent without any problem from the heroku deployed app.

- **Messages** - 
- _local_deployement:_ The application uses the free tier of twilio message sending api. In addition to adding the auto keys in the `.env` file, you must also manually white-list the numbers that you aim to send the message from your twilio developer dashboard. 
- _heroku deployed app:_ For the deployed version of the application, I have whitelisted my phone numbers. Therefore, the messages will be sent only to those two numbers.
