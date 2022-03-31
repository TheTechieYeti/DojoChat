
console.log('page loaded')
function bring_to_top(params) {
    console.log('working')
    document.getElementById("private_chat_form").style.zIndex = "auto";
    document.getElementById("public_chat_form").style.zIndex = "auto";
    document.getElementById("private_chat_form").style.visibility = "hidden";
    document.getElementById("public_chat_form").style.visibility = "hidden";
    document.getElementById(params).style.zIndex=1;
    document.getElementById(params).style.visibility="visible";
}


function flash_messages() {
  if (document.querySelector('.chatroom_form_msg')){
    document.getElementById('chat_room_form_button').click()
  }
  
  
}
flash_messages()