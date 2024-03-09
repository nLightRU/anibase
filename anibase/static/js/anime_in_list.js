function modifyButton(response) {
    if (response.ok){
        let button = document.querySelector('[name=list-edit-button]');
        action = document.getElementById("action");
        if(action.value == "add"){
            button.textContent = "Remove";
            button.className = "btn btn-warning";
            button.onclick = "removeFromList()";
            action.value = "remove"
        }
        else{
            button.textContent = "Add";
            button.className = "btn btn-primary";
            button.onclick = "addToList()";
            action.value = "add"
        }
    }
}

function addToList() {
    const csrf = document.getElementById('csrf-token').value;
    const username = document.querySelector('[name=username]').value;
    const url = '/users/' + username + '/animelist';

    const json = JSON.stringify(
        {
            anime_id: parseInt(document.querySelector('[name=anime-id]').value)
        }
    );

    console.log(json)

    fetch(url, {
        method: 'POST',
        headers: {
            'X-CSRF-TOKEN': csrf,
            'Content-Type': "application/json"
        },
        body: json
    }).then(modifyButton);
}

function removeFromList() {
    const csrf = document.getElementById('csrf_token').value;
    const username = document.querySelector('[name=username]').value;
    const url = '/users/' + username + '/animelist';

    const json = JSON.stringify(
        {
            anime_id: parseInt(document.querySelector('[name=anime-id]').value)
        }
    );

    fetch(url, {
        method: 'PATCH',
        headers: {
            'X-CSRF-TOKEN': csrf,
            'Content-Type': "application/json"
        },
        body: json
    }).then(modifyButton);
}
