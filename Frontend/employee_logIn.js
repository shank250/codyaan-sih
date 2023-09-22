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
function updateInfo() {
    var zone = document.getElementById("zoneselect");
    if (zone.value == "Banking sector") {
        var Bank=document.querySelectorAll(".bank_name");
        Bank.forEach(element => {
            element.style.display = "block";
        });
    }
    zone.classList.add("selected");
}

function signin_show() {
    document.querySelector(".log-in").classList.remove("disabled")
    document.querySelector(".sign-up").classList.add("disabled")
}
function signup_show() {
    document.querySelector(".log-in").classList.add("disabled")
    document.querySelector(".sign-up").classList.remove("disabled")
}