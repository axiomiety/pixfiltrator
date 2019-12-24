'use strict';

const convertHexStringToRgba = (str) => {
  const decimalValue = parseInt(str,16);
  const paletteWidth = 47;
  let val = decimalValue*paletteWidth;
  const color = {r: 0, g: 0, b: 0};
  if (val > 255*2) {
    color.b = Math.round(val - 255*2);
    color.r = color.g = 255;
  } else if (val > 255) {
    color.g = Math.round(val - 255);
    color.r = 255;
  } else {
    color.r = Math.round(val);
  }    
  return `rgba(${color.r}, ${color.g}, ${color.b}, 1)`;
  //return '#FF0000';
}
  
const formatByteStringToHexNumbersArray = (str) => {
  const ret = [];
  if (str.length == 1) {
    ret.push('0', str);
  } else {
    ret.push(str[0], str[1]);
  }
  return ret;
}

const clearCanvas = (ctx) => {
  ctx.beginPath();
  ctx.rect(0, 0, ctx.canvas.width, ctx.canvas.height);
  ctx.fillStyle = '#000000';//convertHexStringToRgb("0"); //"#FF0000";
  ctx.fill();
  ctx.closePath();
};

const drawSquare = (hexStr, idx, ctx, width) => {
  const canvas_width = ctx.canvas.width;
  const startX = idx*width % canvas_width;
  const startY = Math.floor(idx*width/canvas_width)*width;
 
  ctx.beginPath();
  ctx.rect(startX, startY, width, width);
  ctx.fillStyle = convertHexStringToRgba(hexStr);
  ctx.fill();
  ctx.closePath();
}

const getNumSquaresPerPage = (ctx, sqWidth, withMeta=true) => {
  const w = ctx.canvas.width;
  const h = ctx.canvas.height;

  const metaData = withMeta ? w*sqWidth : 0;
  return (w*h-metaData)/sqWidth/sqWidth;
};

const calcNumPages = (numHalfBytes, ctx, sqWidth) => {
  const numSquaresPerPage = getNumSquaresPerPage(ctx, sqWidth);
  return Math.ceil(numHalfBytes / numSquaresPerPage);
};

const updateNumPages = () => {
  const elem = document.getElementById("pageTracker");
  elem.innerHTML = `${offset+1}/${numPages}`;
}

const handleFiles = (files) => {
  if (!files.length) {
    fileList.innerHTML = "<p>No files selected!</p>";
  } else {
    fileList.innerHTML = "";
    const list = document.createElement("ul");
    fileList.appendChild(list);
    // technically there's only one file, but heh...
    for (let i = 0; i < files.length; i++) {
      const li = document.createElement("li");
      list.appendChild(li);
      
      const img = document.createElement("img");
      img.src = window.URL.createObjectURL(files[i]);
      img.height = 60;
      img.onload = function() {
        window.URL.revokeObjectURL(this.src);
      }
      li.appendChild(img);
      const info = document.createElement("span");
      info.innerHTML = files[i].name + ": " + files[i].size + " bytes";
      li.appendChild(info);

      foo(files[i]);
    }
  }
}

async function digestMessage(msgUint8) {
  const hashBuffer = await crypto.subtle.digest('SHA-256', msgUint8);           // hash the message
  const hashArray = Array.from(new Uint8Array(hashBuffer));                     // convert buffer to byte array
  const hashHex = hashArray.map(b => b.toString(16).padStart(2, '0')).join(''); // convert bytes to hex string
  return hashHex;
}

//const digestHex = await digestMessage(text);

exports.convertHexStringToRgba = convertHexStringToRgba;
exports.formatByteStringToHexNumbersArray = formatByteStringToHexNumbersArray;
exports.getNumSquaresPerPage = getNumSquaresPerPage;