import React from "react";
import { connect } from "react-redux";
import { createStructuredSelector } from "reselect";
import { BrowserRouter as Router, Route, Routes } from "react-router-dom";

import { Home } from "./pages/home";
import {About}  from "./pages/about";
import { Contact } from "./pages/contact";
import { NoMatch } from "./pages/noMatch";
// import Login from "./pages/login";
// import Find from "./pages/find";
// import Share from "./pages/share";

import Footer from "./components/footer";
import { TopBar, NavBar } from "./components/topbar";



import "./App.css";

function App({ currentUser }) {
  return (
    <React.Fragment>
      <TopBar />
      <NavBar />
        <Routes>
          <Route path="/" element={<Home />} />
          <Route path="/about" element={<About />} />
          <Route path="/contact" element={<Contact />} />
          {/* <Route path="/find" element={<Find />} />
          <Route path="/share" element={<Share />} /> */}
          {/* <Route
            path="/signin"
            element={currentUser ? <Navigate to="/" replace /> : <Login />}
          /> */}
          <Route path="*" element={<NoMatch />} />
        </Routes>
      <Footer />
    </React.Fragment>
  );
}

const mapStateToProps = createStructuredSelector({
  // currentUser: selectCurrentUser,
});

export default connect(mapStateToProps, null)(App);
