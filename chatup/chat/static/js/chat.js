const id = JSON.parse(document.getElementById('json-username').textContent);
const message_username = JSON.parse(document.getElementById('json-message-username').textContent);
const receiver = JSON.parse(document.getElementById('json-username-receiver').textContent);

let targetDiv = document.querySelector('.content-chat')

const socket = new WebSocket( 'ws://' + window.location.host + '/ws/chat/' + id + '/' );

socket.onopen = function(e){
    console.log("The connection was setup successfully !");
};

socket.onclose = function(e){
    console.log("Something unexpected happened !");
};

socket.onerror = function(e){
    console.log("Error Occured");
};

socket.onmessage = function(e){
    const data = JSON.parse(e.data);
    const filePath = data.filePath

    let content;
    if(data.message != ""){
        content = `<p class="chat-msg">${ data.message }</p>`
    } else {
        content = `<img src='${ filePath }' class='reply-img'></img>`
    }
    
    if(data.username == message_username){
        targetDiv.innerHTML += `<div class="chat-reply-wrapper">
                            <div class="d-flex chat-detail">
                                <span class="in-reply-time text-muted">
                                <!---------- Delete Message Button ---------->
                                <button type="button" class="btn btn-danger delete-btn text-danger" data-toggle="modal"
                                    data-target="#exampleModalCenter-${data.chat_id}">
                                    Delete
                                </button><br>
                                <!-- Modal If Delete Message เมื่อมีการกดลบข้อความ-->
                                <div class="modal fade" id="exampleModalCenter-${data.chat_id}" tabindex="-1" role="dialog"
                                    aria-labelledby="exampleModalCenterTitle" aria-hidden="true">
                                    <div class="modal-dialog modal-dialog-centered" role="document">
                                        <div class="modal-content">
                                            <div class="modal-header">
                                                <h5 class="modal-title text-danger" id="exampleModalLongTitle">Delete
                                                    Message</h5>
                                                <button type="button" class="close" data-dismiss="modal" aria-label="Close">
                                                    <span aria-hidden="true">&times;</span>
                                                </button>
                                            </div>
                                            <div class="modal-body">
                                                Do you want to delete this message?
                                            </div>
                                            <div class="modal-footer">
                                                <a href="{% url 'chat:delete_message_chat' ${data.chat_id} %}" class="delete-btn text-danger">
                                                    Delete
                                                </a>
                                            </div>
                                        </div>
                                    </div>
                                    ${data.date}
                                </span>
                                <div class="chat-reply">
                                    ${content}
                                </div>
                            </div>
                        </div>`
    }else{
        targetDiv.innerHTML += `<div class="chat">
                            <div class="img-wrapper-chat">
                                <img src="${data.img_profile}" width="40px" class="avatar-pic" alt="avatar-pic">
                            </div>
                            <div class="chat-detail-head">
                                <div class="d-flex chat-detail">
                                    <div class="chat-box">
                                        ${content}
                                    </div>
                                    <span class="in-chat-time text-muted">
                                        ${data.date}
                                    </span>
                                </div>
                            </div>
                        </div>`
    }
    setTimeout(() => {
        targetDiv.scrollTop = targetDiv.scrollHeight;
      }, 200);
  
}
