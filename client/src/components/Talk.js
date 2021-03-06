import React, { useState } from 'react';

const Talk = () => {
    const [content, setContent] = useState('');

    const handleChange = e => setContent(e.target.value);

    const handleSubmit = e => {
        if (e.key === 'Enter') {
             fetch('/input', {
                 method: "POST",
                 body: JSON.stringify(content),
                 headers: new Headers({
                     "content-type": "application/json"
                 }),
            })
                .then((res) => res.json())
                .then((status) => console.log(status));
        }

    }

    return (
        <div className="input-field">
            <p>{content}</p>
            <label for="input">What do you want pepper to say?</label>
            <input id='input' type='text' onChange={handleChange} onKeyDown={handleSubmit} />
        </div>
    )
}

export default Talk;

