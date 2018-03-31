/**
 * Created by yueqingji on 2018/2/27.
 */


/**
 * ObserverList 类  存储了一个subject的观察者列表
 * @constructor
 */
function ObserverList() {
    this.observerList = [];
}

ObserverList.prototype.add = function (observer) {
    return this.observerList.push(observer);
};

ObserverList.prototype.empty = function () {
    this.observerList = [];
};

ObserverList.prototype.count = function () {
    return this.observerList.length;
};

ObserverList.prototype.get = function (index) {
    if (index >= 0 && index < this.observerList.length) {
        return this.observerList[index];
    }
};

ObserverList.prototype.insert = function (observer, index) {
    if (index >= 0 && index < this.observerList.length) {
        this.observerList.splice(index, 0, observer);
    }
};

ObserverList.prototype.indexOf = function (observer, startIndex = 0) {
    let i = startIndex;
    while (i < this.observerList.length) {
        if (this.observerList[i] === observer) {
            return i;
        }
        i++;
    }
    return -1;
};

ObserverList.prototype.removeIndexAt = function (index) {
    if (index >= 0 && index < this.observerList.length) {
        this.observerList.splice(index, 1);
    }
};

