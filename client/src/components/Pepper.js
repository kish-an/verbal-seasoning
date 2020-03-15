import React from 'react';
import Talk from './Talk';
import pepper from '../pepper.png'

const Pepper = () => {
    return (
        <div className="pepper">
            <h1>
            <img
                alt="Verbal Seasoning"
                src={pepper}
                width="auto"
                height="50"
                padding-left="20"
                className="d-inline-block align-top pepper-logo"
            />Pepper</h1>
            <Talk />
        </div>
    )
}

export default Pepper;
