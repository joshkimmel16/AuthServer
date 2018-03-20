const React = require('react');
const axios = require('axios');
const Q = require('q');

class LandingPage extends React.Component {
    constructor(options) {
        super();
        this.state = {
            "listHeading": options.listHeading || "",
            "listOptions": options.listOptions || [],
            "userId": options.userId || "",
            "rights": options.rights || 0
        };
    }
    
    componentWillReceiveProps(nextProps) {
        this.setState(nextProps);
    }
    
    handleClick (linkObj) {
        //get index from linkObj
        var index = parseInt(linkObj.dataset.index);
        if (isNaN(index) === false && index > -1 && index < this.state.listOptions.length) {
            var opt = this.state.listOptions[index];
            if (opt.isAdmin === false || (opt.isAdmin === true && this.state.rights === 1)) {
                window.location.href = opt.target;   
            }
        }
    }
    
    render () {
        return (
            <div className='background'>
                <div className='dialog'>
                    <span className='landingHeader'>{this.state.listHeading}</span>
                    <ul className='landingOptions'>
                        {this.state.listOptions.map(function (opt, i) {
                            return <li key={i} className={'landingOption ' + (opt.isAdmin === true && this.state.rights === 0 ? 'hide' : '')} ><a className='landingLink' href='javascript:void(0)' data-index={i} onClick={function (e) {this.handleClick(e.target);}.bind(this)}>{opt.text}</a></li>
                            }.bind(this)
                        )}
                    </ul>
                </div>
            </div>
        )
    }
}

module.exports = LandingPage;