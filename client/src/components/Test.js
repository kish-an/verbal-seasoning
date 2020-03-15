import React, { useState } from 'react';

const Test = () => {
    const [content, setContent] = useState('');

    const handleChange = e => setContent(e.target.value);

    const handleSubmit = e => {
        if (e.key === 'Enter') {
             fetch('/input', {
                 method: "POST",
                 body: content,
                 headers: new Headers({
                     "content-type": "application/json"
                 }),
            })
                .then((res) => res.json())
                .then((status) => console.log(status));
        }

    }

    return (
        <div>
            <p>{content}</p>
            <input id='input' type='text' onChange={handleChange} onKeyDown={handleSubmit} />
        </div>
    )
}

export default Test;

