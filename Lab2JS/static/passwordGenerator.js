function clearPasswords(){
    const passwordsWindow = document.getElementById("passwords");
    passwordsWindow.innerHTML = '';
}

function generatePassword() {
    const engDownerCharset = "abcdefghijklmnopqrstuvwxyz"
    const engUpperCharset = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    const ruDownerCharset = "абвгдеёжзийклмнопрстуфхцчшщъыьэюя"
    const ruUpperCharset = "АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ"
    const numbers = "0123456789";
    let passwordCharset = "";
    if (document.getElementById("eng-upper-check").checked) {
        passwordCharset += engUpperCharset;
    }
    if (document.getElementById("eng-downer-check").checked) {
        passwordCharset += engDownerCharset;
    }
    if (document.getElementById("ru-upper-check").checked) {
        passwordCharset += ruUpperCharset;
    }
    if (document.getElementById("ru-downer-check").checked) {
        passwordCharset += ruDownerCharset;
    }
    if (document.getElementById("numbers-check").checked) {
        passwordCharset += numbers;
    }
    const passwordLength = document.getElementById("input-length").value;
    const passwordQuantity = document.getElementById("input-quantity").value;
    let passwords = [];
    for (let i = 0; i < passwordQuantity; i++) {
        let passwordString = "";
        for (let j = 0; j < passwordLength; j++) {
            const index = Math.floor(Math.random() * passwordCharset.length);
            passwordString += passwordCharset[index];
        }
        passwords.push(passwordString);
    }

    const passwordsDiv = document.getElementById('passwords');
    for (let index = 0; index < passwords.length; index++) {
        let passwordElem = document.createElement('input');
        passwordElem.value = passwords[index];
        passwordElem.classList.add('clickable');
        passwordElem.classList.add('password-result');
        passwordElem.style.width = (passwords[index].length + 4) + 'ch';
        passwordElem.addEventListener('select', (event) => {
            const selection = event.target.value.substring(
                event.target.selectionStart,
                event.target.selectionEnd,
            );
            saveToFile(selection);
        });
        passwordsDiv.appendChild(passwordElem);
    }

}

function saveToFile(password) {
    fetch('/downloadPassword', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ password }),
    })
        .then(response => response.json())
        .then(data => {
            alert(data.message);
        })
        .catch(error => console.error('Error:', error));
}