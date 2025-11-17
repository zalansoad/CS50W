document.addEventListener('DOMContentLoaded', function() {
  const createPostForm = document.querySelector('#create-post');
  if (createPostForm) {
    document.querySelector('#create-post').onsubmit = create_post;
  }

  const likeIcons = document.querySelectorAll('.fa.fa-heart, .fa.fa-heart-o');
  if (likeIcons.length > 0) {
    likeIcons.forEach(icon => {
    icon.addEventListener('click', event => like(event, icon))
  });
  }

  const editButtons = document.querySelectorAll('.edit-clickable');
  if (editButtons.length > 0) {
  editButtons.forEach(editbutton => {
    editbutton.addEventListener('click', event => editpost(event, editbutton))
  });
  }
  const followingButton = document.querySelector('#following_button');

  if (followingButton) {
    followingButton.addEventListener('click', following_);
  }
});



function editpost(event, editbutton){
  event.preventDefault();
  let card = editbutton.closest('.card');      
  let postId = card.dataset.postid;
  console.log('clicked' + postId);

  let messageP = card.querySelector('p.mt-3');
  let currentText = messageP.textContent.trim();

  if (editbutton.textContent === "Save") {
  
  const newText = card.querySelector('textarea').value.trim();

  fetch('/edit_post', {
        method: 'PUT',
        body: JSON.stringify({
        post_id: postId,
        message: newText
        })
      })
      .then(response => response.json())
      .then(result => {

        messageP.innerHTML = result.message;
        editbutton.textContent = "Edit";
      })
  } else {

      messageP.innerHTML = `<textarea class="form-control edit-textarea" rows="3">${currentText}</textarea>`;
      editbutton.textContent = "Save";
  }
}

function following_(){
  const btn = document.querySelector('#following_button');
  const usernameToFollow = document.querySelector('#following_button').dataset.username;


    if (btn.classList.contains('btn-primary')) {
        fetch('/follow', {
        method: 'PUT',
        body: JSON.stringify({
        Follow: usernameToFollow,
        })
      })
      .then(response => {
        if (response.status === 400) {
          return response.json().then(data => {
            alert("Error: " + data.error);
          });
        } else if (response.status === 201){
          return response.json().then( data => {
            document.querySelector('#follower_count').textContent = data.follower_count;
          })
        }
      })
        btn.classList.remove('btn-primary');
        btn.classList.add('btn-danger');
        btn.textContent = "Unfollow";
    }
    else {

      fetch('/follow', {
        method: 'PUT',
        body: JSON.stringify({
        UnFollow: usernameToFollow,
        })
      })
      .then(response => {
        if (response.status === 400) {
          return response.json().then(data => {
            alert("Error: " + data.error);
          });
        } else if (response.status === 201){
          return response.json().then( data => {
            document.querySelector('#follower_count').textContent = data.follower_count;
          })
        }
      })
        btn.classList.remove('btn-danger');
        btn.classList.add('btn-primary');
        btn.textContent = "Follow";
    }
}

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
                                <a href="/profile/${data.creator}" style="text-decoration: none;"><h6 class="fw-bold text-primary mb-1">${data.creator}</h6></a>
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