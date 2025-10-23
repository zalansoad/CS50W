document.addEventListener('DOMContentLoaded', function() {
  document.querySelector('#create-post').onsubmit = create_post;
});

function create_post(event) {

  event.preventDefault();
    console.log('clicked');
  let message = document.querySelector('#message').value
    console.log("message: " + message);
  fetch('/new_post', {
    method: 'POST',
    body: JSON.stringify({
      msg: message,
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

        const element = document.createElement('div');
        element.innerHTML = `
        <div class="card text-body">
            <div class="card-body p-4">
                <h6 class="fw-bold mb-1">User:${data.creator}</h6>
                <div class="d-flex align-items-center mb-3">
                    <p class="mb-0">
                        ${data.message}
                    </p>
                </div>
                    <p class="mb-0">
                        ${data.created_at}
                    </p>
                    <p class="mb-0">
                        ${data.likes}
                    </p>
            </div>
        </div>
        `
        document.querySelector('#posts-container').prepend(element);
        document.querySelector('#message').value = "";
        alert("New post created successfully");
      });
    }
  })
}