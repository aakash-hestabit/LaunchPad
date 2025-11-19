const main = document.getElementsByTagName("main")[0];
const sort_btn = document.getElementsByClassName("sort-btn")[0];
const searchInput = document.getElementById("search");

let products=[];
let sorted ;
sort_btn.addEventListener("click",()=>{
    if(sorted){
        sort_btn.innerHTML = "ALREADY SORTED !!"
        setTimeout(()=>{
            sort_btn.innerHTML = "SORT(HIGH TO LOW)"
        },2000)
        return;
    }
    sorted = [...products].sort((a, b) => b.price - a.price);
    main.innerHTML ="";
    sorted.forEach((s)=>appendProduct(s));
})

searchInput.addEventListener("input",(e)=>{
    if(e.target.value.trim === ""){
        return;
    }
    search(e.target.value);
})

function debounce(fn,delay){
    let timer;
    return function(){
        const args = arguments;
        clearInterval(timer);
        timer = setTimeout(() => {
            fn.apply(this,args);
        }, delay);
    }   
}

const search = debounce((input)=>{
    const filtered = products.filter((p) =>
        p.title.toLowerCase().includes(input.toLowerCase())
    );
    main.innerHTML = "";
    if(filtered && filtered.length>0){
        filtered.forEach((p)=>appendProduct(p));
    }else{
        noProducts("NO PRODUCTS AVAILABLE FOR THE REQUESTED QUERY!!")
    }
},400);

function noProducts(text){
    const p = document.createElement("p");
    p.innerHTML = text;
    p.classList.add("no-products");
    main.appendChild(p);
}
function appendProduct(product){
    const card = document.createElement("article");
    card.classList.add("card");


    const img = document.createElement("img")
    img.classList.add("img")
    img.src = product.image[0];
    card.appendChild(img)
    img.addEventListener("mouseenter",()=>{
        if(product.image[1]){
            img.src = product.image[1];
        }
    })
    img.addEventListener("mouseleave",()=>{
        img.src = product.image[0];
    })

    const title = document.createElement("p")
    title.classList.add("title")
    title.innerHTML = product.title;
    card.appendChild(title)

    const price = document.createElement("p")
    price.classList.add("price")
    price.innerHTML = `$ ${product.price}`;
    card.appendChild(price)

    main.appendChild(card);

}
async function initializePage(){
    try {
        const res = await fetch("https://dummyjson.com/products");
        const res2 = await res.json();
        products = res2.products.map((product)=>{

            const image = product.images.slice(0, 2);
            return {id:product.id,title:product.title,price : product.price,image, status:product.availabilityStatus}
        })
        products.forEach(element => {
            appendProduct(element);
        });
        console.log(products);
    } catch (e) {
        noProducts("WE WILL BE BACK SOON");
        console.log(e);
    }
}


initializePage()