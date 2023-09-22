// var bank = document.querySelector('.bank');
//     console.log(bank)
// // bank.onclick = ()=>{
// //     document.querySelector(".bank_name").style.display = "block";
// //     console.log("gr");
// // }
// bank.addEventListener('click',()=>{
//     // document.querySelector(".bank_name").style.display = "block";
//     console.log("gr");
// })
// function updateInfo() {
//     var zone = document.getElementById("zoneselect");
//     if (zone.value == "Banking sector") {
//         var Bank=document.querySelectorAll(".bank_name");
//         Bank.forEach(element => {
//             element.style.display = "block";
//         });
//     }
//     zone.classList.add("selected");
// }

function signup_show() {
    document.querySelector(".log-in").classList.add("disabled")
    document.querySelector(".sign-up").classList.remove("disabled")
}

function signin_show() {
    document.querySelector(".log-in").classList.remove("disabled")
    document.querySelector(".sign-up").classList.add("disabled")
}




function validatePhone(input) {
    const maxLength = 10;
    const inputValue = input.value.toString();

    if (inputValue.length > maxLength) {
        // document.getElementById('phoneError').textContent = 'Phone number should be up to 10 digits.';
        input.value = inputValue.slice(0, maxLength); // Truncate input
    } else {
        document.getElementById('phoneError').textContent = '';
    }
}
function validateAdhaarNumber(input) {
    const maxLength = 12;
    const inputValue = input.value.toString();

    if (inputValue.length > maxLength) {
        // document.getElementById('phoneError').textContent = 'Phone number should be up to 10 digits.';
        input.value = inputValue.slice(0, maxLength); // Truncate input
    } else {
        document.getElementById('phoneError').textContent = '';
    }
}