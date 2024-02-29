
const usernameField = document.querySelector('#usernameField');
const emailField = document.querySelector('#emailField');
const feedbackArea = document.querySelector('.invalid_feedback');
const emailFeedbackArea = document.querySelector('.emailFeedbackArea');
const usernameSuccessOutput = document.querySelector('.usernameSuccessOutput');
const showPassword = document.querySelector('.showPassword');
const passwordField = document.querySelector('#passwordField');
const submitBtn = document.querySelector('.submit-btn');
// lam hiện, ẩn password
showPassword.addEventListener('click',(e) =>{
    if(showPassword.textContent==='SHOW'){
        showPassword.textContent = 'HIDE';
        passwordField.setAttribute("type", "text");
    }else{
        showPassword.textContent = 'SHOW';
        passwordField.setAttribute("type", "password");
    }
})




// username validate
usernameField.addEventListener('keyup',(e) =>{
    
    const usernameVal = e.target.value;
    // hieu ung check username xanh
    usernameSuccessOutput.style.display = "block";
    usernameSuccessOutput.textContent =`Checking ${usernameVal}`;
    
    // console.log("usernameVal", usernameVal);

    usernameField.classList.remove('is-invalid');
    feedbackArea.style.display  =   'none';

    if(usernameVal.length>0){
        fetch("/authentication/validate-username", {
            body : JSON.stringify({ username: usernameVal }),
            method : "POST",
        })
        .then((res) => res.json())
        .then((data) => {
            
            usernameSuccessOutput.style.display = "none";
            if(data.username_error){
                usernameField.classList.add('is-invalid');
                feedbackArea.style.display  =   'block';
                feedbackArea.innerHTML  =   `<p>${data.username_error}</p>`;
                submitBtn.disabled = true;
            }else{
                submitBtn.removeAttribute('disabled');
            }
        });
    }
})
// email validate
emailField.addEventListener('keyup',(e) =>{
    // console.log("777777",777777);
    const emailVal = e.target.value;
    // console.log("emailVal", emailVal);

    emailField.classList.remove('is-invalid');
    emailFeedbackArea.style.display  =   'none';

    if(emailVal.length>0){
        fetch("/authentication/validate-email", {
            body : JSON.stringify({ email: emailVal }),
            method : "POST",
        })
        .then((res) => res.json())
        .then((data) => {
            console.log("data" , data);
            
            if(data.email_error){
                emailField.classList.add('is-invalid');
                emailFeedbackArea.style.display  =   'block';
                emailFeedbackArea.innerHTML  =   `<p>${data.email_error}</p>`;
                submitBtn.disabled = true;
            }else{
                submitBtn.removeAttribute('disabled');
            }
        });
    }
})