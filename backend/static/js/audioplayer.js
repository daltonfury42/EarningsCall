/**
 * Create a WaveSurfer instance.
 */
var wavesurfer;
var currentSplitId;
var emotionColor = {"Happy": "rgba(0, 255, 0, 0.1)",
                    "Sad": "rgba(255, 0, 0, 0.1)",
                    "Strategical": "rgba(0, 0, 255, 0.1)",
                    "Analytical": "rgba(255, 255, 0, 0.1)",
                    "Neutral": "rgb(211, 211, 211)"};

var emotionCount = {"Happy": 0,
                    "Sad": 0,
                    "Neutral": 0,
                    "Strategical": 0,
                    "Analytical": 0};
/**
 * Init & load.
 */
document.addEventListener('DOMContentLoaded', function() {
    // Init wavesurfer
    wavesurfer = WaveSurfer.create({
        container: '#waveform',
        height: 100,
        pixelRatio: 1,
        scrollParent: true,
        normalize: true,
        minimap: true,
        backend: 'MediaElement',
        fillParent: true,
        plugins: [
            WaveSurfer.regions.create(),
            WaveSurfer.minimap.create({
                height: 30,
                waveColor: '#ddd',
                progressColor: '#999',
                cursorColor: '#999'
            }),
            WaveSurfer.timeline.create({
                container: '#wave-timeline'
            })
        ]
    });

    wavesurfer.load("/static/mp3/" + callId + ".mp3");

    wavesurfer.on('ready', function() {
        loadRegions();
        initHistoryPane();
    });

    wavesurfer.on('region-click', function(region, e) {
        e.stopPropagation();
        // Play on click, loop on shift click
        e.shiftKey ? region.playLoop() : region.play();
    });
    wavesurfer.on('region-in', showNote);

    wavesurfer.on('region-play', function(region) {
        region.once('out', function() {
            wavesurfer.play(region.start);
            wavesurfer.pause();
        });
    });

    /* Toggle play/pause buttons. */
    var playButton = document.querySelector('#play');
    var pauseButton = document.querySelector('#pause');
    wavesurfer.on('play', function() {
        playButton.style.display = 'none';
        pauseButton.style.display = '';
    });
    wavesurfer.on('pause', function() {
        playButton.style.display = '';
        pauseButton.style.display = 'none';
    });
});

/*
 * Display annotation.
 */
function showNote(region) {
    if (!showNote.el) {
        showNote.el = document.querySelector('#subtitle');
    }
    showNote.el.textContent = region.id;
    currentSplitId = region.id;

    updateHistoryPane(currentSplitId);

    var cardDisplayDiv = document.getElementById("subtitleCard");
    while (cardDisplayDiv.firstChild) {
        cardDisplayDiv.removeChild(cardDisplayDiv.firstChild);
    }

    cardDisplayDiv.appendChild(createPara(region.id))

}

function updateHistoryPane(currentSplitId) {
    for (var emotion in emotionCount) {
        emotionCount[emotion] = 0;
    }

    for (var splitId in dataJson) {
        var dataPoint = dataJson[splitId];
        var historyPaneElem = document.getElementById('history-pane-' + splitId);
        if (Number(splitId.substr(1)) <= Number(currentSplitId.substr(1))) {

            emotionCount[dataPoint.emotion] += 1;

            if(historyPaneElem.classList.contains('disabled')) {
                historyPaneElem.classList.remove('disabled');
                historyPaneElem.setAttribute('style', 'background-color: ' + emotionColor[dataPoint.emotion]);

                if (document.getElementById('history-pane-emotion-' + splitId) == undefined) {
                    var emotionSpanElem = document.createElement('span');
                    emotionSpanElem.setAttribute('class', 'badge badge-primary');
                    emotionSpanElem.setAttribute('id', 'history-pane-emotion-' + splitId);
                    emotionSpanElem.innerHTML = dataPoint.emotion;
                    historyPaneElem.appendChild(emotionSpanElem);
                }
            }
        } else {


            var emotionSpanElem = document.getElementById('history-pane-emotion-' + splitId);
            if (emotionSpanElem != null) {
                emotionSpanElem.parentNode.removeChild(emotionSpanElem);
                historyPaneElem.className += ' disabled';
                historyPaneElem.removeAttribute('style');
            }
        }
    }

    $('#history-pane-' + currentSplitId).scrollintoview();

    for (var emotion in emotionCount) {
        var emotionCountElem = document.getElementById(emotion + '-count');
        emotionCountElem.innerHTML = emotionCount[emotion];
    }
//
//    var speakerIconOld = document.getElementById('speaker-icon');
//    if (speakerIconOld) {
//        speakerIconOld.parentNode.removeChild(speakerIconOld);
//    }
//
//    if (null === document.getElementById('speaker-icon')) {
//        var speakerIcon = document.createElement('i');
//        speakerIcon.setAttribute('class', 'material-icons');
//        speakerIcon.innerHTML = 'record_voice_over';
//
//        var historyPaneElemCurrent = document.getElementById('history-pane-' + currentSplitId);
//        historyPaneElemCurrent.firstChild.appendChild(speakerIcon);
//    }

}

