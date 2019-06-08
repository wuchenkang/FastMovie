function newItem(table, id, name, price, count, modify){
    var item = document.createElement("tr");
    item.setAttribute("id", table+"movie-"+id);
    var movieID = document.createElement("td");
    var movieName = document.createElement("td");
    var moviePrice = document.createElement("td");
    var movieCount = document.createElement("td");
    var temp = document.createElement("b");

    movieID.innerHTML = id;
    movieName.innerHTML = name;
    moviePrice.innerHTML = price;
    temp.innerHTML = count;
    movieCount.appendChild(temp);

    item.appendChild(movieID);
    item.appendChild(movieName);
    item.appendChild(moviePrice);
    item.appendChild(movieCount);

    if(modify){
        var addButton = document.createElement("button");
        var subButton = document.createElement("button");
        addButton.innerText = "+";
        addButton.setAttribute("onclick", "addCount(this)");
        subButton.innerText = "-";
        subButton.setAttribute("onclick", "subCount(this)");
        movieCount.insertBefore(subButton, temp);
        movieCount.appendChild(addButton);
    }

    document.getElementById(table).appendChild(item);
}

function addCount(ele){
    var item = document.getElementById(ele.parentElement.parentElement.getAttribute("id"));
    item.children[3].children[1].innerText = (parseInt(item.children[3].children[1].innerText) + 1).toString();
}

function subCount(ele){
    var item = document.getElementById(ele.parentElement.parentElement.getAttribute("id"));
    item.children[3].children[1].innerText = (parseInt(item.children[3].children[1].innerText) - 1).toString();
    if(parseInt(item.children[3].innerText) == 0){
        item.parentNode.removeChild(item);
    }
}