import React, { useState } from 'react'

const Dashboard = () => {
    const [phrase, setPhrase] = useState('');
    const [currEmotion, setCurrEmotion] = useState('');

    const handlePhraseChange = e => {
        setPhrase(e.target.value);
    }

    const handleEmotion = e => {
        setCurrEmotion(e.target.id);
    }

    const emotions = ['angry', 'fear', 'sad', 'happy', 'suprised', 'neutral'];

    return (
        <div>
            <div className='form__group'>
                {/* {currEmotion ? <h4>Add Phrases to {currEmotion[0].toUpperCase() + currEmotion.slice(1)}</h4> : null} */}
                <input
                    value={phrase}
                    type='text'
                    onChange={handlePhraseChange}
                    className='form__input'
                    id='emotion'
                    placeholder={currEmotion ? `Add Phrases to ${currEmotion[0].toUpperCase() + currEmotion.slice(1)}` : ''}
                />
                <label for="emotion" class="form__label">{currEmotion ? `Add Phrases to ${currEmotion[0].toUpperCase() + currEmotion.slice(1)}` : ''}</label>
            </div>
            <div className='button-list'>
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
