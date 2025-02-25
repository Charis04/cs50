document.addEventListener('DOMContentLoaded', function() {

  // Use buttons to toggle between views
  document.querySelector('#inbox').addEventListener('click', () => load_mailbox('inbox'));
  document.querySelector('#sent').addEventListener('click', () => {
    load_mailbox('sent');
  });
  document.querySelector('#archived').addEventListener('click', () => load_mailbox('archive'));
  document.querySelector('#compose').addEventListener('click', compose_email);

  // submit email
  document.querySelector('#compose-form').addEventListener('submit', (e) => {
    e.preventDefault();
    post_email();
    load_mailbox('sent');
  });

  // By default, load the inbox
  load_mailbox('inbox');
});

function compose_email() {

  // Show compose view and hide other views
  document.querySelector('#emails-view').style.display = 'none';
  document.querySelector('#compose-view').style.display = 'block';

  // Clear out composition fields
  document.querySelector('#compose-recipients').value = '';
  document.querySelector('#compose-subject').value = '';
  document.querySelector('#compose-body').value = '';
}

function load_mailbox(mailbox) {
  
  // Show the mailbox and hide other views
  document.querySelector('#emails-view').style.display = 'block';
  document.querySelector('#compose-view').style.display = 'none';

  // Show the mailbox name
  document.querySelector('#emails-view').innerHTML = `<h3>${mailbox.charAt(0).toUpperCase() + mailbox.slice(1)}</h3>`;
  
  // Get emails
  get_emails(mailbox);
}

function post_email() {
  fetch('/emails', {
    method: 'POST',
    body: JSON.stringify({
        recipients: document.querySelector('#compose-recipients').value,
        subject: document.querySelector('#compose-subject').value,
        body: document.querySelector('#compose-body').value
    })
  })
}

function get_emails(mailbox) {
  fetch(`/emails/${mailbox}`)
  .then(response => response.json())
  .then(emails => {
    console.log(emails);
    emails.forEach(email => {
      const emailDiv = document.createElement('div');
      emailDiv.innerHTML = `
        <div class="email" data-id="${email.id}" data-read="${email.read}">
          <div class="email-sender">${email.sender}</div>
          <div class="email-subject">${email.subject}</div>
          <div class="email-timestamp">${email.timestamp}</div>
        </div>
      `;
      document.querySelector('#emails-view').appendChild(emailDiv);
    });
    style_email();
  })
}

function style_email() {
  const emails = document.querySelectorAll('.email')
  emails.forEach(email => {
    email.style.border = '1px solid #ccc';
    email.style.padding = '10px';
    email.style.margin = '10px 0';
    email.style.cursor = 'pointer';
    email.style.backgroundColor = email.dataset.read === 'true' ? '#f0f0f0' : '#ffffff';
    email.addEventListener('click', () => {
      // Add functionality to open the email
      view_email(email.dataset.id);
    });
  });
}

function view_email(email_id) {
  fetch(`/emails/${email_id}`)
  .then(response => response.json())
  .then(email => {
    console.log(email);
    document.querySelector('#emails-view').innerHTML = `
      <div class="email">
        <div class="email-sender">From: ${email.sender}</div>
        <div class="email-recipients">To: ${email.recipients}</div>
        <div class="email-subject">Subject: ${email.subject}</div>
        <div class="email-timestamp">Timestamp: ${email.timestamp}</div>
        <button class="btn btn-sm btn-outline-primary">Reply</button>
        <button class="btn btn-sm btn-outline-primary">Archive</button>
        <hr>
        <div class="email-body">${email.body}</div>
      </div>
    `;
  });
}
