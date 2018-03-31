/**
 * Created by yueqingji on 2018/3/2.
 */

function Board (el, size) {
    this.size = size || 15;
    this.el = typeof el === 'string' ? document.getElementById(el) : el;
    this.unit = 0;
    this.map = [];
}

Board.prototype.init = function () {
    this.el.innerHTML = '';
    this.map = [];
    let frag = document.createDocumentFragment();
    for (let i = 0; i < this.size; i++) {
        let row = document.createElement('div');
        row.className = 'row';
        this.map[i] = [];
        for (let j = 0; j < this.size; j++) {
            let cell = document.createElement('div');
            cell.className = 'cell';
            this.map[i].push(cell);
            row.appendChild(cell);
        }
        frag.appendChild(row);
    }
    this.el.appendChild(frag);
    let maxWidth = Math.min(document.body.clientWidth * 0.8, this.size * 40);
    let w = ~~(maxWidth / (this.size - 1));
    this.el.style.height = this.el.style.width = w * (this.size - 1) + 'px';
    this.unit = this.el.querySelector('.cell').getBoundingClientRect().width;
};

Board.prototype.get = function (coordinates) {
    return this.map[coordinates[0]][coordinates[1]];
};