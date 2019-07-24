'use strict';

function HistoryRow(props) {

    const minutes = Math.floor(props.dataPoint.startTime / 60);
    const seconds = Math.round(props.dataPoint.startTime - minutes * 60);
    const title = '(' + pad(minutes, 2) + ':' + pad(seconds, 2) + ')  ' + props.dataPoint.speaker;
    return (
        <a  className='list-group-item disabled list-group-item-action flex-column align-items-start' 
            onClick={props.onClick}
            style={{backgroundColor: emotionColor[props.dataPoint.emotion]}}
        >
            <div className='d-flex w-100 justify-content-between'>
                <h5 className="mb-1">{ title }</h5>
                <small className="text-muted">{ props.dataPoint.emotion }</small>
            </div>
            <p className="text-muted text-center">{ props.dataPoint.tags.join(' ') }</p>
        </a>
    )
}

class HistoryPane extends React.Component {
    constructor(props) {
        super(props);
        this.dataJson = props.dataJson;
    }

    renderRows() {
        var rows = [];
        var i = 1;
        while(true) {
            const splitId = generateSplitId(i);
            const row = <HistoryRow dataPoint={this.dataJson[splitId]} onClick={() => this.props.onRowClick(splitId)}/>
            rows.push(row);

            if (splitId === this.props.currentSplitId) {
                break;
            }
            i += 1;
        }
        
        return rows;
    }

    render() {
        if (this.props.currentSplitId) {
            return this.renderRows();
        } else {
            return null;
        }
    }
}

window.HistoryPane = HistoryPane