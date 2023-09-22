const mongoose = require("mongoose");

const complaintSchema = new mongoose.Schema({
    employeeId: {
        type: String,
        // required: true
    },
    userId: {
        type: String,
        // required: true
    },
    complaint :{
        type: String,
        // required: true
    },
    status:{
        type: String,
        // required: true
    },
    tag:{
        type: String,
        // required: true
    }
});

const Complaint = new mongoose.model("Complaint", complaintSchema);

module.exports = Complaint;