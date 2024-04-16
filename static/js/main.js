let bd=document.querySelector("body");
let menu=document.querySelector(".toggle-menu");
let tog=document.querySelector(".toggled");


bd.addEventListener("click",function(e){
    if(e.target === menu){
        if(tog.style.display="block"){
            tog.style.display="block";
        }else{
            tog.style.display="block";
        }
    }else{
        tog.style.display="none";
    }
})

