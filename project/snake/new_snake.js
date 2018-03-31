/**
 * Created by yueqingji on 2018/3/2.
 */


function Game (el) {
    this.dirMap = {
        LEFT: 37,
        TOP: 38,
        RIGHT: 39,
        BOTTOM: 40
    };
    this.speed = 100;
    this.dir = this.dirMap.RIGHT;
    this.snake = [];
    this.other = [];
    this.size = 15;
    this.board = new Board(el, this.size);
    this.intervalId = 0;
    this.init();
}

Game.prototype.changeClass = function (coordinates, c) {
    this.board.get(coordinates).className = `cell ${c}`;
};

Game.prototype.init = function () {
    this.board.init();
    let size = this.board.size;
    this.other = Array.from({length: size}, (v, i) => Array.from({length: size}, (v2, j) => [i, j])).reduce((prev, next) => {
        return prev.concat(next);
    },[]);
    this.snake = this.other.splice(0, 4).reverse();
    this.snake.forEach(s => this.changeClass(s, 'snake'));
    this.createFood();
    document.onkeyup = (e) => {
        let event = window.event || e;
        let code = event.keyCode;
        if (code - 2 !== this.dir && code + 2 !== this.dir) {
            this.dir = code;
        }
    }
};

Game.prototype.createFood = function () {
    this.changeClass(this.other[Math.floor(Math.random() * this.other.length)], 'food');
};

Game.prototype.gameOver = function () {
    clearInterval(this.intervalId);
    alert('游戏结束！');
    this.init();
};

Game.prototype.isEqual = function (coo1, coo2) {
    return coo1[0] === coo2[0] && coo1[1] ===  coo2[1];
};

Game.prototype.start = function () {
    this.intervalId = setInterval(this.snakeMove.bind(this), this.speed);
};

Game.prototype.snakeMove = function () {
    let head = this.snake[0];
    let next;
    switch (this.dir) {
        case this.dirMap.RIGHT:
            next = [head[0], head[1] === this.size - 1 ? 0 : head[1] + 1];
            break;
        case this.dirMap.LEFT:
            next = [head[0], head[1] === 0 ? this.size - 1 : head[1] - 1];
            break;
        case this.dirMap.TOP:
            next = [head[0] === 0 ? this.size - 1: head[0] - 1, head[1]];
            break;
        case this.dirMap.BOTTOM:
            next = [head[0] === this.size - 1 ? 0 : head[0] + 1, head[1]];
            break;
        default:
            break;
    }
    let nextDom = this.board.get(next);
    if (nextDom.classList.contains('snake')) {
        this.gameOver();
        return;
    }
    let otherIndex = 0;
    while (!this.isEqual(this.other[otherIndex], next)) {
        otherIndex ++;
    }
    this.other.splice(otherIndex, 1);
    this.snake.unshift(next);
    if (nextDom.classList.contains('food')) {
        this.createFood();
    } else {
        let tail = this.snake.splice(-1)[0];
        this.changeClass(tail, '');
        this.other.push(tail);
    }
    this.changeClass(next, 'snake');
};