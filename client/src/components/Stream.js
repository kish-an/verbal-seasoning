import React from 'react';
import saltAndPeppa from '../salt-n-peppa.png'

const Stream = ({ streamStarted, setStreamStarted, setLoading }) => {
    const handleClick = () => {
        setLoading(true); 
        
        fetch('/animus')
            .then(res => res.json())
            .then(status => {
                if (status.message === 'OK') {
                    setStreamStarted(true);
                    setLoading(false);
                } else if (status.message === 'SERVER ERROR') {
                    console.error('Server error!');
                    setLoading(false);
                }
            })
    }

    return (
        <div onClick={streamStarted ? null : handleClick}>
            <img src={saltAndPeppa} className='robot' />
        </div>
    )
}

export default Stream;
