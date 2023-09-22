var gravience = Array.from(document.querySelector(".graviences").children);
gravience.forEach(element => {
    var div=element.querySelector(".complaint_name").textContent;
    if(element.className === "active")
    document.getElementById("complaint").textContent = div;
    element.onclick = ()=>{
        document.getElementById("complaint").textContent = div;
        for(var i=0;i<gravience.length;i++){
            gravience[i].classList.remove("active");
        }
        element.classList.add("active");
    }
});