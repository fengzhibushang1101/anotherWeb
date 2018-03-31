/**
 * Created by yueqingji on 2018/2/27.
 */




function Observer () {
}

Observer.prototype.update = function (context) {
    console.log(`Observer is updating! Info is ${context}`);
};