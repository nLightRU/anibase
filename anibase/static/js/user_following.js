function modifyButton(response) {
        if (response.ok){
            let button = document.querySelector('button');
            action = document.getElementById("action");
            if(action.value == "follow") {
                button.className = "btn btn-secondary";
                button.textContent = "Unfollow";
                action.value = "unfollow";
            }
            else {
                button.className = "btn btn-primary";
                button.textContent = "Follow";
                action.value = "follow";
            }
        }
    }

    function handleFollowing() {
        const url = '/users/' + document.getElementById("current-username").value + '/following';
        const csrf = document.getElementById("csrf-token").value;

        let req_data = {
            follow_id: document.getElementById("follow-id").value,
            action: document.getElementById("action").value
        }

        let json = JSON.stringify(req_data);

        console.log(url);
        fetch(url, {
            method: 'PATCH',
            headers: {
                'X-CSRF-TOKEN': csrf,
                'Content-Type': "application/json"
            },
            body: json
        }).then(modifyButton);
    }