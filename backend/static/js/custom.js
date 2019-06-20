var audioPlayer = document.getElementById("audiofile");
var currentFocus = undefined

function focusOn(splitId, triggerAudio) {

    if (currentFocus != splitId)
        if (currentFocus != undefined)
            unFocus(currentFocus);
    currentFocus = splitId;
    document.getElementById(splitId + '-emotion').style.visibility = "visible";
    document.getElementById(splitId + '-audioImage').style.visibility = "visible";

    var elem = document.getElementById(splitId);
    elem.style.visibility = "visible"
    elem.classList.add("list-group-item-dark");

    if (triggerAudio) {
        audioPlayer.currentTime = dataJson[splitId]['start'];
        audioPlayer.play();
    }
}

function unFocus(splitId) {
    document.getElementById(splitId + '-audioImage').style.visibility = "hidden";
    var elem = document.getElementById(splitId);
    elem.classList.remove("list-group-item-dark");
}

function createPara(splitId) {
    var a = document.createElement("a");
    var dataPoint = dataJson[splitId];
    a.setAttribute("class", 'list-group-item list-group-item-action flex-column align-items-start ' + dataPoint['emotion'] + ' ' + dataPoint['topic']);
    a.setAttribute("id", splitId);
    a.setAttribute("href", "javascript:focusOn('" + splitId + "', true);");

    var div1 = document.createElement("div");
    div1.setAttribute("class", "d-flex w-100 justify-content-between");

    var speaker = document.createElement("h5");
    speaker.setAttribute("class", "mb-1");
    speaker.setAttribute("id", "spreaker");

    speaker.innerHTML = dataPoint['speaker'];

    div1.appendChild(speaker);

    var speakerIcon = document.createElement("img");
    speakerIcon.setAttribute("src", "/static/img/speaker.png");
    speakerIcon.setAttribute("style", "visibility:hidden;");
    speakerIcon.setAttribute("id", splitId + "-audioImage");

    div1.appendChild(speakerIcon);

    a.appendChild(div1);
    a.appendChild(document.createElement("br"));

    var mainText = document.createElement("p");
    mainText.setAttribute("class", "md-1");
    mainText.innerHTML = dataPoint['text'];
    a.appendChild(mainText);

    var div2 = document.createElement("div");
    div2.setAttribute("class", "d-flex justify-content-between align-items-center");

    var div21 = document.createElement("div");
    var span1 = document.createElement("span");
    span1.setAttribute("class", "badge badge-primary");
    span1.setAttribute("id", splitId + "-emotion");
    span1.innerHTML = dataPoint['emotion'];

    div21.appendChild(span1);

    if (dataPoint['topic'] != 'Notopic') {
        var span2 = document.createElement("span");
        span2.setAttribute("class", "badge badge-pill badge-success");
        span2.setAttribute("id", splitId + "-topic");
        span2.innerHTML = dataPoint['topic'];

        div21.appendChild(span2);
    }

    div2.appendChild(div21);

    div22 = document.createElement('div');
    for (var tagI in dataPoint['tags']) {
        var tagSpan = document.createElement('span');
        tagSpan.setAttribute('class', 'badge badge-secondary badge-pill');
        tagSpan.innerHTML = dataPoint['tags'][tagI];
        div22.appendChild(tagSpan);
    }
    div2.appendChild(div22);

    div2.appendChild(div22);

    a.appendChild(div2);

    return a;


}

(function (win, doc) {

    var subtitles = doc.getElementById("subtitles");

    audioPlayer.addEventListener("timeupdate", function (e) {

        var currentSplitId = undefined;
        for (var splitId in dataJson) {
            if (dataJson[splitId]["startTime"] <= audioPlayer.currentTime && dataJson[splitId]["isVisible"] === undefined) {
                var para = createPara(splitId);
                dataJson[splitId]["isVisible"] = true;
                subtitles.appendChild(para);
                    subtitles.scrollTop = subtitles.scrollHeight;
            }
        }

        if (currentSplitId) {
            focusOn(element.splitId, false);
        }
        });
}(window, document));

function filterSelection(filterClass) {
    rows = document.getElementsByClassName("filterable")

    for (i = 0; i < rows.length; i++)
    {
        row = rows[i];
        if (filterClass == "All" && row.classList.contains('All-filter-display'))
            row.classList.remove("d-none");
        else if (row.classList.contains(filterClass))
            row.classList.remove("d-none");
        else
            row.classList.add("d-none");
    }
}