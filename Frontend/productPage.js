

// Handler to fetch data from the database API
window.onload=function(){
    
    var prod_div = document.getElementById("unique_product_container");
    const queryString = window.location.search;
    const urlParams = new URLSearchParams(queryString);
    const product_id = urlParams.get('uid')
    
    fetch(`http://127.0.0.1:5000/product-query?q=uniqueId ${product_id}`, {
        method: 'GET',
        mode : 'cors',
        headers: {
        'Access-Control-Allow-Origin':'*',
        'Accept': 'application/json',
        'Content-Type': 'application/json'
    }
    }).then(response => response.json()).then((data)=>{
        var filtered_data=data[1][0];
        var tempid=String(filtered_data.uniqueId);
        prod_div.innerHTML+=`
        <div class="unique_card" onclick="window.open('Product.html?uid=${tempid}','_blank');">
            <img id="product_image" src=`+ filtered_data.productImage+`/><br/>
            <p id="price" >₹ ${filtered_data.price}</p>
            <p id="title">${filtered_data.title}</p>
            <p id="desc">${filtered_data.productDescription}</p>
        </div> `;
        
        
    })
}