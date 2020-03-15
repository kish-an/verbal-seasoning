import React from 'react'
import bigGear from '../gear-big.png';
import smallGear from '../gear-small.png';

const Loading = () => {
    return (
        <div className='gears'>
            <img src={bigGear} alt="gear" className="big" />
            <img src={smallGear} alt="gear" className="small" />
            <h3>LOADING</h3>
        </div>
    )
}

export default Loading;
