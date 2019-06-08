function newItem(table, id, name, price, count, modify){
    let item = document.createElement("tr");
    item.setAttribute("id", table+"movie-"+id);
    let movieID = document.createElement("td");
    let movieName = document.createElement("td");
    let moviePrice = document.createElement("td");
    let movieCount = document.createElement("td");
    let temp = document.createElement("b");

    movieID.innerText = id;
    movieName.innerText = name;
    moviePrice.innerText = price;
    temp.innerText = count;
    if(modify){
        temp.setAttribute("id", id+"_count");
    }else{
        temp.setAttribute("id", id+"_count_");
    }
    movieCount.appendChild(temp);

    item.appendChild(movieID);
    item.appendChild(movieName);
    item.appendChild(moviePrice);
    item.appendChild(movieCount);

    if(modify){
        let addButton = document.createElement("button");
        let subButton = document.createElement("button");
        addButton.innerText = "+";
        addButton.setAttribute("onclick", "addCount(this)");
        addButton.setAttribute("class", "btn btn-default");
        subButton.innerText = "-";
        subButton.setAttribute("onclick", "subCount(this)");
        subButton.setAttribute("class", "btn btn-default");
        movieCount.insertBefore(subButton, temp);
        movieCount.appendChild(addButton);
    }

    document.getElementById(table).appendChild(item);
}

function addCount(ele){
    let item = document.getElementById(ele.parentElement.parentElement.getAttribute("id"));
    item.children[3].children[1].innerText = (parseInt(item.children[3].children[1].innerText) + 1).toString();
    document.getElementById(item.children[3].children[1].getAttribute('id')+"_").innerText = item.children[3].children[1].innerText;
}

function subCount(ele){
    let item = document.getElementById(ele.parentElement.parentElement.getAttribute("id"));
    let item_ = document.getElementById(document.getElementById(item.children[3].children[1].getAttribute('id')+"_").parentElement.parentElement.getAttribute("id"));
    item.children[3].children[1].innerText = (parseInt(item.children[3].children[1].innerText) - 1).toString();
    item_.children[3].children[0].innerText = item.children[3].children[1].innerText;
    if(parseInt(item.children[3].innerText) == 0){
        item.parentElement.removeChild(item);
        item_.parentElement.removeChild(item_);
    }
}

function submitTrolley(url){
    let form = document.createElement("form");
    form.action = url;
    form.method = 'post';
    form.style.display = "none";

    let trolley = document.getElementById("trolley-main");
    console.log(trolley.children.length);
    for(let i = 1; i < trolley.children.length; i++){
        let item = trolley.children[i];
        let ele = document.createElement("input");
        ele.name = i-1;
        ele.value = item.children[0].innerText+ "|" + item.children[1].innerText + "|" + item.children[2].innerText + "|" + item.children[3].children[1].innerText;
        form.appendChild(ele);
    }
    document.body.appendChild(form);
    form.submit();
}