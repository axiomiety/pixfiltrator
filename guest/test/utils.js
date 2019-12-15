const wish = require('wish');
const assert = require('assert');
//import convertHexStringToRgb from '../index.js';
const { convertHexStringToRgba, formatByteStringToHexNumbersArray } = require('../lib.js');

describe('utilities', function() {
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

    it('converts a string representing a byte into its individual hex components, 0-padded', function() {
        let ret = formatByteStringToHexNumbersArray('02');
        assert.deepEqual( ['0', '2'], ret );
        ret = formatByteStringToHexNumbersArray('1a');
        assert.deepEqual( ['1', 'a'], ret );
    });
});