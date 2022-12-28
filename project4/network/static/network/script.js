document.addEventListener("DOMContentLoaded", () => {
    disable_the_post_btn()
    followingStatus()
    editPost()
    like()
    
});

function index(){
    fetch(`/emails/${mailbox}`)
    .then(response => response.json())
    .then(posts => {})

}

function like(){
    likeBtn = document.querySelector('#like');
    // find a better way to get all the btn to work with the event listener isntead of the first one only
    // for btn in likeBtn{

    // }
    likeBtn.addEventListener('click', () => {
        parentLikeBtn = likeBtn.parentElement;
        idChildNodes = parentLikeBtn.children;
        post_id = parentLikeBtn.id
        // text = idChildNodes[1].innerText
        // username = idChildNodes[0].innerText
        console.log(post_id)

        // fetch('../like', {
        //     method: 'GET',
        //     body: JSON.stringify({
        //         post: text,
        //         username: username
        //     })
        // })
        // .then(response => response.json())
        // .then(answer => {
        //     console.log(answer)
        
        // })
        // Ignore above.... the deal is below
        fetch('../like/', {
            method: 'PUT',
            body: JSON.stringify({
                post: post_id,
            })
        })
        // .then(response => response.json())
        // .then(answer => {
        //     console.log(answer)
        
        // })
    });
}


function editPost(){
    if(document.querySelector('#edit')){
        // make the edit button take the original form of the post
        const editBtn = document.querySelector('#edit');
        editBtn.addEventListener('click', () => {
            parentEditBtn = editBtn.parentElement
            idChildNodes = parentEditBtn.children
            text = idChildNodes[1].innerText
            idChildNodes[1].innerHTML = `
            <textarea name="post" id="textarea2" cols="30" rows="10">${text}</textarea>
            <button class="btn btn-primary" id="save">Save</button>
            `
            disableBtn("#textarea2", "#save")
            const saveBtn = document.querySelector('#save');
            saveBtn.addEventListener('click', () => {
                const post = document.querySelector('#textarea2').value;
                

                console.log(post)
                
                fetch('../editpost/', {
                    method: 'PUT',
                    body: JSON.stringify({
                        post: post,
                        prevpost: text,
                    })
                })
                // .then(response => response.json())
                // .then(answer => {
                //     console.log(answer)})

                location.reload()
            });
            
        });
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