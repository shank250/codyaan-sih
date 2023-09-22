const mongoose = require("mongoose");
const passportLocalMongoose = require('passport-local-mongoose');
const findOrCreate = require('mongoose-findorcreate');

const employeeSchema = new mongoose.Schema({
    name:{
        type: String,
        // required: true 
    },
    employeeId: {
        type: String,
        // required: true
    },
    designation: {
        type: String,
        // required: true
    },
    complaintSpecialisation: {
        type: String,
        // required: true
    },
    language: {
        type: String,
        // required: true
    },
    bankName: {
        type: String,
    },
    workplace: {
        type: String,
        // required: true
    },
    mobileNo:{
        type: String,
        // required: true
    },
    username: {
        type: String,
        // required: true
    },
    password: {
        type: String
    }
});

employeeSchema.plugin(passportLocalMongoose);
employeeSchema.plugin(findOrCreate);

const Employee = new mongoose.model("Employee", employeeSchema);

module.exports = Employee;