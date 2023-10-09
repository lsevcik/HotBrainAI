const btn = document.querySelector('.btn');
const output = document.querySelector('.output');
const url = 'json6.json';

btn.onclick = ()=>{
    output.innerHTML = 'Connecting......';
    getData();
}


function getData(){
    fetch(url)
    .then(rep => rep.json())
    .then(data =>{
        outData(data.friends);
    })
}



function outData(val){
    console.log(val);

    let html = '';

    val.forEach((ele,ind)=>{
        console.log(ele);
        html +='<div>${ind+1}. ${ele.score} ${ele.age} (${ele.gender})</div>';
    })

    output.innerHTML = html;
}