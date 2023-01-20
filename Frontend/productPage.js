

// Handler to fetch data from the database API
window.onload=function(){
    var prod_div = document.getElementById("unique_product_container");
    // prod_div.style.display="block";
    const queryString = window.location.search;
    const urlParams = new URLSearchParams(queryString);
    const product_id = urlParams.get('uid')
    
    fetch(`https://612b10b7-6879-492a-9c24-e87c114923a4.mock.pstmn.io/product-details?uid=${product_id}`, {
        method: 'GET',
        mode : 'cors',
        headers: {
        'Access-Control-Allow-Origin':'*',
    }
    }).then(response => response.json()).then((data)=>{
        
        var tempid=String(data.uniqueId);
        prod_div.innerHTML+=`
        <div class="unique_card" onclick="window.open('Product.html?uid=${tempid}','_blank');">
            <img id="product_image" src=`+ data.productImage+`/><br/>
            <p id="price" >₹ ${data.price}</p>
            <p id="title">${data.title}</p>
            <p id="desc">${data.productDescription}</p>
        </div> `
        
        
    })
}