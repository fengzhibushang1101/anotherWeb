/**
 * Created by yueqingji on 2018/3/14.
 */



function Carousel (el, images, speed) {
    this.el = typeof el === 'string' ? document.getElementById(el) : el;
    this.images = images;
    this.intervalId = 0;
    this.containter = document.getElementById('images');
    this.dots = document.getElementById('dots');
    this.prevBtn = document.getElementById('prev');
    this.nextBtn = document.getElementById('next');
    this.curIndex = 0;
    this.imageDoms = [];
    this.dotDoms = [];
    this.width = 0;
    this.speed = speed || 3000;
    this.mid = Math.floor(this.images.length/2);
    this.init();
}

Carousel.prototype.init = function () {
    var len = this.images.length;
    var _this = this;
    if (len) {
        this.width = this.el.getBoundingClientRect().width;
        this.dotDoms = this.images.map(function (v, i) {
            var dot = Init.createEl('div', { class: 'dot' });
            dot.onclick = function () {
                _this.next(i -_this.curIndex);
            };
            return dot;
        });
        Init.appendChildren(this.dots, this.dotDoms);
        this.imageDoms = this.images.map(function(src) {
            var image = Init.createEl('img', { src: src, class: 'image' });
            image.style.width = _this.width + 'px';
            return image;
        });
        Init.appendChildren(this.containter, this.imageDoms);
        this.prevBtn.addEventListener('click', _.throttle(function () {
            _this.next(-1);
        }, 500));
        this.nextBtn.addEventListener('click', _.throttle(function () {
            _this.next();
        }, 500));
    }
    this.el.onmouseover = function () {
        _this.stop();
    };
    this.el.onmouseout = function () {
        _this.start();
    };
    this.next(-this.curIndex);
};

Carousel.prototype.next = function (frag) {
    var frag = frag === undefined ? 1 : frag;
    var tmp = this.curIndex + frag;
    var len = this.images.length;
    if ( tmp < 0 ) {
        this.curIndex = len - 1;
    } else if (tmp >=  len) {
        this.curIndex = 0;
    } else {
        this.curIndex = tmp;
    }
    // this.containter.style.left = 0 - this.curIndex * this.width + 'px';
    for (var i = 0; i < this.images.length; i++) {
        var curImageStyle = this.imageDoms[i].style;
        if (i === this.curIndex){
            this.dotDoms[i].className = 'dot on';
            curImageStyle.left = 0;
            curImageStyle.zIndex = 0;
            curImageStyle.display = '';
        } else {
            this.dotDoms[i].className = 'dot';
            var indexFrag = i - this.curIndex;
            if (Math.abs(indexFrag) >= this.mid && indexFrag > 0) {
                indexFrag = indexFrag - len;
            } else if (Math.abs(indexFrag) >= this.mid && indexFrag < 0) {
                indexFrag = len + indexFrag;
            }
            curImageStyle.zIndex = Math.abs(indexFrag) === 1 ? -1 : -2;
            if (Math.abs(indexFrag) > 1) curImageStyle.display = 'none'; else curImageStyle.display = '';
            curImageStyle.left = indexFrag * this.width + 'px';
        }
    }
};

Carousel.prototype.start = function () {
    if (!this.intervalId) {
        var _this = this;
        this.intervalId = setInterval(function () {
            _this.next();
        }, this.speed);
    }
};

Carousel.prototype.stop = function () {
    if (this.intervalId) {
        clearInterval(this.intervalId);
        this.intervalId = 0;
    }
};