function loadRegions() {

    var callEnd = 0.0;

    for (var splitId in dataJson) {
        var dataPoint = dataJson[splitId]
        var region = {  id: splitId,
                        start: dataPoint.startTime,
                        end: dataPoint.endTime,
                        drag: false,
                        resize: false,
                    };

        if (dataPoint.emotion == "Happy") {
            region.color = emotionColor["Happy"];
        } else if (dataPoint.emotion == "Sad") {
            region.color = emotionColor["Sad"];
        } else if (dataPoint.emotion == "Strategical") {
            region.color = emotionColor["Strategical"];
        } else if (dataPoint.emotion == "Analytical") {
            region.color = emotionColor["Analytical"];
        }

        wavesurfer.addRegion(region);
        if (dataPoint.endTime > callEnd) {
            callEnd = dataPoint.endTime;
        }
    }

    var faqRegion = {
        id: 'f100000',
        start: callEnd,
        end: wavesurfer.getDuration(),
        drag: false,
        resize: false,
        color: "rgba(255,255,255,1)",
    };

    wavesurfer.addRegion(faqRegion);


}

function initHistoryPane() {
    var historyPaneElem = document.getElementById('historyPane');
    var dataPoint;
    for (var splitId in dataJson) {
        dataPoint = dataJson[splitId];

        historyPaneElem.appendChild(createHistoryElem(splitId, dataPoint.startTime, dataPoint.speaker));
    }

    var minutes = Math.floor(dataPoint.endTime / 60);
    var seconds = Math.round(dataPoint.endTime - minutes * 60);
    historyPaneElem.appendChild(createHistoryElem('faq', dataPoint.endTime, 'QnA'));

}

function createHistoryElem(splitId, time, speaker) {

        var minutes = Math.floor(time / 60);
        var seconds = Math.round(time - minutes * 60);

        var elem = document.createElement('a');
        elem.setAttribute('class', 'list-group-item disabled list-group-item-action d-flex justify-content-between align-items-center');
        elem.setAttribute('id', 'history-pane-' + splitId);
        elem.setAttribute('href', 'javascript:wavesurfer.play(' + time + ');')

        var leftDiv = document.createElement('div');

        var text = document.createElement('p');
        text.innerHTML = '(' + pad(minutes, 2) + ':' + pad(seconds, 2) + ')  ' + speaker;
        leftDiv.appendChild(text);

        elem.appendChild(leftDiv);

        return elem;
}

var wavesurfer = window.wavesurfer;

var GLOBAL_ACTIONS = {
    play: function() {
        wavesurfer.playPause();
    },

    back: function() {
        currentSplitId = 'f' + pad(Number(currentSplitId.substr(1))-1, 6);

        wavesurfer.play(dataJson[currentSplitId].start);
    },

    forth: function() {
        currentSplitId = 'f' + pad(Number(currentSplitId.substr(1))+1, 6);

        if (currentSplitId == 'f000000') {
            return;
        }

        if (dataJson[currentSplitId] == undefined) {
            // Display FAQ card.
        }

        wavesurfer.play(dataJson[currentSplitId].start);
    },

    'toggle-mute': function() {
        wavesurfer.toggleMute();
    }
};

// Bind actions to buttons and keypresses
document.addEventListener('DOMContentLoaded', function() {
    document.addEventListener('keydown', function(e) {
        var map = {
            32: 'play', // space
            37: 'back', // left
            39: 'forth' // right
        };
        var action = map[e.keyCode];
        if (action in GLOBAL_ACTIONS) {
            if (document == e.target || document.body == e.target) {
                e.preventDefault();
            }
            GLOBAL_ACTIONS[action](e);
        }
    });

    [].forEach.call(document.querySelectorAll('[data-action]'), function(el) {
        el.addEventListener('click', function(e) {
            var action = e.currentTarget.dataset.action;
            if (action in GLOBAL_ACTIONS) {
                e.preventDefault();
                GLOBAL_ACTIONS[action](e);
            }
        });
    });
});

function pad(number, length) {

    var str = '' + number;
    while (str.length < length) {
        str = '0' + str;
    }

    return str;

}