
// Function to handle category calls to the backend. Generates url with all the category params, encodes the same and redirects the page to the url.
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

    
    window.parent.location=`Base.html?cat1=${cat1_value}&cat2=${encodeURIComponent(cat2_value)}&page=1`;
    
}


// Function to handle search query. Generates the search url with all the query parameter and redirects the page with the params. This function also does url encoding.
function searchFunction(){
    var search_val = document.getElementById("search_val").value;
    if(search_val==""){
        search_val="*";
    }
    window.parent.location=`Base.html?q=${encodeURIComponent(search_val)}&page=1`;
    
}


//Onload this function handles fetching category list data for both men and women from the backend and renders the same
window.onload=function(){
    var men_dropdown=document.getElementById("cats1");
    var women_dropdown=document.getElementById("cats2");
    fetch('http://127.0.0.1:5002/subcategory-names', {
            method: 'GET',
            mode : 'cors',
                    headers: {
                'Access-Control-Allow-Origin':'*',
                        'Accept': 'application/json',
                        'Content-Type': 'application/json'
                    }
        }).then(response => response.json()).then((data)=>{
            console.log(data);
            for (const prod of data['men']){

                men_dropdown.innerHTML+=`
                <option value='${prod}'>${prod}</option>`
            
            }
            for (const prod of data['women']){

                women_dropdown.innerHTML+=`
                <option value='${prod}'>${prod}</option>`
            
            }
        }).catch(err=>{
            // window.location="Page500.html"
            console.log(err);
        });
}
