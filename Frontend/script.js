var carousel = document.querySelector('.carousel-inner');
var carousel_items = carousel.children;
var i=1;
setInterval(() => {
    carousel_items[i-1>=0?i-1:carousel_items.length-1].setAttribute('data-set', 'beforeactive');
    carousel_items[i].setAttribute('data-set', 'active');
    carousel_items[i<2?i+1:0].setAttribute('data-set', 'afteractive');
    i+1>2?i=0:i++;
}, 2000);