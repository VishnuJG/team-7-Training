function product_details(data, prod_div){
    try{
        
        prod_div.innerHTML+=`
        <div class="unique_card" >
            <img id="product_image" src=`+ data.productImage+`/><br/>
            <p id="title">${ data.title.charAt(0).toUpperCase() + data.title.slice(1)}</p>
            <p id="price" >$ ${data.price}</p>
            <p id="desc">${data.productDescription!=null ? data.productDescription : ""}</p>
        </div> `;
    }
    catch(err){
        // console.log(err);
        window.location = "Page404.html";
    }
    document.getElementById("loader").style.display='none';
}


// Handler to fetch data pertaining to a single product from the database API
window.onload=function(){
    document.getElementById("loader").style.display='block';
    var prod_div = document.getElementById("unique_product_container");
    const queryString = window.location.search;
    const urlParams = new URLSearchParams(queryString);
    const product_id_search = urlParams.get('uid')
    const product_id_cat = urlParams.get('catuid')
    const header_details={'Access-Control-Allow-Origin':'*',
    'Accept': 'application/json',
    'Content-Type': 'application/json'}

    var final_data;

    if(product_id_search!=null){
        console.log(product_id_search)
        fetch(`http://127.0.0.1:5002/products/search/${product_id_search}`, {
            method: 'GET',
            mode : 'cors',
            headers: header_details
        }).then(response => response.json()).then((data)=>{
            console.log(data);
            final_data = data[1][0]
            console.log(final_data)
            product_details(final_data, prod_div)
            
        }).catch(err=>{
            window.location="Page500.html"
            // console.log(err);
        })
    }
    else{
        fetch(`http://127.0.0.1:5002/products/catalog/${product_id_cat}`, {
            method: 'GET',
            mode : 'cors',
            headers: header_details
        }).then(response => response.json()).then((data)=>{
            console.log(data)
            product_details(data, prod_div);
        }).catch(err=>{
            window.location="Page500.html"
            // console.log(err);
        })
    }
}