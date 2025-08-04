

(function () {
  var parent = document.querySelector("#rangeSlider");
  if (!parent) return;
 
  var rangeS = parent.querySelectorAll("input[type=range]"),
    numberS = parent.querySelectorAll("input[type=number]");
 
  rangeS.forEach(function (el) {
    el.oninput = function () {
      var slide1 = parseFloat(rangeS[0].value),
        slide2 = parseFloat(rangeS[1].value);
 
      if (slide1 > slide2) {
        [slide1, slide2] = [slide2, slide1];
      }
 
      numberS[0].value = slide1;
      numberS[1].value = slide2;
    };
  });
 
  numberS.forEach(function (el) {
    el.oninput = function () {
      var number1 = parseFloat(numberS[0].value),
        number2 = parseFloat(numberS[1].value);
 
      if (number1 > number2) {
        var tmp = number1;
        numberS[0].value = number2;
        numberS[1].value = tmp;
      }
 
      rangeS[0].value = number1;
      rangeS[1].value = number2;
    };
  });
 })();

if($('.reveal').length){gsap.registerPlugin(ScrollTrigger);let revealContainers=document.querySelectorAll(".reveal");revealContainers.forEach((container)=>{let image=container.querySelector("img");let tl=gsap.timeline({scrollTrigger:{trigger:container,toggleActions:"play none none none"}});tl.set(container,{autoAlpha:1});tl.from(container,1.5,{xPercent:-100,ease:Power2.out});tl.from(image,1.5,{xPercent:100,scale:1.3,delay:-1.5,ease:Power2.out});});}




        //==== search area all ====
        document.addEventListener('DOMContentLoaded', function() {
          let searchToggle = document.getElementById('search-toggle');
          let searchBar = document.getElementById('search-bar');
          let searchIcon = document.getElementById('search-icon');
          let closeIcon = document.getElementById('close-icon');
        
          if (searchToggle && searchBar && searchIcon && closeIcon) {
            searchToggle.addEventListener('click', function() {
              // Toggle visibility of search bar
              searchBar.classList.toggle('active');
              searchBar.classList.toggle('hidden');
        
              // Toggle icons between search and close (X)
              searchToggle.classList.toggle('active');
              searchIcon.classList.toggle('hidden');
              closeIcon.classList.toggle('hidden');
        
              // Automatically focus on the search input when it's active
              if (searchBar.classList.contains('active')) {
                searchBar.focus();
              }
            });
          }
        });

        const listItems = document.querySelectorAll('.list-container li');
        const images = document.querySelectorAll('.image-container .image');

        listItems.forEach(item => {
            item.addEventListener('mouseover', () => {
                const targetImageId = item.getAttribute('data-image');
                images.forEach(div => {
                    div.classList.remove('active');
                    if (div.id === targetImageId) {
                        div.classList.add('active');
                    }
                });
            });
        });


        // preloader js =====

        /**
 * @function removeClass
 * @description remove class from Dom element/s
 * @param {Object} elem - Dom element
 * @param {String} className - class name to remove
 *
 **/
function removeClass(elem, className) {
  let l = elem.length;

  if (l == undefined) {
      _removeClass(elem, className);
  } else {
      let i = l - 1;

      while (i >= 0) {
          _removeClass(elem[i], className);
          i--;
      }
  }
}

/**
* @function _removeClass
* @description internal method to remove class from Dom element
* @param {Object} elem - Dom element
* @param {String} newClass - class name to remove
*
**/
function _removeClass(elem, newClass) {
  if (elem.classList) {
      elem.classList.remove(newClass);
  } else {
      let exp = '(^|\\b)' + newClass.split(' ').join('|') + '(\\b|$)';
      elem.className = elem.className.replace(new RegExp(exp, 'gi'), ' ');
  }
}

/**
* @function addClass
* @description add class to Dom element
* @param {Object} elem - Dom element
* @param {String} className - class name to add
*
**/
function addClass(elem, className) {
 let l = elem.length;

 if (l == undefined) {
    _addClass(elem, className);
 } else {
    let i = l - 1;

    while (i >= 0) {
       _addClass(elem[i], className);
       i--;
    }
 }
}


/**
* @function _addClass
* @description internal method add class to Dom element
* @param {Object} elem - Dom element
* @param {String} newClass - class name to add
*
**/
function _addClass(elem, newClass) {
 if (elem.classList) {
    elem.classList.add(newClass);
 } else {
    elem.className += ' ' + className;
 }
}

let loaderDashoffsetTotal = 502;
let preloader = document.querySelector('.preloader');
let preloaderOuter = preloader.querySelector('.outer');
let logo = preloader.querySelector('.logo');
let loaded = 0;
let total = 10;

function onProgress() {
let percentLoaded = Math.round(( loaded / total ) * 100);
      let calc = (loaderDashoffsetTotal /100);
      let percent = Math.round(calc * percentLoaded);
      let offset = loaderDashoffsetTotal - percent;
      preloaderOuter.style.strokeDashoffset =offset + 'px';
}

function init() {
 let startLength = loaderDashoffsetTotal + 'px';
 preloaderOuter.style.strokeDashoffset = startLength;
 preloaderOuter.style.opacity = 1;

 setTimeout(() => {
    let newLength = (loaderDashoffsetTotal) + 'px';
    preloaderOuter.style.strokeDashoffset = newLength;
    addClass(preloaderOuter, 'loading');
    loadImages();


 }, 500);
}
init();

function loadImages() {
  load();

}

function load() {
loaded++;
onProgress();

if(loaded == total){
  setTimeout(() => {
    onDone();
  }, 1000);
} else {
  setTimeout(() => {
    load();
  }, 100);
}

}

function onDone() {
 addClass(preloader, 'out');
 removeClass(logo, 'fade-in');
 addClass(logo, 'fade-out');

setTimeout(() => {
  loaded = 0;
  removeClass(preloader, 'out');
 addClass(logo, 'fade-in');
 removeClass(logo, 'fade-out');
  preloaderOuter.style.strokeDashoffset = loaderDashoffsetTotal + 'px';
 removeClass(preloaderOuter, 'loading');
 
    init();
  
}, 1000);
}