/**
 * Created by yueqingji on 2018/2/24.
 */



function approximate(number) {
    if(number - Math.floor(number) > 0.5) {
        return Math.ceil(number);
    }
    return Math.floor(number);
}

function Game (engine, size) {
    this.engine = engine || 'DOM';
    this.end = false;
    this.data = [];
    this.size = size || 15;
    this.currentPlayer = 'white';
    this.board = '';
    this.init();
}

Game.prototype.init = function () {
    this.end = false;
    this.currentPlayer = 'white';
    this.data = Array.from({length: this.size}, () => Array.from({length: this.size}, () => 0));
    this.updateIndicator();
};

Game.prototype.start = function () {
    this.board = new Board('.board');
    this.board.init();

    let rect = this.board.el.getBoundingClientRect();
    this.board.el.addEventListener('click', function(event) {
        let ptX = event.clientX - rect.left;
        let ptY = event.clientY - rect.top;
        let x = approximate(ptX / this.board.unit);
        let y = approximate(ptY / this.board.unit);
        this.play(x, y);
    }.bind(this));

    let btnUndo = document.querySelector('.undo');
    let btnRedo = document.querySelector('.redo');
    let btnRestart = document.querySelector('.restart');
    btnUndo.addEventListener('click', function() {
        this.undo();
    }.bind(this));

    btnRedo.addEventListener('click', function() {
        this.redo();
    }.bind(this));

    btnRestart.addEventListener('click', function() {
        this.init();
        this.board.init();
    }.bind(this));
};
Game.prototype.updateIndicator = function() {
    let el = document.querySelector('.turn');
    if (this.currentPlayer === 'white') {
        el.classList.add('black');
        el.classList.remove('white');
    } else {
        el.classList.add('white');
        el.classList.remove('black');
    }
};

Game.prototype.play = function (x, y) {
    if (this.end || this.data[x][y]) {
        return;
    }
    if(!this.lockPlayer) {
        this.currentPlayer = this.currentPlayer === 'black' ? 'white' : 'black';this.data[x][y] = this.currentPlayer;
    }
    this.lockPlayer = false;
    let piece = new Piece(x, y, this.currentPlayer);
    let pieceEl = this.board.drawPiece(piece);
    this.updateIndicator();
    let winner = this.judge(x, y, this.currentPlayer);
    this.ended = winner !== 0;
    if(this.ended) {
        setTimeout(function() {
            this.gameOver();
        }.bind(this), 0);
    }
    this.move = {
        piece: piece,
        el: pieceEl
    };
};

Game.prototype.gameOver = function() {
    alert((this.currentPlayer === 'black' ? '黑方' : '白方') + '胜！');
};

Game.prototype.undo = function() {
    if(this.ended) {
        return;
    }
    this.lockPlayer = true;
    this.move.el.remove();
    let piece = this.move.piece;
    this.data[piece.x][piece.y] = 0;
};

Game.prototype.redo = function() {
    if(this.ended) {
        return;
    }
    this.lockPlayer = true;
    this.board.el.appendChild(this.move.el);
    let piece = this.move.piece;
    this.data[piece.x][piece.y] = piece.player;
};

//判断胜负
Game.prototype.judge = function(x, y, player) {
    let horizontal = 0;
    let vertical = 0;
    let cross1 = 0;
    let cross2 = 0;

    let gameData = this.data;
    //左右判断
    for (let i = x; i >= 0; i--) {
        if (gameData[i][y] !== player) {
            break;
        }
        horizontal++;
    }
    for (let i = x + 1; i < this.size; i++) {
        if (gameData[i][y] !== player) {
            break;
        }
        horizontal++;
    }
    //上下判断
    for (let i = y; i >= 0; i--) {
        if (gameData[x][i] !== player) {
            break;
        }
        vertical++;
    }
    for (let i = y + 1; i < this.size; i++) {
        if (gameData[x][i] !== player) {
            break;
        }
        vertical++;
    }
    //左上右下判断
    for (let i = x, j = y; i >= 0, j >= 0; i--, j--) {
        if (gameData[i][j] !== player) {
            break;
        }
        cross1++;
    }
    for (let i = x + 1, j = y + 1; i < this.size, j < this.size; i++, j++) {
        if (gameData[i][j] !== player) {
            break;
        }
        cross1++;
    }
    //右上左下判断
    for (let i = x, j = y; i >= 0, j < this.size; i--, j++) {
        if (gameData[i][j] !== player) {
            break;
        }
        cross2++;
    }
    for (let i = x + 1, j = y - 1; i < this.size, j >= 0; i++, j--) {
        if (gameData[i][j] !== player) {
            break;
        }
        cross2++;
    }
    console.log(horizontal, vertical, cross1, cross2);
    if (horizontal >= 5 || vertical >= 5 || cross1 >= 5 || cross2 >= 5) {
        return player;
    }
    return 0;
};