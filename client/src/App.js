import React, { useState, useEffect } from 'react';
import Nav from './components/Nav';
import Container from 'react-bootstrap/Container';
import Row from 'react-bootstrap/Row';
import Col from 'react-bootstrap/Col';
import Stream from './components/Stream';
import Loading from './components/Loading';
import Summary from './components/Summary';
import Dashboard from './components/Dashboard';

function App() {
    const [streamStarted, setStreamStarted] = useState(null);
    const [loading, setLoading] = useState(false);

    return (
        <div className="App">
            <header className="App-header">
                <Nav />
            </header>

            <Container fluid>
                <Row>
                    <Col>
                        <Stream setStreamStarted={setStreamStarted} />
                    </Col>
                    <Col>
                        {!streamStarted
                            ? <Summary />
                            : <Dashboard />}
                    </Col>
                </Row>
            </Container>
        </div>
    );
}

export default App;
