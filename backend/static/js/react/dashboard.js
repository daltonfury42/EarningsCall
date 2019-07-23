class DashBoard extends React.Component {
    constructor(props) {
        super(props);
        this.state = { currentSplitId: null };
        this.dataJson = props.dataJson;
        this.callId = props.callId;
    }

    componentDidMount() {
        this.initilizeWavesurfer();
        this.updateScroll();
    }

    componentDidUpdate() {
        this.updateScroll();
    }

    updateScroll(){
        var element = document.getElementById("historyPane");
        element.scrollTop = element.scrollHeight;
    }

    render() {
        return (
            <div className="row">
                <div className="col-md-1"></div>
                <div className="col-md-3">
                    <div className="container">
                        <div className="row">
                            <div className="list-group scrollable w-100" id="historyPane">
                                <window.HistoryPane 
                                    dataJson={this.dataJson} 
                                    currentSplitId={this.state.currentSplitId}
                                />
                            </div>
                        </div>
                    </div>
                </div>

                <div className="col-md-7">
                    <div className="row">
                        <div id="demo" className="w-100">

                            <div id="wave-timeline"></div>

                            <div id="waveform">
                                
                            </div>

                            <div className="row" style={{margin: '45px 0'}}>
                                <div className="col-sm-8">
                                        <button type="button" className="btn btn-secondary" data-toggle="modal" data-target="#highlightsModal">
                                        Highlights
                                        </button>
                                        <div id="like_button_container"></div>
                                </div>

                                <div className="col-sm-2">
                                    <div className="btn-group">
                                        <button className="btn btn-secondary btn-block" data-action="play">
                                            <span id="play">
                                                <i className="material-icons">play_arrow</i>
                                            </span>

                                            <span id="pause" style={{display: "none"}}>
                                                <i className="material-icons">pause</i>
                                            </span>
                                        </button>
                                    </div>
                                </div>
                            </div>
                            <div className="row">
                                <div className="col-md-8">
                                    <div id="subtitleCard" className="w-100">
                                        <window.Subtitle 
                                            currentSplitId={this.state.currentSplitId}
                                            dataPoint={this.props.dataJson[this.state.currentSplitId]}
                                        />
                                    </div>
                                </div>
                                <div className="col-md-4">
                                    <window.LiveCounter 
                                        currentSplitId={this.state.currentSplitId}
                                        dataJson={this.dataJson} 
                                    />
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
                <div className="col-md-1"></div>
            </div>
        );
    }

    loadRegions() {
        var callEnd = 0.0;

        for (var splitId in this.dataJson) {
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

            this.wavesurfer.addRegion(region);
            if (dataPoint.endTime > callEnd) {
                callEnd = dataPoint.endTime;
            }
        }
    }


    initilizeWavesurfer() {

        this.wavesurfer = WaveSurfer.create({
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
    
        this.wavesurfer.load("/static/mp3/" + this.callId + ".mp3");
    
        this.wavesurfer.on('ready', () => this.loadRegions());
    
        this.wavesurfer.on('region-in', (region) => this.setState({currentSplitId: region.id}));
        
    
        this.wavesurfer.on('region-play', (region) => {
            region.once('out', () => {
                this.wavesurfer.play(region.start);
                this.wavesurfer.pause();
            });
        });
    
        /* Toggle play/pause buttons. */
        var playButton = document.querySelector('#play');
        var pauseButton = document.querySelector('#pause');
        this.wavesurfer.on('play', () => {
            playButton.style.display = 'none';
            pauseButton.style.display = '';
        });
        this.wavesurfer.on('pause', () => {
            playButton.style.display = '';
            pauseButton.style.display = 'none';
        });

        var GLOBAL_ACTIONS = {
            play: () => {
                this.wavesurfer.playPause();
            },
        
            back: () => {
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

        [].forEach.call(document.querySelectorAll('[data-action]'), function(el) {
            el.addEventListener('click', function(e) {
                var action = e.currentTarget.dataset.action;
                if (action in GLOBAL_ACTIONS) {
                    e.preventDefault();
                    GLOBAL_ACTIONS[action](e);
                }
            });
        });
        
        // Bind actions to buttons and keypresses
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
        

    }
}


const domContainer = document.querySelector('#dash-board');
ReactDOM.render(<DashBoard dataJson={dataJson} callId={callId}/>, domContainer);

