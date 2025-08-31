document.addEventListener('DOMContentLoaded', function() {

  // Use buttons to toggle between views
  document.querySelector('#inbox').addEventListener('click', () => load_mailbox('inbox'));
  document.querySelector('#sent').addEventListener('click', () => load_mailbox('sent'));
  document.querySelector('#archived').addEventListener('click', () => load_mailbox('archive'));
  document.querySelector('#compose').addEventListener('click', compose_email);
  document.querySelector('#compose-form').onsubmit = send_email;

  // By default, load the inbox
  load_mailbox('inbox');
});

function compose_email() {

  // Show compose view and hide other views
  document.querySelector('#emails-view').style.display = 'none';
  document.querySelector('#compose-view').style.display = 'block';
  document.querySelector('#showemail').style.display = 'none';

  // Clear out composition fields
  document.querySelector('#compose-recipients').value = '';
  document.querySelector('#compose-subject').value = '';
  document.querySelector('#compose-body').value = '';
}

function load_mailbox(mailbox) {
  
  // Show the mailbox and hide other views
  document.querySelector('#emails-view').style.display = 'block';
  document.querySelector('#compose-view').style.display = 'none';
  document.querySelector('#showemail').style.display = 'none';

  // Show the mailbox name
  document.querySelector('#emails-view').innerHTML = `<h3>${mailbox.charAt(0).toUpperCase() + mailbox.slice(1)}</h3>`;

  // if inbox
  display_emails(mailbox);
}

function display_emails(mailbox) {

  fetch(`/emails/${mailbox}`)
    .then(response => response.json())
      .then(emails => {
          // Print emails
          console.log(emails);
          if (emails.length === 0) {
            return;
          }
          const element = document.createElement('table');
          element.className = 'table';
          const firstheader = mailbox === 'inbox' ? 'From' : 'To'
          element.innerHTML = `
            <thead>
              <tr>
                <th scope="col">${firstheader}</th>
                <th scope="col">Subject</th>
                <th scope="col">Time</th>
              </tr>
            </thead>
            <tbody>
            </tbody>
          `;

          
          emails.forEach((email) => {
            const tbody = element.querySelector("tbody");
            const row = document.createElement('tr');
            if (email.read) {
              row.className = "table-secondary" 
            }
            const emailtodisp = mailbox === 'inbox' ? email.sender : email.recipients[0]
            row.innerHTML = `
              <th scope="row">${emailtodisp}</th>
              <td>${email.subject}</td>
              <td>${email.timestamp}</td>
            `;

          row.addEventListener('click', function() {
              console.log('This element has been clicked!');
              show_email(email)

            });
            tbody.appendChild(row);
          });
          document.querySelector('#emails-view').append(element);
      });
    }

    function show_email(email) {
      console.log(`${email.subject} has been clicked!`);
      document.querySelector('#emails-view').style.display = 'none';
      document.querySelector('#showemail').style.display = 'block';

      const element = document.createElement('div');

      element.innerHTML = `
      <div>
        <div><b>From:</b> ${email.sender}</div>
        <div><b>To:</b> ${email.recipients}</div>
        <div><b>Subject:</b> ${email.subject}</div>
        <div><b>Timestamp:</b> ${email.timestamp}</div>
      </div>
      <hr>
      <div style="white-space: pre-line;">
        ${email.body}
      </div>  
      `;
      
      document.querySelector('#showemail').append(element);
    }

function send_email(event) {

  event.preventDefault();

  let recipients = document.querySelector('#compose-recipients').value
  let subject = document.querySelector('#compose-subject').value
  let body = document.querySelector('#compose-body').value
  fetch('/emails', {
    method: 'POST',
    body: JSON.stringify({
      recipients: recipients,
      subject: subject,
      body: body
    })
  }) 
  .then(response => {
    if (response.status === 400) {
      return response.json().then(data => {
        alert("Error: " + data.error);
      });
    }
    if (response.status === 201) {
      return response.json().then( data => {
        alert("Message: " + data.message);
        load_mailbox('inbox');
      });
    }
  })
}
