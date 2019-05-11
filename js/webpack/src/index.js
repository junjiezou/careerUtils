import _ from 'lodash';
import './style.css';
import Icon from './webpack.png';
import printMe from './print.js';
import mie from './mie.js';


function component() {
    var element = document.createElement('div');

    // Lodash, now imported by this script
    element.innerHTML = _.join(['Hello', 'webpack'], ' ');
    element.classList.add('hello');

    var myIcon = new Image();
    myIcon.src = Icon;
    element.appendChild(myIcon);
    
    var btn = document.createElement('button');
    btn.innerHTML = 'Click me and check the console!';
    btn.onclick = printMe;
    element.appendChild(btn);

    var mieBtn = document.createElement('button');
    mieBtn.innerHTML = 'Click me and check the console!';
    mieBtn.onclick = mie;
    element.appendChild(mieBtn);

    return element;
  }

  document.body.appendChild(component());

// if (module.hot) {
//   module.hot.accept('./print.js', function() {
//     console.log('Accepting the updated printMe module!');
//     printMe();
//   })
// }