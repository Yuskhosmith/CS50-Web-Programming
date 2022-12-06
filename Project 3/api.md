# API
This application supports the following API routes:

`GET /emails/<str:mailbox>`

Sending a GET request to `/emails/<mailbox>` where `<mailbox>` is either `inbox`, `sent`, or `archive` will return back to you (in JSON form) a list of all emails in that mailbox, in reverse chronological order. For example, if you send a GET request to `/emails/inbox`, you might get a JSON response like the below (representing two emails):
```JSON
[
    {
        "id": 100,
        "sender": "foo@example.com",
        "recipients": ["bar@example.com"],
        "subject": "Hello!",
        "body": "Hello, world!",
        "timestamp": "Jan 2 2020, 12:00 AM",
        "read": false,
        "archived": false
    },
    {
        "id": 95,
        "sender": "baz@example.com",
        "recipients": ["bar@example.com"],
        "subject": "Meeting Tomorrow",
        "body": "What time are we meeting?",
        "timestamp": "Jan 1 2020, 12:00 AM",
        "read": true,
        "archived": false
    }
]
```
Notice that each email specifies its `id` (a unique identifier), a `sender` email address, an array of `recipients`, a string for `subject`, `body`, and `timestamp`, as well as two boolean values indicating whether the email has been `read` and whether the email has been `archived`.

How would you get access to such values in JavaScript? Recall that in JavaScript, you can use `fetch` to make a web request. Therefore, the following JavaScript code
```js
fetch('/emails/inbox')
.then(response => response.json())
.then(emails => {
    // Print emails
    console.log(emails);

    // ... do something else with emails ...
});
```
would make a `GET` request to `/emails/inbox`, convert the resulting response into JSON, and then provide to you the array of emails inside of the variable `emails`. You can print that value out to the browser’s console using `console.log` (if you don’t have any emails in your inbox, this will be an empty array), or do something else with that array.

Note also that if you request an invalid mailbox (anything other than `inbox`, `sent`, or `archive`), you’ll instead get back the JSON response `{"error": "Invalid mailbox."}`.

`GET /emails/<int:email_id>`

Sending a GET request to `/emails/email_id` where `email_id` is an integer id for an email will return a JSON representation of the email, like the below:
```JSON
{
    "id": 100,
    "sender": "foo@example.com",
    "recipients": ["bar@example.com"],
    "subject": "Hello!",
    "body": "Hello, world!",
    "timestamp": "Jan 2 2020, 12:00 AM",
    "read": false,
    "archived": false
}
```
Note that if the email doesn’t exist, or if the user does not have access to the email, the route instead return a 404 Not Found error with a JSON response of `{"error": "Email not found."}`.

To get email number 100, for example, you might write JavaScript code like
```js
fetch('/emails/100')
.then(response => response.json())
.then(email => {
    // Print email
    console.log(email);

    // ... do something else with email ...
});
```

`POST /emails`

So far, we’ve seen how to get emails: either all of the emails in a mailbox, or just a single email. To send an email, you can send a `POST` request to the `/emails` route. The route requires three pieces of data to be submitted: a `recipients` value (a comma-separated string of all users to send an email to), a `subject` string, and a `body` string. For example, you could write JavaScript code like
```js
fetch('/emails', {
  method: 'POST',
  body: JSON.stringify({
      recipients: 'baz@example.com',
      subject: 'Meeting time',
      body: 'How about we meet tomorrow at 3pm?'
  })
})
.then(response => response.json())
.then(result => {
    // Print result
    console.log(result);
});
```
If the email is sent successfully, the route will respond with a 201 status code and a JSON response of `{"message": "Email sent successfully."}`.

Note that there must be at least one email recipient: if one isn’t provided, the route will instead respond with a 400 status code and a JSON response of `{"error": "At least one recipient required."}`. All recipients must also be valid users who have registered on this particular web application: if you try to send an email to `baz@example.com` but there is no user with that email address, you’ll get a JSON response of `{"error": "User with email baz@example.com does not exist."}`.

`PUT /emails/<int:email_id>`

The final route that you’ll need is the ability to mark an email as read/unread or as archived/unarchived. To do so, send a `PUT` request (instead of a GET) request to `/emails/<email_id>` where `email_id` is the id of the email you’re trying to modify. For example, JavaScript code like
```js
fetch('/emails/100', {
  method: 'PUT',
  body: JSON.stringify({
      archived: true
  })
})
```
would mark email number 100 as archived. The body of the `PUT` request could also be `{archived: false}` to unarchive the message, and likewise could be either `{read: true}` or `{read: false}` to mark the email as read or unread, respectively.