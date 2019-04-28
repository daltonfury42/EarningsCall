var EPPZScrollTo =
{
    /**
     * Helpers.
     */
    documentVerticalScrollPosition: function () {
        if (self.pageYOffset) return self.pageYOffset; // Firefox, Chrome, Opera, Safari.
        if (document.documentElement && document.documentElement.scrollTop) return document.documentElement.scrollTop; // Internet Explorer 6 (standards mode).
        if (document.body.scrollTop) return document.body.scrollTop; // Internet Explorer 6, 7 and 8.
        return 0; // None of the above.
    },

    viewportHeight: function () { return (document.compatMode === "CSS1Compat") ? document.documentElement.clientHeight : document.body.clientHeight; },

    documentHeight: function () { return (document.height !== undefined) ? document.height : document.body.offsetHeight; },

    documentMaximumScrollPosition: function () { return this.documentHeight() - this.viewportHeight(); },

    elementVerticalClientPositionById: function (id) {
        var element = document.getElementById(id);
        var rectangle = element.getBoundingClientRect();
        return rectangle.top;
    },

    /**
     * Animation tick.
     */
    scrollVerticalTickToPosition: function (currentPosition, targetPosition) {
        var filter = 0.2;
        var fps = 60;
        var difference = parseFloat(targetPosition) - parseFloat(currentPosition);

        // Snap, then stop if arrived.
        var arrived = (Math.abs(difference) <= 0.5);
        if (arrived) {
            // Apply target.
            scrollTo(0.0, targetPosition);
            return;
        }

        // Filtered position.
        currentPosition = (parseFloat(currentPosition) * (1.0 - filter)) + (parseFloat(targetPosition) * filter);

        // Apply target.
        scrollTo(0.0, Math.round(currentPosition));

        // Schedule next tick.
        setTimeout("EPPZScrollTo.scrollVerticalTickToPosition(" + currentPosition + ", " + targetPosition + ")", (1000 / fps));
    },

    /**
     * For public use.
     *
     * @param id The id of the element to scroll to.
     * @param padding Top padding to apply above element.
     */
    scrollVerticalToElementById: function (id, padding) {
        var element = document.getElementById(id);
        if (element == null) {
            console.warn('Cannot find element with id \'' + id + '\'.');
            return;
        }

        var targetPosition = this.documentVerticalScrollPosition() + this.elementVerticalClientPositionById(id) - padding;
        var currentPosition = this.documentVerticalScrollPosition();

        // Clamp.
        var maximumScrollPosition = this.documentMaximumScrollPosition();
        if (targetPosition > maximumScrollPosition) targetPosition = maximumScrollPosition;

        // Start animation.
        this.scrollVerticalTickToPosition(currentPosition, targetPosition);
    }
};

var audioPlayer = document.getElementById("audiofile");
var currentFocus = undefined

function focusOn(splitId, triggerAudio) {

    if (currentFocus != splitId)
        if (currentFocus != undefined)
            unFocus(currentFocus);
    currentFocus = splitId;
    console.log('splitID:');
    console.log(splitId)
    document.getElementById(splitId + '-emotion').style.visibility = "visible";
    document.getElementById(splitId + '-audioImage').style.visibility = "visible";

    var elem = document.getElementById(splitId);
    var index = parseInt(splitId.slice(1, splitId.length)) - 1
    timeData = syncData[index]

    elem.classList.add("list-group-item-dark");

    if (triggerAudio) {
        audioPlayer.currentTime = timeData['start'];
        audioPlayer.play();
    } else {
        EPPZScrollTo.scrollVerticalToElementById(splitId, 90);
    }
}

function unFocus(splitId) {
    document.getElementById(splitId + '-audioImage').style.visibility = "hidden";
    var elem = document.getElementById(splitId);
    elem.classList.remove("list-group-item-dark");
}

(function (win, doc) {

    var subtitles = doc.getElementById("subtitles");

    audioPlayer.addEventListener("timeupdate", function (e) {

        syncData.forEach(function (element, index, array) {
            if (audioPlayer.currentTime >= element.start && audioPlayer.currentTime <= element.end && !subtitles.children[index].classList.contains("list-group-item-dark")) {
                console.log(element.splitId)
                focusOn(element.splitId, false);
            }
        });
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