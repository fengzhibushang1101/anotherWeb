/**
 * Created by yueqingji on 2018/2/24.
 */
function Board(el, size) {
    this.size = size || 15;
    this.el = typeof el === 'string' ? document.querySelector(el) : el;
    this.unit = 0;
}

Board.prototype.init = function () {
    this.el.innerHTML = '';
    let frag = document.createDocumentFragment();
    for (let i = 0; i < this.size; i++) {
        let row = document.createElement('div');
        for (let j = 0; j < this.size; j++) {
            let cell = document.createElement('div');
            cell.classList.add('cell');
            row.appendChild(cell);
        }
        row.classList.add('row');
        frag.appendChild(row);
    }
    this.el.appendChild(frag);
    let maxWidth = Math.min(document.body.clientWidth * 0.8, this.size * 40);
    let w = ~~(maxWidth / (this.size - 1));
    console.log(w);
    this.el.style.height = this.el.style.width = w * (this.size - 1) + 'px';
    console.log(this.el.style.height);
    this.unit = this.el.querySelector('.cell').getBoundingClientRect().width;
};

Board.prototype.drawPiece = function (piece) {
    let dom = document.createElement('div');
    dom.classList.add('piece');
    dom.style.width = dom.style.height = this.unit + 'px';
    dom.style.left = ~~((piece.x - .5) * this.unit) + 'px';
    dom.style.top = ~~((piece.y - .5) * this.unit) + 'px';
    dom.classList.add(piece.player === 'black' ? 'black' : 'white');
    this.el.appendChild(dom);
    return piece;
};
