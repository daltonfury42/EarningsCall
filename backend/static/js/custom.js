function createPara(splitId) {

    if (splitId == 'f100000') {
        return createQnAPara();
    }

    var a = document.createElement("a");
    var dataPoint = dataJson[splitId];
    a.setAttribute("class", 'list-group-item list-group-item-action flex-column align-items-start ' + dataPoint['emotion'] + ' ' + dataPoint['topic']);
    a.setAttribute("id", splitId);
    a.setAttribute("href", "#");



    var div1 = document.createElement("div");
    div1.setAttribute("class", "d-flex w-100 justify-content-between");

    var speaker = document.createElement("h5");
    speaker.setAttribute("class", "mb-1");
    speaker.setAttribute("id", "spreaker");

    speaker.innerHTML = dataPoint['speaker'];

    div1.appendChild(speaker);

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

function createQnAPara() {
    var a = document.createElement('a');
    a.setAttribute('class', "card text-center");

    var divCard = document.createElement('div');
    divCard.setAttribute('class', 'card-body');

    var text = document.createElement('p');
    text.innerHTML = 'Question and Answer Session';

    divCard.appendChild(text);

    a.appendChild(divCard);

    return a;
}