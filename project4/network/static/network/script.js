document.addEventListener("DOMContentLoaded", () => {
    disable_the_post_btn()
    followingStatus()
    editPost()
    like()
    if (document.querySelector('#username')){
        removeSpace();
    }
    
});

function removeSpace(){
    const usernameEl = document.querySelector('#username');
    const u_er = document.querySelector('#u-er');
    u_er.style.display = 'none';
    
    usernameEl.onkeyup = () => {
        if (usernameEl.value.includes(' ')){
            u_er.innerText = "username can't contain space";
            u_er.style.display = 'block';
            document.querySelector('#btnforreg').disabled = true;
        } else {
            u_er.style.display = 'none';
            document.querySelector('#btnforreg').disabled = false;
        }

    }
    
}

function like(){
    likeBtn = document.querySelectorAll('#like');
    likeBtn.forEach(item => {
        item.addEventListener('click', () => {
            console.log("click")
            parentLikeBtn = item.parentElement.parentElement;
            likeCountParent = parentLikeBtn.children[4];
            // likeCountEl = likeCountParent.querySelector('#count');
            post_id = parentLikeBtn.id

            oneLikeBtn = parentLikeBtn.querySelector('#like');
            if (oneLikeBtn.dataset.value == "like"){
                parentLikeBtn.querySelector('.fa-heart').style.color = "red";
                console.log("Like--Pass 1")
                oneLikeBtn.dataset.value = "unlike";
                count = parseInt(oneLikeBtn.dataset.count) + 1
                oneLikeBtn.dataset.count = count
                parentLikeBtn.querySelector(`#liked${post_id}`).innerText = count
            } else if (oneLikeBtn.dataset.value == "unlike") {
                parentLikeBtn.querySelector('.fa-heart').style.color = "black";
                console.log("Unlike--Pass 1")
                oneLikeBtn.dataset.value = "like";
                count = parseInt(oneLikeBtn.dataset.count) - 1
                oneLikeBtn.dataset.count = count
                parentLikeBtn.querySelector(`#liked${post_id}`).innerText = count
            } else{
                return;
            }
            
            fetch('../like/', {
                method: 'PUT',
                body: JSON.stringify({
                    post: post_id,
                })
            })
            // .then(response => response.json())
            // .then(r => {
            //     console.log(r)
            // })
            
        });

    })
}

function editPost(){
    if(document.querySelector('#edit')){
        const editBtn = document.querySelectorAll('#edit');
        editBtn.forEach(item => {
            item.addEventListener('click', () => {
                item.style.display = 'none';
                parentEditBtn = item.parentElement
                post_id = parentEditBtn.id
                idChildNodes = parentEditBtn.children
    
                fetch(`../getpost/${post_id}`, {method: 'GET'})
                .then(response => response.json())
                .then(post => {
                    idChildNodes[1].innerHTML = `
                    <textarea name="post" id="textarea2" cols="30" rows="10">${post.post}</textarea>
                    <button class="btn btn-primary" id="save">Save</button>
                    `
                    disableBtn("#textarea2", "#save")
                    const saveBtn = document.querySelector('#save');
                    saveBtn.addEventListener('click', () => {
                        const post = document.querySelector('#textarea2').value;
                        
                        fetch('../editpost/', {
                            method: 'PUT',
                            body: JSON.stringify({
                                post_id: post_id,
                                post: post,
                            })
                        })
                        location.reload()
                    });
                })
            });
        })
    }
}

function disable_the_post_btn(){
    if (document.querySelector('#new-post')) {
        disableBtn("#textarea", "#submit")
    }
}

function disableBtn(inputfield, btn){
    // by default disabled
    document.querySelector(`${btn}`).disabled = true;

    // check if it's not empty
    if (document.querySelector(`${inputfield}`).value.length > 0){
        document.querySelector(`${btn}`).disabled = false;
    }

    // now for every key the user press, even if it's backspace
    document.querySelector(`${inputfield}`).onkeyup = () => {
        // if the input field is empty disable the button
        if (document.querySelector(`${inputfield}`).value.length > 0){
            document.querySelector(`${btn}`).disabled = false;
        } else{
            document.querySelector(`${btn}`).disabled = true;
        }
    }
}


function followingStatus(){
    if (document.querySelector('#following_status')){
        const user = document.querySelector('#user').innerText
        const x = document.querySelector('#following_status')
        fetch(`../check/following/${user}`)
        .then(response => response.json())
        .then(answer => {
            console.log(answer)
            if (answer){
                const y = `<a class ='btn btn-primary-outline'>Unfollow</a>`
                x.innerHTML = y
                x.firstChild.addEventListener('click', () => {
                    fetch('../unfollow/', {
                        method: 'PUT',
                        body: JSON.stringify({
                            unfollow: user
                        })
                    })
                    location.reload()
                })
            } else {
                const y = `<a class ='btn btn-primary-outline'>Follow</a>`
                x.innerHTML = y
                x.firstChild.addEventListener('click', () => {
                    // console.log("pass1")
                    fetch('../follow/', {
                        method: 'PUT',
                        body: JSON.stringify({
                            follow: user
                        })
                    })
                    location.reload()
                })
            }
        })
        // Switch the follow and unfollow button

        // for the following aspect - get the url
        // alert("The URL of this page is: " + window.location.href);
    }

}
