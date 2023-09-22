var pic_add = document.getElementById("profile_pic_add");
var pic = document.getElementById("profile_pic");
pic_add.addEventListener("change", (event) => {
  var file = pic_add.files[0];
  var reader = new FileReader();
  reader.onloadend = function () {
    pic.src = reader.result;
  }
  if (file) {
    reader.readAsDataURL(file);
  } else {
    pic.src = "assets/profile.png";
  }
}
);
var edit = document.getElementById("edit");
edit.onclick = () => {
  var inputs = Array.from(document.querySelectorAll(".editable"));
  inputs.forEach(element => {
    if (element.hasAttribute("disabled")===true) {
      element.removeAttribute("disabled");
      edit.textContent = "Cancel";
      edit.style.backgroundColor = "Green";
      document.querySelector(".edit_submit").style.display = "block";
    }
    else {
      element.setAttribute("disabled","");
      edit.textContent = "Edit";
      edit.style.backgroundColor = "var(--color)";
      document.querySelector(".edit_submit").style.display = "none";
    }
  });

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