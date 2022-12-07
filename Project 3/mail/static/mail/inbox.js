document.addEventListener('DOMContentLoaded', function() {

  // Use buttons to toggle between views
  document.querySelector('#inbox').addEventListener('click', () => load_mailbox('inbox'));
  document.querySelector('#sent').addEventListener('click', () => load_mailbox('sent'));
  document.querySelector('#archived').addEventListener('click', () => load_mailbox('archive'));
  document.querySelector('#compose').addEventListener('click', compose_email);
  document.querySelector('#compose-form').onsubmit = send_mail

  // By default, load the inbox
  load_mailbox('inbox');
});

function compose_email() {

  // Show compose view and hide other views
  document.querySelector('#emails-view').style.display = 'none';
  document.querySelector('#single-email-view').style.display = 'none';
  document.querySelector('#compose-view').style.display = 'block';

  // Clear out composition fields
  document.querySelector('#compose-recipients').value = '';
  document.querySelector('#compose-subject').value = '';
  document.querySelector('#compose-body').value = '';
}

function load_mailbox(mailbox) {
  
  // Show the mailbox and hide other views
  document.querySelector('#emails-view').style.display = 'block';
  document.querySelector('#single-email-view').style.display = 'none';
  document.querySelector('#compose-view').style.display = 'none';

  // Show the mailbox name
  document.querySelector('#emails-view').innerHTML = `<h3>${mailbox.charAt(0).toUpperCase() + mailbox.slice(1)}</h3>`;

  //mailbox details
  fetch(`/emails/${mailbox}`)
  .then(response => response.json())
  .then(emails => {
    // Print emails
    // console.log(emails);
    emailViewTag = document.querySelector('#emails-view');

    emails.forEach(email => {
      divTag = document.createElement('div');
      emailViewTag.appendChild(divTag).innerHTML = `<div class='one-line' onclick=view_email(${email.id})>From: ${email["sender"]} <span class='sp'>Subject: ${email["subject"]}</span> <span class='sp'>Time: ${email["timestamp"]}</span></div>`;
      
      if (email.read) {
        divTag.style = 'background-color: gray;';
      } else {
        divTag.style = 'background-color: white;';
      }
    });

    if (document.querySelector('#single-email-view').innerHTML){
      document.querySelector('#single-email-view').innerHTML = ''
    }


    // ... do something else with emails ...
});
}

function view_email(mailid){
  document.querySelector('#emails-view').style.display = 'none';
  document.querySelector('#single-email-view').style.display = 'block';
  document.querySelector('#compose-view').style.display = 'none';

  emailViewTag = document.querySelector('#single-email-view');
  divTag = document.createElement('div');
  
  
  fetch(`/emails/${mailid}`)
  .then(response => response.json())
  .then(email => {
    // Print email
    // console.log(email);

    // Mark as read
    if (!email.read){
      fetch(`/emails/${mailid}`, {
        method: 'PUT',
        body: JSON.stringify({
            read: true
        })
      })
    }
    
    //  to avoid redundancy
    const htext = `<h3>${email.subject}</h3>
    <h5>From: ${email.sender}</h5>
    <h5>Recipents: ${email.recipients}</h5>
    <h5>TimeStamp; ${email.timestamp}</h5>
    <p>${email.body}</p>
    <button class="reply btn btn-outline-primary">Reply</button>
    `

    boolean = email.archived
    // Archive
    if (document.querySelector('h2').innerText !== email.sender){
      if (boolean){
        emailViewTag.appendChild(divTag).innerHTML = `${htext}
        <button class="archive btn btn-primary">Unarchive</button>
        `;
      } else{
        emailViewTag.appendChild(divTag).innerHTML = `${htext}
        <button class="archive btn btn-primary">Archive</button>
        `;
      }
      document.querySelector('.archive').addEventListener('click', () => {
        archive_mail(mailid, !boolean);
      });
      
    } else {
      //  thou shall not display the archive button
      emailViewTag.appendChild(divTag).innerHTML = `${htext}`;
    }
    document.querySelector('.reply').addEventListener('click', () => {reply_mail(email)});
    



    // ... do something else with email ...
  });
  // console.log(mailid);
}

function reply_mail(email){
  compose_email()
  document.querySelector('#compose-recipients').value = email.sender;
  if (email.subject.slice(0, 4) === 'Re: ') {
    document.querySelector('#compose-subject').value = `${email.subject}`;
  } else {
    document.querySelector('#compose-subject').value = `Re: ${email.subject}`;
  };
  document.querySelector('#compose-body').value = `On ${email.timestamp} ${email.sender} wrote: \n ${email.body}`;
}

function archive_mail(mailid, boolean){
  fetch(`/emails/${mailid}`, {
    method: 'PUT',
    body: JSON.stringify({
      archived: boolean
    })
  })
  .then(() => load_mailbox('inbox'));
}

function send_mail(){
  // recipient, subject and body
  const r = document.querySelector('#compose-recipients').value.trim();
  const s = document.querySelector('#compose-subject').value.trim();
  const b = document.querySelector('#compose-body').value.trim();

  // Do something about this, absolutely wrong..... built on the assumptions that everything goes well
  if (r == "" || s == "" || b == "") {
    return false;
  }

  // console.log(r,s,b);

  fetch('/emails', {
    method: 'POST',
    body: JSON.stringify({
        recipients: r,
        subject: s,
        body: b
    })
  })
  .then(response => response.json())
  .then(result => {
      // Print result
      // console.log(result);
      load_mailbox('sent');
  });

  return false;
}