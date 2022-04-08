document.addEventListener("DOMContentLoaded", function(){
    setTimeout(modeSwitch, 1000)
});

function modeSwitch() {
    var colorBotton = document.querySelector('.colorButton');
    console.log("Loaded");

    colorBotton.addEventListener('click', function(){
        var headerDiv = document.getElementById('headerDiv');
        var bodyColor = document.getElementById('bodyBackgroundColor');
        var banner = document.getElementsByName('banner');
        if(colorBotton.innerHTML == "Light Mode"){
            colorBotton.innerHTML = "Dark Mode";
            headerDiv.style.backgroundColor= "#1fb8a8";
            bodyColor.style.backgroundColor= "#e8d5be";
            banner.style.color= "white";
        }else{
            colorBotton.innerHTML = "Light Mode";
            headerDiv.style.backgroundColor= "#1d2b37";
            bodyColor.style.backgroundColor= "#15202B";
            banner.style.color="#8f9daa";
        }
        
    });
}