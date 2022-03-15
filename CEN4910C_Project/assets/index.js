window.addEventListener("load", function(){
    var colorBotton = document.querySelector('.colorButton');

    colorBotton.addEventListener('click', function(){
        var headerDiv = document.getElementById('headerDiv');
        var bodyColor = document.getElementById('bodyBackgroundColor');
        
        if((headerDiv.style.backgroundColor == "rgb(34, 48, 60)")){
            headerDiv.style.backgroundColor= "#1fb8a8";
            bodyColor.style.backgroundColor= "#e8d5be";
            colorBotton.innerHTML = "Dark Mode";
        }else{
            headerDiv.style.backgroundColor= "#22303C";
            bodyColor.style.backgroundColor= "#15202B";
            colorBotton.innerHTML = "Light Mode";
        }
        
    });

})


