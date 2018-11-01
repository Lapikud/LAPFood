// Random data vomitator.
function stringGen(len) {
    var text = "";
    var charset = "abcdefghijklmnopqrstuv    ";
    for (var i = 0; i < len; i++)
        text += charset.charAt(Math.floor(Math.random() * charset.length));
    return text;
}

function priceGen(len) {
    var text = "";
    var charset = "1234567890.";
    for (var i = 0; i < len; i++) {
        text += charset.charAt(Math.floor(Math.random() * charset.length));
    }
    text += '€';
    return text;
}

function getData(type) {

    if (type == 'name') {
        var namelist = ['bitStop', 'Daily', 'rahvatoit', 'SOC', 'raamatukogu', 'Peamaja', 'U01', 'U06'];
        var placeName = namelist[Math.floor(Math.random()*namelist.length)];
        return placeName;
    }
    else if (type == 'category') {
        var cats = ['lunch', 'dinner', 'breakfast'];
        var category = cats[Math.floor(Math.random()*cats.length)];
        return category;
    }
    else if (type == 'food') {
        var text = stringGen(Math.floor((Math.random() * 70) + 1));
        var price = priceGen(Math.floor((Math.random() * 3) + 1));
        return [text, price];
    }
    else if (type == 'img') {
        var images = ['bg.jpg', 'food.jpg', '1.jpg', '2.jpg', '3.jpg'];
        var image = images[Math.floor(Math.random()*images.length)];
        return image;
    }
    else if (type == 'table') {
        var table = tablefiller(Math.floor((Math.random() * 7) + 1), getData('category'));
        return table;
    }
}

//TODO: remove this s#it
function morningMenu(){
    var header = document.getElementsByClassName('breakfast');
    for (var i = 0; i < header.length; i++) {
        var menu = header[i];
        menu.style.transition = "transform 1s ease 0s";
        menu.style.transform = 'translateY(-100%)';
        //menu.removeChild(document.getElementsByClassName('breakfast'));
        //setTimeout(shit, 1000, menu);
    }
}
function shit(menu) {
    menu.style.transform = 'translateY(0%)';
    var x = document.getElementsByClassName('breakfast');
    //console.log(x[0]);
    menu.removeChild(x[0]);
}

//I guess this works?
function creator() {
    var div = document.createElement("div");
    div.className = "menu";

    var name = getData('name');
    //div.id = name;
    var title = document.createElement("div");
    title.appendChild(document.createTextNode(name));
    title.className = "title " + name;
    div.appendChild(title);

    var container = document.createElement("div");
    container.className = 'container';
    
    var image = getData('img');
    div.style.backgroundImage = 'url(images/background/' + image + ')';

    for (var i = 0; i < Math.floor((Math.random() * 3) + 1); i++) {
        container.appendChild(getData('table'));

    }

    div.appendChild(container);
    document.getElementById("main").appendChild(div);

}

function tablefiller(rows, category) {

    var table = document.createElement("TABLE");
    table.className = category;
    var row = table.insertRow(-1);

    var titleCell = row.insertCell(0);
    titleCell.className = "category";        
    titleCell.colSpan = '2';

    for (var i = 0; i < rows; i++) {

        var food = getData('food');
        var row = table.insertRow(-1);

        var foodCell = row.insertCell(0);
        foodCell.className = "foods";        
        foodCell.innerHTML = food[0];

        var priceCell = row.insertCell(1);
        priceCell.className = "price";
        priceCell.innerHTML = food[1];
    }
    titleCell.innerHTML = category;
    return table;
}

function deleter() {
    var body = document.getElementById('main');
    var menu = document.getElementsByClassName('menu');
    body.style.transition = "None";
    body.style.transform = 'translateX(0)';
    menu[0].parentNode.removeChild(menu[0]);
    //cell[0].parentNode.appendChild(cell[0]);
}

function move() {
    var body = document.getElementById('main');
    body.style.transition = "transform 5s ease 0s";
    body.style.transform = 'translateX(-20%)';
    setTimeout(deleter, 5500);
}

function clock() {
    setInterval(clock, 1000);
    var x = document.getElementById('header');
    var d = new Date();
    var h = d.getHours();
    var m = d.getMinutes();
    var s = d.getSeconds();
    
    if (h < 10) {h = '0' + h}
    if (m < 10) {m = '0' + m}
    if (s < 10) {s = '0' + s}
    
    x.innerHTML = h + ':' + m + ':' + s;
}

function populate() {
    var i;
    for (i = 0; i < 4; i++) {
        creator();
    }
    main();
    clock();
}

function main() {
    creator();
    move();
    setTimeout(main, 10000);
}
