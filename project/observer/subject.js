/**
 * Created by yueqingji on 2018/2/27.
 */

/**
 * Subject 类 将会extend到观察的对象上
 * @constructor
 */
function Subject() {
    this.observers = new ObserverList();
}

Subject.prototype.addObserver = function (observer) {
    this.observers.add(observer);
};

Subject.prototype.removeObserver = function (observer) {
    this.observers.removeIndexAt(this.observers.indexOf(observer));
};

Subject.prototype.notify = function (context) {
    let count = this.observers.count();
    for (let i = 0; i < count; i++) {
        this.observers.get(i).update(context);
    }
};