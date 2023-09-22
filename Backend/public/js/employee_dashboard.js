var gravience = Array.from(document.querySelector(".graviences").children);
var div2 = document.getElementById("complaint").getAttribute("data-set");
gravience.forEach(element => {
    var div=element.querySelector(".complaint_name").getAttribute("data-set");
    if(div===div2){
        for(var i=0;i<gravience.length;i++){
            gravience[i].classList.remove("active");
        }
        element.classList.add("active");
    }
});

