
// Function to handle category calls to the backend
function categoryAPICall(cat1_value){
    // var cat1_value = document.getElementById("cats1").value;
    if (cat1_value=='men'){
        var cat2_value = document.getElementById("cats1").value;
    }
    else if(cat1_value){
        var cat2_value = document.getElementById("cats2").value;
    }
    else{
        var cat2_value = "";
    }
    
    window.parent.location=`Base.html?cat1=${cat1_value}&cat2=${cat2_value}`;
    
}



// Function specially to hande exp requests only
// function expAPIhandler(){
//     var cat1_value="exp";
//     var cat2_value="";
//     window.parent.location=`Base.html?cat1=${cat1_value}&cat2=${cat2_value}`;
//     fetch('https://bf71dea9-0477-42c5-9aab-7893926a7fa5.mock.pstmn.io/testpost', {
//         method: 'POST',
//         mode : 'cors',
//         headers: {
//             'Access-Control-Allow-Origin':'*',
//             'Accept': 'application/json',
//             'Content-Type': 'application/json'
//         },
//         body: JSON.stringify({ "cat1" : cat1_value, "cat2" :  cat2_value})
//     }).then(response => response.json()).then(response => console.log(JSON.stringify(response)))
// }

// Function to handle search query
function searchFunction(){
    var search_val = document.getElementById("search_val").value;
    if(search_val==""){
        search_val="*";
    }
    window.parent.location=`Base.html?q=${search_val}&page=1`;
    
}