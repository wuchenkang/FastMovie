function newItem(){
    console.log("click");
    var item = document.createElement("tr");
    var movieID = document.createElement("td");
    var movieName = document.createElement("td");
    var moviePrice = document.createElement("td");
    var movieCount = document.createElement("td");

    movieID.innerText = "10086";
    movieName.innerText = "Test Movie";
    moviePrice.innerText = 25.3;
    movieCount.innerText = 3;

    item.appendChild(movieID);
    item.appendChild(movieName);
    item.appendChild(moviePrice);
    item.appendChild(movieCount);

    document.getElementById("trolley").appendChild(item);
}