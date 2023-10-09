const output = document.querySelector('.output');
const button = document.querySelector('button');
const url = 'https://docs.google.com/spreadsheets/d/';
const sheetID = '1nquRawfdcz_vrHA_LDl2rsAAUUKmbi8LuD6OwDUz8s0';
const query1 = '/gviz/tq?';
const query2 = 'tqx=out:json';
const query3 = 'sheet=sheet1';


button.addEventListener('click',getData);

function getData(){
    let url1 = '${url}${sheetID}${query1}&${query2}&${query3}';
    //output.innerHTML = url1;
    fetch(url1)
    .then(res => res.text())
    .then(data => {
        const json = JSON.parse(data.substr(47).slice(0,-2));
        console.log(json.table);
        const heading = makeCell(output,'','heading')
        json.table.cols.forEach((col)=>{
            const elem = makeCell(heading,col.label,'box');
        })
        json.table.rows.forEach((row)=>{
            const div = makeCell(output,'','row');
            row.c.forEach((cell)=>{
                const elem1 = makeCell(div,'${cell.v}','box');
            })
        })
    })
}


function makeCell(parent,html,classAdd){
    const element = document.createElement('div');
    parent.append(element);
    element.innerHTML = html;
    element.classList.add(classAdd);
    return element;
}
