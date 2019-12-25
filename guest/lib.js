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
  
const clearCanvas = (ctx) => {
  ctx.beginPath();
  ctx.rect(0, 0, ctx.canvas.width, ctx.canvas.height);
  ctx.fillStyle = '#000000';//convertHexStringToRgb("0"); //"#FF0000";
  ctx.fill();
  ctx.closePath();
};

const drawSquare = (hexStr, idx, ctx, sqWidth) => {
  const canvas_width = ctx.canvas.width;
  const startX = idx*sqWidth % canvas_width;
  const startY = Math.floor(idx*sqWidth/canvas_width)*sqWidth;
 
  ctx.beginPath();
  ctx.rect(startX, startY, sqWidth, sqWidth);
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

const calcNumPages = (numHalfBytes, numSquaresPerPage) => {
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

const digestMessage = async (algo, msgUint8) => {
  const hashBuffer = await crypto.subtle.digest(algo, msgUint8);           // hash the message
  const hashArray = Array.from(new Uint8Array(hashBuffer));                     // convert buffer to byte array
  const hashHex = hashArray.map(b => b.toString(16).padStart(2, '0')).join(''); // convert bytes to hex string
  return hashHex;
}

const drawMeta = (ctx, sqWidth, meta) => {
  const startY = ctx.canvas.height - sqWidth;
  for (let i=0; i<meta.length; i++) {
    const startX = i*sqWidth;
    ctx.beginPath();
    ctx.rect(startX, startY, sqWidth, sqWidth);
    ctx.fillStyle = convertHexStringToRgba(meta[i]);
    ctx.fill();
    ctx.closePath();
  }
};

const addMetaData = (ctx, sqWidth, hexArray, offset, numSquaresPerPage, numHalfBytesOnPage, numPages) => {
  /*  metadata format is as follows
       2 bytes for the page number
       2 bytes for the total number of pages
       2 bytes for the number of squares on this page
      20 bytes for the SHA-1 of the chunk displayed (excludes metadata)
      --
      26 bytes, which is 52 squares

      this means we expect a width of at least 52*sqWidth pixels on the canvas
  */

  const currOffset = offset*numSquaresPerPage;
  const data = hexArray.slice(currOffset, currOffset + numHalfBytesOnPage);
  const array = new Uint8Array(data);
  digestMessage('SHA-1', array).then(digest => {
    console.log(`SHA-1 of block ${offset}: ${digest}`);
    const pageNum = offset.toString(16).padStart(4, '0');
    const totNumPages = numPages.toString(16).padStart(4, '0');
    const sqOnPage = numSquaresPerPage.toString(16).padStart(4,'0');
    const meta = pageNum + totNumPages + sqOnPage + digest;
    drawMeta(ctx, sqWidth, meta);
  });
}

const draw = (ctx, offset, arr, numSquaresPerPage, numPages) => {
  const canvasWidth = ctx.canvas.width;
  const canvasHeight = ctx.canvas.height;
  clearCanvas(ctx);
  const currOffset = offset*numSquaresPerPage;
  const nextOffset = (offset+1)*numSquaresPerPage;
  const numHalfBytesOnPage = hexArray.length - currOffset;

  console.log(`pages: ${offset}/${numPages}`);
  console.log(`offsets - current: ${currOffset}, next: ${nextOffset}`);
  console.log(`number of half-bytes on page: ${numHalfBytesOnPage}`);

  // 'draw' the squares
  for(let j=currOffset; (j<hexArray.length) && (j<nextOffset); j++) {
      drawSquare(hexArray[j], j%numSquaresPerPage, ctx, sqWidth);
  }
  // add the metadata
  addMetaData(ctx, sqWidth, hexArray, offset, numSquaresPerPage, numHalfBytesOnPage, numPages);
};


//const digestHex = await digestMessage(text);

exports.convertHexStringToRgba = convertHexStringToRgba;
exports.getNumSquaresPerPage = getNumSquaresPerPage;