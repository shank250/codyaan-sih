require('dotenv').config();
const express = require("express");
const session = require('express-session');
const passport = require('passport');
const ejs = require('ejs');


const app = express();

app.set('view engine', 'ejs');
//allowing website to read data from frontend
app.use(express.urlencoded());
app.use(express.static('public'));
app.use(session({
    secret : "ourLittleSecret",
    resave : false,
    saveUninitialized : false,
    cookie : {
        expires : 600000000000
    }
}));

app.use(passport.initialize());
app.use(passport.session());

//calling database from db
require("./db/conn");
//calling model from model
const User = require("./model/userSchema");
const Employee = require("./model/employeeSchema");
const Complaint = require("./model/complaintSchema");

passport.use(User.createStrategy());
passport.serializeUser(function(user, cb) {
    process.nextTick(function() {
      return cb(null, {
        id: user.id,
        username: user.username,
        picture: user.picture
      });
    });
});
  
passport.deserializeUser(function(user, cb) {
    process.nextTick(function() {
      return cb(null, user);
    });
});

passport.use(Employee.createStrategy());
passport.serializeUser(function(employee, cb) {
    process.nextTick(function() {
      return cb(null, {
        id: employee.id,
        username: employee.username,
        picture: employee.picture
      });
    });
});
passport.deserializeUser(function(user, cb) {
  process.nextTick(function() {
    return cb(null, user);
  });
});

const authRouter = require("./router/auth").router;
const indexRouter =require("./router/index");
app.use(authRouter);
app.use(indexRouter);

const Port = process.env.PORT;
app.listen(Port, () => {
    console.log("Server is running on port " + Port);
})