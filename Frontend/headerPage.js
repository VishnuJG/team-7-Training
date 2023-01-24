
// Function to handle category calls to the backend
function categoryAPICall(cat1_value){

    if (cat1_value=='men'){
        var cat2_value = document.getElementById("cats1").value;
    }
    else if(cat1_value){
        var cat2_value = document.getElementById("cats2").value;
    }
    else{
        var cat2_value = "";
    }
    
    window.parent.location=`Base.html?cat1=${cat1_value}&cat2=${cat2_value}&page=1`;
    
}


// Function to handle search query
function searchFunction(){
    
    var search_val = document.getElementById("search_val").value;
    if(search_val==""){
        search_val="*";
    }
    window.parent.location=`Base.html?q=${search_val}&page=1`;
    
}