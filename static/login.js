function myFunction(){
    var x = document.getElementById('login_btn2');
    if(x.type == "password"){
        x.type = "text";
    }
    else{
        x.type = "password";
    }
}
function func(){
    window.open('/home','_self');
}
function validatepass(){
    var username = document.getElementById("user").value;
    var pswd = document.getElementById("pswd").value;

    if(username.length == 0 || pswd.length == 0){
        alert("No field can be empty");
        return false;
    }
    if(pswd.length<12){
        alert("password length must be atleast 12");
        return false;
    }
    if(!/[!@#$%^&*()_+\-=\[\]{};':"\\|,.<>\/?]+/.test(pswd)){
        alert("Password must contain at least one special character");
        return false;
    }
    return true;
}
function sendmail(){
        fetch('/forgot', {
            method: 'POST'
        })
        .then(response => {
            if (response.ok) {
                alert('Password reset email sent successfully!');
            } else {
                alert('Failed to send password reset email. Please try again later.');
            }
        })
        .catch(error => {
            console.error('Error:', error);
            alert('An error occurred. Please try again later.');
        });
}
function gotosignup(){
   window.open('signup.html');
}