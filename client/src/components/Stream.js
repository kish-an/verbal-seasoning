import React from 'react';
import saltAndPeppa from '../salt-n-peppa.png'

const Stream = ({ setStreamStarted }) => {
    const handleClick = () => {
        console.log('clicked');
        setStreamStarted(true);
    }

    return (
        <div onClick={handleClick}>
            <img src={saltAndPeppa} className='robot' />
        </div>
    )
}

export default Stream;
