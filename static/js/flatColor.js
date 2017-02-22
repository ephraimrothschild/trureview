(function($) {
    function generateCustomFlatColorWithOrder(num, colors, startIndex) {
        //StartIndex is the number that num should start at. If there is a value here, startIndex number of
        //colors will be skipped. The default is set to 1 because 0 causes an error.
        if (startIndex == null) {
            startIndex = 1;
        }
        var colorBase = 256;
        var red = 0;
        var green = 0;
        var blue = 0;
        num = Math.round(num);
        num = num + startIndex;
        if (num != null) {
            red = (num*colors[0]) % 256;
            green = (num*colors[1]) % 256;
            blue = (num*colors[2]) % 256;
        }
        var redString = Math.round((red + colorBase) / 2).toString();
        var greenString = Math.round((green + colorBase) / 2).toString();
        var blueString = Math.round((blue + colorBase) / 2).toString();
        return "rgb("+redString+", "+greenString+", "+blueString+")";
    }

    function generateFlatColorWithOrder(num) {
        //Possible color values to use. Uncomment whichever you prefer.
        var colors = [32, 12, 102];
        // var colors = [243, 721, 423];
        // var colors = [768, 528, 721];
        //var colors = [391, 837, 716];
        //var colors = [224, 296, 709];
        //var colors = [268, 389, 404];
        //var colors = [480, 501, 390];
        //var colors = [340, 49, 644];
        // var colors = [591, 741, 672];
        // var colors = [119, 998, 115];
        // var colors = [293, 746, 950];
        //var colors = [417, 124, 707];
        // var colors = [444, 461, 677];
        // var colors = [333, 230, 513];
        // var colors = [-1.02, -1.25, 0.1];

        return generateCustomFlatColorWithOrder(num, colors, 2);
    }

    //Nothinig is done with this. Here for the future.
    function generateRandomFlatColor() {
        return generateFlatColorWithOrder(Math.round(Math.random()*1000));
    }

    //Gives each div with the class 'flat-color-gen' a unique flat background-color.
    $('.flat-color-gen').each(function(i, obj) {
        //console.log(generateFlatColorWithOrder(i));
        $(this).css("background-color",generateFlatColorWithOrder(i).toString());
    });
})(window.jQuery);