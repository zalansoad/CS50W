document.addEventListener('DOMContentLoaded', function() {
  document.querySelector('#create-post').onsubmit = create_post;
  document.querySelectorAll('.fa.fa-heart-o').forEach(icon => {
    icon.addEventListener('click', event => like(event, icon))
  });
});

function like(event, icon) {
  event.preventDefault();
  let card = icon.closest('.card');      
  let postId = card.dataset.postid;

  console.log('clicked' + postId)
  fetch('/post_like', {
    method: 'POST',
    body: JSON.stringify({
      post_id: postId,
    })
  })

  .then(response => {
    if (response.status === 400) {
      return response.json().then(data =>{
        alert("Error: " + data.error);
      });
    } else if (response.status === 201){
        console.log('status 201');
        return response.json().then( data => {
          if(data.like_type === "like"){
              icon.classList.remove('fa-heart-o');
              icon.classList.add('fa-heart');
          } else if (data.like_type === "dislike"){
            icon.classList.remove('fa-heart');
            icon.classList.add('fa-heart-o');
          }
          
          icon.textContent = " " + data.likes;

        })
    } else {
      alert("Error: returned status not defined");
    }
   
  })

}

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
        <div class="container py-1">
            <div class="row d-flex justify-content-center">
                <div class="col-md-12 col-lg-10 col-xl-8">
                    <div class="card" data-postid=${data.id}>
                      <div class="card-body">
                        <div class="d-flex flex-start align-items-center">
                            <div>
                                <h6 class="fw-bold text-primary mb-1">${data.creator}</h6>
                                <p class="text-muted small mb-0">
                                ${data.created_at}
                                </p>
                            </div>
                        </div>
                        <p class="mt-3 mb-4 pb-2">
                          ${data.message}
                        </p>
                        <div class="d-flex justify-content-between align-items-center small">
                            <i class="fa fa-heart-o" aria-hidden="true"> ${data.likes}</i>
                            <a href="#!" class="text-decoration-none">
                                <p class="mb-0">Edit</p>
                            </a>
                        </div>
                      </div>
                    </div>
                </div>
            </div>
        </div>
        `
        document.querySelector('#posts-container').prepend(element);
        document.querySelector('#message').value = "";

        let newIcon = element.querySelector('.fa.fa-heart-o');
        newIcon.addEventListener('click', event => like(event, newIcon));

        alert("New post created successfully");
      });
    }
  })
}