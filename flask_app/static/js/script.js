console.log ("page loaded")
function loading(params) {
    console.log ("This is WOrking")
    
}
function bring_to_top(params) {
    console.log('working')
    document.getElementById("private_chat_form").style.zIndex = "auto";
    document.getElementById("public_chat_form").style.zIndex = "auto";
    document.getElementById(params).style.zIndex=1;
}
var myModal = document.getElementById('myModal')
var myInput = document.getElementById('myInput')

myModal.addEventListener('shown.bs.modal', function () {
  myInput.focus()
})