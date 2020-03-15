import React, { useState } from 'react'
import Loading from './Loading';

const Dashboard = ({ loading, streamStarted }) => {
    const [phrase, setPhrase] = useState('');
    const [currEmotion, setCurrEmotion] = useState('');

    const handlePhraseChange = e => {
        setPhrase(e.target.value);
    }

    const handleEmotion = e => {
        setCurrEmotion(e.target.id);
    }

    const submitEmotionPhrase = e => {
        if (e.key === 'Enter' && currEmotion) {
            fetch('/emotion-phrase', {
                method: "POST",
                 body: JSON.stringify(phrase),
                 headers: new Headers({
                     "content-type": "application/json"
                 }),
            }) 
                .then(res => res.json())
                .then(status => {
                    if (status.message === 'OK') {
                        console.log(status)
                    } else if (status.message === 'SERVER ERROR') {
                        console.error('Server Error!')
                    }
                })
        }
    }

    const emotions = ['angry', 'fear', 'sad', 'happy', 'suprised', 'neutral'];

    if (loading) {
        return <Loading />
    } else if (!streamStarted) {
        return null;
    }

    return (
        <div>
            <div className='form__group'>
                <input
                    value={phrase}
                    type='text'
                    onChange={handlePhraseChange}
                    className='form__input'
                    id='emotion'
                    onKeyDown={submitEmotionPhrase}
                    placeholder={currEmotion ? `Add Phrases to ${currEmotion[0].toUpperCase() + currEmotion.slice(1)}` : 'Select an emotion'}
                />
                <label for="emotion" class="form__label">{currEmotion ? `Add Phrases to ${currEmotion[0].toUpperCase() + currEmotion.slice(1)}` : ''}</label>
            </div>
            <div className='button-list'>
                <h4>Select an emotion</h4>
                {emotions.map(emotion => (
                        <button
                            key={emotion}
                            id={emotion}
                            onClick={handleEmotion}
                            className={`button ${emotion === currEmotion ? '' : 'inactive'} ${emotion}`}
                        >
                                {emotion}
                        </button>
                    )
                )}
            </div>
        </div>
    )
}

export default Dashboard
