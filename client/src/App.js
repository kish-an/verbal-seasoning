import React from 'react';
import Nav from './components/Nav';
import BCI from './components/BCI';
import Pepper from './components/Pepper';
import Container from 'react-bootstrap/Container'
import Row from 'react-bootstrap/Row'
import Col from 'react-bootstrap/Col'

function App() {
    return (
        <div className="App">
            <header className="App-header">
                <Nav />
            </header>
            <Container>
              <Row>    
                <Col><BCI /></Col>
                <Col><Pepper /></Col>
              </Row>
            </Container>
        </div>
    );
}

export default App;
