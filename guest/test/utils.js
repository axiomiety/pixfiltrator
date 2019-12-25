const wish = require('wish');
const assert = require('assert');
//import convertHexStringToRgb from '../index.js';
const { convertHexStringToRgba,
        formatByteStringToHexNumbersArray,
        getNumSquaresPerPage } = require('../lib.js');

describe('Utilities', function() {
    it('converts a hexadecimal string (0-f) to an RGB triplet', function() {
        let ret = convertHexStringToRgba('0');
        wish( 'rgba(0, 0, 0, 1)' === ret);
        ret = convertHexStringToRgba('1');
        wish( 'rgba(47, 0, 0, 1)' === ret);
        ret = convertHexStringToRgba('6');
        wish( 'rgba(255, 27, 0, 1)' === ret);
        ret = convertHexStringToRgba('f');
        wish( 'rgba(255, 255, 195, 1)' === ret);
    });

    it('calculates the number of squares per page, with/without metadata', function() {
        /*  if we have a width of 200 and a height of 100,
            and the area of each square is 10x10, we would
            expect 200 squares
        */
       const ctx = {
        canvas: {
            width: 200,
            height: 100
        }
       };
       const sqWidth = 10;
       wish( 200 === getNumSquaresPerPage(ctx, sqWidth, false) );

       /*   if we add meta-data, that will occupy the first row
            that's 10x200 pixels for a total of 20 squares
       */
       wish( 180 === getNumSquaresPerPage(ctx, sqWidth, true) );
    });
});