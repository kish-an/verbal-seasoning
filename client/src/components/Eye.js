import React from 'react';
import Button from 'react-bootstrap/Button'

const BCI = () => {
    return (
        <div className='dev'>
            <h1>BCI</h1>
            <div className="input-field">
                <Button variant="primary" size="sm" className='button button-'>
                    Large button
                </Button>
                <Button variant="primary" size="sm" className='button button-'>
                    Large button
                </Button>
                <Button variant="primary" size="sm" className='button button-'>
                    Large button
                </Button>
            </div>
        </div>
    )
}

export default BCI;
