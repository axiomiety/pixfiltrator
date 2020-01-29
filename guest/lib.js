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
  
const clearCanvas = (ctx_) => {
  ctx_ = ctx_ || ctx;
  ctx_.beginPath();
  ctx_.rect(0, 0, ctx_.canvas.width, ctx_.canvas.height);
  ctx_.fillStyle = '#000000';//convertHexStringToRgb("0"); //"#FF0000";
  ctx_.fill();
  ctx_.closePath();
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
  elem.innerHTML = `<h1>page ${offset+1}/${numPages}</h1>`;
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
      const li_fname = document.createElement("li");
      list.appendChild(li_fname);      
      const info = document.createElement("span");
      info.innerHTML = files[i].name;
      li_fname.appendChild(info);
      const li_size = document.createElement("li");
      list.appendChild(li_size);      
      const sz = document.createElement("span");
      sz.innerHTML = files[i].size + " bytes";
      li_size.appendChild(sz);
      
      kickoff(files[i]);
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

const fromHexString = hexString =>
  new Uint8Array(hexString.match(/.{1,2}/g).map(byte => parseInt(byte, 16)));

const addMetaData = (ctx, sqWidth, hexArray, offset, numSquaresPerPage, numHalfBytesOnPage, numPages, playNext, refreshSpeed) => {
  /*  metadata format is as follows
       2 bytes for the page number
       2 bytes for the total number of pages
       2 bytes for the number of bytes on this page
      20 bytes for the SHA-1 of the chunk displayed (excludes metadata)
       4 bytes for 0xFEEDC0DE - metadata has successfully been added
      --
      30 bytes, which is 60 squares

      this means we expect a width of at least 60*sqWidth pixels on the canvas
  */

  const currOffset = offset*numSquaresPerPage;
  const data = hexArray.slice(currOffset, currOffset + numHalfBytesOnPage);
  // to compute SHA1 'properly', we need to convert our half-bytes back into bytes
  const array = new Uint8Array(fromHexString(data.join('')));
  digestMessage('SHA-1', array).then(digest => {
    console.log(`SHA-1 of block ${offset}: ${digest}`);
    // +1 because we start at offset 0 for the first page
    const pageNum = (offset+1).toString(16).padStart(4, '0');
    const totNumPages = numPages.toString(16).padStart(4, '0');
    const numBytesOnPage = (numHalfBytesOnPage/2).toString(16).padStart(4,'0');
    const meta = pageNum + totNumPages + numBytesOnPage + digest + 'feedc0de';
    //console.log(meta);
    drawMeta(ctx, sqWidth, meta);
    if (playNext === true) {
      setTimeout(next, refreshSpeed, offset < numPages);
    }
  });
}

const draw = (ctx, offset, hexArray, numSquaresPerPage, numPages, playNext, refreshSpeed) => {
  const canvasWidth = ctx.canvas.width;
  const canvasHeight = ctx.canvas.height;
  clearCanvas(ctx);
  const currOffset = offset*numSquaresPerPage;
  const nextOffset = (offset+1)*numSquaresPerPage;
  const numHalfBytesOnPage = Math.min(hexArray.length,nextOffset) - currOffset;

  console.log(`pages: ${offset+1}/${numPages}`);
  console.log(`offsets - current: ${currOffset}, next: ${nextOffset}`);
  console.log(`number of half-bytes on page: ${numHalfBytesOnPage}`);
  
  // 'draw' the squares
  for(let j=currOffset; (j<hexArray.length) && (j<nextOffset); j++) {
      drawSquare(hexArray[j], j%numSquaresPerPage, ctx, sqWidth);
  }
  // add the metadata
  addMetaData(ctx, sqWidth, hexArray, offset, numSquaresPerPage, numHalfBytesOnPage, numPages, playNext, refreshSpeed);
};


//const digestHex = await digestMessage(text);

exports.convertHexStringToRgba = convertHexStringToRgba;
exports.getNumSquaresPerPage = getNumSquaresPerPage;