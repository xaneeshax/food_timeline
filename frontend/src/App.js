import React from 'react';
import {BrowserRouter as Router, Switch, Route} from 'react-router-dom'
import {Timeline} from "./components/Timeline";
import { HomePage } from './components/HomePage';
import { Navbar } from './components/Navbar';
import { Upload } from './components/Upload';
import { Login } from './components/Login';

function App() {
  return (
    <Router>
      <Navbar />
      <div>
        <Switch>
          <Route path="/timeline" component={Timeline} />
          <Route path="/upload" component={Upload} />
          <Route path="/login" component={Login} />
          <Route path="/" component={HomePage} />
        </Switch>
      </div>
    </Router>
  );
}

export default App;
