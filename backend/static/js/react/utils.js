function generateSplitId(number) {
    var str = pad(number, 6)

    return 'f' + str;
}

function pad(number, length) {

    var str = '' + number;
    while (str.length < length) {
        str = '0' + str;
    }

    return str;

}


var emotionColor = {"Happy": "rgba(0, 255, 0, 0.1)",
                    "Sad": "rgba(255, 0, 0, 0.1)",
                    "Strategical": "rgba(0, 0, 255, 0.1)",
                    "Analytical": "rgba(255, 255, 0, 0.1)",
                    "Neutral": "rgb(211, 211, 211)"};