

function message_div(msg) {
    let msgDiv = document.createElement('div');
    msgDiv.innerHTML = `From <b>${msg.senderName} (${msg.senderId})</b> to <b>${msg.receiverName} (${msg.receiverId})</b> &emsp; &emsp; ${msg.timestamp} <br> ${msg.text}`;
    msgDiv.classList.add("message");
    return msgDiv;
}

function display_message_list(msgs, elementId = "message_list") {
    let length = msgs.length;
    let listDiv = document.getElementById(elementId);
    listDiv.innerHTML = "";

    for (let i = 0; i < length; i++) {
        let msg = msgs[i];
        let msgDiv = message_div(msg);
        listDiv.appendChild(msgDiv);
    }
}

async function display_received_message_list(elementId = "message_list") {
    let msgs = await get_received_messages();
    display_message_list(msgs, elementId);
}

async function display_sent_message_list(elementId = "message_list") {
    let msgs = await get_sent_messages();
    display_message_list(msgs, elementId);
}

function user_div(id, username) {
    let userDiv = document.createElement('div');
    userDiv.innerHTML = `<b>${username}</b> (${id}) <a href = "/chat?to=${id}">Chat</a>`;
    userDiv.classList.add('message');
    return userDiv;
}

function display_user_list(users, elementId = "user_list") {
    let length = users.length;
    let listDiv = document.getElementById(elementId);
    listDiv.innerHTML = "";

    for (let i = 0; i < length; i++) {
        let user = users[i];
        let userDiv = user_div(user.id, user.username);
        listDiv.appendChild(userDiv)
    }
}

async function display_main_list() {
    let users = await get_user_list();
    // console.log(users)
    display_user_list(users);
}


