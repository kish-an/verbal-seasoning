import React from 'react';
import Nav from './components/Nav';
import BCI from './components/BCI';
import Pepper from './components/Pepper';

function App() {
    return (
        <div className="App">
            <header className="App-header">
                <Nav />
            </header>
            <div className='container'>
                <BCI />
                <Pepper />
            </div>
        </div>
    );
}

export default App;
