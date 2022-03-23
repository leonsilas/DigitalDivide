window.addEventListener("load", function(){
    var colorBotton = document.querySelector('.colorButton');

    colorBotton.addEventListener('click', function(){
        var headerDiv = document.getElementById('headerDiv');
        var bodyColor = document.getElementById('bodyBackgroundColor');
        var banner = document.getElementsByName('banner');
        
        if(colorBotton.innerHTML == "Light Mode"){
            headerDiv.style.backgroundColor= "#1fb8a8";
            bodyColor.style.backgroundColor= "#e8d5be";
            banner.style.color= "white";
            colorBotton.innerHTML = "Dark Mode";
        }else{
            headerDiv.style.backgroundColor= "#1d2b37";
            bodyColor.style.backgroundColor= "#15202B";
            banner.style.color="#8f9daa";
            colorBotton.innerHTML = "Light Mode";
        }
        
    });

})


