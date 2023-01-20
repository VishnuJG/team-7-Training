
window.onload=function(){
    var queryString = window.location.search;
    var urlParams = new URLSearchParams(queryString);
    var cat1_value = urlParams.get('cat1');
    var cat2_value =urlParams.get('cat2');
    var prod_query =urlParams.get('q');
    var page_number=urlParams.get('page');


    if (cat1_value!=null){
        var product_block=document.getElementById("product_list");
        fetch(`https://33bd8667-5c26-4e78-9318-11e0e0eb3a22.mock.pstmn.io/get-products?cat1=${cat1_value}&cat2=${cat2_value}`, {
            method: 'GET',
            mode : 'cors',
                    headers: {
                'Access-Control-Allow-Origin':'*',
                        'Accept': 'application/json',
                        'Content-Type': 'application/json'
                    }
        }).then(response => response.json()).then((data)=>{
            for (const prod of data){
                var tempid=String(prod.uniqueId);
                product_block.innerHTML+=`
                <div class="card" onclick="window.open('Product.html?uid=${tempid}','_blank');">
                    <img id="product_image" src=`+ prod.productImage+`/><br/>
                    <p>$ <span id="price">${prod.price}</span></p>
                    <p id="desc">${prod.title}</p>
                </div> `
            
            }
        })
    }
    else if(prod_query!=null){
        var product_block=document.getElementById("product_list");
        fetch(`http://127.0.0.1:5000/product-query?q=${prod_query}&page=${page_number}`, {
        method: 'GET',
        mode : 'cors',
        headers: {
        'Access-Control-Allow-Origin':'*',
        'Accept': 'application/json',
        'Content-Type': 'application/json'
        }}).then(response => response.json()).then((data)=>{
            console.log(typeof(data))
            console.log(data)
            for (const prod of data[1]){
                var tempid=String(prod.uniqueId);
                product_block.innerHTML+=`
                <div class="card" onclick="window.open('Product.html?uid=${tempid}','_blank');">
                    <img id="product_image" src=`+ prod.productImage+`/><br/>
                    <p>$ <span id="price">${prod.price}</span></p>
                    <p id="desc">${prod.title}</p>
                </div> `
            
            }
            console.log(data[0])
            paginationHandler(data[0], page_number)
        })
        
    }
    else{
        var product_block=document.getElementById("product_list");
        fetch('https://33bd8667-5c26-4e78-9318-11e0e0eb3a22.mock.pstmn.io/get-products', {
            method: 'GET',
            mode : 'cors',
                    headers: {
                'Access-Control-Allow-Origin':'*',
                        'Accept': 'application/json',
                        'Content-Type': 'application/json'
                    }
        }).then(response => response.json()).then((data)=>{
            for (const prod of data){
                var tempid=String(prod.uniqueId);
                product_block.innerHTML+=`
                <div class="card" onclick="window.open('Product.html?uid=${tempid}','_blank');">
                    <img id="product_image" src=`+ prod.productImage+`/><br/>
                    <p >$ <span id="price">${prod.price}</span></p>
                    <p id="desc">${prod.title}</p>
                </div> `
            
            }
        })
    }
    
    
}


// Handles enabling and disabling button based on number of products left
function paginationHandler(number_of_products, page_number){
    var whole_pages = Math.floor(number_of_products/10);
    var reminder_page = number_of_products%10;
    if(page_number=='1'){
        document.getElementById("page-left").disabled = true;
    }
    else{
        document.getElementById("page-left").disabled = false;
    }
    
    if(Number(page_number)==whole_pages && Number(reminder_page)==0){
        document.getElementById("page-right").disabled = true;
    }
    else if(Number(page_number)>=whole_pages && Number(reminder_page)!=0){
        document.getElementById("page-right").disabled = true;
    }
    else{
        document.getElementById("page-right").disabled = false;   
    }
    if (Number(page_number) > whole_pages+1){
        window.open("https://jgvishnu.github.io/")
    }
    document.getElementById("page-num").innerHTML=page_number;
}



// Redirects the page to the next page
function pageButtonHandler(side){
    var queryString = window.location.search;
    var urlParams = new URLSearchParams(queryString);
    var search_val = urlParams.get('q');
    var cur_page_num = Number(urlParams.get('page'));

    if(side == 'left'){
        
        window.location=`Base.html?q=${search_val}&page=${cur_page_num-1}`;
    }
    else{
        window.location=`Base.html?q=${search_val}&page=${cur_page_num+1}`;   
    }
}
