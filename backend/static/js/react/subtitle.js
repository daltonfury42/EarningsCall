class Subtitle extends React.Component {

    render() {
        if (this.props.currentSplitId == null) {
            return(
              <div className="card text-center">
                <div className="card-body">
                  <p className="card-text">Click on the play button to start. Click on the audio spectogram or use the 
                  left pane to quickly navigate back and forth.</p>
                </div>
              </div>
            )
        }
        else {
            const tags = this.props.dataPoint.tags.map((tag) => <span className="badge badge-secondary badge-pill">{tag}</span>)
            return(
                <a className="list-group-item list-group-item-action flex-column align-items-start Neutral Notopic">
                    <div className="d-flex w-100 justify-content-between">
                        <h5 className="mb-1">{ this.props.dataPoint.speaker }</h5>
                    </div>
                    <br />
                    <p className="md-1">
                    { this.props.dataPoint.text }
                    </p>
                    <div className="d-flex justify-content-between align-items-center">
                        <div><span className="badge badge-primary">{ this.props.dataPoint.emotion }</span></div>
                        <div>
                            {tags}
                        </div>
                    </div>
                </a>);
        }
    }
}

window.Subtitle = Subtitle