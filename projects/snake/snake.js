/**
 * Created by yueqingji on 2018/3/1.
 */


let DIR = {
    LEFT: 37,
    TOP: 38,
    RIGHT: 39,
    BOTTOM: 40
};

let map = {
    width: 900,
    height: 500
};

let box = {
    width: 50,
    height: 50
};

let nums = {
    hNum: map.width / box.width,
    vNum: map.height / box.height
};

let snake = [];
let other = [];
let dir = DIR.RIGHT;


window.onload = function () {
    initMap();
    showFood();
    setInterval(snakeMove, 400);
    document.onkeyup = function (e) {
        let event = window.event || e;
        let code = e.keyCode;
        if (code - 2 !== dir && code + 2 !== dir) {
            dir = code;
        }
    }
};

function initMap () {
    let mapTarget = document.getElementById('map');
    mapTarget.style.width = map.width + 'px';
    mapTarget.style.height = map.height + 'px';
    let newSpan = null;
    for (let i = 0; i < nums.hNum * nums.vNum; i++) {
        newSpan = document.createElement('span');
        newSpan.style.width = box.width + 'px';
        newSpan.style.height = box.height + 'px';
        newSpan.id = i;
        mapTarget.appendChild(newSpan);
        if (i < 5) {
            newSpan.className = 'snake';
            snake.push(newSpan);
        } else {
            other.push(newSpan);
        }
    }
}

function showFood () {
    other[Math.floor(Math.random() * other.length)].className = 'food';
}

function snakeMove () {
    let headId;
    switch (dir) {
        case DIR.LEFT:
            headId = parseInt(snake[snake[snake.length - 1]].id) - 1;
            if (headId % nums.hNum === 0) headId += nums.hNum; // 如果在地图最右边？？？
            break;
        case DIR.TOP:
            headId = parseInt(snake[snake.length - 1].id) - nums.hNum;
            if (headId < 1) headId+=nums.hNum*nums.vNum; // 如果现在在地图最上面
            break;
        case DIR.RIGHT:
            headId = parseInt(snake[snake.length - 1].id) + 1;
            if(headId % nums.hNum === 1) headId -= nums.hNum;
            break;
        case DIR.BOTTOM:
            headId = parseInt(snake[snake.length - 1].id) + nums.hNum;
            if (headId > nums.hNum * nums.vNum) headId -= nums.hNum * nums.vNum;
            break;
        default:
            break;
    }
    let head = document.getElementById(headId);
    for (let i = 0; i < snake.length; i++) {
        if (headId === snake[i].id) {
            alert('Game Over!');
            location.reload();
        }
    }
    let index;
    for (let i = 0; i < other.length; i++) {
        if (headId === other[i].id) {
            index = i;
            break;
        }
    }
    other.splice(index, 1);
    snake.push(head);
    if (head.className === 'food') {
        showFood();
    } else {
        snake[0].className = '';
        other.push(snake.shift());
    }
    head.className = 'snake';
}
