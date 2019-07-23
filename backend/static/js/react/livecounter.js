class LiveCounter extends React.Component {

    calculateEmotionCount() {
        var emotionCount = {
                'Happy': 0,
                'Sad': 0,
                'Neutral': 0,
                'Analytical': 0,
                'Strategical': 0,
        }

        if (this.props.currentSplitId != null) {
            console.log(this.props.currentSplitId)
            var i = 1;
            while(true) {
                const splitId = generateSplitId(i);
                
                emotionCount[this.props.dataJson[splitId].emotion] += 1

                if (splitId === this.props.currentSplitId) {
                    break;
                }
                i += 1;
            }
        }

        return emotionCount
        
    }    
    render() {

        const emotionCount = this.calculateEmotionCount();
        return(
        <ul className="list-group">
                                    <li className="list-group-item d-flex justify-content-between align-items-center">
                                        Happy
                                        <span className="badge badge-primary badge-pill" id="Happy-count">{emotionCount['Happy']}</span>
                                    </li>
                                    <li className="list-group-item d-flex justify-content-between align-items-center">
                                        Sad
                                        <span className="badge badge-primary badge-pill" id="Sad-count">{emotionCount['Sad']}</span>
                                    </li>
                                    <li className="list-group-item d-flex justify-content-between align-items-center">
                                        Neutral
                                        <span className="badge badge-primary badge-pill" id="Neutral-count">{emotionCount['Neutral']}</span>
                                    </li>
                                        <li className="list-group-item d-flex justify-content-between align-items-center">
                                        Analytical
                                        <span className="badge badge-primary badge-pill" id="Analytical-count">{emotionCount['Analytical']}</span>
                                    </li>
                                    <li className="list-group-item d-flex justify-content-between align-items-center">
                                        Strategical
                                        <span className="badge badge-primary badge-pill" id="Strategical-count">{emotionCount['Strategical']}</span>
                                    </li>
                                    </ul>
        )
    }
    
}

window.LiveCounter = LiveCounter