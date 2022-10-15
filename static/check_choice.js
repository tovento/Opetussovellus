function check_choice(formName, inputName, message) {
    const form = document.forms[formName];
    const answer = form.querySelector(`input[name="${inputName}"]:checked`);
    if (answer) {
        form.submit();
    }
    else {
        window.alert(message);
    }
}
