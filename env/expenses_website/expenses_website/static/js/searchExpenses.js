const searchField = document.querySelector("#searchField");
const tableOutput = document.querySelector(".table-output");
tableOutput.style.display = 'none';
const appTable = document.querySelector(".app-table");
const paginationContainer = document.querySelector(".pagination-container");
const tbody = document.querySelector(".table-body");
searchField.addEventListener('keyup',(e)=>{

    const searchVal = e.target.value;

    if(searchVal.trim().length > 0){
        paginationContainer.style.display = 'none';
        tbody.innerHTML = "";
        console.log('searchVal', searchVal);
        fetch("/search-expenses", {
            body : JSON.stringify({ searchTxt: searchVal }),
            method : "POST",
        })
        .then((res) => res.json())
        .then((data) => {
            console.log('data', data);
            appTable.style.display = 'none';
            tableOutput.style.display = 'block';
            
            if(data.length === 0 ){
                tableOutput.innerHTML = 'No results';
                
            }else{
                data.forEach(item => {
                    tbody.innerHTML += `
                    <tr >
                    <td>${item.amount}</td>
                    <td>${item.description}</td>
                    <td>${item.category}</td>
                    <td>${item.date}</td>
                    </tr>
                    `;
                });
            }
        });
    }else{
        appTable.style.display = 'block';
        tableOutput.style.display = 'none';
        paginationContainer.style.display = 'flex';
    }
})